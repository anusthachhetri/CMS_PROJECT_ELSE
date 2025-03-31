from tidylib import tidy_document
from html5validator import Validator
from contextlib import redirect_stderr
from pyld import jsonld
from bs4 import BeautifulSoup
from rfc3987 import parse
from itertools import islice

from .definitions import ELSEVIER_LD_IRI_PATTERN

import shutil
import io
import os
import re
import json

TIDY_OPTIONS = {
    "input-xml": "true",
    "doctype": "html5",
    "output-xhtml": "true",
    "show-warnings": "false"
}

HTML5VALIDATOR_OPTIONS = {
    "format": "json",
    "errors_only": True,
    "vnu_args": ['--asciiquotes']
}


class SyntaxValidator(object):

    def __init__(self, filename, htmlvalidator="tidy"):
        self.filename = filename
        self.xhtml_valid = None
        self.jsonld_valid = None
        self.soup = None
        self.documentIRI = None
        self.jsonld = None
        self.nquads = None
        self.schema_locations = None

        if htmlvalidator in ["tidy", "html5validator"]:
            self.htmlvalidator = htmlvalidator
        else:
            raise Exception("HTML Validator '{}' not supported".format(htmlvalidator))

    def validate(self):
        report = self.validate_xhtml()

        if self.xhtml_valid:
            print("XHTML document is syntactically valid LED")
            report += self.validate_jsonld()

            if not self.jsonld_valid:
                print("Document does not contain syntactically valid JSON-LD")
            else:
                print("JSON-LD data contained in XHTML document is syntactically valid LED")
        else:
            print("Document is not valid LED compliant XHTML")

        return report

    def extract_jsonld(self):
        """
        :return: An array of all JSON-LD data embedded in the XHTML

        TODO: Does NOT include any JSON-LD referred to through a src attribute
        """
        if self.xhtml_valid is True and self.soup is not None:
            self.jsonld = [json.loads(jsonld_tag.string) for jsonld_tag in self.soup.find_all("script", attrs={"type": "application/ld+json"})]

            return self.jsonld
        else:
            raise Exception("Cannot extract JSON-LD from unvalidated or invalid XHTML")

    def validate_jsonld(self):
        """
        Validate the JSON-LD by running it through a JSON-LD 1.1 compliant JSON-LD parser (pyLD)

        :raises: JsonLdError if JSON-LD cannot be parsed.
        :return: All JSON-LD extracted as NQuads
        """
        report = []

        if self.jsonld is None:
            self.extract_jsonld()

        try:
            self.nquads = jsonld.to_rdf(self.jsonld, {'format': 'application/n-quads'})
            m = re.search("(\n|^)\s*<{}>".format(self.documentIRI), self.nquads)
            if m is None:
                raise Exception(
                    "JSON-LD data does not contain any statements about the document IRI ({}) set in XHTML".format(
                        self.documentIRI))
        except Exception as e:
            report.append(str(e))

        if len(report) > 0 :
            self.jsonld_valid = False
        else:
            self.jsonld_valid = True

        return report

    def validate_xhtml(self):
        """
        Wrapper for the supported validation packages, ensures a uniform response format compatible with Tidy output.

        Example: 'line 105 column 1 - Error: unexpected </head> in <script>'

        Sets self.xhtml_valid flag, self.document_iri and self.soup (a BeautifulSoup object of the document)

        TODO: Investigate whether we can use https://github.com/unsoup/validator/blob/gh-pages/schema-release/html5
        /xhtml5full-xhtml.rnc

        :raises: Exception if the specified validator is not supported (should be tidy or html5validator)\
        """
        report = []

        # Test standard XHTML validity
        if self.htmlvalidator == "tidy":
            tidiness = self.tidy()
            for l in tidiness.splitlines():
                report.append(l)

        elif self.htmlvalidator == "html5validator":
            validity = self.html5validator()
            for message in validity['messages']:
                report.append("line {lastLine} column {firstColumn} - {type}: {message} in '{extract}'".format(**message))
        else:
            raise Exception("Unsupported validator")

        try:
            # Test LED specific XHTML validity
            with open(self.filename, "r") as f:
                self.soup = BeautifulSoup(f, 'xml')

            document_iri = self.soup.find("meta", attrs={"name": "id"})['content']
            if document_iri is None:
                raise Exception("Document does not specify a '<meta>' element with a value for the 'id' attribute")

            # Make sure that document IRI is a valid absolute IRI
            parse(document_iri, rule='IRI')

            # Make sure that the document IRI is a valid Elsevier Linked Data IRI
            # https://data.elsevier.com/(lifescience|research|health)
            m = re.match(ELSEVIER_LD_IRI_PATTERN, document_iri)
            if m is None:
                raise Exception("Document specifies an IRI that is not a valid Elsevier Linked Data IRI: {}".format(document_iri))

            # Make sure that the document IRI does not end with a hash
            if document_iri.endswith("#"):
                raise Exception("Document IRI must not end with a # character: {}".format(document_iri))

            self.documentIRI = document_iri

            json_ld = self.soup.find("script", attrs={"type": "application/ld+json"})
            if json_ld is None:
                raise Exception("Document must specify a '<script>' element with JSON-LD content")


        except Exception as e:
            report.append(str(e))

        if len(report) > 0:
            self.xhtml_valid = False
        else:
            self.xhtml_valid = True

        return report

    def tidy(self):
        with open(self.filename, "r") as f:
            document, errors = tidy_document(f.read(), options=TIDY_OPTIONS)
            return errors

    def html5validator(self):
        """
        Use the html5validator that wraps vnu.jar (V.nu).

        NB: this validator only tests XHTML conformance for files with the .led extension!
        """
        validator = Validator(**HTML5VALIDATOR_OPTIONS)

        if self.filename.endswith('.html'):
            # xhtml5validator only validates .xhtml files as XHTML
            xhtml_filename = self.filename.replace('.html', '.xhtml')
            shutil.copyfile(self.filename, xhtml_filename)
        else:
            xhtml_filename = self.filename

        f = io.StringIO()
        with redirect_stderr(f):
            status = validator.validate([xhtml_filename])

        if self.filename.endswith('.html'):
            # clean up created .xhtml file
            os.remove(xhtml_filename)

        validity = json.loads(f.getvalue())
        return validity


