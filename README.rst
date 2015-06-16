Scraper for the German Federal Budget
=====================================

This scraper is an extended and updated version of the one used to generate the 
original visualizations on Bund.OffenerHaushalt.de. It uses JSON data available
on the "Bundeshaushalt-Info" web site of the Federal Ministry of Finance
(Bundesministerium für Finanzen). 

Running the scraper
-------------------

To run the scraper, please make sure you have the specified dependencies 
installed in a virtualenv, e.g. like this::

  virtualenv pyenv
  source pyenv/bin/activate
  pip install -r requirements.txt

Having ensured the dependencies are installed, you can run the scraper::

  python scraper.py

This will attempt to extract all budget line items for the budgets between
2012 and 2015. If you want to scrape only a single year, edit the list at the
bottom of ``scraper.py``. 

Issues and Contact
------------------

The scraper was written by Friedrich Lindenberg <friedrich@pudo.org> for
the OpenSpending project. The code is licensed under the MIT License.

Please report bugs and questions to the issue tracker on GitHub.
