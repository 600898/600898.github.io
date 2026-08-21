class HTMLNode():
    def __init__(self, tag: str=None, value:str=None, children: list=None, props: dict[str, str]=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_str = ""
        for p in self.props:
            html_str += f'{p}="{self.props[p]}" '
        return html_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented

        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )