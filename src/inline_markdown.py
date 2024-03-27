import re
from textnode import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list =[]
    for textnode in old_nodes:
        if isinstance(textnode, TextNode):
            text = textnode.text
            old_text_type = textnode.text_type
            if text.find(delimiter) == -1:
                new_list.append(textnode)
                continue
            else:
                split_text_lst = text.split(delimiter)
                if len(split_text_lst) % 2 ==0:
                    raise ValueError(f"The string is not closed with {delimiter}")
                for i in range(len(split_text_lst)):
                    if i%2 != 0:
                        if split_text_lst[i]:
                            new_list.append(TextNode(split_text_lst[i], text_type))
                    else:
                        if split_text_lst[i]:
                            new_list.append(TextNode(split_text_lst[i], old_text_type))
        else:
            new_list.append(textnode)
    return new_list

def extract_markdown_image(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    if text is None:
        raise ValueError("Text is None")
    else:
        return re.findall(pattern, text)

def extract_markdown_link(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    anti_pattern = r"!\[(.*?)\]\((.*?)\)"

    if text is None:
        raise ValueError("Text is None")
    else:
        pattern_lst = re.findall(pattern, text)
        anti_pattern_lst = re.findall(anti_pattern, text)
        new_lst = list(filter(lambda x: x not in anti_pattern_lst, pattern_lst))
        return new_lst
    
def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        text = node.text
        old_text_type = node.text_type
        if text:
            image_lst = extract_markdown_image(text)
            if len(image_lst) == 0:
                new_list.append(node)
                continue
            else:
               tmp_text = text
               for i, image in enumerate(image_lst):
                    image_txt = f"![{image[0]}]({image[1]})"
                    split_lst = tmp_text.split(image_txt)
                    if split_lst[0]:
                       new_list.append(TextNode(split_lst[0], old_text_type))
                       new_list.append(TextNode(image[0], "image", image[1]))
                    else:
                       new_list.append(TextNode(image[0], "image", image[1]))
                    if len(split_lst[1:])>1:
                        tmp_text = image_txt.join(split_lst[1:])
                    elif len(split_lst[1:]) == 1:
                        if i == len(image_lst)-1:
                            if split_lst[-1]:
                                new_list.append(TextNode(split_lst[-1], old_text_type))
                        else:
                            tmp_text=split_lst[-1]
    return new_list
                    

def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        text = node.text
        old_text_type = node.text_type
        if text:
            link_lst = extract_markdown_link(text)
            if len(link_lst) == 0:
                new_list.append(node)
                continue
            else:
               tmp_text = text
               for i, link in enumerate(link_lst):
                    link_txt = f"[{link[0]}]({link[1]})"
                    split_lst = tmp_text.split(link_txt)
                    if split_lst[0]:
                       new_list.append(TextNode(split_lst[0], old_text_type))
                       new_list.append(TextNode(link[0], "link", link[1]))
                    else:
                       new_list.append(TextNode(link[0], "link", link[1]))
                    if len(split_lst[1:])>1:
                        tmp_text = link_txt.join(split_lst[1:])
                    elif len(split_lst[1:]) == 1:
                        if i == len(link_lst)-1:
                            if split_lst[-1]:
                                new_list.append(TextNode(split_lst[-1], old_text_type))
                        else:
                            tmp_text=split_lst[-1]
    return new_list

def text_to_textnodes(text):
    text_node_lst = [TextNode(text, "text")]
    bold_delim_lst = split_nodes_delimiter(text_node_lst, "**", "bold")
    italic_delim_lst = split_nodes_delimiter(bold_delim_lst, "*", "italic")
    code_delim_lst = split_nodes_delimiter(italic_delim_lst, "`", "code")
    image_delim_lst = split_nodes_image(code_delim_lst)
    final_lst = split_nodes_link(image_delim_lst)

    return final_lst
