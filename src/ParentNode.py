from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is None")

        if self.children is None:
            raise ValueError("No children in parentNode")

        html_str = f"<{self.tag}"

        if self.props:
            html_str += f" {self.props_to_html().rstrip()}"

        html_str += ">"

        for child in self.children:
            html_str += child.to_html()

        html_str += f"</{self.tag}>"

        return html_str