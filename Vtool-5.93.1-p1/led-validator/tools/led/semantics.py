from rdflib import Literal, XSD, ConjunctiveGraph, URIRef

from .structure import StructureValidator
from .definitions import EDM, LED, SH, EDM_SCHEMA_LOCATION

class SemanticsValidator(object):

    def __init__(self, structure_validator):
        """

        :param syntax_validator: led.syntax.SyntaxValidator
        """
        if not isinstance(structure_validator, StructureValidator):
            raise Exception("Must provide a valid StructureValidator object")
        # elif not structure_validator.valid:
        #     raise Exception("Can only perform structure validation on structurally valid LED document")

        self.structure_validator = structure_validator
        self.valid = False

    def validate_edm(self, results):
        print("Checking conformance of IRI usage against EDM")
        all_resources = set(self.structure_validator.graph.objects())
        all_resources.update(self.structure_validator.graph.subjects())
        all_resources.update(self.structure_validator.graph.predicates())

        # String representation of the EDM namespace IRI
        #edm_iri = str(EDM)
        #Added new line
        edm_iri = str(EDM_SCHEMA_LOCATION)

        try:
            # Load the EDM into a graph
            edm_graph = ConjunctiveGraph()
            edm_graph.load(edm_iri, format="json-ld")
        except Exception as e:
            results.append("Could not load EDM from {} as JSON-LD.".format(edm_iri))
            return results

        claimed_edm_iris = set()
        for resource in all_resources:
            if (isinstance(resource, Literal) and resource.datatype == XSD.anyURI) or isinstance(resource, URIRef):
                # Added new line to assign the EDM Path
                if str(resource).startswith(EDM):
                    claimed_edm_iris.add(URIRef(str(resource)))

        # Check whether the EDM is the object of a led:conformsTo or sh:shapesGraph predicate.
        conformsTo = [str(schema) for schema in self.structure_validator.graph.objects(self.structure_validator.documentIRI, LED.conformsTo)]
        shapesGraphs = [str(schema) for schema in self.structure_validator.graph.objects(self.structure_validator.documentIRI, SH.shapesGraph)]

        schemas = conformsTo + shapesGraphs

        if not str(EDM) in schemas:
            raise Exception("Since the document contains EDM IRIs, the Document IRI must specify a led:conformsTo or sh:shapesGraph that points to the EDM "
                            "schema {}".format(EDM))

        # Get all IRIs from the EDM
        all_edm_iris = [iri for iri in edm_graph.all_nodes() if isinstance(iri, URIRef)]
        # For all claimed EDM IRIs, if they're not defined in the EDM, this is a violation.
        for iri in claimed_edm_iris:
            if iri not in all_edm_iris:
                results.append("The resource {} is not a valid EDM resource".format(iri))

        return results


    def validate(self):
        results = []
        results = self.validate_edm(results)

        if len(results) > 0:
            self.valid = False
            print("JSON-LD does not conform to limited EDM semantics")
            for r in results:
                print("====")
                print(r)
        else:
            print("JSON-LD conforms to limited EDM semantics")
            self.valid = True