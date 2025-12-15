# Loads movies/music into a tree + graph
import json
from typing import Tuple, List
import numpy as np

from app.models.tree import MediaTree
from app.models.graph import MediaGraph

# Basic cosine similarity between feature vectors
def cosine_similarity(a: dict, b: dict) -> float:
    if not a or not b:
        return 0.0
    common_keys = list(set(a.keys()) & set(b.keys()))
    if not common_keys:
        return 0.0

    va = np.array([float(a[k]) for k in common_keys], dtype=float)
    vb = np.array([float(b[k]) for k in common_keys], dtype=float)

    denom = float(np.linalg.norm(va) * np.linalg.norm(vb))
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)


# Loads movies and build tree + similarity graph
def build_movie_tree_graph(path_json: str) -> Tuple[MediaTree, MediaGraph, List[dict]]:
    with open(path_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    tree = MediaTree("Media Library")
    G = MediaGraph()

    # Insert into tree and graph
    for m in data:
        tree.insert_movie(m)
        G.add_node(m["id"])

    # Build similarity edges based on metadata
    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = data[i], data[j]
            w = 0.0

            # Same genre
            if a.get("genre") == b.get("genre"):
                w += 0.2
            # Same director
            if a.get("director") == b.get("director"):
                w += 0.4
            # Shared actors
            if set(a.get("actors", [])) & set(b.get("actors", [])):
                w += 0.3
            # Feature similarity
            w += 0.3 * cosine_similarity(a.get("features", {}), b.get("features", {}))

            if w > 0.0:
                G.add_edge(a["id"], b["id"], min(w, 1.0))

    return tree, G, data

# Loads songs and build tree + similarity graph
def build_music_tree_graph(path_json: str) -> Tuple[MediaTree, MediaGraph, List[dict]]:
    with open(path_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    tree = MediaTree("Media Library")
    G = MediaGraph()

    for s in data:
        tree.insert_song(s)
        G.add_node(s["id"])

    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = data[i], data[j]
            w = 0.0

            # Same genre
            if a.get("genre") == b.get("genre"):
                w += 0.2
            # Same artist
            if a.get("artist") == b.get("artist"):
                w += 0.5
            # Same album
            if a.get("album") and a.get("album") == b.get("album"):
                w += 0.2
            # Feature similarity (mood, energy, etc.)
            w += 0.5 * cosine_similarity(a.get("features", {}), b.get("features", {}))

            if w > 0.15:
                G.add_edge(a["id"], b["id"], min(w, 1.0))

    return tree, G, data



