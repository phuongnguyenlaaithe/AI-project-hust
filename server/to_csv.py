import networkx as nx
import csv

def graphml_nodes_to_csv(graphml_file, csv_file):
    # Read the GraphML file
    graph = nx.read_graphml(graphml_file)

    # Extract node information
    nodes = list(graph.nodes(data=True))
    edges = list(graph.edges(data=True))

    # Write to CSV
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['osmid'] + list(nodes[0][1].keys()) + ['highway']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for node in nodes:
            node_data = {'osmid': node[0]}
            node_data.update(node[1])
            writer.writerow(node_data)

def graphml_edges_to_csv(graphml_file, csv_file):
    # Read the GraphML file
    graph = nx.read_graphml(graphml_file)

    # Extract node information
    edges = list(graph.edges(data=True))

    prev_s = None
    prev_t = None

    # Write to CSV
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['source', 'target'] + list(edges[0][2].keys()) + [
            'highway', 'lanes', 'name', 'junction', 'geometry', 'access', 'service', 'landuse', 'tunnel', 'width'
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for edge in edges:
            # if highway is footway, ignore
            if edge[2].get('highway') is not None:
                if edge[2]['highway'] == 'footway':
                    continue
                if edge[2]['highway'] == 'unclassified':
                    continue
            # print(edge)
            if edge[0] == edge[1]:
                continue
            if prev_s == edge[0] and prev_t == edge[1]:
                continue
            edge_data = {'source': edge[0], 'target': edge[1]}
            edge_data.update(edge[2])
            writer.writerow(edge_data)
            prev_s = edge[0]
            prev_t = edge[1]

    # TODO xử lí lặp data cạnh, reversed các thứ

if __name__ == "__main__":
    graphml_file = "data/map.graphml"
    csv_file_nodes = "data/n.csv"
    csv_file_edges = "data/e.csv"
    graphml_nodes_to_csv(graphml_file, csv_file_nodes)
    graphml_edges_to_csv(graphml_file, csv_file_edges)
