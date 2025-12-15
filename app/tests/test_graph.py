# Basic test: graph should link similar movies
from app.utils.data_loader import build_movie_tree_graph

def test_graph_edges():
    # Load structure
    tree, G, items = build_movie_tree_graph("app/data/movies.json")
    # Pick two movies from the same director
    ids = [x["id"] for x in items if x["director"].startswith("Christopher Nolan")]
    assert len(ids) >= 2
    a, b = ids[0], ids[1]
    # They should be connected in the graph
    assert b in G.adj[a]
