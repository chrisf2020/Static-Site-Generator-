import os
import tempfile
import unittest

from main import generate_pages_recursive


class TestGeneratePagesRecursive(unittest.TestCase):
    def test_generates_pages_at_matching_nested_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            content_dir = os.path.join(temp_dir, "content")
            blog_dir = os.path.join(content_dir, "blog", "glorfindel")
            output_dir = os.path.join(temp_dir, "public")
            os.makedirs(blog_dir)

            with open(os.path.join(content_dir, "index.md"), "w", encoding="utf-8") as f:
                f.write("# Home\n\nWelcome.")
            with open(os.path.join(content_dir, "notes.txt"), "w", encoding="utf-8") as f:
                f.write("Not a page.")
            with open(os.path.join(blog_dir, "index.md"), "w", encoding="utf-8") as f:
                f.write("# Glorfindel\n\nA blog post.")

            template_path = os.path.join(temp_dir, "template.html")
            with open(template_path, "w", encoding="utf-8") as f:
                f.write("<title>{{ Title }}</title>{{ Content }}")

            generate_pages_recursive(content_dir, template_path, output_dir)

            with open(os.path.join(output_dir, "index.html"), encoding="utf-8") as f:
                home_page = f.read()
            with open(
                os.path.join(output_dir, "blog", "glorfindel", "index.html"),
                encoding="utf-8",
            ) as f:
                blog_page = f.read()

            self.assertIn("<title>Home</title>", home_page)
            self.assertIn("<title>Glorfindel</title>", blog_page)
            self.assertIn("<p>A blog post.</p>", blog_page)


if __name__ == "__main__":
    unittest.main()
