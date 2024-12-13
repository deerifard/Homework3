import unittest
from xml.etree.ElementTree import Element
from main import ConfigTranslator

class TestConfigTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = ConfigTranslator()

    def test_translate_value(self):
        element = Element('value')
        element.text = '42'
        self.assertEqual(self.translator.translate(element), '42')

    def test_translate_array(self):
        array = Element('array')
        child1 = Element('value')
        child1.text = '1'
        child2 = Element('value')
        child2.text = '2'
        child3 = Element('value')
        child3.text = '3'
        array.extend([child1, child2, child3])
        self.assertEqual(self.translator.translate(array), '( 1, 2, 3 )')

    def test_translate_dict(self):
        dict_element = Element('dict')
        child1 = Element('value', name='key1')
        child1.text = 'value1'
        child2 = Element('value', name='key2')
        child2.text = 'value2'
        dict_element.extend([child1, child2])
        expected = "$[\n  key1 : value1,\n  key2 : value2\n]"
        self.assertEqual(self.translator.translate(dict_element), expected)

    def test_translate_constant(self):
        const_element = Element('def', name='PI')
        const_element.text = '3.14'
        self.assertEqual(self.translator.translate(const_element), 'def PI := 3.14')
        self.assertIn('PI', self.translator.constants)
        self.assertEqual(self.translator.constants['PI'], '3.14')

    def test_translate_compute(self):
        # Define a constant first
        const_element = Element('def', name='TEN')
        const_element.text = '10'
        self.translator.translate(const_element)

        compute_element = Element('compute')
        compute_element.text = 'TEN 2 +'
        # Since the constant is replaced with its value, the output should reflect that
        self.assertEqual(self.translator.translate(compute_element), '?{10 2 + => 12}')

    def test_invalid_expression(self):
        compute_element = Element('compute')
        compute_element.text = '1 2 + +'
        with self.assertRaises(ValueError):
            self.translator.translate(compute_element)

    def test_unknown_element(self):
        unknown_element = Element('unknown')
        with self.assertRaises(ValueError):
            self.translator.translate(unknown_element)

if __name__ == '__main__':
    unittest.main()
