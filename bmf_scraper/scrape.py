#coding: utf-8
import codecs
import re
import sys
import json
import logging
import os
from os.path import join
from pprint import pprint
from lxml import html
from urlparse import urljoin

import sqlaload as sl
#from webstore.client import URL as WebStore

BASE_URL = "http://www.bundesfinanzministerium.de/bundeshaushalt%s/html/ep00.html"
UNIQUE_COLUMNS = ['year', 'flow', 'financial_type', 'titel_id', 'commitment_year']

log = logging.getLogger(__name__)

def clean(elem):
    return elem.xpath("string()").strip()

def anchors(doc, rfilter):
    f = re.compile(rfilter)
    for a in doc.findall('.//a'):
        href = a.get('href')
        if href is None:
            continue
        match = f.match(href)
        if match:
            yield (href, clean(a))

def encode_val(v):
    return v
    if isinstance(v, bool):
        return '1' if v else '0'
    return unicode(v)

def load_budget(base_url, year, engine, table):
    context = {'data_year': year}
    print "\nHaushalt: %s" % year
    i = 0
    for row in load_einzelplaene(base_url % year, context):
        row['titel_id'] = row['id']
        del row['id']
        row['remarks'] = "\n\n".join(row['remarks'])
        commitment_appropriations = row['commitment_appropriations'].copy()
        del row['commitment_appropriations']
        #if len(commitment_appropriations):
        #    #print len(commitment_appropriations)
        
        row['commitment_year'] = None
        row['source_id'] = str(year) + "." + str(i)
        sl.upsert(engine, table, row, UNIQUE_COLUMNS)
        i += 1

        for year, amount in commitment_appropriations.items():
            ca = row.copy()
            ca['commitment_year'] = context['data_year']
            ca['year'] = year
            ca['amount'] = amount
            ca['financial_type'] = 'VE'
            ca['source_id'] = str(year) + "." + str(i)
            sl.upsert(engine, table, ca, UNIQUE_COLUMNS)
            i += 1
        #pprint(row)

def expand_classifications(row):
    id = row['titel_id']
    row['hauptgruppe_id'] = id[4:5] + "00"
    row['obergruppe_id'] = id[4:6] + "0"
    row['gruppe_id'] = id[4:7]
    row['hauptfunktion_id'] = id[10:11] + "00"
    row['oberfunktion_id'] = id[10:12] + "0"
    row['funktion_id'] = id[10:13]
    return row


def load_einzelplaene(url, context):
    doc = html.parse(url)
    for (href, label) in anchors(doc, "ep\d{2,}/ep\d{2,}.html"):
        print " -> ", label.encode('utf-8')
        ep_url = urljoin(url, href)
        ep_context = context.copy()
        name = ep_context['ep_id'] = re.match('.*ep(\d*).html', ep_url).group(1)
        ep_context['ep_url'] = urljoin(url, "../html/ep" + name + "/ep" + name + ".html")
        ep_context['ep_pdf'] = urljoin(url, "../pdf/epl" + name + ".pdf")
        ep_context['ep_label'] = label
        for r in load_kapitel(ep_url, ep_context):
            yield r

def load_kapitel(url, context):
    doc = html.parse(url)
    exp = "ep" + context.get('ep_id') + "kp\d{2,}.html"
    for (href, label) in anchors(doc, exp):
        kp_url = urljoin(url, href)
        name_part = re.match('.*kp(\d*).html', kp_url).group(1)
        ep_id = context.get('ep_id')
        kp_context = context.copy()
        kp_context['kp_label'] = label
        kp_context['kp_url'] = kp_url = urljoin(url, href) 
        kp_context['kp_pdf'] = urljoin(url, "../../pdf/epl" + ep_id + "/s" + \
            ep_id + name_part + ".pdf")
        kp_context['kp_id'] = ep_id + name_part
        doc = html.parse(kp_url)
        exp = ".*kp" + name_part + "nr[ae].*.html"
        for (href, label) in anchors(doc, exp):
            group_file = urljoin(kp_url, href)
            for r in load_titelgruppe(group_file, label, kp_context):
                yield r


def load_titelgruppe(url, label, context):
    grp_context = context.copy()
    grp_context['tgr_label'] = label
    grp_context['url'] = url
    doc = html.parse(url)
    match = re.match('.*nr([ae])(\d*).html', url)
    grp_context['tgr_id'] = context.get('kp_id') + "-" + match.group(2)
    grp_context['flow'] = 'revenue' if match.group(1) == 'e' else 'spending'
    
    for row in doc.findall('.//tr'):
        for r in load_posten_row(row, grp_context):
            yield r


def load_posten_row(row, context):
    pcontext = context.copy()
    pcontext['commitment_appropriations'] = {}
    pcontext['description'] = ''
    pcontext['remarks'] = []
    pcontext['pdf'] = ''
    year = int(context.get('data_year'))
    entries = []
    for i, column in enumerate(row.findall('./td')):
        if i == 0:
            name = column.xpath("string()").strip()
            if not len(name):
                break
            if 'Tgr' in name:
                break
            if 'F ' in name:
                pcontext['flexible'] = True
                #name = name[1:]
            else: 
                pcontext['flexible'] = False
            name = [c for c in name if c in '-0123456789']
            if not len(name) == 9:
                #print "FAIL NAME", name
                break
            name = pcontext.get('kp_id') + "".join(name)
            pcontext['id'] = name.strip()
        if i == 1:
            pcontext['label'] = column.text.strip() if column.text else None
            section = ""
            for elem in column:
                if elem.tag == 'hr': 
                    parse_section(section, pcontext)
                    section = ""
                elif 'title' in elem.keys() and \
                    elem.get('title').strip().startswith('PDF'):
                    pcontext['pdf'] = urljoin(pcontext.get('url'), elem.get('href'))
                else:
                    section += html.tostring(elem).strip()
                    if elem.tail:
                        section += elem.tail
            if len(section):
                parse_section(section, pcontext)
        if i == 2:
            entries.append(parse_posten(column, 'Ansatz', year, context))
        if i == 3:
            entries.append(parse_posten(column, 'Ansatz', year - 1, context))
        if i == 4:
            entries.append(parse_posten(column, 'Ist', year - 2, context))
    if not 'id' in pcontext: 
        return 

    for entry in entries:
        e = pcontext.copy()
        e.update(entry)
        yield e  

def handle_number(num):
    try:
        val = "".join([c for c in num if c in '-0123456789'])
        val = int(val) * 1000
        return float(val)
    except:
        return 0.0


def parse_posten(column, fin_type, year, context):
    p = {'financial_type': fin_type, 'year': year}
    p['amount'] = handle_number(column.text)
    return p

re_YEAR = re.compile(".*(20\d{2}).*")
def parse_section(section, context): 
    if not len(section.strip()): 
        return
    doc = html.fragment_fromstring("<span>" + section + "</span>")
    h4 = doc.findtext('.//h4')
    assert h4 is not None, section.encode('utf-8')
    if u'Verpflichtungser' in h4:
        #print section.encode('utf-8')
        capps = {}
        if context['data_year'] >= 2012:
            #print "VE", 
            for row in doc.findall('.//tr'):
                if not len(row.findall('td')) == 2:
                    #print row
                    continue
                label, amt = row.findall('td')
                label = label.xpath('string()').strip()
                year = re_YEAR.match(label)
                #print label.xpath('string()').encode('utf-8'), year
                if year is not None:
                    text = amt.xpath('string()')
                    capps[int(year.group(1))] = handle_number(text)
        else:
            for p in doc.findall('.//p'):
                if u'davon fällig' in p.text: 
                    continue
                year = re_YEAR.match(p.text)
                if year is not None:
                    span = p.find('./span')
                    capps[int(year.group(1))] = handle_number(span.text)
        context['commitment_appropriations'] = capps
    elif u'Erläuterungen' in h4:
        context['description'] = section
    elif u'Haushaltsvermerk' in h4:
        for tr in doc.findall('.//tr'):
            tds = tr.findall('./td')
            assert len(tds)==2
            context['remarks'].append(tds[1].xpath("string()").strip())


if __name__ == '__main__': 
    assert len(sys.argv)==2, "Need argument: engine-url!"
    engine = sl.connect(sys.argv[1])
    table = sl.get_table(engine, 'bund')
    for year in [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]:
    #for year in [2012]:
        load_budget(BASE_URL, year, engine, table)


