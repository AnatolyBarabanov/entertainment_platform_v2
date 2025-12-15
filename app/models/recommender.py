# Recommendation logic combining metadata + graph
from __future__ import annotations
from typing import Dict, List, Tuple


class Recommender:
    def __init__(self, graph, items: List[dict]):
        self.G = graph
        self.items_list = items
        # Map id -> item dict (quick lookup)
        self.items: Dict[str, dict] = {it["id"]: it for it in items}

    ## SCORE
    # Computes metadata-based score
    def score_item(self, item: dict, prefs: dict) -> float:
        score = 0.0

        # Genre matching (highest priority)
        if prefs.get("genre") and item.get("genre") == prefs["genre"]:
            score += 0.5

        # Director or Artist matching
        fav = prefs.get("artist") or prefs.get("director")
        if fav and (item.get("artist") == fav or item.get("director") == fav):
            score += 0.3

        # Actor matching (movies)
        if prefs.get("actor") and prefs["actor"] in item.get("actors", []):
            score += 0.2

        # Feature similarity (mood/traits)
        feat = item.get("features", {})
        for k in prefs.get("features", []):
            if feat.get(k, 0):
                score += 0.05

        # Popularity factor: rating (movies) or listeners (music)
        if "rating" in item:
            score += 0.1 * (float(item["rating"]) / 10.0)
        elif "listeners" in item:
            score += 0.1 * (float(item["listeners"]) / 2000.0)  # listeners ~ up to 2000k

        return round(score, 3)

    ## RANK
    def rank(self, seeds: List[str], prefs: dict, top_k: int = 50) -> List[Tuple[str, float]]:
        # Base score from metadata
        scores: Dict[str, float] = {
            iid: self.score_item(item, prefs) for iid, item in self.items.items()
        }

        # Graph-based similarity boost from seeds
        for s in seeds:
            for nbr, w in self.G.neighbors(s):
                scores[nbr] = scores.get(nbr, 0.0) + 0.2 * w

        # Do not recommend the seed item itself
        for s in seeds:
            scores.pop(s, None)

        # Sorts by: score first, then popularity (rating/listeners)
        def popularity(iid: str) -> float:
            item = self.items[iid]
            return float(item.get("rating", item.get("listeners", 0.0)))

        ranked = sorted(
            scores.items(),
            key=lambda kv: (kv[1], popularity(kv[0])),
            reverse=True,
        )
        return ranked[:top_k]

    ## GROUP
    # Splits items into Best / Similar / Hidden
    def group_recommendations(
        self,
        ranked: List[Tuple[str, float]],
        prefs: dict,
    ):
        best, similar, hidden = [], [], []

        for iid, score in ranked:
            item = self.items[iid]

            # Matches flags
            g = bool(item.get("genre") == prefs.get("genre"))
            d = bool(
                prefs.get("director")
                and item.get("director") == prefs.get("director")
            )
            a = bool(
                prefs.get("actor")
                and prefs["actor"] in item.get("actors", [])
            )

            matches = []
            if g:
                matches.append("Genre")
            if d or (prefs.get("artist") and item.get("artist") == prefs.get("artist")):
                # Treat artist or director as same "role" in description
                matches.append("Director/Artist")
            if a:
                matches.append("Actor")

            match_count = len(matches)
            match_str = ", ".join(matches) if matches else "None"

            # Popularity used for sorting and hidden gems
            pop_val = float(item.get("rating", item.get("listeners", 0.0)))

            info = {
                "id": iid,
                "score": score,
                "match_str": match_str,
                "popularity": pop_val,
            }

            # Classification logic
            if match_count >= 2 or score >= 0.8:
                # Strong match
                best.append(info)
                continue

            if match_count == 1:
                # At least one direct match
                similar.append(info)
                continue

            # Cross-artist / cross-genre logic for music: same artist, different genre still goes to "You Might Also Like"
            if (
                prefs.get("artist")
                and item.get("artist") == prefs["artist"]
                and item.get("genre") != prefs.get("genre")
            ):
                info["match_str"] = (
                    f"Artist ({prefs['artist']}) – different genre ({item.get('genre')})"
                )
                similar.append(info)
                continue

            # Hidden gems: same genre, lower popularity
            if g:
                # Thresholds: slightly below the "top" range
                if "rating" in item and pop_val < 7.8:
                    hidden.append(info)
                elif "listeners" in item and pop_val < 1400:
                    hidden.append(info)

        # Sort groups by (score, popularity) descending
        def sort_group(group):
            group.sort(key=lambda x: (x["score"], x["popularity"]), reverse=True)

        for group in (best, similar, hidden):
            sort_group(group)

        return best, similar, hidden
