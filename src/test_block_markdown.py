import unittest
from block_markdown import markdown_to_blocks

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

if __name__ =="__main__":
    unittest.main()