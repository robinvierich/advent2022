import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines

from enum import Enum

from thirdparty.parse.parse import *


class CommandType(Enum):
    CD = 1
    LS = 2

class Command:
    command_format = "$ {cmd} {args}"

    def __init__(self, line) -> None:
        self.type, self.args  = parse(command_format, line.strip())


class NodeType(Enum):
    File = 1
    Dir = 2


class FSNode:
    def __init__(self, name, node_type, size = 0) -> None:
        self.name = name
        self.node_type = node_type
        self.size = size

        self.parent = None
        self.children = []
    
    def find_child(self, child_name):
        for child in self.children:
            if child.name == child_name:
                return child
        
        return None




class FSTree:

    def __init__(self) -> None:
        self.root = FSNode("/", NodeType.Dir)
        self.cwd = None
    
    def add_node(self, node, parent = None):
        node.parent = parent or self.root

        node.parent.children.append(node)

    def breadth_first_walk(self, start_node = None):
        queue = [start_node or self.root]

        while len(queue) > 0:
            node = queue.pop(0)

            yield node

            queue.extend(node.children)
        
    def get_all_dirs(self):
        bfs = self.breadth_first_walk()

        dirs = [node for node in bfs if node.node_type == NodeType.Dir]

        return dirs

    
    def get_total_size(self, start_node = None):
        bfs = self.breadth_first_walk(start_node)

        total_size = sum(node.size for node in bfs)

        return total_size

   


def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    command_format = "$ {cmd} {args}"

    dir_node_format = "dir {name}"
    file_node_format = "{size:d} {name}"

    fstree = FSTree()

    cwd = fstree.root

    for line in lines:
        parsed_cmd = parse(command_format, line.strip())

        if parsed_cmd:
            cmd = parsed_cmd.named['cmd']
            args = parsed_cmd.named['args']

            if cmd == "cd":
                if args == "/":
                    cwd = fstree.root
                elif args == "..":
                    cwd = cwd.parent
                else:
                    child = cwd.find_child(args)
                    if child:
                        cwd = child
                    else:
                        print("couldn't find child with name {}!".format(args))

            elif cmd == "ls":
                pass

            # parsed line as cmd, move to next line
            continue
        
        parsed_dir_node = parse(dir_node_format, line.strip())

        if parsed_dir_node:
            node = FSNode(parsed_dir_node.named['name'], NodeType.Dir)
            fstree.add_node(node, cwd)

            # parsed line as dir, move to next line
            continue


        parsed_file_node = parse(file_node_format, line.strip())

        if parsed_file_node:
            node = FSNode(parsed_file_node.named['name'], NodeType.File, parsed_file_node.named['size'])
            fstree.add_node(node, cwd)
        


        # if command, parse output
            # cd: change cwd
            # ls: read output and add nodes until next cmd

    dirs = fstree.get_all_dirs()
    print("all dirs: {dirs}".format(dirs = ", ".join(dir.name for dir in dirs)))

    max_fs_space = 70000000
    required_space = 30000000
    used_space = fstree.get_total_size()

    unused_space = max_fs_space - used_space

    space_to_clear = required_space - unused_space

    # cache dir sizes
    for dir in dirs:
        dir.size = fstree.get_total_size(dir)  

    large_enough_dirs = (dir for dir in dirs if dir.size > space_to_clear)

    min_dir = min(large_enough_dirs, key = lambda d: d.size)

    print("dir to delete: {dir} @ {size}".format(dir = min_dir.name, size = min_dir.size))

        




    
if __name__ == "__main__":
    main()