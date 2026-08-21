from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType,) -> list[TextNode]:
    new_nodes = []

    for on in old_nodes:
        if on.text_type != TextType.Text:
            new_nodes.append(on)
            continue

        if delimiter not in on.text:
            new_nodes.append(on)
            continue

        sections = on.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise Exception(f"ERROR: unmatched delimiter {delimiter}")

        for i, section in enumerate(sections):
            if section == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.Text))
            else:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No title found")

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for on in old_nodes:
        if on.text_type != TextType.Text:
            new_nodes.append(on)
            continue

        images = extract_markdown_images(on.text)

        if not images:
            new_nodes.append(on)
            continue

        remaining = on.text

        for alt, url in images:
            image_markdown = f"![{alt}]({url})"
            parts = remaining.split(image_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.Text))

            new_nodes.append(TextNode(alt, TextType.Image, url))
            remaining = parts[1]

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.Text))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for on in old_nodes:
        if on.text_type != TextType.Text:
            new_nodes.append(on)
            continue

        links = extract_markdown_links(on.text)

        if not links:
            new_nodes.append(on)
            continue

        remaining = on.text

        for text, url in links:
            link_markdown = f"[{text}]({url})"
            parts = remaining.split(link_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.Text))

            new_nodes.append(TextNode(text, TextType.Link, url))
            remaining = parts[1]

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.Text))

    return new_nodes

def text_to_textnodes(text) -> list[TextNode]:
    new_nodes = [TextNode(text, TextType.Text)]

    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.Bold)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.Italic)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.Code)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes