from engine import calculate_probabilty, expected_value
import numpy as np
import matplotlib.pyplot as plt

def plot_as_graph():
    total_wins = 0
    history = []
    iterations = 100
    batch_size = 100

    for i in range(1, iterations + 1):
        wins_in_batch = calculate_probabilty(batch_size, multicore=False)
        total_wins += wins_in_batch
        current_equity = total_wins / (i * batch_size)
        history.append(current_equity)

    history = np.array(history)
    x_points = np.arange(batch_size, (iterations * batch_size) + 1, batch_size)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_points, history, label="Running Equity")
    plt.axhline(y=history[-1], color='r', linestyle='--', label=f"Final: {history[-1]:.2%}")
    
    plt.title("Convergence of Win Probability (Monte Carlo)")
    plt.xlabel("Total Number of Simulations")
    plt.ylabel("Win %")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

win_prob = calculate_probabilty(1000000)
print(expected_value(win_prob, 1000, 250))


