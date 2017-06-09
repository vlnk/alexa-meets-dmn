#!/usr/bin/python

import sys, getopt
from lxml import etree

def read_xml(path):
    tree = etree.parse(path)

    decision_table_path = "/semantic:definitions/semantic:decision/semantic:decisionTable"
    input_tag = "semantic:input"
    input_expression_tag = "semantic:inputExpression"

    dmn = {
        'semantic': 'http://www.omg.org/spec/DMN1-2Alpha/20160929/MODEL',
        'triso': 'http://www.trisotech.com/2015/triso/modeling'
    }

    for decision_table in tree.xpath(decision_table_path, namespaces=dmn):
        print(decision_table.get("id"));

        for input in decision_table.findall(input_tag, namespaces=dmn):
            print(input.get("id"));

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('dmnToSpeech.py <input> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    read_xml(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
