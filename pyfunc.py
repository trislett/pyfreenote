#!/usr/bin/env python

#    Various functions for TFCE_mediation
#    Copyright (C) 2016  Tristram Lett, Lea Waller

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import numpy as np

# APA Lett, Tristram A., et al. "The genome-wide supported microRNA-137 variant predicts phenotypic heterogeneity within schizophrenia." Molecular psychiatry 18.4 (2013): 443.

class Citation(object):
	def __init__(self, uniqueid, authors, title, journal_title, year, volume, volume_number, pages, reftype = None, publisher = None, doi = None, pmid = None, link = None, pdf_avail = False):
		self.uniqueid = uniqueid
		self.authors = authors
		self.title = title
		self.journal_title = journal_title
		self.year = year
		self.volume = volume
		self.volume_number = volume_number
		self.pages = pages
		self.reftype = reftype
		self.publisher = publisher
		self.doi = doi
		self.pmid = pmid
		self.link = link
		self.pdf_avail = pdf_avail

def find_parens(s, bracket_type = ['{','}']): # lazy ->from stack overflow
	toret = {}
	pstack = []
	for i, c in enumerate(s):
		if c == bracket_type[0]:
			pstack.append(i)
		elif c == bracket_type[1]:
			if len(pstack) == 0:
				raise IndexError("No matching closing parens at: " + str(i))
			toret[pstack.pop()] = i
	if len(pstack) > 0:
		raise IndexError("No matching opening parens at: " + str(pstack.pop()))
	start = list(toret)[-1] # just the outermost brackets
	stop = toret[start]
	return start, stop

def read_bibtex(bib_file, uniqueid, verbose = False):
	bibfileobject = open(bib_file)
	reader = 'start'
	while reader is not '':
		reader = bibfileobject.readline().strip()
		if verbose:
			print(reader)
		if reader.startswith('@'):
			reftype = reader.split('@')[1]
			reftype = reftype.split('{')[0]
		if reader.startswith('title'):
			indices = find_parens(reader)
			title = reader[indices[0]+1:indices[1]]
		if reader.startswith('author'):
			indices = find_parens(reader)
			authors = reader[indices[0]+1:indices[1]]
			author_list = authors.split(' and ')
		if reader.startswith('journal'):
			indices = find_parens(reader)
			journal_title = reader[indices[0]+1:indices[1]]
		if reader.startswith('volume'):
			indices = find_parens(reader)
			volume = reader[indices[0]+1:indices[1]]
		if reader.startswith('number'):
			indices = find_parens(reader)
			volume_number = reader[indices[0]+1:indices[1]]
		if reader.startswith('pages'):
			indices = find_parens(reader)
			pages = reader[indices[0]+1:indices[1]]
		if reader.startswith('year'):
			indices = find_parens(reader)
			year = reader[indices[0]+1:indices[1]]
		if reader.startswith('publisher'):
			indices = find_parens(reader)
			publisher = reader[indices[0]+1:indices[1]]
	return Citation(uniqueid = uniqueid, authors = author_list, title = title, journal_title = journal_title, year = year, volume = volume, volume_number = volume_number, pages = pages, publisher = publisher, reftype = reftype)




