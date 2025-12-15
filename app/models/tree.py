# Tree data structure used for displaying the library
from __future__ import annotations
from typing import Dict, List


class TreeNode:
    def __init__(self, name: str, level: str):
        self.name = name
        self.level = level      # Level type (genre, director, etc.)
        self.children: Dict[str, "TreeNode"] = {}

    # Insert a path like: [("type", "Movies"), ("genre", "Sci-Fi"), ("director", "Nolan"), ("item", "Inception")]
    def add_path(self, labels: List[tuple[str, str]]) -> "TreeNode":
        node = self
        for lvl, name in labels:
            key = f"{lvl}:{name}"
            if key not in node.children:
                node.children[key] = TreeNode(name=name, level=lvl)
            node = node.children[key]
        return node

    # Converts tree into a list of text lines
    def to_lines(self, depth: int = 0) -> List[str]:
        pad = "  " * depth
        lines = [f"{pad}- {self.level}: {self.name}"]
        for child in self.children.values():
            lines.extend(child.to_lines(depth + 1))
        return lines

# Tree wrapper for movies and music
class MediaTree:
    def __init__(self, root_name: str = "Media Library"):
        self.root = TreeNode(root_name, "root")

    # Inserts movie nodes into the tree
    def insert_movie(self, movie: dict) -> None:
        labels: List[tuple[str, str]] = [
            ("type", "Movies"),
            ("genre", movie.get("genre", "Unknown")),
            ("director", movie.get("director", "Unknown")),
        ]
        if movie.get("series"):
            labels.append(("series", movie["series"]))
        labels.append(("item", f"{movie.get('title', 'Unknown')} ({movie.get('id', '')})"))
        self.root.add_path(labels)
    # Inserts song nodes into the tree
    def insert_song(self, song: dict) -> None:
        labels: List[tuple[str, str]] = [
            ("type", "Music"),
            ("genre", song.get("genre", "Unknown")),
            ("artist", song.get("artist", "Unknown")),
        ]
        if song.get("album"):
            labels.append(("album", song["album"]))
        labels.append(("item", f"{song.get('title', 'Unknown')} ({song.get('id', '')})"))
        self.root.add_path(labels)

    # Returns tree as formatted text
    def pretty(self) -> str:
        return "\n".join(self.root.to_lines())
