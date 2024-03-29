from generate_page import generate_pages_recursive
from copystatic import copy_static_to_public


def main():
    # Copies all files and folder recurresively from static to public in root
    copy_static_to_public()
    # Conert .md file in content folder and convert them to .html file and paste them to public folder
    generate_pages_recursive("./content/", "./template.html", "./public/")


main()