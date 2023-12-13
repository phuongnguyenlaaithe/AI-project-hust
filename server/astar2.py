import time
import pandas as pd
from conv_id import convert_id, convert_id_list
from nn import k_nearest_nodes, nearest_node
from haversine import haversine

edf = pd.read_csv("data/e.csv")
file = open('log/log_'+str(time.time())+'.txt', 'w')

class Node:
    def __init__(self, lat, lon, id):
        self.f = 0
        self.g = 0
        self.id = id
        self.lat = lat
        self.lon = lon
        self.parent = None
    
    def __str__(self):
        return f"Node id: {self.id}"
    

def find_adj_nodes(n_id, k):
    adj_nodes = []
    d=[]
    # search in edf for k nearest nodes that has edge with node
    adj_n = edf.loc[(edf['source'] == n_id)].sort_values(by=['length'])

    if len(adj_n) == 0:
        point = convert_id(n_id)[:2]
        adj_nodes = k_nearest_nodes(point, k)
        d = [haversine(point, convert_id(n)[:2], unit='m') for n in adj_nodes]

    else:
        if len(adj_n) < k:
            k = len(adj_n)
        adj_nodes = adj_n['target'].values.tolist()[:k]
        d = adj_n['length'].values.tolist()[:k]

    dict = {"adj_nodes": adj_nodes, "d": d}
    file.write(dict.__str__())
    file.write("\n")
    return dict

def astar(start, goal):

    start = list(start)
    goal = list(goal)
    print("start:", start)
    print("goal:", goal)

    def dist(p1, p2):
        return haversine([p1.lat, p1.lon], [p2.lat, p2.lon], unit='m')
    
    def reconstruct_path(came_from, current):
        total_path = [current]
        file.write("total_path:")
        file.write("\n")
        while current in came_from.keys():
            # file.write(current)
            current = came_from[current]
            total_path.append(current)
        file.write(total_path[:-1].__str__())
        file.write("\n")
        return total_path[:-1]
    
    sn_id = nearest_node(start)
    gn_id = nearest_node(goal)

    sn = convert_id(sn_id)
    gn = convert_id(gn_id)
    sn = Node(sn[0], sn[1], sn[2])
    gn = Node(gn[0], gn[1], gn[2])

    closed_set = set()
    open_set = {sn}
    came_from = {}
    path = []

    while (len(open_set) > 0):
        file.write("open_set:")
        file.write("\n")
        for item in open_set:
            file.write(item.id.__str__())
            file.write(" ")
        file.write("\n")

        cur = min(open_set, key = lambda node: node.f)

        file.write(cur.__str__())
        file.write("\n")

        open_set.remove(cur)
        came_from[cur.id] = cur.parent

        cur_nbs_dict = find_adj_nodes(cur.id, 10)
        cur_nbs = cur_nbs_dict['adj_nodes']
        dist_nbs = cur_nbs_dict['d']

        for i, nb_id in enumerate(cur_nbs):

            nb = convert_id(nb_id)
            nb_node = Node(nb[0], nb[1], nb[2])
            nb_node.parent = cur.id

            if nb_node.id in closed_set:
                continue
            
            # calculate heuristic

            nb_node.g   = cur.g + dist_nbs[i]
            file.write(nb_node.id.__str__())
            file.write("\nnb_node.g = ")
            file.write(str(nb_node.g))
            file.write("\n")
            # nb_node.g   = cur.g + dist(cur, nb_node)
            h           = dist(nb_node, gn)
            file.write(str(h))
            nb_node.f   = nb_node.g + h
            file.write("\nnb_node.f = ")
            file.write(str(nb_node.f))
            file.write("\n")

            # file.write(nb_node, f"\t\tnb.f =", nb_node.f)
            
            open_set.add(nb_node)
            rm = False

            for (node) in open_set:
                if node.parent == nb_node.parent and node.f < nb_node.f:
                    rm = True
                    continue
            
            if rm:
                open_set.remove(nb_node)
                closed_set.add(nb_node.id)

            # if successor is the goal, stop search
            if nb_node.id == gn.id or h < 50:
                print(h)
                came_from[nb_node.id] = cur.id
                file.write("found goal: ")
                file.write(nb_node.id.__str__())
                file.write("\n")
                path = reconstruct_path(came_from, nb_node.id)
                return path

        # if reconstruct path here, it will return the last path tried
        path = reconstruct_path(came_from, cur.id)
        # convert_id_list(path)
        closed_set.add(cur.id)

    return path

if __name__ == "__main__":
    start = [21.0208502, 105.8564046]
    goal = [21.0227259, 105.8582766]
    path = astar(start, goal)
    convert_id_list(path)