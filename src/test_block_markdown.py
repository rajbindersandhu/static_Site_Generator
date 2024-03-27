import unittest
from htmlnode import ParentNode, LeafNode
from block_markdown import markdown_to_blocks, block_to_block_type, generate_html_heading

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        test_cases = [
            (
                """
                This is **bolded** paragraph

                This is another paragraph with *italic* text and `code` here
                This is the same paragraph on a new line

                * This is a list
                * with items

                """,
                ["This is **bolded** paragraph", 
                 "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                 "* This is a list\n* with items"]
            ),
            ("", [])
        ]

        for test in test_cases:
            expected_lst = test[1]
            recieved_lst = markdown_to_blocks(test[0])

            self.assertListEqual(recieved_lst, expected_lst)

    def test_block_to_block_type(self):
        test_cases = [
            ("# Hello", "heading"),
            ("#Hello", "paragraph"),
            ("```Coding the text\ntestit```", "code"),
            ("```Coding the text\ntestit", "paragraph"),
            (">Hello\n>World\n>testing", "quote"),
            (">Hello\n>World\ntesting", "paragraph"),
            ("*Hello\n*World\n*testing", "ul"),
            ("-Hello\n-World\n-testing", "ul"),
            ("-Hello\n*World\n-testing", "paragraph"),
            ("1. Hello\n2. World\n3. testing", "ol"),
            ("1. Hello\n4. World\n3. testing", "paragraph"),
        ]
        
        error_case = None

        for test in test_cases:
            expected = test[1]
            recieved = block_to_block_type(test[0])

            self.assertEqual(recieved, expected)

        with self.assertRaises(ValueError):
            error = block_to_block_type(error_case)

    def test_generate_html_heading(self):
        test_cases = [
            (
                "# Hello", ParentNode("h1", [LeafNode(None, "Hello")]),
            ),
            (
                "# Hello **world** this is *tests*", ParentNode("h1", [LeafNode(None, "Hello "), LeafNode("b", "world"), LeafNode(None, " this is "), LeafNode("i", "tests")]),
            ),
            (
                "# ![test](Www.com) No image [no add](test)", ParentNode("h1", [LeafNode("img", "", {"src": "Www.com", "alt": "test"}), LeafNode(None, " No image "), LeafNode("a", "no add", {"href": "test"})]),
            )
        ]

        for test in test_cases:
            expected = test[1]
            print(expected)
            recieved = generate_html_heading(test[0])
            print(recieved)
            self.assertEqual(recieved.tag, expected.tag)
            if expected.children:
                for i, childnode in enumerate(expected.children):
                    self.assertEqual(recieved.children[i].tag, childnode.tag)
                    self.assertEqual(recieved.children[i].value, childnode.value)
                    self.assertEqual(recieved.children[i].props, childnode.props)
                    



if __name__ =="__main__":
    unittest.main()