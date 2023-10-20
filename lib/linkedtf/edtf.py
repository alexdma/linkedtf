import urllib.parse

from edtf import parse_edtf
from rdflib import Graph, Namespace, RDF, URIRef

EDTFO = Namespace('https://periodo.github.io/edtf-ontology/edtfo.ttl#')
Time = Namespace('http://www.w3.org/2006/time#')


class LEDTF(object):
    def __init__(self, namespace):
        if not namespace:
            raise ValueError('namespace must be non-empty and should respect the URL syntax.')
        self.namespace = namespace

    def uri(self, edtf_val) -> URIRef:
        parsed = parse_edtf(edtf_val)
        return URIRef(self.namespace + urllib.parse.quote_plus(edtf_val))

    def description(self, edtf_val: [str, URIRef]) -> Graph:
        """
        Generates an RDF description of the EDTF value.

        :param edtf_val: an EDTF string or a URI, will be used as subject
        (directly in the latter case, converted to URIRef in the former).
        :return:
        """
        s = edtf_val if isinstance(edtf_val,URIRef) else self.uri(edtf_val)
        g = Graph()
        g.add((s, RDF.type, Time.DateTimeDescription))
        return g
