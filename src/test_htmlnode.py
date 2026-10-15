import unittest
from htmlnode import *

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "This is a div", [], {"class": "my-class"})
        node2 = HTMLNode("div", "This is a div", [], {"class": "my-class"})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("div", "This is a div", [], {"class": "my-class"})
        node2 = HTMLNode("span", "This is a span", [], {"class": "my-class"})
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("a", "Click here", [], {"href": "https://example.com"})
        expected_html = ' href="https://example.com"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", {"class": "child-class"})
        parent_node = ParentNode("div", [child_node], {"id": "parent-id"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="parent-id"><span class="child-class">child</span></div>',
        )