import unittest
import xml.etree.ElementTree as ET
from io import StringIO
from translator import process_xml_element, process_comment, process_constant, process_expression

class TestXmlToConfigConverter(unittest.TestCase):

    def test_comment_processing(self):
        xml = """
        <comment>
            <line>Это однострочный комментарий</line>
        </comment>
        """
        element = ET.fromstring(xml)
        self.assertEqual(process_comment(element), "\\ Это однострочный комментарий")

        xml_multiline = """
        <comment>
            <line>Это многострочный</line>
            <line>комментарий</line>
        </comment>
        """
        element_multiline = ET.fromstring(xml_multiline)
        self.assertEqual(
            process_comment(element_multiline),
            "=begin\nЭто многострочный\nкомментарий\n=cut"
        )

    def test_constant_processing(self):
        xml_integer = """
        <constant name="num">
            <value type="integer">10</value>
        </constant>
        """
        element_integer = ET.fromstring(xml_integer)
        self.assertEqual(process_constant(element_integer), "num is 10")

        xml_string = """
        <constant name="str">
            <value type="string">Hello</value>
        </constant>
        """
        element_string = ET.fromstring(xml_string)
        self.assertEqual(process_constant(element_string), 'str is "Hello"')

        xml_array = """
        <constant name="numbers">
            <value type="integer">
                <array>
                    <item>1</item>
                    <item>2</item>
                </array>
            </value>
        </constant>
        """
        element_array = ET.fromstring(xml_array)
        self.assertEqual(process_constant(element_array), "numbers is << 1, 2 >>")

    def test_expression_processing(self):
        xml_add = """
        <expression operation="add">
            <operands>
                <operand>num</operand>
                <operand>5</operand>
            </operands>
        </expression>
        """
        element_add = ET.fromstring(xml_add)
        self.assertEqual(process_expression(element_add), "$+ num 5$")

        xml_abs = """
        <expression operation="abs">
            <operands>
                <operand>-20</operand>
            </operands>
        </expression>
        """
        element_abs = ET.fromstring(xml_abs)
        self.assertEqual(process_expression(element_abs), "$abs -20$")

    def test_full_xml_processing(self):
        xml = """
        <config>
            <comment>
                <line>Это однострочный комментарий</line>
            </comment>
            <constant name="num">
                <value type="integer">10</value>
            </constant>
            <expression operation="add">
                <operands>
                    <operand>num</operand>
                    <operand>5</operand>
                </operands>
            </expression>
        </config>
        """
        element = ET.fromstring(xml)
        expected_result = "\\ Это однострочный комментарий\nnum is 10\n$+ num 5$"
        self.assertEqual(process_xml_element(element), expected_result)

if __name__ == "__main__":
    unittest.main()