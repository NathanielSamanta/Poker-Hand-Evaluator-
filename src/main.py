from engine import calculate_probabilty, expected_value
import numpy as np
import matplotlib.pyplot as plt

def plot_as_graph():
    total_wins = 0
    history = []
    iterations = 1000
    batch_size = 1000

    for i in range(1, iterations + 1):
        _, wins_in_batch = calculate_probabilty(batch_size, multicore=False)
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

import time
import multiprocessing
from engine import worker_task

def run_benchmark(n_sims, use_multiprocessing=True):
    start_time = time.perf_counter()
    
    if use_multiprocessing:
        cores = multiprocessing.cpu_count()
        sims_per_core = n_sims // cores
        with multiprocessing.Pool(processes=cores) as pool:
            pool.map(worker_task, [sims_per_core] * cores)
    else:
        worker_task(n_sims)
        
    end_time = time.perf_counter()
    return end_time - start_time

# --- EXECUTION ---
for total in [10000, 100000, 1000000]:
    # Single Core
    t_single = run_benchmark(total, use_multiprocessing=False)
    # Multi Core
    t_multi = run_benchmark(total, use_multiprocessing=True)
    
    print(f"Sims: {total} | Single: {t_single:.4f}s | Multi: {t_multi:.4f}s")

# win_prob = calculate_probabilty(1000000)
# print(expected_value(win_prob, 1000, 250))

#plot_as_graph()


