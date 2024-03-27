from htmlnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other) -> bool:
        if (self.text == other.text and self.text_type == other.text_type and self.url == other.url):
            return True
        return False

    def __repr__(self) -> str:
        return f"Textnode({self.text}, {self.text_type}, {self.url})"
    

def text_node_to_html_node(textnode: TextNode):
    if textnode.text_type == "text":
        return LeafNode(None, textnode.text, None)
    elif textnode.text_type == "bold":
        return LeafNode("b", textnode.text, None)
    elif textnode.text_type == "italic":
        return LeafNode("i", textnode.text, None)
    elif textnode.text_type == "code":
        return LeafNode("code", textnode.text, None)
    elif textnode.text_type == "link":
        return LeafNode("a", textnode.text, {"href": f'"{textnode.url}"'})
    elif textnode.text_type == "image":
        return LeafNode("img", "", {"src": f'"{textnode.url}"', "alt": f'"{textnode.text}"'})
    else:
        raise Exception(f"{textnode.text_type} is not a valid text type")
    

