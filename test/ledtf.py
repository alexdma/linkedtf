import unittest
import urllib.parse

from pyparsing import ParseException
from rdflib import RDF

from edtf2 import parse_edtf as parse

from linkedtf import EDTFO, LEDTF, Time
from linkedtf.model import guess_types


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

    def testTypeGuessing(self):
        e = LEDTF(EDTF._NS_EXAMPLE)
        ts = guess_types(parse('1970-01-01'))
        self.assertIn(Time.Instant, ts)
        self.assertNotIn(Time.Interval, ts)
        # Proper interval
        ts = guess_types(parse('1970-01-01/1971-12-31'))
        self.assertNotIn(Time.Instant, ts)
        self.assertIn(Time.Interval, ts)
        # Backwards interval, what happens to upper and lower?
        ts = guess_types(parse('1972-01-01/1971-12-31'))
        self.assertNotIn(Time.Instant, ts)
        self.assertIn(Time.Interval, ts)
        # Obsolete interval specification
        try:
            val = '1970-01-01/open'
            ts = guess_types(parse(val))
            self.fail('Obsolete open interval value "{}" was supposed to raise an exception.'.format(val))
        except ParseException:
            pass
        # Open interval ("still ongoing")
        ts = guess_types(parse('1970-01-01/..'))
        self.assertNotIn(Time.Instant, ts)
        self.assertIn(Time.Interval, ts)
        self.assertNotIn(EDTFO.OpenBeginningInterval, ts)
        self.assertIn(EDTFO.OpenEndInterval, ts)
        # Unknown start interval ("no idea when it began")
        ts = guess_types(parse('/1970-01-01'))
        self.assertNotIn(Time.Instant, ts)
        self.assertIn(Time.Interval, ts)
        # Fully open interval
        ts = guess_types(parse('../..'))
        self.assertNotIn(Time.Instant, ts)
        self.assertIn(Time.Interval, ts)
        self.assertIn(EDTFO.OpenBeginningInterval, ts)
        self.assertIn(EDTFO.OpenEndInterval, ts)
        # (a time in a) Month of a year
        ts = guess_types(parse('1970-01'))
        self.assertIn(Time.Instant, ts)

    def testRDFDecade(self):
        e = LEDTF(EDTF._NS_EXAMPLE)
        val = '199X-XX-XX'
        rdf = e.description(val)
        """
        ex:when a time:Instant ;
  time:inDateTime  [
    a edtfo:DecadeDescription ;
    time:unitType time:unitYear ;
    edtfo:decade 201
    ]
  .
        """

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
        g = e.description(val)
        self.assertGreater(len(g), 0)
        for s in g.subjects(RDF.type, Time.DateTimeDescription):
            self.assertEqual(s, u)


if __name__ == '__main__':
    unittest.main()
