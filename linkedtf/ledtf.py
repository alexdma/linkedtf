import urllib.parse
import re

from .model import guess_types, make_decade, EDTFO, Time
from edtf2 import parse_edtf, PRECISION_DECADE
from rdflib import Graph, RDF, URIRef , Literal


class LEDTF(object):
    """
    Basic implementation that does not maintain a resident RDF graph, but creates them on the fly.
    """
    def __init__(self, namespace):
        if not namespace:
            raise ValueError('namespace must be non-empty and should respect the URL syntax.')
        self.namespace = namespace

    def uri(self, edtf_val) -> URIRef:
        # Re-raise any exception for now
        parse_edtf(edtf_val)
        return URIRef(self.namespace +  urllib.parse.quote_plus(edtf_val))

    def uri_decade(self, decade) -> URIRef:
        """
        Creates a named RDF resource of a decade description.

        :param decade: e.g. 201 for the 2010's
        :param g:
        :return: a reusable URIRef that represents the decade
        """
        pattern = r'^[1-9]\d{0,2}$'
        if not re.match(pattern, decade):
            raise ValueError('Invalid decade value {}: must be 1 to 3 digits and not start with a zero.'.format(decade))
        return URIRef(self.namespace + 'decade' + '/' + decade)

    def description(self, edtf_val: str) -> Graph:
        """
        Generates an RDF description of the EDTF value.

        :param edtf_val: an EDTF string or a URI, will be used as subject
        (directly in the latter case, converted to URIRef in the former).
        :return:
        """
        s = self.uri(edtf_val)
        do = parse_edtf(edtf_val)
        g = Graph()
        g.add((s, RDF.type, Time.DateTimeDescription))
        t = guess_types(do)



        return g

    def _description_decade(self, decade_val: str) -> Graph:
        """
        Creates an RDF representation of a decade description, as in
        https://periodo.github.io/edtf-ontology/#Decadedescription
        but avoiding blank nodes.

        :param decade_val: a string of 1 to 3 digits that doesn't start with a zero.
        :return: a Graph containing the
        """
        s = self.uri_decade(decade_val)
        return make_decade(s, decade_val, Graph())
