import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<a>", "LINK", [], {})
        node2 = HTMLNode("<a>", "LINK", [], {})
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("<a>", "LINK", [], dict())
        node2 = HTMLNode("<a>", "LINK", [], {"href" : "youtube.com"})
        self.assertNotEqual(node.props_to_html, node2.props_to_html)

    def test_eq3(self):
        node = HTMLNode("<a>", "LINK", [], dict())
        node2 = HTMLNode("<h1>", "LINK", [], dict())
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()