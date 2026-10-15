import os
import shutil
from block import markdown_to_html_node

dir_path_static = "./static"
dir_path_public = "./public"
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


def generate_page(from_path, template_path, dest_path):
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

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(from_path):
            generate_pages_recursive(
                from_path, template_path, os.path.join(dest_dir_path, entry)
            )
        elif entry.endswith(".md"):
            page_name = os.path.splitext(entry)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, page_name)
            generate_page(from_path, template_path, dest_path)


def main():
    # 1. Clean public directory
    if os.path.exists(dir_path_public):
        print(f"Removing old {dir_path_public} directory...")
        shutil.rmtree(dir_path_public)

    # 2. Copy static files over
    print(f"Copying files from {dir_path_static} to {dir_path_public}...")
    copy_directory_recursive(dir_path_static, dir_path_public)

    # 3. Generate all content pages
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()