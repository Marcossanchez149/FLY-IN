*This project has been created as part of the 42 curriculum by marcsan2*

# Fly-in: Multi-Agent Drone Routing Simulator

# Description

Fly-in is a discrete-turn simulation and pathfinding engine designed to route a fleet of drones through a complex network of interconnected zones. The core objective is to move all drones from a designated starting hub to an end hub in the absolute minimum number of total simulation turns.

The map consists of various zone types (normal, priority, restricted, and blocked) and connections, each with specific capacity constraints (maximum drones allowed per turn). The project challenges us to solve a classic Multi-Agent Pathfinding (MAPF) problem: scheduling concurrent paths to maximize throughput while strictly avoiding path conflicts, capacity overflows, and deadlocks.

# Instructions

# Prerequisites
Python 3.8+ (or a compatible version specified by your environment)

pygame library (strictly used for the visual rendering component, not for graph logic)

# Installation
Clone the repository and install the required visualization dependency:

Bash
git clone git@vogsphere-v2.42madrid.com:vogsphere/intra-uuid-9fdf384d-4e67-49a1-9006-70ba3f8f1247-7333387-marcsan2
cd fly-in
make
Execution
Run the main script, passing the map configuration file as an argument:

Bash
python3 fly_in.py path/to/map_file.txt

# Controls (GUI)
SPACEBAR: Advance the simulation by exactly 1 turn. This will update the graphical interface and simultaneously print the strictly formatted movement logs to the standard output.

R: Restart the simulation (resets all drones to the starting hub at Turn 0).

ESC: Exit the simulator.

# Algorithm Choices and Implementation Strategy

To solve the routing problem efficiently without violating the "no external graph libraries" rule, the project relies on a custom implementation of Cooperative Space-Time Dijkstra.

1. The Space-Time Graph (Reservation Table):
A standard shortest-path algorithm fails in multi-agent scenarios because all agents will greedily choose the exact same route, causing immediate collisions. By adding the dimension of Time, our algorithm creates a "Reservation Table." When Drone 1 finds its optimal path, it reserves those specific hubs and connections for those specific turns. When Drone 2 calculates its path, it treats those reserved space-time coordinates as temporary walls, forcing it to either find an alternate route or execute "strategic waiting.

2. Separation of "Turn" and "Cost" (The Tie-Breaker):
To prevent the "Blind Tie" problem where drones would rather wait indefinitely than take a slightly longer path, the priority queue is sorted strictly by Turns first, and Cost second.Turns (Time): Dictate the actual length of the simulation.Cost (Preference): Acts as a tie-breaker to guide drone behavior.priority zones: Cost 0.1 (Highly attractive).normal zones: Cost 1.0.waiting (staying in place): Cost 1.5 (Slightly penalized to encourage taking alternative physical routes over idling).restricted zones: Cost 5.0 (Requires a 2-turn commitment, heavily penalized to act as a last resort)

# Visual Representation Features
To transform raw movement logs into a highly observable simulation, a custom Pygame-based 2D renderer was built.

Dynamic Auto-Scaling: The renderer mathematically scans the lowest and highest X/Y coordinates of the parsed map and dynamically calculates an offset and scale factor. This ensures that any map—whether it spans 5 units or 5,000 units—perfectly fits and centers within the window without manual camera adjustments.

# Resources
Multi-Agent Pathfinding (MAPF): General theory on Cooperative A* and Space-Time Pathfinding.

Python Official Documentation: For native data structures (Lists, Tuples, Sets) used to construct the custom priority queues.

Pygame Documentation: Used for the 2D rendering and event loop handling.