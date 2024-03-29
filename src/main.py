from generate_page import generate_page
from copystatic import copy_static_to_public


def main():
    copy_static_to_public()
    generate_page("./content/index.md", "./template.html", "./public/index.html")


main()