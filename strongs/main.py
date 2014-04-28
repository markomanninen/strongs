#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# file: main.py

import re
import pandas as pd
from os.path import isfile
from tagpy import helper as h, table
from isopsephy import preprocess_greek, to_roman, isopsephy

dictionary = pd.DataFrame()

def load_dataframe(csv = "nt-strongs.csv"):
    global dictionary
    if isfile(csv):
        print "Retrieving data from local csv copy..."
        dictionary = pd.read_csv(csv, sep = "\t")
        # greek sords are pre processed for simpler forms without accents
        dictionary['word'] = dictionary['word'].map(lambda x: preprocess_greek(x))
        # adding transliteration of the words to the dataframe
        dictionary['transliteration'] = dictionary['word'].map(lambda x: to_roman(x))
        # adding word isopsephy value to the dataframe
        dictionary['isopsephy'] = dictionary['word'].map(lambda x: isopsephy(x))
    else:
        print "Cannot read csv file: %s! Please check path/filename and reload dictionary with load_dataframe(csv = \"your_filename\") function" % csv

def find(query, column):
    global dictionary
    # if culumn is "isopsephy" use == compare
    return dictionary[dictionary[column] == query] if column == 'isopsephy' else dictionary[dictionary[column].str.contains(query)]

def search_strongs_dictionary_table(query, field):
    # initialize tagpy table object
    tbl = table(Class='data')
    # add head row columns
    tbl.addHeadRow(h.tr(h.th('Lemma'), h.th('Word'), h.th('Transliteration'), h.th('Translation'), h.th('Isopsephy')))
    # make search. if field is isopsephy, force search item to int type
    rows = find(int(query) if field == 'isopsephy' else re.compile(query, re.IGNORECASE), field)
    for i, item in rows.iterrows():
        tbl.addBodyRow(h.tr(h.td(item.lemma), h.td(item.word), h.td(item.transliteration), h.td(item.translation), h.td(item.isopsephy)))
    return tbl

def search_strongs_dictionary_html(query, field):
    # using print data stream instead of returning data makes 
    # less hassle with unicodes and character encodings
    print str(search_strongs_dictionary_table(query, field))