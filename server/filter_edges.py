import xml.dom.minidom as mn

def reduce_edges(graphml_file_path, output_file_path):
    # Parse the GraphML file using XML DOM
    doc = mn.parse(graphml_file_path)

    # Get the root element
    root = doc.documentElement
    graph_element = root.getElementsByTagName("graph")[0]
    # print(graph_element._get_childNodes())

    edges = root.getElementsByTagName("edge")

    # only retain edges that have key = d6 or d8
    rm = True
    for edge in edges[:]:
        # print(edge.data.__str__())
        # if edge.data.getAttribute("key") not in ["d6", "d8"]:
        #     graph_element.removeChild(edge)
        data_elements = edge.getElementsByTagName('data')
        for data_element in data_elements:
            if data_element.getAttribute("key") in ["d8", "d10"]:
                # print(data_element.getAttribute("key"))
                if (data_element.firstChild.data in ["service"]):
                    continue
                rm = False
                break
        if rm:
            graph_element.removeChild(edge)

        rm = True


    after_edges = root.getElementsByTagName("edge")

    # Filter nodes that are not associated with edges
    nodes_with_edges = set()
    for edge in after_edges:
        nodes_with_edges.add(edge.getAttribute("source"))
        nodes_with_edges.add(edge.getAttribute("target"))
    
    print(len(nodes_with_edges))

    nodes = root.getElementsByTagName("node")
    print(len(nodes))
    for node in nodes[:]:
        node_id = node.getAttribute("id")
        if node_id not in nodes_with_edges:
            graph_element.removeChild(node)

    nodes = root.getElementsByTagName("node")
    print(len(nodes))

    with open(output_file_path, "w") as output_file:
        doc.writexml(output_file)

def add_nodes():
    import pandas as pd

    # Read the CSV file
    df = pd.read_csv('data/e.csv')

    # Create a new DataFrame to store the modified edges
    new_edges = pd.DataFrame(columns=df.columns)
    new_nodes = pd.DataFrame(columns=['osmid'])

    # Loop through each row in the original DataFrame
    for index, row in df.iterrows():
        # Split the edge into two edges
        edge1 = row.copy()
        edge2 = row.copy()

        # Create a new node ID (you may want to use a proper logic for this)
        new_node = max(df['target']) + 1

        # Update the target of the first edge to the new node
        edge1['target'] = new_node
        # Update the source of the second edge to the new node
        edge2['source'] = new_node

        # Halve the length of both edges
        edge1['length'] = row['length'] / 2
        edge2['length'] = row['length'] / 2

        new_lat = (row['y'] + df.at[row['target'], 'y']) / 2
        new_lon = (row['x'] + df.at[row['source'], 'x']) / 2


        # Append the modified edges to the new DataFrame
        new_edges = new_edges.append(edge1, ignore_index=True)
        new_edges = new_edges.append(edge2, ignore_index=True)
        new_nodes = new_nodes.append({'osmid': new_node, 'y':new_lat, 'x':new_lon}, ignore_index=True)

    # Write the new DataFrame to a new CSV file
    new_edges.to_csv('data/e2.csv', index=False)
    new_nodes.to_csv('data/n2.csv', index=False)

if __name__ == "__main__":
    # reduce_edges("data/map_full.graphml", "data/map.graphml")
    add_nodes()
