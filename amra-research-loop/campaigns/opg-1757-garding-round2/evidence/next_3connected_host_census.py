#!/usr/bin/env python3
"""Exact unlabeled census of the first hosts after the audited W4 case."""

import json
import networkx as nx


def edge_orbits(graph):
    edges = {tuple(sorted(edge)) for edge in graph.edges()}
    unseen = set(edges)
    orbits = []
    matcher = nx.algorithms.isomorphism.GraphMatcher(graph, graph)
    automorphisms = list(matcher.isomorphisms_iter())
    while unseen:
        edge = min(unseen)
        orbit = {
            tuple(sorted((mapping[edge[0]], mapping[edge[1]])))
            for mapping in automorphisms
        }
        assert orbit <= edges
        orbits.append(sorted(orbit))
        unseen -= orbit
    return sorted(orbits, key=lambda orbit: (len(orbit), orbit))


def name(graph):
    if nx.is_isomorphic(graph, nx.wheel_graph(5)):
        return "W4"
    if graph.number_of_nodes() == 5:
        complement_edges = nx.complement(graph).number_of_edges()
        if complement_edges == 2 and max(dict(nx.complement(graph).degree()).values()) == 1:
            return "K5-minus-matching2"
        if complement_edges == 1:
            return "K5-minus-edge"
    if nx.is_isomorphic(graph, nx.complete_bipartite_graph(3, 3)):
        return "K3,3"
    if nx.is_isomorphic(graph, nx.circular_ladder_graph(3)):
        return "triangular-prism"
    return "unidentified"


records = []
for graph in nx.graph_atlas_g():
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    if not (4 <= n <= 6 and 7 <= m <= 9):
        continue
    if nx.node_connectivity(graph) < 3:
        continue
    relabelled = nx.convert_node_labels_to_integers(graph, ordering="sorted")
    orbits = edge_orbits(relabelled)
    records.append({
        "name": name(relabelled),
        "vertices": n,
        "edges": m,
        "degree_sequence": sorted((degree for _, degree in relabelled.degree()), reverse=True),
        "edge_orbit_count": len(orbits),
        "edge_orbit_sizes": [len(orbit) for orbit in orbits],
        "edge_orbit_representatives": [list(orbit[0]) for orbit in orbits],
        "graph6": nx.to_graph6_bytes(relabelled, header=False).decode().strip(),
    })

records.sort(key=lambda item: (item["edges"], item["vertices"], item["degree_sequence"], item["graph6"]))
assert [item["name"] for item in records].count("W4") == 1
assert {item["name"] for item in records if item["edges"] <= 9} == {
    "W4", "K5-minus-edge", "K3,3", "triangular-prism"
}

print(json.dumps({
    "schema": "amra.opg1757.next-3connected-host-census.v1",
    "scope": "all unlabeled simple 3-connected graphs with 4<=n<=6 and 7<=m<=9 from the NetworkX graph atlas",
    "host_count": len(records),
    "hosts": records,
    "conclusion": "W4 is isomorphic to K5 minus a two-edge matching. After audited W4, exactly three irreducible hosts remain through nine edges: K5-e, K3,3, and the triangular prism.",
    "finite_routing_only": True,
    "public_problem_closed": False
}, indent=2, sort_keys=True))
