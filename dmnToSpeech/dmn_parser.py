from speech_elements import Decision, Input, ItemDefinition
from lxml import etree

class DMNParser:
    def __init__(self, path):
        self.__decisions = {}
        self.__inputs = {}

        self.__dmn_namespaces = {
            'semantic': 'http://www.omg.org/spec/DMN1-2Alpha/20160929/MODEL',
            'triso': 'http://www.trisotech.com/2015/triso/modeling'
        }

        self.__dmn_tree = etree.parse(path)
        self.create_decisions()

    @property
    def decisions(self):
        return self.__decisions.values()

    def __str__(self):
        result = ''

        for decision_value in self.__decisions.values():
            result += decision_value.__str__()

            result += '\n'

        return result

    def create_decisions(self):
        decision_path = '/semantic:definitions/semantic:decision/semantic:decisionTable'
        for decision_xml in self.__dmn_tree.xpath(decision_path, namespaces=self.__dmn_namespaces):
            decision_name = decision_xml.get('outputLabel')
            decision_id = decision_xml.get('id')

            if decision_name is None:
                continue

            self.__decisions[decision_id] = Decision(decision_name)
            self.create_inputs(etree.ElementTree(decision_xml), decision_id)

    def create_inputs(self, decision_tree, decision_id):
        input_path = '/semantic:decisionTable/semantic:input'
        for input_xml in decision_tree.xpath(input_path, namespaces=self.__dmn_namespaces):
            input_id = input_xml.get('id')
            input_name = input_id

            input_expr_path = '/semantic:input/semantic:inputExpression'
            input_type_ref = ''
            input_tree = etree.ElementTree(input_xml)

            for input_expr_xml in input_tree.xpath(input_expr_path, namespaces=self.__dmn_namespaces):
                input_type_ref = input_expr_xml.get('typeRef')

                input_name_path = '/semantic:inputExpression/semantic:text'
                input_expr_tree = etree.ElementTree(input_expr_xml)

                for input_name_xml in input_expr_tree.xpath(input_name_path, namespaces=self.__dmn_namespaces):
                    input_name = input_name_xml.text

            self.__inputs[input_id] = Input(input_name)
            self.create_item_definition(input_type_ref, input_id)

            self.__decisions[decision_id].add_input(self.__inputs[input_id])

    def create_item_definition(self, type_reference, input_id):
        item_def_path = '/semantic:definitions/semantic:itemDefinition'
        for item_def_xml in self.__dmn_tree.xpath(item_def_path, namespaces=self.__dmn_namespaces):
            item_def_name = item_def_xml.get('name')

            if (item_def_name == type_reference):
                item_tree = etree.ElementTree(item_def_xml)

                item_constraint = 'simple'
                item_values = ''

                constraint_path = '/semantic:itemDefinition/semantic:allowedValues'
                for constraint_xml in item_tree.xpath(constraint_path, namespaces=self.__dmn_namespaces):
                    item_constraint = constraint_xml.get('{' + self.__dmn_namespaces['triso'] + '}constraintsType')

                    constraint_tree = etree.ElementTree(constraint_xml)
                    values_path = '/semantic:allowedValues/semantic:text'
                    for values_xml in constraint_tree.xpath(values_path, namespaces=self.__dmn_namespaces):
                        items_values = values_xml.text

                item_definition = ItemDefinition(item_def_name, item_constraint, items_values)
                self.__inputs[input_id].add_item(item_definition)
