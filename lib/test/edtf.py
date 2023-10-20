import unittest
import urllib.parse

from pyparsing import ParseException
from rdflib import RDF

from ..linkedtf import LEDTF, Time


class EDTF(unittest.TestCase):
    _NS_EXAMPLE = 'http://example.org/ns/test/linkedtf/'
    _NS_EXAMPLE_GEMINI = 'gemini://example.org/ns/test/linkedtf/'

    def testNamespace(self):
        try:
            e = LEDTF(None)
            self.fail('LEDTF(namespace=None) did not raise expected ValueError')
        except ValueError:
            pass
        e = LEDTF(EDTF._NS_EXAMPLE)
        self.assertEqual(e.namespace, EDTF._NS_EXAMPLE)
        e = LEDTF(EDTF._NS_EXAMPLE_GEMINI)
        self.assertEqual(e.namespace, EDTF._NS_EXAMPLE_GEMINI)

    def testURI(self):
        e = LEDTF(EDTF._NS_EXAMPLE)
        try:
            val = 'pippobaudo'
            e.uri(val)
            self.fail('Erroneous value "{}" should have raised an exception.'.format(val))
        except ParseException:
            pass
        val = '1987/1981'
        self.assertEqual(str(e.uri(val)), EDTF._NS_EXAMPLE + urllib.parse.quote_plus(val))

    def testRDF(self):
        e = LEDTF(EDTF._NS_EXAMPLE)
        try:
            val = 'pippobaudo'
            e.description(val)
            self.fail('Erroneous value "{}" should have raised an exception.'.format(val))
        except ParseException:
            pass
        val = '1987/1981'
        u = e.uri(val)
        g = e.description(u)
        self.assertGreater(len(g), 0)
        for s in g.subjects(RDF.type, Time.DateTimeDescription):
            self.assertEqual(s, u)


if __name__ == '__main__':
    unittest.main()
