import unittest
from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is test", "bold")
        node2 = TextNode("This is test", "bold")
        self.assertEqual(node1, node2)
    
    def test_not_eq(self):
        node1 = TextNode("This is test1", "bold")
        node2 = TextNode("This is test", "bold")
        self.assertFalse(node1 == node2)

    def test_isEqual(self):
        node1 = TextNode("This is test", "bold")
        node2 = TextNode("This is test", "bold")
        self.assertTrue(node1 == node2)

    def test_repr(self):
        node1 = TextNode("Hello", "invalid", "www.invalid.com")
        output = f"Textnode({"Hello"}, {"invalid"}, {"www.invalid.com"})"
        self.assertEqual(repr(node1), output)

    def text_text_node_to_html_node(self):
        test_cases = [
            (
                TextNode("This is test", "text"),
                LeafNode(None, "This is test", None)
            ),
            (
                TextNode("This is test", "bold"),
                LeafNode("b", "This is test", None)
            ),
            (
                TextNode("This is test", "italic"),
                LeafNode("i", "This is test", None)
            ),
            (
                TextNode("This is test", "code"),
                LeafNode("code", "This is test", None)
            ),
            (
                TextNode("This is test", "link", "www.test.com"),
                LeafNode("s", "This is test", {"href": "www.test.com"})
            ),
            (
                TextNode("This is test", "image", "www.test.com"),
                LeafNode("image", "", {"href": "www.test.com", "alt": "This is test"})
            )
        ]

        error_lst = [
            TextNode("This is test", "z"),
            TextNode("This is test", "Image"),
            TextNode("This is test", "test")
        ]

        for test in test_cases:
            expected = test[1]
            recieved = text_node_to_html_node(test[0])
            self.assertEqual(expected, recieved)

        for testnode in error_lst:
            with self.assertRaises(Exception):
                error = text_node_to_html_node(testnode)
    

        
if __name__ =="__main__":
    unittest.main()