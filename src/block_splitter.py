from enum import Enum
import re
from htmlnode import HTMLNode
from ParentNode import ParentNode
from delimiter import split_nodes_delimiter, split_nodes_link, split_nodes_image
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    Paragraph = 0
    Heading = 1
    Code = 2
    Quote = 3
    Unordered_List = 4
    Ordered_List = 5

def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = [b.strip() for b in markdown.split("\n\n")]

    return raw_blocks

def block_to_block_type(markdown_block: str) -> BlockType:
    lines = markdown_block.split("\n")

    if re.match(r"^#{1,6} ", markdown_block):
        return BlockType.Heading

    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.Code

    if all(line.startswith(">") for line in lines):
        return BlockType.Quote

    if all(line.startswith("- ") for line in lines):
        return BlockType.Unordered_List

    current_number = 1

    for line in lines:
        match = re.match(r"^(\d+)\. ", line)

        if not match:
            break

        number = int(match.group(1))

        if number != current_number:
            break

        current_number += 1
    else:
        return BlockType.Ordered_List

    return BlockType.Paragraph

def text_to_children(text: str) -> list[HTMLNode]:
    nodes = [TextNode(text, TextType.Text)]

    nodes = split_nodes_delimiter(
        nodes, "**", TextType.Bold
    )

    nodes = split_nodes_delimiter(
        nodes, "_", TextType.Italic
    )

    nodes = split_nodes_delimiter(
        nodes, "`", TextType.Code
    )

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    html_nodes = []

    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for b in blocks:
        block_type = block_to_block_type(b)

        match block_type:
            case BlockType.Paragraph:
                children = text_to_children(b)
                block_nodes.append(ParentNode("p", children))

            case BlockType.Heading:
                # Count the # characters
                heading_level = 0
                while heading_level < len(b) and b[heading_level] == "#":
                    heading_level += 1

                text = b[heading_level + 1:]
                children = text_to_children(text)

                block_nodes.append(
                    ParentNode(f"h{heading_level}", children)
                )
            case BlockType.Unordered_List:
                lines = b.split("\n")
                children = []

                for line in lines:
                    text = line[2:]
                    li_children = text_to_children(text)
                    children.append(ParentNode("li",  li_children))

                block_nodes.append(ParentNode("ul", children))
            case BlockType.Ordered_List:
                lines = b.split("\n")
                children = []

                for line in lines:
                    text = line[line.index(" ") + 1:]
                    li_children = text_to_children(text)
                    children.append(ParentNode("li", li_children))

                block_nodes.append(ParentNode("ol", children))
            case BlockType.Quote:
                lines = b.split("\n")
                text = "\n".join(line[1:].lstrip() for line in lines)
                children = text_to_children(text)

                block_nodes.append(ParentNode("blockquote", children))
            case BlockType.Code:
                code = b[4:-3]
                text_node = TextNode(code, TextType.Text)
                html_node = text_node_to_html_node(text_node)

                code_node = ParentNode("code", [html_node])
                pre_node = ParentNode("pre", [code_node])

                block_nodes.append(pre_node)

    return ParentNode("div", block_nodes)
