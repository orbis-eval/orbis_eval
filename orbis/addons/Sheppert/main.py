#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
from os import walk

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from networkx.readwrite import json_graph

import plotly


def get_functions():
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))

    paths = []
    for (dirpath, dirnames, filenames) in walk(root):
        folder = dirpath.split("github.com/")[-1]

        for filename in filenames:
            if filename[-3:] == "pyc":
                continue

            module_name = filename.replace(".py", "")
            paths.append(f"{folder}/{module_name}")

            with open(f"{dirpath}/{filename}") as open_file:
                for line in open_file.readlines():
                    try:
                        function = True if line.strip()[0:3] == "def" else False
                    except Exception:
                        function = False

                    if function:
                        function = line.strip()
                        function = function[3:].strip()[:-1].split("(")[0]
                        paths.append(f"{folder}/{module_name}/{function}")

    modules = {}
    for item in paths:

        p = modules
        for x in item.split('/'):
            p = p.setdefault(x, {})

    return modules


def get_imports(only_orbis=False):
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))

    imports = {}
    for (dirpath, dirnames, filenames) in walk(root):
        folder = dirpath.split("github.com/")[-1]

        for filename in filenames:
            if filename.endswith("pyc"):
                continue
            if filename.endswith("html"):
                continue

            module_name = filename.replace(".py", "")
            module_path = f"{folder}/{module_name}".replace("/", ".")

            with open(f"{dirpath}/{filename}") as open_file:
                for line in open_file.readlines():
                    if only_orbis and "orbis" not in line:
                        continue

                    if line.strip().startswith("import "):
                        imported = line.strip()[7:]
                        imported = imported.split(" as ")[0]

                    if line.strip().startswith("from "):
                        base_module = line.split("import")[0][5:].strip()
                        if "." in base_module and len(set(base_module)) == 1:
                            printable_line = line.replace("\n", "")
                            print(f'Relative import found: {printable_line}')
                        else:
                            imported = line.split("import")[-1].strip()
                            imported = imported.split(" as ")[0]
                            imported = f"{base_module}.{imported}"

                    if "," not in line:
                        if imports.get(module_path):
                            imports[f"{module_path}"].append(imported)
                        else:
                            imports[f"{module_path}"] = [imported]
                    else:
                        print(f"Problem: {dirpath}/{filename}: {line}")

                    print(f"found import: {imported}")
    return imports


def build_graph(imports):
    directed_graph = nx.DiGraph()

    for key, values in imports.items():
        directed_graph.add_node(key)

        for value in values:
            directed_graph.add_node(value)
            directed_graph.add_edge(key, value)

    return directed_graph


def draw_graph(graph):

    degrees = nx.degree(graph)
    weight = [(name, degree) for degree, name in sorted([(degree, name) for name, degree in degrees], reverse=True)]

    """
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, font_size=8, font_color="k",
            node_color="b", edge_color="gray",
            with_labels=True, arrows=True,
            weight=weight,
            nodelist=[node[0] for node in degrees],
            node_size=[(node[1] + 1) * 10 for node in degrees])
    """

    # write_dot(G,'test.dot')

    # same layout using matplotlib with no labels
    # plt.title('draw_networkx')
    # neato, dot, twopi, circo, fdp, nop, wc, acyclic, gvpr, gvcolor, ccomps, sccmap, tred, sfdp, unflatten
    pos = graphviz_layout(graph, prog='sfdp')
    # print(pos)
    offset = {name: size for name, size in degrees}
    label_pos = {name: (x, y + offset[name] * 10) for name, (x, y) in pos.items()}

    nx.draw(graph, pos, font_size=8, font_color="k",
        node_color="b", edge_color="gray",
        with_labels=False, arrows=True,
        nodelist=[node[0] for node in degrees],
        node_size=[(node[1]) * 20 for node in degrees])

    nx.draw_networkx_labels(
        graph,
        label_pos,
        font_size=8,
        font_family="sans-serif"
    )
    # plt.savefig('nx_test.png')
    plt.show()


def sankey(graph):

    node_link_json = json_graph.node_link_data(graph)
    # print(node_link_json)
    labels = [node['id'] for node in node_link_json['nodes']]
    colors = ["blue" for n in range(len(labels))]

    sources = []
    targets = []
    values = []
    for item in node_link_json['links']:
        sources.append(labels.index(item['source']))
        targets.append(labels.index(item['target']))
        # values.append(len(targets))
        values.append(2)

    data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            label=labels,
            color=colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        ),
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        )
    )

    layout = dict(
        title="Orbis Functions",
        font=dict(
            size=20
        )
    )
    # data['orientation'] = 'v'
    data['node.thickness'] = 15

    fig = dict(data=[data], layout=layout)
    plotly.offline.plot(fig, validate=False)


def main():
    # functions = get_functions()
    imports = get_imports(only_orbis=True)
    graph = build_graph(imports)
    # draw_graph(graph)
    sankey(graph)


if __name__ == '__main__':
    main()
