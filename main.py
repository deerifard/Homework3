import xml.etree.ElementTree as ET
import re
import sys


class ConfigTranslator:
    def __init__(self):
        self.constants = {}

    def parse_xml(self, xml_text):
        try:
            root = ET.fromstring(xml_text)
            return root
        except ET.ParseError as e:
            raise ValueError(f"XML Parsing Error: {e}")

    def translate(self, element):
        if element.tag == "array":
            return self.translate_array(element)
        elif element.tag == "dict":
            return self.translate_dict(element)
        elif element.tag == "def":
            return self.translate_constant(element)
        elif element.tag == "compute":
            return self.translate_compute(element)
        elif element.tag == "value":
            return element.text.strip()
        else:
            raise ValueError(f"Unknown element: {element.tag}")

    def translate_array(self, element):
        values = [self.translate(child) for child in element]
        return f"( {', '.join(values)} )"

    def translate_dict(self, element):
        pairs = [f"{child.attrib['name']} : {self.translate(child)}" for child in element]
        return f"$[\n  {',\n  '.join(pairs)}\n]"

    def translate_constant(self, element):
        name = element.attrib.get("name")
        value = element.text.strip() if element.text else None
        if name is None or value is None:
            raise ValueError("Invalid constant definition.")
        self.constants[name] = value
        return f"def {name} := {value}"

    def translate_compute(self, element):
        expression = element.text.strip()
        for const, value in self.constants.items():
            expression = expression.replace(const, value)
        result = self.evaluate_expression(expression)
        return f"?{{{expression} => {result}}}"

    def evaluate_expression(self, expression):
        try:
            stack = []
            tokens = expression.split()
            for token in tokens:
                if token.isdigit():
                    stack.append(int(token))
                elif token == "+":
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a + b)
                elif token == "mod":
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a % b)
                else:
                    raise ValueError(f"Unknown token: {token}")
            return stack[0]
        except (IndexError, ValueError):
            raise ValueError("Invalid expression")

    def translate_document(self, xml_text):
        root = self.parse_xml(xml_text)
        return "\n".join(self.translate(child) for child in root)


def main():
    xml_input = sys.stdin.read()
    translator = ConfigTranslator()
    try:
        output = translator.translate_document(xml_input)
        print(output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
