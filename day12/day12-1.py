import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines

from common.grid import Grid, GridDir


def is_start_loc(char: str):
    return char == "S"

def is_end_loc(char: str):
    return char == "E"

def get_height_from_char(char : str):
    if is_start_loc(char):
        char_ord = ord("a")
    elif is_end_loc(char):
        char_ord = ord("z")
    else:
        char_ord = ord(char)
    
    return char_ord - ord("a")


class GraphNode:
    def __init__(self, id, value) -> None:
        self.id = id
        self.value = value

    def __str__(self) -> str:
        return "{id}={val}".format(id = self.id, val = self.value)
    
    def __repr__(self) -> str:
        return "GN {id}".format(id = self.id, val = self.value)


class NodeHeap(object):
    def __init__(self, initial=None, key=lambda x:x):
        self.key = key
        self.index = 0
        if initial:
            self._data = [(key(item), i, item) for i, item in enumerate(initial)]
            self.index = len(self._data)
            heapq.heapify(self._data)
        else:
            self._data = []
    
    def __len__(self):
        return len(self._data)

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), self.index, item))
        self.index += 1

    def pop(self):
        return heapq.heappop(self._data)[2]


import math
import heapq

class Graph:

    def __init__(self) -> None:
        self.adj_lists = {}

    def add_edge(self, from_node : GraphNode, to_node : GraphNode):
        adj_list = self.adj_lists.setdefault(from_node, [])
        if to_node not in adj_list:
            adj_list.append(to_node)
    

    def find_shortest_path_dist(self, start_node, end_node, grid : Grid):

        node_dists = {start_node: 0}

        node_queue = NodeHeap([], lambda node: node_dists.get(node, math.inf))
        visited = []

        for node in self.adj_lists.keys():
            node_dists[node] = math.inf
        
        node_dists[start_node] = 0

        node_queue.push(start_node)
        visited.append(start_node)

        shortest_dist = math.inf

        while len(node_queue) > 0:
            node = node_queue.pop()

            base_dist = node_dists[node]

            # not connected
            if base_dist == math.inf:
                return math.inf

            if node == end_node:
                shortest_dist = base_dist
                break
            
            adj_nodes = self.adj_lists.get(node, [])

            for adj_node in adj_nodes:
                new_dist = base_dist + 1
                prev_dist = node_dists.get(adj_node, math.inf)

                if new_dist < prev_dist:
                    node_dists[adj_node] = new_dist
                    node_queue.push(adj_node)

                if adj_node not in visited:
                    visited.append(adj_node)
                    node_queue.push(adj_node)



        for y in range(grid.height):
            row_str = ""

            for x in range(grid.width):
                node = grid.get_tile(x, y)

                if node in visited:
                    row_str += "x"
                else:
                    row_str += " "
            
            print(row_str)

    
        return shortest_dist




    def walk_graph(self, start_node):

        node_queue = [start_node]
        visited = []

        while len(node_queue) > 0:
            node = node_queue.pop(0)

            if node in visited:
                continue

            visited.append(node)

            yield node

            node_queue.extend(self.adj_lists.get(node, []))



def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    grid_width = len(lines[0].strip())
    grid_height = len(lines)

    hmap = Grid(grid_width, grid_height)

    start_loc, end_loc = None, None

    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):

            if is_start_loc(char):
                start_loc = x, y
            
            if is_end_loc(char):
                end_loc = x, y

            height = get_height_from_char(char)
            node = GraphNode((x,y), height)

            hmap.set_tile(x, y, node)
    
    path_graph = Graph()

    for x, y, node in hmap.enumerate_grid():

        #for dir in [GridDir.Down]: #GridDir.all_dirs:
        for dir in GridDir.all_dirs:
            adj_x, adj_y = hmap.get_next_loc_in_dir(x, y, dir)

            if hmap.is_valid_loc(adj_x, adj_y):
                adj_node = hmap.get_tile(adj_x, adj_y)

                height_diff = adj_node.value - node.value

                if height_diff <= 1: 
                    path_graph.add_edge(node, adj_node)
                
                if -height_diff <= 1:
                    path_graph.add_edge(adj_node, node)
    
    for y in range(hmap.height):

        print("".join("{h}".format(h = node.value).ljust(3) for xi, yi, node in hmap.enumerate_row(y)))
        
    
    start_node = hmap.get_tile(*start_loc)
    end_node = hmap.get_tile(*end_loc)

    for node in path_graph.walk_graph(start_node):
        adj_nodes = path_graph.adj_lists.get(node, [])

        print("{node} -> [ {adj} ]".format(
            node = str(node),
            adj = ", ".join(str(adj_node) for adj_node in adj_nodes)))
    
    dist = path_graph.find_shortest_path_dist(start_node, end_node, hmap)

    print("shortest path dist = {dist}".format(dist = dist))

    


    
if __name__ == "__main__":
    main()