# Basic test: tree should include correct labels
from app.utils.data_loader import build_music_tree_graph

def test_tree_insertion():
    tree, G, items = build_music_tree_graph("app/data/music.json")
    txt = tree.pretty()
    # Tree must contain these keywords
    assert "type: Music" in txt
    assert "genre:" in txt
