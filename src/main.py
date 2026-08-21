from textnode import TextNode, TextType
import os
import shutil
from block_splitter import markdown_to_html_node
from delimiter import extract_title
import sys

def main():
    print(TextNode("This is some anchor text", TextType.Link, "https://www.boot.dev"))
    source_to_dest_directory()
    basepath = sys.argv

    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        basepath
    )

public_directory = "docs"
source_directory = "static"

def source_to_dest_directory(src: str = source_directory, pub: str = public_directory):
    if(os.path.exists(pub) and os.path.exists(src)):
        remove_files(pub)
        copy_files(src, pub)
            
    else:
        raise Exception("Public or Source directory path is wrong or does not exist.")

def remove_files(directory):
    if(os.path.exists(directory)):
        for f in os.listdir(directory):
            path = os.path.join(directory,f)
            if(os.path.isfile(path)):
                os.remove(path)
            elif(os.path.isdir(path)):
                remove_files(path)
                os.rmdir(path)

def copy_files(src, dest):
    for f in os.listdir(src):
        path = os.path.join(src, f)
        if(os.path.isfile(path)):
            shutil.copy(path,dest)
        elif(os.path.isdir(path)):
            new_path = os.path.join(dest, f)
            if os.path.isdir(new_path):
                copy_files(path, new_path)
            else:
                os.mkdir(new_path)
                copy_files(path, new_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}.')

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="{basepath}')
    template = template.replace('src="/', 'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, entry)

        if os.path.isfile(content_path):
            if entry.endswith(".md"):
                dest_path = os.path.join(
                    dest_dir_path,
                    entry.replace(".md", ".html")
                )

                generate_page(
                    content_path,
                    template_path,
                    dest_path,
                    basepath
                )

        elif os.path.isdir(content_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)

            os.makedirs(new_dest_dir, exist_ok=True)

            generate_pages_recursive(
                content_path,
                template_path,
                new_dest_dir,
                basepath
            )

if __name__ == "__main__":
    main()
