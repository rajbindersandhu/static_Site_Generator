import unittest
from htmlnode import ParentNode, LeafNode
from block_markdown import markdown_to_blocks, block_to_block_type, generate_html_heading, generate_html_code, generate_html_quote, generate_html_unodr_lst, generate_html_odr_lst, generate_html_para

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
            recieved = generate_html_heading(test[0])
            self.assertEqual(recieved.tag, expected.tag)
            if expected.children:
                for i, childnode in enumerate(expected.children):
                    self.assertEqual(recieved.children[i].tag, childnode.tag)
                    self.assertEqual(recieved.children[i].value, childnode.value)
                    self.assertEqual(recieved.children[i].props, childnode.props)

    def test_generate_html_code(self):
        test_cases = [
            (
                "``` Hello\nworld```", ParentNode("pre", [LeafNode("code", " Hello\nworld")]),
            )
        ]

        for test in test_cases:
            expected = test[1]
            recieved = generate_html_code(test[0])
            self.assertEqual(recieved.tag, expected.tag)
            if expected.children:
                for i, childnode in enumerate(expected.children):
                    self.assertEqual(recieved.children[i].tag, childnode.tag)
                    self.assertEqual(recieved.children[i].value, childnode.value)
                    self.assertEqual(recieved.children[i].props, childnode.props)
                    

    def test_generate_html_quote(self):
        test_cases = [
            (
                ">Hello **World**",
                ParentNode("blockquote", [LeafNode(None, "Hello "), LeafNode("b", "World")])
            ),
            (
                ">Hello\n>World\n>test",
                ParentNode("blockquote", [LeafNode(None, "Hello"), LeafNode(None, "World"), LeafNode(None, "test")])
            ),
            (
                ">Hello **Test**\n>World *italic*\n>test [text](test.com)",
                ParentNode("blockquote", [LeafNode(None, "Hello "), LeafNode("b", "Test"), LeafNode(None, "World "), LeafNode("i", "italic"), LeafNode(None, "test "), LeafNode("a", "text", {"href": "test.com"})])
            )
        ]

        for test in test_cases:
            expected = test[1]
            recieved = generate_html_quote(test[0])
            self.assertEqual(recieved.tag, expected.tag)
            if expected.children:
                for i, childnode in enumerate(expected.children):
                    self.assertEqual(recieved.children[i].tag, childnode.tag)
                    self.assertEqual(recieved.children[i].value, childnode.value)
                    self.assertEqual(recieved.children[i].props, childnode.props)

    def test_generate_html_unodr_lst(self):
        test_case = [
            (
                "* Hello\n* World",
                ParentNode("ul", [ParentNode("li", [LeafNode(None, "Hello")]), ParentNode("li", [LeafNode(None, "World")])])
            ),
            (
                "* Hello **Test**\n*World *italic*\n* test [text](test.com)",
                ParentNode("ul", [ParentNode("li", [LeafNode(None, "Hello "), LeafNode("b", "Test")]), ParentNode("li", [LeafNode(None, "World "), LeafNode("i", "italic")]), ParentNode("li", [LeafNode(None, "test "), LeafNode("a", "text", {"href":"test.com"})])])
            ),
            (
                "- Hello\n- World",
                ParentNode("ul", [ParentNode("li", [LeafNode(None, "Hello")]), ParentNode("li", [LeafNode(None, "World")])])
            ),
            (
                "- Hello **Test**\n-World *italic*\n- test [text](test.com)",
                ParentNode("ul", [ParentNode("li", [LeafNode(None, "Hello "), LeafNode("b", "Test")]), ParentNode("li", [LeafNode(None, "World "), LeafNode("i", "italic")]), ParentNode("li", [LeafNode(None, "test "), LeafNode("a", "text", {"href":"test.com"})])])
            )
        ]

        for test in test_case:
            expected = test[1]
            recieved = generate_html_unodr_lst(test[0])
            self.assertEqual(expected.tag, recieved.tag)

            if expected.children:
                for i, childnode in enumerate(expected.children):
                    self.assertEqual(childnode.tag, recieved.children[i].tag)
                    for j, grandchild in enumerate(childnode.children):
                        self.assertEqual(recieved.children[i].children[j].tag, grandchild.tag)
                        self.assertEqual(recieved.children[i].children[j].value, grandchild.value)
                        self.assertEqual(recieved.children[i].children[j].props, grandchild.props)

    def test_generate_html_odr_lst(self):
        test_case = [
            (
                "1. Hello\n2. World",
                ParentNode("ol", [ParentNode("li", [LeafNode(None, "Hello")]), ParentNode("li", [LeafNode(None, "World")])])
            ),
            (
                "1. Hello **Test**\n2. World *italic*\n3. test [text](test.com)",
                ParentNode("ol", [ParentNode("li", [LeafNode(None, "Hello "), LeafNode("b", "Test")]), ParentNode("li", [LeafNode(None, "World "), LeafNode("i", "italic")]), ParentNode("li", [LeafNode(None, "test "), LeafNode("a", "text", {"href":"test.com"})])])
            )
        ]

        for test in test_case:
            expected = test[1]
            recieved = generate_html_odr_lst(test[0])
            self.assertEqual(expected.tag, recieved.tag)

            if expected.children:
                for i, childnode in enumerate(expected.children):
                    self.assertEqual(childnode.tag, recieved.children[i].tag)
                    for j, grandchild in enumerate(childnode.children):
                        self.assertEqual(recieved.children[i].children[j].tag, grandchild.tag)
                        self.assertEqual(recieved.children[i].children[j].value, grandchild.value)
                        self.assertEqual(recieved.children[i].children[j].props, grandchild.props)

    def test_generate_html_para(self):
        test_cases = [
            (
                "Hello\nworld\ntesting para",
                ParentNode("p", [LeafNode(None, "Hello"), LeafNode(None, "world"), LeafNode(None, "testing para")])
            ),
            (
                "Hello **Test**\nWorld *italic*\n>test [text](test.com)",
                ParentNode("p", [LeafNode(None, "Hello "), LeafNode("b", "Test"), LeafNode(None, "World "), LeafNode("i", "italic"), LeafNode(None, ">test "), LeafNode("a", "text", {"href": "test.com"})])
            ),
            (
                " ",
                ParentNode("p", [])
            )
        ]

        for test in test_cases:
            expected = test[1]
            recieved = generate_html_para(test[0])
            self.assertEqual(recieved.tag, expected.tag)
            if expected.children:
                for i, childnode in enumerate(expected.children):
                    self.assertEqual(recieved.children[i].tag, childnode.tag)
                    self.assertEqual(recieved.children[i].value, childnode.value)
                    self.assertEqual(recieved.children[i].props, childnode.props)


if __name__ =="__main__":
    unittest.main()