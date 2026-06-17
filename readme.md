*This project has been created as part of the 42 curriculum by msbayihi.*

## Description

Fly-in is a graph-based routing and logistics simulation. At its core, the project models a network where **Nodes** represent distinct physical areas called **Zones** (or hubs), and **Edges** represent the **Connections** (routes) linking them together. 

The primary objective of the simulation is to navigate a fleet of drones from a designated **start** zone to an **end** zone in the absolute minimum number of turns, optimizing the overall pathing strategy.

### Network Dynamics & Mechanics

To successfully route the drones, the simulation must account for several rules and constraints:

* **Zone Types & Movement Costs:** Every map requires at least one `start` zone (where all drones initially spawn) and an `end` zone (the final destination). The intermediate zones behave differently based on their type:
  * **Normal:** Standard zones with a basic movement cost.
  * **Priority:** Highly favored zones that the pathfinding algorithm should prioritize.
  * **Restricted:** Zones that are difficult to traverse, effectively doubling the movement cost (Cost = 2).
  * **Blocked:** Completely impassable zones that drones must route around.
  
* **Turn-Based Movement & Capacities:** A "turn" represents a synchronized movement phase across the network. Multiple drones can move simultaneously during a single turn, but they are strictly bound by limits. A drone can only enter a connection or a zone if it respects the `max_link_capacity` (the maximum number of drones allowed on a specific edge at once) and the `max_drones` limit (the maximum capacity of the target node).

## Instructions

The project is equipped with a `Makefile` to streamline the installation, execution, and testing processes. It is highly recommended to run this project within a Python virtual environment to maintain dependency isolation.

### 1. Installation
To install all required project dependencies (including `pygame`, `flake8`, and `mypy`) via the provided `requirements.txt`, run the following command at the root of the repository:

make install

### 2. Execution
To execute the main simulation using the default map, simply run:
make run

f you want to test a specific map configuration, you can run the main script directly through the Python interpreter by providing the file path as an argument or you can go to Makefile file and change the part ' MAP = ' by any map you want :
python3 main.py path/to/your/map.txt

### 3. Debugging
To run the main script in debug mode using Python's built-in debugger (pdb):
make debug

### 4. Code Quality & Linting

This project strictly adheres to typing and formatting standards. To execute the mandatory linting checks (flake8 and mypy):

make lint

### 5.Cleanup
To keep the project environment clean by removing temporary files and caches (such as __pycache__ and .mypy_cache), use:

make clean

## Resources

**Classic References:**
* [Graph (Discrete Mathematics) - Wikipedia](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) - Used to understand the foundational mathematical concepts of nodes and edges.
* [Graph Connectivity - Wikipedia](https://en.wikipedia.org/wiki/Connectivity_(graph_theory)) - Reference for understanding how different zones connect within a network.
* [Graph Theory Connectivity - Tutorialspoint](https://www.tutorialspoint.com/graph_theory/graph_theory_connectivity.htm) - Additional reading on graph connectivity, components, and network traversal.
* [Algorithm & Pathfinding Tutorial (YouTube)](https://youtu.be/rvxt42na8Ss) - Video reference for understanding the logic behind pathfinding algorithms.
* [Graph Traversal Tutorial (YouTube)](https://youtu.be/H2Fyau6ZpRg) - Video reference for network routing and graph search techniques.

**AI Usage:**
Artificial Intelligence (LLMs) was strictly used as a learning assistant and debugging tool during the development of this project. Specifically, AI was utilized for:
* **Project Comprehension & Structuring:** Breaking down the initial project prompt to fully understand the requirements, and organizing ideas logically to write this `README.md` file.
* **Strict Typing Debugging:** Resolving complex `mypy` strict typing errors, particularly those related to dictionary indexing, tuple unpacking, and function return signatures.
* **Algorithm Adaptation:** Assisting in the conceptual modification of the routing algorithm (based on Dijkstra) to calculate and return multiple optimal paths (e.g., the top 4 to 6 routes) rather than just a single shortest path, which was essential for distributing the drones efficiently.


## Algorithm Choices and Implementation Strategy

The core routing and simulation management rely on a carefully tuned strategy to ensure maximum efficiency and prevent network congestion:

* **Pathfinding with Controlled Cost Margin:** The pathfinding algorithm is designed to discover up to 6 optimal paths. Instead of indiscriminately taking any valid route, it identifies the absolute shortest path to use as a strict baseline reference. Any alternative path selected must have a cost difference of no more than 3 compared to this reference path. Originally, a margin of 10 was tested, but it resulted in excessively long paths and bloated turn counts. Constraining the margin to 3 ensures that all selected routes remain highly competitive and minimize the total simulation time.
* **Sequential Drone Distribution:** During the simulation phase, the optimal paths are distributed among the drone fleet using a round-robin assignment strategy (`assigned_path = self.paths[i % num_paths]`). This ensures that traffic is evenly spread across the available routes. For example, if 4 paths are found and 6 drones are deployed, the 5th and 6th drones will seamlessly loop back to reuse the 1st and 2nd best paths.

## Algorithm Choices and Implementation Strategy

The core routing and simulation management rely on a carefully tuned strategy to ensure maximum efficiency and prevent network congestion:

* **Pathfinding with Controlled Cost Margin:** The pathfinding algorithm is designed to discover up to 6 optimal paths. Instead of indiscriminately taking any valid route, it identifies the absolute shortest path to use as a strict baseline reference. Any alternative path selected must have a cost difference of no more than 3 compared to this reference path. Originally, a margin of 10 was tested, but it resulted in excessively long paths and bloated turn counts. Constraining the margin to 3 ensures that all selected routes remain highly competitive and minimize the total simulation time.
* **Sequential Drone Distribution:** During the simulation phase, the optimal paths are distributed among the drone fleet using a round-robin assignment strategy (`assigned_path = self.paths[i % num_paths]`). This ensures that traffic is evenly spread across the available routes. For example, if 4 paths are found and 6 drones are deployed, the 5th and 6th drones will seamlessly loop back to reuse the 1st and 2nd best paths.

* **Conflict Resolution & Prioritization:** To prevent traffic jams and collisions when multiple drones attempt to enter the exact same zone simultaneously, the simulation implements a smart priority system. Access priority is automatically granted to the drone that is logically closest to the `end` destination. By advancing the furthest drones first, the system actively clears up network capacity and prevents gridlocks for trailing drones.

## Visual Representation

The project includes a graphical interface built with `pygame` to provide a real-time visual representation of the network, significantly enhancing the user experience and debugging process:

* **Dynamic Screen Scaling:** To ensure the map is always clear, perfectly framed, and easy to read regardless of the dataset, the visualizer calculates the maximum `x` and `y` coordinates present in the parsed map. It then dynamically scales and offsets all nodes and edges to fit nicely within the window, preventing elements from overlapping or rendering off-screen.
* **Turn-by-Turn Tracking:** The interface dynamically tracks and animates the specific moves occurring during every single turn. By visually updating the drones' transit states and logging the operations simultaneously, it provides an intuitive way for the user to monitor the synchronized movements and verify that the routing and capacity logic is functioning perfectly.


