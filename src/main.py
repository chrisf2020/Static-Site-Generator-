import os
import shutil
import sys
from block import markdown_to_html_node

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def copy_directory_recursive(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            copy_directory_recursive(s, d)
        else:
            shutil.copy2(s, d)
            print(f"Copied: {s} -> {d}")


def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# ") or line == "#":
            return line.lstrip("#").strip()

    raise ValueError("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()

    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )
    basepath_prefix = basepath.rstrip("/")
    if basepath_prefix:
        basepath_prefix += "/"
    else:
        basepath_prefix = "/"
    full_html = full_html.replace('href="/', f'href="{basepath_prefix}').replace(
        'src="/', f'src="{basepath_prefix}'
    )

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(from_path):
            generate_pages_recursive(
                from_path, template_path, os.path.join(dest_dir_path, entry), basepath
            )
        elif entry.endswith(".md"):
            page_name = os.path.splitext(entry)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, page_name)
            generate_page(from_path, template_path, dest_path, basepath)


def main():
    # 1. Clean docs directory
    if os.path.exists(dir_path_docs):
        print(f"Removing old {dir_path_docs} directory...")
        shutil.rmtree(dir_path_docs)

    # 2. Copy static files over
    print(f"Copying files from {dir_path_static} to {dir_path_docs}...")
    copy_directory_recursive(dir_path_static, dir_path_docs)

    # 3. Generate all content pages
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)


if __name__ == "__main__":
    main()