import os
import shutil

def remove_dirtree_from(path):
    nodes = os.listdir(path)
    if nodes:
        for node in nodes:
            node_path = os.path.join(path, node)
            if os.path.isfile(node_path):
                os.remove(node_path)
            else:
                shutil.rmtree(node_path)

def list_all(path):
    nodes_list = []
    if os.path.isfile(path):
        nodes_list.append(path) 
        return nodes_list
    cur_nodes = os.listdir(path) 
    if not cur_nodes:
        nodes_list.append(path) 
        return nodes_list
    for node in cur_nodes:
        node_path = os.path.join(path, node)
        nodes_list += list_all(node_path)
    return nodes_list



def copy_static_to_public():
    public_base_path = "./public"
    static_base_path = "./static"
    src_nodes_list = list_all(static_base_path)
    remove_dirtree_from(public_base_path)

    for node in src_nodes_list:
        item_lst = node.replace(static_base_path+"/", "").split("/")
        item_path = public_base_path
        for index, item in enumerate(item_lst):
            item_path = os.path.join(item_path, item) 
            if index == len(item_lst)-1 and os.path.isfile(node):
                shutil.copy(node, item_path)
            else:
                if not os.path.exists(item_path):
                    os.mkdir(item_path)

