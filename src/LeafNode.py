from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None and self.tag != "img":
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        if self.props:
            props = self.props_to_html().rstrip()
            if self.tag == "img":
                return f"<{self.tag} {props}>"
            return f"<{self.tag} {props}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"