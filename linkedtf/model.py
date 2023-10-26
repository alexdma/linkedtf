from edtf2 import EDTFObject, Date, Interval, PartialUnspecified, UnspecifiedIntervalSection
from rdflib import Graph, Literal, Namespace, RDF, URIRef

EDTFO = Namespace('https://periodo.github.io/edtf-ontology/edtfo.ttl#')
Time = Namespace('http://www.w3.org/2006/time#')


def guess_types(date_obj: EDTFObject) -> [URIRef]:
    types = []
    print('{}: {}'.format(type(date_obj), date_obj))
    if isinstance(date_obj, Date):
        types.append(Time.Instant)
    if isinstance(date_obj, Interval):
        types.append(Time.Interval)
        print((date_obj.lower, date_obj.upper))
        if isinstance(date_obj.lower, UnspecifiedIntervalSection):
            types.append(EDTFO.OpenBeginningInterval)
        if isinstance(date_obj.upper, UnspecifiedIntervalSection):
            types.append(EDTFO.OpenEndInterval)
    if isinstance(date_obj, PartialUnspecified):
        types.append(Time.Instant)
        # Detect a decade: regardless of the precision, the least significant digit of the year is X
        print(date_obj.get_year())
        print(date_obj.upper_strict())
        print(date_obj.lower_fuzzy())
        types.append(EDTFO.DecadeDescription)
    return types


def make_decade(subject, decade_val, graph: Graph = Graph()):
    graph.add((subject, RDF.type, EDTFO.DecadeDescription))
    graph.add((subject, Time.unitType, Time.unitYear))
    graph.add((subject, EDTFO.decade, Literal(decade_val)))
    return graph
