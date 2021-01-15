import io
import unittest
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import clean_notacast

TEST_DATA_PATH = Path(__file__).resolve().parent


def parse_input(filename) -> Element:
    return ElementTree.parse(TEST_DATA_PATH / filename).getroot()


class TestCleanNotACast(unittest.TestCase):
    def assert_equal_to_output(self, filename, xml):
        expected = (TEST_DATA_PATH / filename).read_text(encoding="utf-8")
        actual = ElementTree.tostring(xml, encoding='unicode')
        self.assertEqual(expected, actual)

    def test_indent_one_item(self):
        xml = parse_input("test_1_input.xml")
        clean_notacast.indent(xml, spaces=4)
        self.assert_equal_to_output("test_1_output.xml", xml)

    def test_indent_two_items(self):
        xml = parse_input("test_2_input.xml")
        clean_notacast.indent(xml, spaces=4)
        self.assert_equal_to_output("test_2_output.xml", xml)

    def test_indent_three_items(self):
        xml = parse_input("test_3_input.xml")
        clean_notacast.indent(xml)
        self.assert_equal_to_output("test_3_output.xml", xml)

    def test_remove_duplicates(self):
        xml = parse_input("test_4_input.xml")
        clean_notacast.remove_duplicate_items(xml)
        clean_notacast.indent(xml, spaces=4)
        self.assert_equal_to_output("test_4_output.xml", xml)

    def test_update_metadata(self):
        xml = parse_input("test_5_input.xml")
        clean_notacast.update_metadata(xml)
        clean_notacast.indent(xml, spaces=4)
        self.assert_equal_to_output("test_5_output.xml", xml)

