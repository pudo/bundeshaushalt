{
  "dataset": {
    "model_rev": 1,
    "name": "bund",
    "label": "Bundeshaushalt", 
    "description": "Der deutsche Bundeshaushalt, wie auf der Webseite des Bundesministeriums für Finanzen veröffentlicht.",
    "currency": "EUR",
    "unique_keys": ["titel.name", "financial_type", "time.from.year"],
    "temporal_granularity": "year"
  },
  "mapping": {
    "amount": {
      "type": "value",
      "label": "Betrag",
      "description": "",
      "column": "amount",
      "datatype": "float"
    },
    "time": {
      "type": "value",
      "label": "Jahr",
      "description": "",
      "column": "year",
      "datatype": "date"
    },
    "data_year": {
      "type": "value",
      "label": "Berichtsjahr",
      "description": "Urpsrungsjahr dieser Angabe",
      "column": "data_year",
      "datatype": "string"
    },
    "financial_type": {
      "type": "value",
      "label": "Finanztyp",
      "description": "",
  	  "facet": true,
      "column": "financial_type",
      "datatype": "string"
    },
    "remarks": {
      "type": "value",
      "label": "Bemerkungen",
      "description": "",
  	  "facet": false,
      "column": "remarks",
      "datatype": "string"
    },
    "flexible": {
      "type": "value",
      "label": "Flexibilisiert",
      "description": "",
  	  "facet": false,
      "column": "flexible",
      "datatype": "string"
    },
    "flow": {
      "type": "value",
      "label": "Flussrichtung",
      "description": "Einnahme oder Ausgabe",
  	  "facet": false,
      "column": "flow",
      "datatype": "string"
    },
    "from": {
      "label": "Quelle",
      "type": "entity",
      "facet": false,
      "description": "",
      "fields": [
        {"constant": "Bundeshaushalt", "name": "label", "datatype": "constant"}
      ]
    },
    "to": {
      "label": "Einzelplan",
      "type": "entity",
      "facet": true,
      "fields": [
        {"column": "ep_id", "name": "name", "datatype": "string"},
        {"column": "ep_label", "name": "label", "datatype": "string"},
	    	{"column": "ep_color", "name": "color", "datatype": "string"},
	    	{"column": "ep_pdf", "name": "pdf_url", "datatype": "string"},
	    	{"column": "ep_url", "name": "source_url", "datatype": "string"},
		    {"constant": "true", "name": "bund_ep", "datatype": "constant"}
      ]
    },
    "kapitel": {
      "label": "Kapitel",
      "type": "classifier",
      "taxonomy": "bund",
      "facet": false,
      "fields": [
        {"column": "kp_id", "name": "name", "datatype": "string"},
        {"column": "kp_label", "name": "label", "datatype": "string"},
		    {"column": "kp_color", "name": "color", "datatype": "string"},
	    	{"column": "kp_pdf", "name": "pdf_url", "datatype": "string"},
	    	{"column": "kp_url", "name": "source_url", "datatype": "string"},
		    {"constant": "true", "name": "bund_kapitel", "datatype": "constant"}
      ]
    },
    "titelgruppe": {
      "label": "Titelgruppe",
      "type": "classifier",
      "taxonomy": "bund",
      "facet": false,
      "fields": [
        {"column": "tgr_id", "name": "name", "datatype": "string"},
        {"column": "tgr_label", "name": "label", "datatype": "string"},
		    {"column": "tgr_color", "name": "color", "datatype": "string"},
	    	{"column": "tgr_pdf", "name": "pdf_url", "datatype": "string"},
	    	{"column": "tgr_url", "name": "source_url", "datatype": "string"},
		    {"constant": "true", "name": "bund_titelgruppe", "datatype": "constant"}
      ]
    },
    "titel": {
      "label": "Titel",
      "type": "classifier",
      "taxonomy": "bund",
      "facet": false,
      "fields": [
        {"column": "id", "name": "name", "datatype": "string"},
        {"column": "label", "name": "label", "datatype": "string"},
		    {"column": "color", "name": "color", "datatype": "string"},
	    	{"column": "pdf", "name": "pdf_url", "datatype": "string"},
	    	{"column": "url", "name": "source_url", "datatype": "string"},
	    	{"column": "description", "name": "description", "datatype": "string"},
		    {"constant": "true", "name": "bund_titel", "datatype": "constant"}
      ]
    },
    "hauptfunktion": {
      "label": "Hauptfunktion",
      "type": "classifier",
      "taxonomy": "funktionenplan-bund",
      "facet": true,
      "fields": [
        {"column": "hauptfunktion_id", "name": "name", "datatype": "string"},
        {"column": "hauptfunktion_label", "name": "label", "datatype": "string"},
		    {"column": "hauptfunktion_color", "name": "color", "datatype": "string"},
		    {"column": "hauptfunktion_desc", "name": "description", "datatype": "string"},
		    {"constant": "1", "name": "level", "datatype": "constant"}
      ]
    },
    "oberfunktion": {
      "label": "Oberfunktion",
      "type": "classifier",
      "taxonomy": "funktionenplan-bund",
      "facet": false,
      "fields": [
        {"column": "oberfunktion_id", "name": "name", "datatype": "string"},
        {"column": "oberfunktion_label", "name": "label", "datatype": "string"},
		    {"column": "oberfunktion_color", "name": "color", "datatype": "string"},
		    {"column": "oberfunktion_desc", "name": "description", "datatype": "string"},
		    {"constant": "2", "name": "level", "datatype": "constant"}
      ]
    },
    "funktion": {
      "label": "Funktion",
      "type": "classifier",
      "taxonomy": "funktionenplan-bund",
      "facet": false,
      "fields": [
        {"column": "funktion_id", "name": "name", "datatype": "string"},
        {"column": "funktion_label", "name": "label", "datatype": "string"},
		    {"column": "funktion_color", "name": "color", "datatype": "string"},
		    {"column": "funktion_desc", "name": "description", "datatype": "string"},
		    {"constant": "3", "name": "level", "datatype": "constant"}
      ]
    },
    "hauptgruppe": {
      "label": "Hauptgruppe",
      "type": "classifier",
      "taxonomy": "gruppierungsplan-bund",
      "facet": true,
      "fields": [
        {"column": "hauptgruppe_id", "name": "name", "datatype": "string"},
        {"column": "hauptgruppe_label", "name": "label", "datatype": "string"},
		    {"column": "hauptgruppe_color", "name": "color", "datatype": "string"},
		    {"column": "hauptgruppe_desc", "name": "description", "datatype": "string"},
		    {"constant": "1", "name": "level", "datatype": "constant"}
      ]
    },
    "obergruppe": {
      "label": "Obergruppe",
      "type": "classifier",
      "taxonomy": "gruppierungsplan-bund",
      "facet": false,
      "fields": [
        {"column": "obergruppe_id", "name": "name", "datatype": "string"},
        {"column": "obergruppe_label", "name": "label", "datatype": "string"},
		    {"column": "obergruppe_color", "name": "color", "datatype": "string"},
		    {"column": "obergruppe_desc", "name": "description", "datatype": "string"},
		    {"constant": "2", "name": "level", "datatype": "constant"}
      ]
    },
    "gruppe": {
    "label": "Gruppe",
      "type": "classifier",
      "taxonomy": "gruppierungsplan-bund",
      "facet": false,
      "fields": [
        {"column": "gruppe_id", "name": "name", "datatype": "string"},
        {"column": "gruppe_label", "name": "label", "datatype": "string"},
		    {"column": "gruppe_color", "name": "color", "datatype": "string"},
		    {"column": "gruppe_desc", "name": "description", "datatype": "string"},
		    {"constant": "3", "name": "level", "datatype": "constant"}
      ]
    }
  },
  "views": []
}


