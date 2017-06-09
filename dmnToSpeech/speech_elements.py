import re

class SpeechElement:
    def __init__(self, name, speechType):
        self.__name = name.replace(' ', '')
        self.__speechType = speechType

    @property
    def name(self):
        return self.__name

    @property
    def speechType(self):
        return self.__speechType

class Decision(SpeechElement):
    def __init__(self, name):
        SpeechElement.__init__(self, name, 'intent')
        self.__inputs = []

    @property
    def inputs(self):
        return self.__inputs

    def add_input(self, input):
        self.__inputs.append(input)

    def __str__(self):
        result = self.name

        for input_value in self.__inputs:
            result += '\n\t' + input_value.__str__()

        return result

class ItemDefinition(SpeechElement):
    def __init__(self, name, constraint_type, constraint_values):
        SpeechElement.__init__(self, name, 'slot')

        type_matcher = {
            'enumeration': self.set_enumeration,
            'simple': self.set_simple
        }

        self.__values = type_matcher[constraint_type](constraint_values)

    @property
    def values(self):
        return self.__values

    def set_enumeration(self, enumeration):
        values = enumeration.split(',')
        return [value.replace('"', '') for value in values]

    def set_simple(self, simple):
        match_simple = re.search('\[(\d+)\.\.(\d+)\]', simple)
        simple_min = int(match_simple.group(0))
        simple_max = int(match_simple.group(1))

        if (simple_min is not None and simple_max is not None):
            return [value for value in range(simple_min, simple_max + 1)]

        return []

    def __str__(self):
        result = self.name + ': '
        result += ', '.join(self.__values)

        return result

class Input(SpeechElement):
    def __init__(self, name):
        SpeechElement.__init__(self, name, 'intent')
        self.__items = []

    @property
    def items(self):
        return self.__items

    def add_item(self, item):
        if (item not in self.__items):
            self.__items.append(item)

    def __str__(self):
        result = self.name
        for item_definition in self.__items:
            result += '\n\t' + item_definition.__str__()

        return result
