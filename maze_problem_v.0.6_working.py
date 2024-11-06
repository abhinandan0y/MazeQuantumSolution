import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import cirq
import random
import time

# Define the maze matrix
maze_matrix = np.array([
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 1],  # 0 = path (white), 1 = wall (black)
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1]
])

# Starting and exit positions
start = (1, 1)
exit_points = [(i, j) for i in range(maze_matrix.shape[0]) for j in range(maze_matrix.shape[1]) 
               if (i == 0 or i == maze_matrix.shape[0] - 1 or j == 0 or j == maze_matrix.shape[1] - 1) 
               and maze_matrix[i, j] == 0]

# Define qubits
qubits = [cirq.LineQubit(i) for i in range(2)]
# Define the quantum circuit
circuit = cirq.Circuit()

# Apply Hadamard gates to create superposition
circuit.append([cirq.H(q) for q in qubits])

# Define Oracle for the quantum solution
def oracle(circuit, qubits):
    circuit.append(cirq.CCX(qubits[0], qubits[1], cirq.LineQubit(2)))

# Define Diffusion Operator
def diffusion(circuit, qubits):
    circuit.append([cirq.H(q) for q in qubits])
    circuit.append([cirq.X(q) for q in qubits])
    circuit.append(cirq.CZ(qubits[0], qubits[1]))
    circuit.append([cirq.X(q) for q in qubits])
    circuit.append([cirq.H(q) for q in qubits])

# Apply the Oracle and Diffusion
oracle(circuit, qubits)
diffusion(circuit, qubits)

# Measure the qubits
circuit.append(cirq.measure(*qubits, key='result'))

# Simulate the circuit
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)

# Output measurement results
measurement_counts = result.histogram(key='result')
print("Measurement Results:", measurement_counts)


def quantum_path_search(start, exit_points, maze_matrix, max_steps=20):
    """Simulate quantum search to find the path from start to an exit point."""
    path = [start]
    position = start
    for _ in range(max_steps):
        # Randomly select next step to mimic probabilistic path finding
        possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        random.shuffle(possible_moves)  # Randomize move order
        found_move = False
        for move in possible_moves:
            next_position = (position[0] + move[0], position[1] + move[1])
            # Check if move is within bounds, is a path (0), and has not been visited
            if (0 <= next_position[0] < maze_matrix.shape[0] and
                0 <= next_position[1] < maze_matrix.shape[1] and
                maze_matrix[next_position] == 0 and
                next_position not in path):
                path.append(next_position)
                position = next_position
                found_move = True
                if next_position in exit_points:  # Exit found
                    return path
                break
        if not found_move:
            break  # If no valid moves, break out of loop
    return None  # Return None if no path found within max steps

# Search for a valid path
solution_path = None
for _ in range(100):  # Attempt multiple searches to find a solution
    solution_path = quantum_path_search(start, exit_points, maze_matrix)
    if solution_path:
        break

# If no path found
if not solution_path:
    print("No solution path found with quantum search.")
else:
    print("Solution path found:", solution_path)

# Visualization
# Set up the color mapping for the maze
wall_color = 'black'
path_color = 'white'
solution_color = 'red'
cmap = ListedColormap([path_color, wall_color])

# Plot the maze with the solution path
plt.figure(figsize=(8, 8))
plt.imshow(maze_matrix, cmap=cmap, origin='upper')

# Overlay the solution path in red if it exists
if solution_path:
    y_coords, x_coords = zip(*solution_path)
    plt.plot(x_coords, y_coords, color=solution_color, linewidth=2.5, label="Solution Path")

# Mark start and exits
plt.text(start[1], start[0], 'Start', ha='center', va='center', color='green', fontsize=12, fontweight='bold')
for exit_point in exit_points:
    plt.text(exit_point[1], exit_point[0], 'Exit', ha='center', va='center', color='blue', fontsize=12, fontweight='bold')

# Format the plot for publication
plt.legend(loc='upper right')
plt.axis('off')
plt.title("Maze Solution Path Using Quantum Search", fontsize=16, fontweight='bold')
plt.show()

