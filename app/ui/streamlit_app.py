import os
import sys
import streamlit as st
import networkx as nx
from pyvis.network import Network

# PATH FIX
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.utils.data_loader import (
    build_movie_tree_graph,
    build_music_tree_graph,
)
from app.models.recommender import Recommender


# STREAMLIT CONFIG (MUST BE FIRST)
st.set_page_config(
    page_title="Entertainment Platform",
    layout="wide"
)

# THEME SELECTOR
st.sidebar.title("🎨 Appearance")
theme = st.sidebar.selectbox("Theme", ["Base Dark", "Light", "Cyber"])


def apply_theme(theme):
    if theme == "Base Dark":
        bg, text, sidebar, highlight, card, border = (
            "#0E1117", "#FAFAFA", "#161B22", "#3B82F6", "#1C2128", "#30363D"
        )
        badge_bg, badge_text = "rgba(255,255,255,0.12)", "#FAFAFA"

    elif theme == "Light":
        bg, text, sidebar, highlight, card, border = (
            "#FCFCFD", "#353A42", "#E6E9ED", "#2D7CE2", "#FFFFFF", "#C7CCD1"
        )
        badge_bg, badge_text = "#EAF2FF", "#1E5ED8"

    else:  # Cyber
        bg, text, sidebar, highlight, card, border = (
            "#120D22", "#F0F6F7", "#1B1F3B", "#ED189C", "#191134", "#2E2A55"
        )
        badge_bg, badge_text = "rgba(255,255,255,0.14)", "#F0F6F7"

    st.markdown(f"""
    <style>
    /* Base */
    .stApp {{
        background-color: {bg};
        color: {text};
    }}

    section[data-testid="stSidebar"] {{
        background-color: {sidebar};
        border-right: 1px solid {border};
    }}

    /* Headings */
    h1, h2, h3 {{
        color: {highlight} !important;
    }}

    /* Readable text (DO NOT override spans globally) */
    .stApp p,
    .stApp label,
    .stApp small,
    .stApp li {{
        color: {text} !important;
    }}

    /* Cards */
    div[data-testid="stVerticalBlock"] > div {{
        background-color: {card};
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 14px;
        border: 1.5px solid {border};
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }}

    /* Badges */
    code {{
        background-color: {badge_bg} !important;
        color: {badge_text} !important;
        border-radius: 8px;
        padding: 4px 8px;
        font-weight: 600;
        font-size: 0.85em;
        border: 1px solid rgba(0,0,0,0.08);
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{
        color: {text} !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        border-bottom: 3px solid {highlight};
    }}

    /* ✅ Tree view: allow inline colors */
    .tree-view * {{
        color: inherit;
    }}
    .tree-view span[style] {{
        color: unset !important;
    }}
    </style>
    """, unsafe_allow_html=True)

apply_theme(theme)

def build_colored_tree(items, prefs, media_type, seed_id=None):
    html = "📚 Media Library\n\n"

    by_genre = {}
    for item in items:
        by_genre.setdefault(item["genre"], []).append(item)

    for genre, genre_items in sorted(by_genre.items()):
        html += f"• **{genre}**\n"

        for item in genre_items:
            matches = []

            # Match checks
            if prefs.get("genre") == genre:
                matches.append("Genre")

            if media_type == "Music":
                if prefs.get("artist") and item.get("artist") == prefs["artist"]:
                    matches.append("Artist")
            else:
                if prefs.get("director") and item.get("director") == prefs["director"]:
                    matches.append("Director")
                if prefs.get("actor") and prefs["actor"] in item.get("actors", []):
                    matches.append("Actor")

            # Emoji logic
            if len(matches) >= 2:
                emoji = "🔴"
            elif "Genre" in matches:
                emoji = "🔵"
            elif "Artist" in matches:
                emoji = "🟢"
            elif "Director" in matches:
                emoji = "🟠"
            elif "Actor" in matches:
                emoji = "🟣"
            else:
                emoji = "⚪"

            title = item.get("title", "Unknown")

            if item["id"] == seed_id:
                title = f"⭐ {title}"

            match_txt = f" ({', '.join(matches)})" if matches else ""

            html += f"  - {emoji} {title}{match_txt}\n"

        html += "\n"

    return html




# MATCH LOGIC
def get_match_flags(item, media_type, prefs):
    genre = item.get("genre") == prefs.get("genre")
    artist = False
    director = False
    actor = False

    if media_type == "Music" and prefs.get("artist"):
        artist = item.get("artist") == prefs["artist"]

    if media_type == "Movies":
        if prefs.get("director"):
            director = item.get("director") == prefs["director"]
        if prefs.get("actor"):
            actor = prefs["actor"] in item.get("actors", [])

    return bool(genre), bool(artist), bool(director), bool(actor)


def pick_color_from_matches(g, a, d, act, media_type):
    count = g + a + d + act
    if count >= 2:
        return "#ff0000"
    if g:
        return "#0088ff"
    if media_type == "Music" and a:
        return "#00cc44"
    if media_type == "Movies" and d:
        return "#ff8800"
    if media_type == "Movies" and act:
        return "#aa44ff"
    return "#777777"


# GRAPH
def show_interactive_graph(G, items, prefs, seed_id, media_type, theme):
    bg = "#FFFFFF" if theme == "Light" else "#120D22" if theme == "Cyber" else "#0E1117"
    font = "#353A42" if theme == "Light" else "#F0F6F7"

    nxG = nx.Graph()
    for u in G.adj:
        for v, w in G.adj[u].items():
            nxG.add_edge(u, v, weight=w)

    net = Network(height="600px", width="100%", bgcolor=bg, font_color=font)
    net.toggle_physics(False)

    item_by_id = {x["id"]: x for x in items}

    for node_id in nxG.nodes:
        item = item_by_id[node_id]
        flags = get_match_flags(item, media_type, prefs)
        color = pick_color_from_matches(*flags, media_type)
        size = 24 if node_id == seed_id else 14
        if node_id == seed_id:
            color = "#FFFFFF"

        net.add_node(
            node_id,
            label=item.get("title", "")[:18],
            title=item.get("title", ""),
            color=color,
            size=size
        )

    for u, v in nxG.edges:
        u_flags = get_match_flags(item_by_id[u], media_type, prefs)
        v_flags = get_match_flags(item_by_id[v], media_type, prefs)

        if seed_id:
            if u == seed_id:
                edge_color = pick_color_from_matches(*v_flags, media_type)
            elif v == seed_id:
                edge_color = pick_color_from_matches(*u_flags, media_type)
            else:
                edge_color = "#999999"
        else:
            cu = pick_color_from_matches(*u_flags, media_type)
            cv = pick_color_from_matches(*v_flags, media_type)
            edge_color = "#ff0000" if "#ff0000" in (cu, cv) else cu if cu != "#777777" else cv

        width = 3 if edge_color == "#ff0000" else 2 if edge_color != "#999999" else 1
        net.add_edge(u, v, color=edge_color, width=width)

    net.save_graph("graph.html")
    return open("graph.html", encoding="utf-8").read()


# SIDEBAR
st.sidebar.title("🎬 Preferences")
media_type = st.sidebar.selectbox("Media Type", ["Movies", "Music"])

if media_type == "Movies":
    tree, G, items = build_movie_tree_graph("app/data/movies.json")
    prefs = {
        "genre": st.sidebar.selectbox("Genre", sorted({m["genre"] for m in items})),
        "director": st.sidebar.selectbox("Director (optional)", [""] + sorted({m["director"] for m in items})) or None,
        "actor": st.sidebar.selectbox("Actor (optional)", [""] + sorted({a for m in items for a in m.get("actors", [])})) or None,
    }
    seed = st.sidebar.selectbox("Seed Movie (optional)", [""] + [m["id"] for m in items])
else:
    tree, G, items = build_music_tree_graph("app/data/music.json")
    prefs = {
        "genre": st.sidebar.selectbox("Genre", sorted({s["genre"] for s in items})),
        "artist": st.sidebar.selectbox("Artist (optional)", [""] + sorted({s["artist"] for s in items})) or None,
    }
    seed = st.sidebar.selectbox("Seed Song (optional)", [""] + [s["id"] for s in items])


# MAIN UI
st.title("🎧 Entertainment & Media Recommendation Platform")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📌 Recommendations")

    rec = Recommender(G, items)
    ranked = rec.rank([seed] if seed else [], prefs)
    best, similar, _ = rec.group_recommendations(ranked, prefs)

    for title, group in [("Best Match", best), ("You Might Also Like", similar)]:
        if group:
            st.markdown(f"### {title}")
            for info in group:
                item = next(x for x in items if x["id"] == info["id"])
                st.markdown(
                    f"**{item['title']}**  \n"
                    f"🧩 Matches: <code>{info['match_str']}</code>  \n"
                    f"⭐ Score: <code>{info['score']:.2f}</code>",
                    unsafe_allow_html=True
                )

with col2:
    tab1, tab2 = st.tabs(["🌐 Graph", "🌳 Tree"])

    with tab1:
        html = show_interactive_graph(G, items, prefs, seed, media_type, theme)
        st.components.v1.html(html, height=600, scrolling=True)

    with tab2:
        html_tree = build_colored_tree(items, prefs, media_type, seed)
        st.markdown(
            f"<div class='tree-view' style='font-family:monospace'>{html_tree}</div>",
            unsafe_allow_html=True
        )
