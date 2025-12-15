# Lightweight undirected weighted graph
from __future__ import annotations
from typing import Dict, Iterable, Tuple


class MediaGraph:
    def __init__(self):
        self.adj: Dict[str, Dict[str, float]] = {}

    # Adds node if missing
    def add_node(self, u: str) -> None:
        if u not in self.adj:
            self.adj[u] = {}

    # Adds undirected edge u <-> v
    def add_edge(self, u: str, v: str, w: float) -> None:

        # Add undirected edge u <-> v with weight w.
        self.add_node(u)
        self.add_node(v)
        self.adj[u][v] = w
        self.adj[v][u] = w

    # Returns (neighbor, weight) pairs
    def neighbors(self, u: str) -> Iterable[Tuple[str, float]]:
        return self.adj.get(u, {}).items()
