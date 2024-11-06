import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import cirq
import random

# Define the maze matrix (1 = wall, 0 = path)
maze_matrix = np.array([
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1]
])

# Starting and exit points
start = (1, 1)
exit_points = [(i, j) for i in range(maze_matrix.shape[0]) for j in range(maze_matrix.shape[1]) 
               if (i == 0 or i == maze_matrix.shape[0] - 1 or j == 0 or j == maze_matrix.shape[1] - 1) 
               and maze_matrix[i, j] == 0]

# Define qubits and circuit
qubits = [cirq.LineQubit(i) for i in range(3)]
circuit = cirq.Circuit()

# Apply Hadamard gates for superposition (simulating potential path moves)
circuit.append([cirq.H(q) for q in qubits[:2]])

# Define the oracle based on the exit position as a quantum "win" condition
def oracle(circuit, qubits):
    circuit.append(cirq.CCX(qubits[0], qubits[1], qubits[2]))  # Example oracle marking paths

# Define the diffusion operator for amplitude amplification
def diffusion(circuit, qubits):
    circuit.append([cirq.H(q) for q in qubits[:2]])
    circuit.append([cirq.X(q) for q in qubits[:2]])
    circuit.append(cirq.CZ(qubits[0], qubits[1]))
    circuit.append([cirq.X(q) for q in qubits[:2]])
    circuit.append([cirq.H(q) for q in qubits[:2]])

# Apply oracle and diffusion operations
oracle(circuit, qubits)
diffusion(circuit, qubits)

# Measure qubits to simulate pathfinding
circuit.append(cirq.measure(*qubits[:2], key='result'))

# Run the quantum circuit
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=100)
measurement_counts = result.histogram(key='result')

# Convert measurement results into directional moves based on probabilities
move_mapping = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
def select_move(measurement_counts):
    sorted_counts = sorted(measurement_counts.items(), key=lambda item: item[1], reverse=True)
    high_prob_move = sorted_counts[0][0]  # Choose highest probability measurement
    return move_mapping[high_prob_move % 4]  # Map result to direction

# Quantum-inspired pathfinding function

def quantum_path_search(start, exit_points, maze_matrix, max_steps=10000):
    """Simulate quantum search to find the path from start to an exit point."""
    path = [start]
    position = start
    for step in range(max_steps):
        # Randomly select next step to mimic probabilistic path finding
        possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        random.shuffle(possible_moves)  # Randomize move order
        found_move = False
        for move in possible_moves:
            next_position = (position[0] + move[0], position[1] + move[1])
            # Check if move is within bounds, is a path (0), and hasn't been visited
            if (0 <= next_position[0] < maze_matrix.shape[0] and
                0 <= next_position[1] < maze_matrix.shape[1] and
                maze_matrix[next_position] == 0 and
                next_position not in path):                
                path.append(next_position)
                position = next_position
                found_move = True
                if next_position in exit_points:  # Exit found
                    print(f"Exit found at step {step} at position {next_position}.")
                    return path
                break
        if not found_move:
            print(f"Stuck at position {position} on step {step}, no valid moves.")
            break  # If no valid moves, break out of loop
    print("Max steps reached without finding an exit.")
    return None  # Return None if no path found within max steps

# Try searching with a higher step count
solution_path = None
for attempt in range(100):  # Attempt multiple searches to find a solution
    solution_path = quantum_path_search(start, exit_points, maze_matrix, max_steps=40)
    if solution_path:
        break

# Final output
if not solution_path:
    print("No solution path found with quantum-inspired search.")
else:
    print("Solution path found:", solution_path)

# Visualization of the maze and solution path
wall_color = 'black'
path_color = 'white'
solution_color = 'red'
cmap = ListedColormap([path_color, wall_color])
plt.figure(figsize=(8, 8))
plt.imshow(maze_matrix, cmap=cmap, origin='upper')

# Plot solution path if found
if solution_path:
    y_coords, x_coords = zip(*solution_path)
    plt.plot(x_coords, y_coords, color=solution_color, linewidth=2.5, label="Solution Path")

# Mark start and exit points
plt.text(start[1], start[0], 'Start', ha='center', va='center', color='green', fontsize=12, fontweight='bold')
for exit_point in exit_points:
    plt.text(exit_point[1], exit_point[0], 'Exit', ha='center', va='center', color='blue', fontsize=12, fontweight='bold')

plt.legend(loc='upper right')
plt.axis('off')
plt.title("Maze Solution Path Using Quantum-inspired Search", fontsize=16, fontweight='bold')
plt.show()

