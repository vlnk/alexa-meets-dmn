import json, yaml, os, pystache
from speech_elements import *

class SpeechGenerator(object):
    """docstring for SpeechGenerator."""

    def __init__(self, decision, template):
        self.__decision = decision
        self.__custom_slots = {}
        self.__template = template

    def generate_decision_skill(self):
        skill = {}
        skill[self.__decision.speechType] = self.__decision.name

        return skill

    def generate_decision_template(self):
        template = {}
        template['decision'] = 'Welcome to {{ decision }} decision program. Are you ready to start this dmn program?'

        for input_value in self.__decision.inputs:
            template_string = 'What is your '
            template_string += input_value.title
            template_string += '? '

            template_string += 'You have the choice between the values '
            for item_definition in input_value.items:
                for i, value in enumerate(item_definition.values):
                    if i == 0:
                        template_string += value
                        template_string += ' '
                    elif i == len(item_definition.values) - 1:
                        template_string += 'and '
                        template_string += value
                        template_string += '.'
                    else:
                        template_string += value
                        template_string += ', '

            template[input_value.name] = template_string

        return template

    def write_decision_template(self):
        self.check_speech_folder()

        file = open('speech/templates.yaml','w')

        for key, value in self.generate_decision_template().items():
            file.write(key + ': ' + value)
            file.write('\n')

        file.close()

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

    def generate_script_model(self):
        model = {
            'decision': self.__decision.name,
            'title': self.__decision.title,
            'intents': []
        }

        intents = []
        for input_value in self.__decision.inputs:
            skill = self.generate_input_skill(input_value)

            input_model = {
                'name': input_value.name,
                'fn_name': input_value.fn_name,
            }

            for slot in skill['slots']:
                input_model['type'] = slot['name']
                input_model['values'] = self.generate_slot_model(slot['type'])

            intents.append(input_model)

        model['intents'] = intents
        return model

    def generate_slot_model(self, slot_type):
        values = []
        for value in self.__custom_slots[slot_type]:
            values.append({
                'value': value.lower()
            })

        return values

    def generate_script(self):
        model = self.generate_script_model()
        parsed = pystache.parse(self.__template)

        renderer = pystache.Renderer()
        return renderer.render(parsed, model)

    def write_script(self):
        self.check_speech_folder()

        file = open('speech/speech_script.py','w')
        file.write(self.generate_script())
        file.close()
