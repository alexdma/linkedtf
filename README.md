[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

# LinkEDTF

Extended Date-Time Format (EDTF) Linked Data generator.
[EDTF](https://www.loc.gov/standards/datetime/) is a data representation standard proposed by the [Library of Congress](https://www.loc.gov/) for representing non-conventional dates and times, such as missing digits, seasons, decades, intervals, approximation, and uncertainty.

This implementation allows you to generate a semantic representation of those temporal indicators: you can serve these alongside your Linked Dataset without having to materialize endless RDF descriptions of all possible time indicators.

## Features
- A Python programming library. (_WIP_)
- A Linked Data server. (_coming soon..._)
- Represents data according to the [PeriodO specification](https://periodo.github.io/edtf-ontology/).
- Inherits EDTF compliance from [ixc/python-edtf](https://github.com/ixc/python-edtf).

## Usage

```pycon
>>> from linkedtf import LEDTF
# Initialize with a prefix of choice
>>> le = LEDTF('http://example.com/edtf/')
# Create an RDF resource from the plain string value
>>> s = le.uri('1987/2001')
>>> s
rdflib.term.URIRef('http://example.com/edtf/1987%2F2001')
# Get its description in RDF statements
>>> g = le.description(s)
>>> ttl = g.serialize(format="ttl")
>>> ttl
<http://example.com/edtf/1987%2F2001> a <http://www.w3.org/2006/time#DateTimeDescription> .
# ...
```

## Limitations
- EDTF seems to lack support for calendars other than the Gregorian one.
- _Won't do_: SPARQL query engine for EDTF data generated on-the-fly; would be nice to have but some queries could never terminate.

## Rights
[LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.en.html)