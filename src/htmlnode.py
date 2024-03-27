class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        prop_string = ""
        if self.props:
            for key, value in self.props.items():
                prop_string += f' {key}="{value}"'
        return prop_string
    
    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is not None:
            if self.tag and not self.tag == " ":
                if self.props:
                    props_string = self.props_to_html()
                    return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
                else:
                    return f"<{self.tag}>{self.value}</{self.tag}>"
            elif (not self.tag or self.tag == " ") and self.props:
                raise ValueError(f"tag: {self.tag}, value:{self.value} -> Please provide missing tag, as props are provided")
            else:
                return self.value
        else:
            raise ValueError(f"tag: {self.tag}, value:{self.value} -> No text value is provided")
        
    def __repr__(self):
        return f'LeafNode(tag={self.tag}, value={self.value}, props={self.props})'
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag and not self.tag == " ":
            if self.children:
                children_html_string=""
                for child in self.children:
                    children_html_string += child.to_html()
                props_string = self.props_to_html()
                return f'<{self.tag}{props_string}>{children_html_string}</{self.tag}>'
            else:
                raise ValueError("Children node are missing from parent node")
        elif not self.tag and self.props:
            raise ValueError("Props are given but Tag is missing")
        else:
            raise ValueError("Tag is missing")
        
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
    

