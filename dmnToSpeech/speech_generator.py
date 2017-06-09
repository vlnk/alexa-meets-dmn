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

    def generate_decision_utterance(self):
        utterances = {}
        decision = self.__decision.name

        utterance = []
        utterance.append('yes')
        utterance.append('sure')

        utterances[decision] = utterance
        for input_value in self.__decision.inputs:
            utterances[input_value.name] = self.generate_input_utterance(input_value)

        return utterances

    def generate_input_utterance(self, input_value):
        utterance = []
        name = input_value.name

        for item_definition in input_value.items:
            utterance.append('{' + item_definition.name + '}')

        return utterance

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

    def check_speech_folder(self):
        if not os.path.exists('speech'):
            os.makedirs('speech')

    def write_skills(self):
        self.check_speech_folder()

        file = open('speech/skills.json','w')
        file.write(json.dumps(self.generate_skills()))
        file.close()

    def write_custom_slot_types(self):
        self.check_speech_folder()

        for type_key, slot_types in self.__custom_slots.items():
            file = open('speech/' + type_key + '.txt','w')

            for value in slot_types:
                file.write(value)
                file.write('\n')

            file.close()

    def write_utterances(self):
        self.check_speech_folder()
        utterances = self.generate_decision_utterance()
        file = open('speech/utterances.txt','w')

        for intent, utterance in utterances.items():
            for sentance in utterance:
                file.write(intent + ' ' + sentance)
                file.write('\n')

            file.write('\n')

        file.close()
