from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_code
import os

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading" and block.startswith("# "):
            return block.lstrip("# ")
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path, encoding='utf-8') as f:
        markdown = f.read()

    with open(template_path, encoding='utf-8') as f:
        template = f.read()

    html = (markdown_to_html_code(markdown)).to_html()
    title = extract_title(markdown)
    updated_template = (template.replace("{{ Title }}", title)).replace("{{ Content }}", html)
    
    if os.path.exists(dest_path):
        with open(dest_path, "w") as f:
            f.write(updated_template)
    else:
        dir_path = os.path.dirname(dest_path)
        nodes = dir_path.split("/")
        cur_path = ""
        for node in nodes:
            if node == "." or node == "..":
                cur_path += node + "/"
            else:
                cur_path += node + "/"
                if not os.path.exists(cur_path):
                    os.mkdir(cur_path)
                    
        with open(dest_path, "w") as f:
            f.write(updated_template)
