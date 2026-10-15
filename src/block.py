import re
from enum import Enum
from inlines import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType
from htmlnode import *

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6}\s", block):
        return BlockType.heading
    elif re.match(r"^```\w*\n", block):
        return BlockType.code
    elif re.match(r"^>\s", block):
        return BlockType.quote
    elif re.match(r"^(\*|\-|\+)\s", block):
        return BlockType.unordered_list
    elif re.match(r"^\d+\.\s", block):
        return BlockType.ordered_list
    else:
        return BlockType.paragraph

def markdown_to_blocks(markdown):
    lines = markdown.splitlines()
    blocks = []
    current_block_lines = []

    for line in lines:
        if line.strip() == "":
            if current_block_lines:
                blocks.append("\n".join(current_block_lines))
                current_block_lines = []
        else:
            current_block_lines.append(line)

    if current_block_lines:
        blocks.append("\n".join(current_block_lines))

    return blocks

from htmlnode import LeafNode
from textnode import TextType


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")

def block_to_html_node(block, block_type):
    if block_type == BlockType.paragraph:
        tag = "p"
        lines = block.split("\n")
        text = " ".join(line.strip() for line in lines)
        return ParentNode(tag, text_to_children(text))

    elif block_type == BlockType.heading:
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        tag = f"h{count}"
        text = block[count:].strip()
        return ParentNode(tag, text_to_children(text))

    elif block_type == BlockType.code:
        lines = block.split("\n")
        code_text = "\n".join(lines[1:-1]) + "\n"

        code_node = ParentNode("code", [LeafNode(None, code_text)])
        return ParentNode("pre", [code_node])

    elif block_type == BlockType.quote:
        tag = "blockquote"
        lines = block.split("\n")
        cleaned_lines = [line.lstrip(">").strip() for line in lines]
        text = " ".join(cleaned_lines)
        return ParentNode(tag, text_to_children(text))

    elif block_type == BlockType.unordered_list:
        tag = "ul"
        lines = block.split("\n")
        li_nodes = []
        for line in lines:
            item_text = line[2:].strip()
            li_nodes.append(ParentNode("li", text_to_children(item_text)))
        return ParentNode(tag, li_nodes)

    elif block_type == BlockType.ordered_list:
        tag = "ol"
        lines = block.split("\n")
        li_nodes = []
        for line in lines:
            item_text = line.split(". ", 1)[1].strip()
            li_nodes.append(ParentNode("li", text_to_children(item_text)))
        return ParentNode(tag, li_nodes)

    else:
        raise ValueError(f"Invalid block type: {block_type}")

def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return [text_node_to_html_node(node) for node in nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        html_parent_node = block_to_html_node(block, block_type)
        children.append(html_parent_node)

    return ParentNode("div", children)