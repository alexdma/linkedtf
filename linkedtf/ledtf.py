import urllib.parse

from .model import guess_types, Time
from edtf2 import parse_edtf
from rdflib import Graph, RDF, URIRef




class LEDTF(object):
    def __init__(self, namespace):
        if not namespace:
            raise ValueError('namespace must be non-empty and should respect the URL syntax.')
        self.namespace = namespace

    def uri(self, edtf_val) -> URIRef:
        # Re-raise any exception for now
        parse_edtf(edtf_val)
        return URIRef(self.namespace + urllib.parse.quote_plus(edtf_val))

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
