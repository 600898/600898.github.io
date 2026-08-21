from enum import Enum
from LeafNode import LeafNode

class TextType(Enum):
    Text= 0
    Bold= 1
    Italic= 2
    Code= 3
    Link= 4
    Image= 5

class TextNode():
    def __init__(self, text: str, text_type: TextType, url:str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match(text_node.text_type):
        case TextType.Text:
            return LeafNode(None,text_node.text)
        case TextType.Bold:
            return LeafNode("b", text_node.text)
        case TextType.Italic:
            return LeafNode("i", text_node.text)
        case TextType.Code:
            return LeafNode("code", text_node.text)
        case TextType.Link:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.Image:
            return LeafNode("img", "", {
                "src": text_node.url,
                "alt": text_node.text
            })
        case default:
            raise NotImplementedError(f'{text_node.text_type} not implemented')
