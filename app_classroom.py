import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from bfs import bfs
from dfs import dfs
from astar import astar

# Page setup
st.set_page_config(page_title="Smart Drone Navigation", page_icon="🚁", layout="wide")

st.markdown("""
<style>
    .block-container {max-width: 1100px; padding-top: 2rem;}
    h1 {color: #168aad;}
    div[data-testid="stMetric"] {
        background: rgba(100, 160, 200, 0.10);
        border: 1px solid rgba(100, 160, 200, 0.25);
        border-radius: 12px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚁 Smart Delivery Drone Navigation")
st.write("Explore how **BFS, DFS, and A*** find a route through a city while avoiding buildings.")

# 10 x 10 city map: 0 = free space, 1 = building
grid = [[0 for _ in range(10)] for _ in range(10)]
obstacles = [
    (1, 2), (2, 2), (3, 2),
    (4, 4), (4, 5), (4, 6),
    (6, 7), (7, 7), (8, 7),
    (2, 8), (3, 8)
]
for row, col in obstacles:
    grid[row][col] = 1

start = (0, 0)
goal = (9, 9)

algorithms = {"BFS": bfs, "DFS": dfs, "A*": astar}
explanations = {
    "BFS": "Breadth-First Search checks nearby cells first. It finds a shortest route when every move has the same cost.",
    "DFS": "Depth-First Search follows one direction as far as it can, then backtracks. Its route may be longer.",
    "A*": "A* uses the distance to the destination to guide its search. Here it uses Manhattan distance."
}

with st.sidebar:
    st.header("Flight controls")
    algorithm = st.selectbox("Choose an algorithm", list(algorithms))
    st.info(explanations[algorithm])
    find_route = st.button("🚀 Find drone route", type="primary", use_container_width=True)
    st.caption("Map: 10 × 10 | Start: (0, 0) | Destination: (9, 9)")
    st.caption("The drone moves up, down, left, or right.")

# Only run the selected algorithm when the button is pressed.
if find_route:
    path, explored = algorithms[algorithm](grid, start, goal)
    st.session_state["route_result"] = (algorithm, path, explored)

# Draw the map; route becomes visible after running an algorithm.
result = st.session_state.get("route_result")
display_grid = [row[:] for row in grid]

if result:
    used_algorithm, path, explored = result
    for row, col in explored:
        if (row, col) not in (start, goal):
            display_grid[row][col] = 2
    if path:
        for row, col in path:
            if (row, col) not in (start, goal):
                display_grid[row][col] = 3

left, right = st.columns([3, 2], gap="large")

with left:
    st.subheader("🗺️ City map")
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#f8fbfd")
    ax.set_facecolor("#f8fbfd")
    colors = ListedColormap(["#f0f8ff", "#293241", "#a8dadc", "#ffd166"])
    ax.imshow(display_grid, cmap=colors, vmin=0, vmax=3)
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.set_xticks([i - 0.5 for i in range(11)], minor=True)
    ax.set_yticks([i - 0.5 for i in range(11)], minor=True)
    ax.grid(which="minor", color="#bdcbd5", linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.text(start[1], start[0], "S", ha="center", va="center",
            color="#00875a", fontsize=15, fontweight="bold")
    ax.text(goal[1], goal[0], "D", ha="center", va="center",
            color="#c1121f", fontsize=15, fontweight="bold")
    ax.set_title("Drone flight map")
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("📍 Flight details")
    if not result:
        st.info("Choose an algorithm in the sidebar and click **Find drone route**.")
    else:
        used_algorithm, path, explored = result
        if path:
            st.success("Destination reached!")
            st.write(f"**Algorithm used:** {used_algorithm}")
            a, b = st.columns(2)
            a.metric("Moves in route", len(path) - 1)
            b.metric("Cells explored", len(explored))
            st.caption("A move is one step up, down, left, or right.")
        else:
            st.error("No route found with the current map.")

    st.markdown("**Map legend**")
    st.markdown("""
    - 🟩 **S:** Starting point
    - 🟥 **D:** Delivery destination
    - ⬛ **Dark cells:** Buildings (blocked)
    - 🟦 **Light blue cells:** Explored by the algorithm
    - 🟨 **Yellow cells:** Final route
    """)

st.divider()
st.subheader("🧠 How do the algorithms work?")
st.write("**BFS** explores level by level. **DFS** explores deeply before backtracking. **A*** uses a distance estimate to decide where to search next.")
st.caption("This is a simplified grid simulation, not a real drone flight controller.")
