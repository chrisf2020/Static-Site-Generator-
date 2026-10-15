import unittest
from block import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_empty_lines(self):
        md = """This is a paragraph"""
    
    def test_markdown_to_blocks_with_few_lines(self):
        md = """This is a paragraph
This is another paragraph"""

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.heading)
        self.assertEqual(block_to_block_type("```python\ncode\n```"), BlockType.code)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.quote)
        self.assertEqual(block_to_block_type("- List item"), BlockType.unordered_list)
        self.assertEqual(block_to_block_type("1. Ordered item"), BlockType.ordered_list)
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.paragraph)

    def test_block_to_block_type_with_various_headings(self):
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.heading)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.heading)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.heading)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.heading)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.heading)
    
    def test_paragraphs(self):
        md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )