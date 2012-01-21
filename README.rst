OffenerHaushalt.de - Scraper for the German Federal Budget
==========================================================

This scraper is an extended and updated version of the one used to generate the 
original visualizations on Bund.OffenerHaushalt.de. It uses HTML data available
on the web site of the Federal Ministry of Finance (Bundesministerium für 
Finanzen). 

We've repeatedly tried to effect the release of official machine-readable data,
e.g. the XML input data which is used to generate the HTML representation via an
XSL-FO stage. Unfortunately, the ministry has declined to do so, variously citing
the definition of a "public document", quality concerns and their intent to 
release a visualization portal of their own as reasons for secrecy.


Running the scraper
-------------------

To run the scraper, please make sure you have the specified dependencies 
installed in a virtualenv, e.g. like this::

  virtualenv pyenv
  source pyenv/bin/activate
  pip install -r pip-requirements.txt

Having ensured the dependencies are installed, you can run the scraper. This 
requires a database to be set up. While you can use SQLite, we recommend you
use Postgres::

  createdb -E utf-8 bundeshaushalt
  python scrape.py postgresql://localhost/bundeshaushalt

This will attempt to extract all budget line items for the budgets between
2005 and 2012. If you want to scrape only a single year, edit the list at the
bottom of ``scrape.py``. 

After having extraced the budget, you need to join in the classification 
data from the Funktionen- and Gruppierungsplan (functional and accounting 
systematics), as well as to compute colorization information for the 
visualizations::

  python extend.py postgresql://localhost/bundeshaushalt
  python colorize.py postgresql://localhost/bundeshaushalt

You will now have a complete database of the budget documents with a single
table, ``bund`` that you can export to CSV and import into OpenSpending.org.


Indexes
-------

The following indexes have proven to speed up processing::

  CREATE INDEX idx_uniq ON bund (year, flow, financial_type, titel_id);
  CREATE INDEX idx_tid ON bund (titel_id);
  CREATE INDEX idx_ft ON bund (financial_type);


Data interpretation/political issues
------------------------------------

A contentious point in extracting the data is the use of negative revenue
for financial flows between the federal and state/EU-level budget. By marking
such expenditure as negative revenue, it does not get included in the final
tally - resulting in a total of about 306bn EUR, compared to about 360bn if 
expenditure on state budgets and EU own resources is actually considered 
expenditure. While this normalization was applied to the original site, the 
current version of the scraper will actually reproduce the negative revenue 
values faithfully.

As the budget reports both revenue and expenditure, one would expect the sum
of both to be zero. This is not in fact true, as can be seen using the 
following query::

  SELECT 
    (SELECT SUM(amount) FROM bund 
     WHERE year = '2006' and financial_type = 'Ist' AND flow = 'revenue')
    -
    (SELECT SUM(amount) FROM bund 
    WHERE year = '2006' and financial_type = 'Ist' AND flow = 'spending')
    AS total_sum;

For any given year, this will result in excess revenue of about 15-19 bn
EUR. This is most likely an accounting issue that I am misunderstanding.

TODO: Does this just lack a "Rechnungsabgrenzungsposten"? 


QA steps
--------

The scraper is prone to produce several errors, including the following:

* A lack of funds for the Auswärtiges Amt in 2006 which does not correspond
  to reality.
* Funktionanplan and Gruppierungsplan reference data are missing entries used 
  in the actual document.

To see the total number of line items per year and reporting type, use this::

  SELECT DISTINCT COUNT(titel_id), year, financial_type 
    FROM bund 
    GROUP BY year, financial_type 
    ORDER BY year, financial_type;


Issues and Contact
------------------

The scraper was written by Friedrich Lindenberg <friedrich.lindenberg@okfn.org>
for the OpenSpending project. The code is licensed under the GNU GPL v3.

Please report bugs and questions to the issue tracker on GitHub.

