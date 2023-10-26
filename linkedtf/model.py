from edtf2 import EDTFObject
from rdflib import Namespace, URIRef
from edtf2.parser.parser_classes import Date, Interval, UncertainOrApproximate
import edtf

EDTFO = Namespace('https://periodo.github.io/edtf-ontology/edtfo.ttl#')
Time = Namespace('http://www.w3.org/2006/time#')


def guess_types(date_obj: EDTFObject) -> [URIRef]:
    types = []
    print('{}: {}'.format(type(date_obj), date_obj))
    if isinstance(date_obj, Date):
        types.append(Time.Instant)
    if isinstance(date_obj, Interval):
        types.append(Time.Interval)
        #if isinstance(date_obj.lower, UncertainOrApproximate):
        print((date_obj.lower, date_obj.upper))
    return types
