import json
import os
import traceback
import urllib
from io import StringIO, BytesIO
from itertools import islice

from bs4 import Doctype
from lxml import etree
from rdflib import ConjunctiveGraph, URIRef, Namespace, Literal, RDF
from rdflib.resource import Resource
from rfc3987 import parse

from .syntax import SyntaxValidator
from .definitions import LED, EDM, SH, LED_SCHEMA_LOCATION, EDM_SCHEMA_LOCATION

import pyshacl



class StructureValidator(object):

    def __init__(self, syntax_validator):
        """

        :param syntax_validator: led.syntax.SyntaxValidator
        """
        if not isinstance(syntax_validator, SyntaxValidator):
            raise Exception("Must provide a valid SyntaxValidator object")
        elif not syntax_validator.xhtml_valid or not syntax_validator.jsonld_valid:
            raise Exception("Can only perform structure validation on syntactically valid LED document")

        self.syntax_validator = syntax_validator
        self.valid = None

        # Parse the NQuads into a conjunctive graph (not graph aware!)
        self.graph = ConjunctiveGraph()
        self.graph.parse(data=self.syntax_validator.nquads, format="nquads")

        self.documentIRI = URIRef(self.syntax_validator.documentIRI)
        self.DOC = Namespace("{}#".format(self.syntax_validator.documentIRI))

        self.extract_namespaces()

    def extract_namespaces(self):
        for g in self.syntax_validator.jsonld:
            if "@context" in g:
                context = g["@context"]
                if not isinstance(context, list):
                    context = [context]

                for c in context:
                    for key, value in c.items():
                        if ':' not in key and '@' not in key:
                            try:
                                # Make sure the value is a valid IRI
                                parse(value)
                                ns = Namespace(value)
                                self.graph.bind(key, ns)
                            except ValueError:
                                # Not a valid IRI, and therefore not a namespace definition
                                pass

    def validate_namespaces(self):
        results = []
        try:
            if not ('led',LED) in self.graph.namespaces():
                raise Exception("Namespace for 'led' prefix must be bound to {} ".format(LED))
        except Exception as e:
            results.append(str(e))
        try:
            if not ('edm',EDM) in self.graph.namespaces():
                raise Exception("Namespace for 'edm' prefix must be bound to {} ".format(EDM))
        except Exception as e:
            results.append(str(e))
        try:
            if not ('doc', self.DOC) in self.graph.namespaces():
                raise Exception("Namespace for 'doc' prefix must be bound to {} ".format(self.DOC))
        except Exception as e:
            results.append(str(e))

        return results

    def validate_schema(self, schema_uri):
        schema_graph = ConjunctiveGraph()
        schema_graph.parse(location=schema_uri, format="json-ld")
        valid, g, report = pyshacl.validate(self.graph, shacl_graph=schema_graph)

        if valid is False:
            print("JSON-LD does not conform to schema defined in {}".format(schema_uri))
            return report
        else:
            print("JSON-LD conforms to schema defined in {}".format(schema_uri))
            return


    def validate_xml_schemas(self, xml_schema_locations, results):
        """
        For each of the XML schemas, resolve them to a path relative to the referencing HTML file and load them as XML Schema
        Validate the HTML file against the schema

        :param xml_schema_locations:
        :param results:
        :return:
        """
        results = self.decorate_types(results)

        parser = etree.XMLParser()

        self.syntax_validator.soup.html.attrs.pop("xmlns")


        for xml_schema_location in xml_schema_locations:
            print("Checking conformance of HTML structure against {}".format(xml_schema_location))
            file_relative_schema_location = os.path.join(os.path.dirname(self.syntax_validator.filename), xml_schema_location)

            xml_schema = etree.XMLSchema(etree.parse(file_relative_schema_location))
            valid = xml_schema.validate(etree.parse(BytesIO(self.syntax_validator.soup.encode("utf-8")), parser))

            if not valid:
                print("XHTML document does not conform to XML Schema in {}".format(xml_schema_location))
                results.append("{} validation log:".format(xml_schema_location))
                results.append(xml_schema.error_log)
            else:
                print("XHTML document conforms to XML Schema in {}".format(xml_schema_location))

        return results

    def decorate_types(self, results):
        """
        Add 'typeof' values to each XML element referred to as object of the edm:hasPart predicate
        """
        for part_iri in self.graph.objects(self.documentIRI, EDM.hasPart):
            # Only get the fragment identifier for the document part IRI
            _, _, fragment = self.graph.compute_qname(part_iri)

            # Find the element with the fragment ID
            element = self.syntax_validator.soup.find(id=fragment)

            if element is not None:
                # Find the types associated with that part pof the document as QNames
                types = [Resource(self.graph, type).qname() for type in self.graph.objects(part_iri, RDF.type)]

                # Get the existing values for the typeof attribute on the element
                existing_types = element.get_attribute_list('typeof')

                # Get rid of weird artifact [None] when attribute does not exist yet
                if None in existing_types:
                    existing_types.remove(None)

                types += existing_types
                if types != []:
                    # Update the typeof values
                    element['typeof'] = types

                    # Add RDFa lite compliant `resource` attribute
                    element['resource'] = str(part_iri)
            else:
                results.append("The document part {} does not have a corresponding element in the XML".format(part_iri))

        return results


    def validate_schemas(self):
        results = []
        try:
            conformsTo = [str(schema) for schema in self.graph.objects(self.documentIRI, LED.conformsTo)]
            shapesGraphs = [str(schema) for schema in self.graph.objects(self.documentIRI, SH.shapesGraph)]

            schemas = conformsTo + shapesGraphs

            if not str(LED) in schemas:
                raise Exception("Document IRI must specify a led:conformsTo or sh:shapesGraph that points to the LED "
                                "schema {}".format(LED))

            try:
                # XML Schema locations are values for conformsTo that are XSD files
                # TODO: Find a more elegant way to link XSD files to LED
                xml_schema_locations = [ct for ct in conformsTo if ct.endswith('.xsd')]
                # Validate against the XML Schemas available at the specified locations
                results = self.validate_xml_schemas(xml_schema_locations, results)
            except Exception as e:
                results.append(traceback.format_exc(1))

            # Remove the LED IRI as we're going to check against a local instance (prevent checking multiple times)
            schemas.remove(str(LED))
            # Always evaluate against a local LED schema even if it is not explicitly linked (or cannot be downloaded
            # from its namespace IRI)
            results = self.validate_led_schema(results)

            for schema_iri in schemas:
                try:
                    # Make sure the schema_iri is a valid IRI
                    parse(schema_iri)

                    # Validate against the schema graph, and append results (if any)
                    #validation_report = self.validate_schema(schema_iri)
                    #Added new line
                    validation_report = self.validate_schema(EDM_SCHEMA_LOCATION)
                    if validation_report is not None:
                        results.append(validation_report)

                except json.decoder.JSONDecodeError as e:
                    print("Skipping automated schema checking against claimed conformance to <{}> as this IRI does "
                          "not dereference to valid JSON-LD".format(schema_iri))
                except urllib.error.URLError as e:
                    print("Skipping automated schema checking against claimed conformance to <{}> as this location cannot be opened.".format(schema_iri))
                except ValueError as e:
                    """The schema_iri is not a valid URI"""
                    print("Skipping automated schema checking against claimed conformance to '{}' as this is not a "
                          "valid IRI".format(schema_iri))

        except Exception as e:
            results.append(traceback.format_exc(1))
        return results

    def validate_led_schema(self, results):
        """
        Validate against the LED Schema and update results
        :param results:
        :return:
        """
        validation_report = self.validate_schema(LED_SCHEMA_LOCATION)
        if validation_report is not None:
            results.append(validation_report)

        return results

    def validate(self):
        results = []
        results += self.validate_namespaces()
        results += self.validate_schemas()

        if len(results) > 0:
            self.valid = False
            for r in results:
                print("====")
                print(r)
        else:
            self.valid = True



