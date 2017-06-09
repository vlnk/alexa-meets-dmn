import json, os
from speech_elements import *

class SpeechGenerator(object):
    """docstring for SpeechGenerator."""

    def __init__(self, decision):
        self.__decision = decision
        self.__custom_slots = {}

    def generate_decision_skill(self):
        skill = {}
        skill[self.__decision.speechType] = self.__decision.name

        return skill

    def generate_input_skill(self, input_value):
        skill = {}
        skill[input_value.speechType] = input_value.name
        slots = []

        for item in input_value.items:
            slots.append(self.generate_item_definition_slot(item))

        skill['slots'] = slots
        return skill

    def generate_item_definition_slot(self, item_definition):
        slot_name = item_definition.name
        slot_type = 'LIST_OF_' + item_definition.name.upper()

        if slot_type not in self.__custom_slots.keys():
            self.__custom_slots[slot_type] = item_definition.values

        return {
            'name': slot_name,
            'type': slot_type
        }

    def generate_skills(self):
        intents = [self.generate_decision_skill()]
        for input_value in self.__decision.inputs:
            intents.append(self.generate_input_skill(input_value))

        return {
            'intents': intents
        }

    def write_skills(self):
        if not os.path.exists('build'):
            os.makedirs('build')

        file = open('build/skills.json','w')
        file.write(json.dumps(self.generate_skills()))
        file.close()

    def generate_custom_slot_types(self):
        pass
