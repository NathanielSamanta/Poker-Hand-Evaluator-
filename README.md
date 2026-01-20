My first project featuring Gödel numbering, Monte Carlo simulations, the Cactus Kev algorithm, multiprocessing, Expected Value (EV) calculations, and more.

While researching how to undertake this project, I learned about the Cactus Kev algorithm. By assigning each rank a prime value, every 5-card combination yields a unique product, allowing for O(1) lookup times during simulation. To do this, I used 32-bit integers to represent each card:
- **Bits 0–7:** Used to create a unique fingerprint for each card through the multiplication of primes.
- **Bits 8–11:** Used for tie‑breaking logic.
- **Bits 12–15:** Represent the suit of each hand (e.g., 0001 for Spades, 0010 for Hearts, etc.).
- **Bits 16–31:** Used for straight identification. This is a bitmask where, for example, a "1" in the 1st bit signifies a rank of 2, and a "1" in the 2nd bit signifies a rank of 3.


Assigning each rank a prime number and then multiplying those primes together results in a unique product for every combination of ranks. This means that by pre-calculating all possible combinations and ranking them, I can use a hash table for lookups with O(1) time complexity. This efficiency is essential for a project like this, as a Monte Carlo simulation runs tens of thousands of times per calculation. I also utilized Python’s multiprocessing library to distribute the simulations across all CPU cores, which drastically reduces the execution time.

One might ask: why use a Monte Carlo simulation, and why run it so many times? I chose a Monte Carlo approach because it is exceptionally well-suited to poker. Poker features a massive number of card combinations, and since opponents' hands are hidden, the state space is enormous. Monte Carlo methods approximate outcomes through random sampling, allowing for an accurate probability without having to calculate every possible scenario.This probability is then used to calculate the Expected Value (EV), which informs the decision to fold, call, or raise. As the number of trials increases, the win probability converges toward a specific value; in other words, increasing the sample size removes "noise" from the probability calculation. This is a direct application of the Law of Large Numbers. We can see an example of this below:
<img width="986" height="596" alt="image" src="https://github.com/user-attachments/assets/7faed427-0137-44f4-bb56-7c7187c3701f" />

The program also features an equity calculator; by inputting the pot size and the bet amount, it uses the win probability to determine the mathematically optimal action. Below, I have included some benchmarks as well.

| Simulations | Mode        | Execution Time | Throughput (Hands/s) |
|------------|-------------|----------------|------------------------|
| 10,000     | Single-Core | 1.08s          | ~9,259                 |
| 10,000     | Multi-Core  | 1.98s          | ~5,050                 |
| 100,000    | Single-Core | 10.42s         | ~9,596                 |
| 100,000    | Multi-Core  | 4.84s          | ~20,661                |
| 1,000,000  | Single-Core | 101.10s        | ~9,891                 |
| 1,000,000  | Multi-Core  | 41.78s         | ~23,933                |

The most intreseting part of this data is that the multi-core method is twice as slow as the single core for 10,000 hands. This is likely due to overhead costs, such as inisitalisng hte lookup tables. However is is almost 2.5 faster when evaluating 1,000,000 hands 
