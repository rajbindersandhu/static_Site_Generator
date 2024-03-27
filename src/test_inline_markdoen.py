import unittest
from textnode import TextNode
from inline_markdown import split_nodes_delimiter, extract_markdown_image, extract_markdown_link, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):
    def test_bold(self):
        test_cases =[
            (
                [TextNode("This is **test**", "text"), TextNode("this is **code** test`", "code"), TextNode("**this is *italic* test**", "code")],
                "**",
                "bold",
                [
                    TextNode("This is ", "text"),
                    TextNode("test", "bold"),
                    TextNode("this is ", "code"),
                    TextNode("code", "bold"),
                    TextNode(" test`", "code"),
                    TextNode("this is *italic* test", "bold")
                ]
            ),
        ]

        for test in test_cases:
            expected = test[3]
            recieved = split_nodes_delimiter(test[0] ,test[1], test[2])
            self.assertListEqual(expected, recieved)
        
        

    def test_errors(self):

        value_error_lst = [
            [TextNode("This is **test", "text")],
            "**",
            "bold"
        ]

        with self.assertRaises(ValueError):
            error = split_nodes_delimiter(value_error_lst[0], value_error_lst[1], value_error_lst[2])


    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", "text"
        )
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded word", "bold"),
                TextNode(" and ", "text"),
                TextNode("another", "bold"),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        self.assertListEqual(
            [
                TextNode("This is text with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word", "text"),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertListEqual(
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ],
            new_nodes,
        )

    def test_extract_markdown_image(self):
        test_cases=[
            (
                "![test](Www.com) No image",
                [("test", "Www.com")]
            ),
            (
                "![test](Www.com) No image![no add](test)",
                [("test", "Www.com"), ("no add", "test")]
            ),
            (
                "test [image](Wrong type) test",
                []
            )
        ]
        
        for test in test_cases:
            expected = test[1]
            recieved = extract_markdown_image(test[0])
            self.assertListEqual(expected, recieved)
        
        with self.assertRaises(ValueError):
            error = extract_markdown_image(None)

    def test_extract_markdown_link(self):
        test_cases=[
            (
                "[test](Www.com) No image",
                [("test", "Www.com")]
            ),
            (
                "[test](Www.com) No imag [no add](test)",
                [("test", "Www.com"), ('no add', 'test')]
            ),
            (
                "test ![image](Wrong type) test",
                []
            )
        ]
        
        for test in test_cases:
            expected = test[1]
            recieved = extract_markdown_link(test[0])
            self.assertListEqual(expected, recieved)
        
        with self.assertRaises(ValueError):
            error = extract_markdown_link(None)

    def test_split_nodes_image(self):
        test_cases=[
            (
                [TextNode("![test](Www.com) No image", "text")],
                [
                    TextNode("test", "image", "Www.com"),
                    TextNode(" No image", "text")
                ]
            ),
            (
                [TextNode("![test](Www.com) No image ![no add](test)", "text")],
                [TextNode("test", "image","Www.com"), TextNode(" No image ", "text"), TextNode("no add", "image", "test")]
            ),
            (
                [TextNode("test [image](Wrong type) test", "text")],
                [TextNode("test [image](Wrong type) test", "text")]
            )
        ]

        for test in test_cases:
            expected_lst = test[1]
            recieved_lst = split_nodes_image(test[0])
            self.assertListEqual(expected_lst, recieved_lst)

    def test_split_nodes_link(self):
        test_cases=[
            (
                [TextNode("[test](Www.com) No image", "text")],
                [
                    TextNode("test", "link", "Www.com"),
                    TextNode(" No image", "text")
                ]
            ),
            (
                [TextNode("[test](Www.com) No image [no add](test)", "text")],
                [TextNode("test", "link","Www.com"), TextNode(" No image ", "text"), TextNode("no add", "link", "test")]
            ),
            (
                [TextNode("test ![image](Wrong type) test", "text")],
                [TextNode("test ![image](Wrong type) test", "text")]
            )
        ]

        for test in test_cases:
            expected_lst = test[1]
            recieved_lst = split_nodes_link(test[0])
            self.assertListEqual(expected_lst, recieved_lst)

    def test_text_to_textnode(self):
        test_cases = [
            (
                "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)",
                [   TextNode("This is ", "text"),
                    TextNode("text", "bold"),
                    TextNode(" with an ", "text"),
                    TextNode("italic", "italic"),
                    TextNode(" word and a ", "text"),
                    TextNode("code block", "code"),
                    TextNode(" and an ", "text"),
                    TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and a ", "text"),
                    TextNode("link", "link", "https://boot.dev")]
            ),
            (
                "This is with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)",
                [   TextNode("This is with an ", "text"),
                    TextNode("italic", "italic"),
                    TextNode(" word and a ", "text"),
                    TextNode("code block", "code"),
                    TextNode(" and an ", "text"),
                    TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and a ", "text"),
                    TextNode("link", "link", "https://boot.dev")]
            ),
            (
                "This is **text** with an *italic* word and a `code block` and an and a [link](https://boot.dev)",
                [   TextNode("This is ", "text"),
                    TextNode("text", "bold"),
                    TextNode(" with an ", "text"),
                    TextNode("italic", "italic"),
                    TextNode(" word and a ", "text"),
                    TextNode("code block", "code"),
                    TextNode(" and an and a ", "text"),
                    TextNode("link", "link", "https://boot.dev")]
            ),
            (
                "This is with an word and a and an and a",
                [TextNode("This is with an word and a and an and a", "text"),]
            )

        ]

        for test in test_cases:
            expected_lst = test[1]
            recieved_lst = text_to_textnodes(test[0])
            self.assertListEqual(expected_lst, recieved_lst)

if __name__ =="__main__":
    unittest.main()