import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node1 = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node1.to_html()

    def test_props_to_html(self):
        node1 = HTMLNode("h1", "Hello World", props={"id":"test1"})
        node1_prop_exp = f' id="test1"'
        node2 = HTMLNode("a", "Link", node1, {"id":"parent", "href":"www.test.com"})
        node2_prop_exp = f' id="parent" href="www.test.com"'
        node3 = HTMLNode()
        node3_prop_exp = ""

        self.assertEqual(node1.props_to_html(), node1_prop_exp)
        self.assertEqual(node2.props_to_html(), node2_prop_exp)
        self.assertEqual(node3.props_to_html(), node3_prop_exp)

    def test_print(self):
        node1 = HTMLNode("h1", "Hello World", props={"id":"test1"})
        node2 = HTMLNode("a", "Link", node1, {"id":"parent", "href":"www.test.com"})
        node1_print_output_expected = "HTMLNode(tag=h1, value=Hello World, children=None, props={'id': 'test1'})"
        node1_print_output_recieved = repr(node1)
        node2_print_output_expected = "HTMLNode(tag=a, value=Link, children=HTMLNode(tag=h1, value=Hello World, children=None, props={'id': 'test1'}), props={'id': 'parent', 'href': 'www.test.com'})"
        node2_print_output_recieved = repr(node2)
        self.assertEqual(node1_print_output_recieved, node1_print_output_expected)
        self.assertEqual(node2_print_output_recieved, node2_print_output_expected)

    def test_leafnode(self):
        test_list = [
            (LeafNode("p", "This is a paragraph of text."), "<p>This is a paragraph of text.</p>"),
            (LeafNode("a", "Click me!", {"href": "https://www.google.com"}), '<a href="https://www.google.com">Click me!</a>'),
            (LeafNode("", "This is a paragraph of text."), "This is a paragraph of text."),
            (LeafNode(" ", "This is a paragraph of text."), "This is a paragraph of text.")
        ]
        
        error_lst = [
            LeafNode("", "Click me!", {"href": "https://www.google.com"}),
            LeafNode("p", None),
            LeafNode(" ", "Click me!", {"href": "https://www.google.com"}),
        ]

        for test in test_list:
            leafnode = test[0]
            expected_rslt = test[1]
            self.assertEqual(leafnode.to_html(), expected_rslt)

        for test in error_lst:
            leafnode = test
            with self.assertRaises(ValueError):
                leafnode.to_html()

    def test_parentnode(self):
        test_cases=[
            (
                ParentNode("p",[LeafNode("b", "Bold text"),LeafNode("", "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),]),
                "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
            ),
            (
                ParentNode(
                    "div",[
                        ParentNode("sec", [LeafNode("b", "Bold text"),
                                         LeafNode(None, "Normal text"),
                                         LeafNode("i", "italic text")
                                         ]),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text")
                        ]
                        ),
                "<div><sec><b>Bold text</b>Normal text<i>italic text</i></sec>Normal text<i>italic text</i>Normal text</div>"
            )
        ]

        error_lst=[
            ParentNode("", [LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),],),
            ParentNode("test",[]),
            ParentNode("", [LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),],{"href": "https://www.google.com"})
        ]

        for test_case in test_cases:
            recieved = test_case[0].to_html()
            expected_rslt = test_case[1]
            self.assertEqual(recieved, expected_rslt)

        for test in error_lst:
            parentnode = test
            with self.assertRaises(ValueError):
                parentnode.to_html()
  
if __name__ =="__main__":
    unittest.main()