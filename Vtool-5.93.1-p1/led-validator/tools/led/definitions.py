from rdflib import Namespace

ELSEVIER_LD_IRI_PATTERN = "https://data.elsevier.com/(lifescience|research|health)"
LED_SCHEMA_LOCATION = "./led-validator/src/led.schema.jsonld"
EDM_SCHEMA_LOCATION = "./led-validator/src/edm-ontology.jsonld"

LED = Namespace("https://data.elsevier.com/schema/led/")
EDM = Namespace("https://data.elsevier.com/schema/edm/")

SH = Namespace("http://www.w3.org/ns/shacl#")
