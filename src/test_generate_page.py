import unittest
from generate_page import extract_title
import os

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        test_cases = [
            (
                """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item""",
                "This is a heading"
            ),
            (
                """This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item

# This is a heading""",
                "This is a heading"
            )
        ]

        for test in test_cases:
            expected = test[1]
            recieved = extract_title(test[0])
            self.assertEqual(expected, recieved)

    # def test(self):
    #     dir_path = os.path.dirname("./public/test/test1/test2/")
    #     print(dir_path)
    #     nodes = dir_path.split("/")
    #     cur_path = ""
    #     print(nodes)
    #     for node in nodes:
    #         if node == "." or node == "..":
    #             cur_path += node + "/"
    #         else:
    #             cur_path += node + "/"
    #             if not os.path.exists(cur_path):
    #                 os.mkdir(cur_path)

        

if "__name__" == "__main__":
    unittest.main()