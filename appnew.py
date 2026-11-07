#Includes comparison of BFS, DFS and A* algorithms for drone navigation in a grid with obstacles and displayed as bar chart
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time

from bfs import bfs
from dfs import dfs
from astar import astar

st.title("Smart Delivery Drone Navigation")

st.write("Find a path for the delivery drone using AI algorithms.")

# Create a 10 x 10 grid
grid = [[0 for j in range(10)] for i in range(10)]

# Add buildings as obstacles
obstacles = [
    (1, 2), (2, 2), (3, 2),
    (4, 4), (4, 5), (4, 6),
    (6, 7), (7, 7), (8, 7),
    (2, 8), (3, 8)
]

for x, y in obstacles:
    grid[x][y] = 1

# Starting and destination positions
start = (0, 0)
goal = (9, 9)

# Store algorithms
algorithms = {
    "BFS": bfs,
    "DFS": dfs,
    "A*": astar
}

# Select algorithm
algorithm = st.selectbox(
    "Choose AI Algorithm",
    ["BFS", "DFS", "A*"]
)

# Find route button
if st.button("Find Drone Route"):

    path, explored = algorithms[algorithm](grid, start, goal)

    # Copy the grid
    new_grid = [row[:] for row in grid]

    # Mark explored cells
    for x, y in explored:
        if (x, y) != start and (x, y) != goal:
            new_grid[x][y] = 2

    # Mark final path
    if path:
        for x, y in path:
            if (x, y) != start and (x, y) != goal:
                new_grid[x][y] = 3

    # Display grid
    fig, ax = plt.subplots(figsize=(7, 7))

    colors = ListedColormap([
        "white", "black", "lightblue", "yellow"
    ])

    ax.imshow(new_grid, cmap=colors, vmin=0, vmax=3)

    ax.set_xticks(range(10))
    ax.set_yticks(range(10))

    ax.set_xticks([i - 0.5 for i in range(11)], minor=True)
    ax.set_yticks([i - 0.5 for i in range(11)], minor=True)

    ax.grid(which="minor", color="gray", linewidth=1)

    ax.text(0, 0, "S", color="green",
            ha="center", va="center")

    ax.text(9, 9, "D", color="red",
            ha="center", va="center")

    ax.set_title("Drone Navigation using " + algorithm)

    st.pyplot(fig)
    plt.close(fig)

    # Display results
    if path:
        st.success("Drone reached the destination!")

        st.write("Selected Algorithm:", algorithm)
        st.write("Path length:", len(path) - 1)
        st.write("Explored cells:", len(explored))
    else:
        st.error("No path found!")

# Legend
st.write("S - Starting point")
st.write("D - Delivery destination")
st.write("Black - Buildings")
st.write("Blue - Explored cells")
st.write("Yellow - Final path")


# -----------------------------------
# PERFORMANCE COMPARISON
# -----------------------------------

st.divider()

st.header("Algorithm Performance Comparison")

st.write(
    "Compare BFS, DFS and A* using execution time, "
    "explored cells and path length."
)

if st.button("Compare All Algorithms"):

    results = []

    # Run each algorithm 10 times
    for name, function in algorithms.items():

        total_time = 0

        for i in range(10):

            start_time = time.perf_counter()

            path, explored = function(grid, start, goal)

            end_time = time.perf_counter()

            total_time += (end_time - start_time)

        # Calculate average execution time
        avg_time = (total_time / 10) * 1000

        if path:
            path_length = len(path) - 1
        else:
            path_length = 0

        results.append({
            "Algorithm": name,
            "Execution Time (ms)": round(avg_time, 4),
            "Explored Cells": len(explored),
            "Path Length": path_length
        })

    # Display comparison table
    st.subheader("Comparison Table")

    st.table(results)

    # Get values for graphs
    names = [r["Algorithm"] for r in results]
    times = [r["Execution Time (ms)"] for r in results]
    explored_cells = [r["Explored Cells"] for r in results]
    path_lengths = [r["Path Length"] for r in results]

    # Execution time graph
    st.subheader("Execution Time")

    fig1, ax1 = plt.subplots()

    ax1.bar(names, times)
    ax1.set_ylabel("Time (milliseconds)")
    ax1.set_xlabel("Algorithm")
    ax1.set_title("Execution Time Comparison")

    st.pyplot(fig1)
    plt.close(fig1)

    # Explored cells graph
    st.subheader("Explored Cells")

    fig2, ax2 = plt.subplots()

    ax2.bar(names, explored_cells)
    ax2.set_ylabel("Number of cells")
    ax2.set_xlabel("Algorithm")
    ax2.set_title("Explored Cells Comparison")

    st.pyplot(fig2)
    plt.close(fig2)

    # Path length graph
    st.subheader("Path Length")

    fig3, ax3 = plt.subplots()

    ax3.bar(names, path_lengths)
    ax3.set_ylabel("Number of movements")
    ax3.set_xlabel("Algorithm")
    ax3.set_title("Path Length Comparison")

    st.pyplot(fig3)
    plt.close(fig3)