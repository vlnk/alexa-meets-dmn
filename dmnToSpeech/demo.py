import logging

from random import randint

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

import argparse
import sys

from dmn_parser import DMNParser
from speech_generator import SpeechGenerator

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

parser = None

@ask.launch
def new_decision():
    decision_msg = render_template('decision', decision=decision_name)
    return question(decision_msg)

def get_args(argv):
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

    return inputfile

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Process a dmn file to Alexa configuration', prog='DMNToSpeech')
    argparser.add_argument('dmn_path', nargs=1, help='the path of the dmn export')
    args = argparser.parse_args()

    parser = DMNParser(args.dmn_path[0])

    file_template = open('template_backend.mustache', 'r')
    template = file_template.read()
    file_template.close()

    for decision in parser.decisions:
        generator = SpeechGenerator(decision, template)
        generator.write_skills()
        generator.write_custom_slot_types()
        generator.write_utterances()
        generator.write_decision_template()
        generator.write_script()
