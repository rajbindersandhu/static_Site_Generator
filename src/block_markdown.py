import re
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
def markdown_to_blocks(markdown_document):
    split_by_line_lst = markdown_document.split("\n")
    final_lst = []
    temp_str = ""
    for i, item in enumerate(split_by_line_lst):
        if item == '':
            if temp_str:
                final_lst.append(temp_str)
                temp_str = ""
        else:
            if temp_str:
                temp_str += ("\n" + item.strip())
            else:
                temp_str += item.strip()
        if i == len(split_by_line_lst) - 1:
            if temp_str:
                final_lst.append(temp_str)
    return final_lst

def block_to_block_type(markdown_str):
    if markdown_str is not None:
        lines = markdown_str.split("\n")

        if (markdown_str.startswith("# ") or
            markdown_str.startswith("## ") or
            markdown_str.startswith("### ") or 
            markdown_str.startswith("#### ") or
            markdown_str.startswith("##### ") or
            markdown_str.startswith("###### ") ):
                return "heading"
        elif markdown_str.startswith("```"):
            if markdown_str.endswith("```"):
                return "code"
            else:
                return "paragraph"
        elif markdown_str.startswith(">"):
            for line in lines:
                if not line.startswith(">"):
                    return "paragraph"
            return "quote"
        elif markdown_str.startswith("*"):
            for line in lines:
                if not line.startswith("*"):
                    return "paragraph"
            return "ul"
        elif markdown_str.startswith("-"):
            for line in lines:
                if not line.startswith("-"):
                    return "paragraph"
            return "ul"
        elif markdown_str.startswith("1."):
            for i, line in enumerate(lines):
                if not line.startswith(f"{i+1}."):
                    return "paragraph"
            return "ol"
        else:
            return "paragraph"
    else:
        raise ValueError("Markdown is None")
    
def generate_html_heading(line):
    heading_type = ""
    text = ""
    children=[]
    if line.startswith("# "):
        heading_type = "h1"
        text = line.strip("# ")
    elif line.startswith("## "):
        heading_type = "h2"
        text = line.strip("## ")
    elif line.startswith("### "):
        heading_type = "h3"
        text = line.strip("### ")
    elif line.startswith("#### "):
        heading_type = "h4"
        text = line.strip("#### ")
    elif line.startswith("##### "):
        heading_type = "h5"
        text = line.strip("##### ")
    elif line.startswith("###### "):
        heading_type = "h6"
        text = line.strip("###### ")
    if text:
        text_nodes = text_to_textnodes(text)
        for textnode in text_nodes:
            leafnode = text_node_to_html_node(textnode)
            children.append(leafnode)
    return ParentNode(heading_type, children)

def generate_html_code(block):
    text = block.strip("```")
    children = [LeafNode("code", text)]
    return ParentNode("pre", children)