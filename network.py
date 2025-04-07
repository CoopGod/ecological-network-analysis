"""
Purpose: This program uses an object oriented approach to preform network
    distance calculations using a Breadth-First-Search algorithm. It also constructs a visual network
    to interpret the calculations.
Author: Cooper Goddard
Date: April 21, 2025
"""

import pandas
import networkx as nx
from pyvis.network import Network
import os

DATA_FILE = "generated_data/interaction_and_spearmans.csv"
DATA_OUTPUT_FILE = "generated_data/completed_network_data.csv"
NETWORK_OUTPUT_FILE = "network.html"
DISTANCE_COLUMN_NAME = "distance"
SPECIES_PAIR_COLUMN_NAME = "species_pair_nn"  # Note: The species pair is assumed to be structured: 'Spc1-Spc2' where Spc1 < Spc2


class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def add_connection(self, connectee: object) -> None:
        self.connections.append(connectee)

    def get_connections(self) -> list:
        return self.connections


def createNetworkVisualizer(nodes: dict) -> None:
    """
    This function uses a dictionary of directly connected nodes to construct a visualization of the network.
    The output is a .HTML document with a interactive visualization of the network.

    :param nodes: a dictionary of Node objects
    """
    # Create a NetworkX graph
    G = nx.Graph()

    # Add nodes and edges
    for species, node in nodes.items():
        G.add_node(species)  # Add species as nodes
        for connection in node.get_connections():
            G.add_edge(species, connection.name)  # Add connections as edges

    # Create an interactive network visualization
    net = Network(notebook=True, height="750px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(G)
    net.force_atlas_2based(
        gravity=-50,
        central_gravity=0.01,
        spring_length=100,
        spring_strength=0.01,
        damping=0.95,
        overlap=0,
    )  # These can be adjusted to increase/reduce movement of nodes in the visualizer

    # Save and display the network
    net.show(NETWORK_OUTPUT_FILE)


def initalizeZeroDistanceNodes(df: pandas.DataFrame) -> dict:
    """
    This function uses 0 distance species pairs to construct an object oriented network.

    :param df: a pandas dataframe with species pairs and their distances (only zero distances should be known at this point)
    :returns: a dictionary of newly initalized Node objects
    """
    # Start by Initializing all 0-distance pairs
    nodes = {}  # use hash map to efficiently find already created nodes
    df_distance_0 = df[df[DISTANCE_COLUMN_NAME] == 0]
    for index, row in df_distance_0.iterrows():
        species1, species2 = row[SPECIES_PAIR_COLUMN_NAME].split("-")
        species1_node = nodes.get(species1, None)
        species2_node = nodes.get(species2, None)
        if species1_node == None:
            species1_node = Node(species1)
            nodes[species1] = species1_node
        if species2_node == None:
            species2_node = Node(species2)
            nodes[species2] = species2_node
        species1_node.add_connection(species2_node)
        species2_node.add_connection(species1_node)
    return nodes


def calculateNetworkDistances(df: pandas.DataFrame, nodes: dict) -> None:
    """
    This function uses the 0 distance species pair nodes to calculate the network distances
    for all other nodes using a Breadth-First-Search approach.

    :param df: a pandas dataframe with species pairs and their distances (only zero distances should be known at this point)
    :param nodes: a dictionary of Node objects
    :returns: the modified dataframe with all distances now calculated
    """
    # Use 0-distance nodes to find distances between all other nodes
    completed_pairs = (
        {}
    )  # use dictionary as hash map, using 'species_pair_nn' as candidate key
    for index, row in df[df[DISTANCE_COLUMN_NAME] != 0].iterrows():
        distance = completed_pairs.get(row[SPECIES_PAIR_COLUMN_NAME], None)
        if distance == None:
            species1, species2 = row[SPECIES_PAIR_COLUMN_NAME].split("-")
            species1_node = nodes.get(species1, None)
            species2_node = nodes.get(species2, None)
            if species1_node == None or species2_node == None:
                print(f"Unable to find distance for: {row[SPECIES_PAIR_COLUMN_NAME]}")
                distance = -1
            else:
                # Use Breadth-First Search to Find Minimum Distance Between Nodes
                queue = [(species1_node, 0)]
                visited_nodes = []
                found = False
                while len(queue) != 0 and not found:
                    current_node, current_depth = queue.pop(0)
                    for node in current_node.get_connections():
                        if node in visited_nodes:
                            continue
                        if node == species2_node:
                            found = True
                            distance = current_depth
                        else:
                            queue.append((node, current_depth + 1))
                    visited_nodes.append(current_node)
            completed_pairs[row[SPECIES_PAIR_COLUMN_NAME]] = distance
        df.at[index, DISTANCE_COLUMN_NAME] = distance
    return df


def main() -> None:
    cwd = os.getcwd()
    df = pandas.read_csv(os.path.join(cwd, DATA_FILE), encoding="UTF-16")
    nodes = initalizeZeroDistanceNodes(df)
    createNetworkVisualizer(nodes)
    calculateNetworkDistances(df, nodes).to_csv(
        os.path.join(cwd, DATA_OUTPUT_FILE)
    )  # calculate and export data


if __name__ == "__main__":
    main()
