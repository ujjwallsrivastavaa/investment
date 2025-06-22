import matplotlib
matplotlib.use('Agg')  

import matplotlib.pyplot as plt
from market_sim.pow.proof_of_work import ProofOfWork
import os

def plot_mining_times(samples=10, difficulty=20):
    pow_engine = ProofOfWork(difficulty_bits=difficulty)
    times = []
    for i in range(samples):
        data = f"block-{i}"
        _, _, elapsed = pow_engine.mine(data)
        times.append(elapsed)
    
    plt.figure(figsize=(10, 5))
    plt.hist(times, bins=5, edgecolor='black')
    plt.xlabel("Mining Time (seconds)")
    plt.ylabel("Frequency")
    plt.title(f"Proof-of-Work Mining Times (Difficulty={difficulty})")
    plt.grid(True)
    plt.tight_layout()

  
    save_path = os.path.join(os.path.dirname(__file__), "pow_mining_times.png")
    plt.savefig(save_path)
    print(f"Plot saved as {save_path}")

if __name__ == "__main__":
    plot_mining_times()
