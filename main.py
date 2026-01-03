import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from instruction import Instruction
from pipeline import pipeline
from user_input import get_user_input

def main():
    
    plt.style.use("seaborn-v0_8-whitegrid")
    
    ## Uncomment this block for hardcoded Instructions
    program = [
        Instruction(instruction="ADD", src_regs=("x2","x3"), dst_reg="x1"),
        Instruction(instruction="ADD", src_regs=("x1","x5"), dst_reg="x4"),
        Instruction(instruction="ADD", src_regs=("x6","x7"), dst_reg="x8"),
        Instruction(instruction="SUB", src_regs =("x1","x8"), dst_reg="x9")]
   
    ## Uncomment for dynamic Instructions
    """
    program = get_user_input()
    if not program:
        print("No instructions entered. Exiting.")
        return
    """
    
    
    data = pipeline(program)
    data_df = pd.DataFrame(data)
    empty_data = "---------------"
    
    stages = ["IF", "ID", "EX", "MEM", "WB"]
    total_cycles = len(data_df)
    
    # Retired instructions (Completed WB)
    valid_wb = data_df["WB"] != empty_data
    retired = data_df.loc[valid_wb]
    retired_count = retired.shape[0] # Get the Rows of valid retired df
    
    # Stall cycles
    valid_stall = data_df["stall"]
    stall = data_df.loc[valid_stall]
    stall_count = stall.shape[0]    #Get the Rows of valid stall df
    
    # Metric variables
    stall_rate = 0
    cpi = 0
    
    # Metrics
    if(total_cycles > 0):
        stall_rate = (stall_count/total_cycles)
    else:
        stall_rate = 0
    
    if(retired_count > 0):
        cpi = (total_cycles/retired_count)
    else:
        cpi = np.nan
    
    active = data_df.loc[:,stages] != empty_data

    # Add column to data_df
    data_df["occupancy"] = active.sum(axis=1)
    
    avg_occupancy = np.mean(data_df["occupancy"])
    
    # Export to csv
    data_df.to_csv("program_data.csv", index=False)
    
    print("\n===== Metrics (from trace) =====")
    print("Total cycles:", total_cycles)
    print("Retired:", retired_count)
    print("Stall cycles:", stall_count)
    print(f"Stall rate: {stall_rate:.3f}")
    print(f"CPI: {cpi:.2f}")
    print(f"Average occupancy: {avg_occupancy:.2f}")
    
    ## Plotting data
    plt.figure(figsize=(8, 4))

    plt.plot(
        data_df["cycle"],
        data_df["occupancy"],
        marker="o",
        linewidth=2,
        label="Pipeline Occupancy")

    
    stall_cycles = data_df.loc[data_df["stall"], "cycle"]
    for c in stall_cycles:
        plt.axvline(c, color="red", alpha=0.22) ## Set transparency to 0.22
 
    # Dummy handle for stall legend entry
    plt.plot([], [], color="red", alpha=0.22, linewidth=4, label="Stall cycle")

    plt.xlabel("Cycle", fontsize=11)
    plt.ylabel("Active Pipeline Stages", fontsize=11)
    plt.title("Pipeline Occupancy vs Cycle", fontsize=13)

    plt.ylim(0, 5)
    plt.xticks(data_df["cycle"])

    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig("images/pipeline_occupancy.png", dpi=200)
    plt.show()

    # Plot Stall Cycles  
    plt.figure(figsize=(8, 2.5))

    plt.step(
        data_df["cycle"],
        data_df["stall"].astype(int),
        where="post",
        linewidth=2)

    plt.yticks([0, 1], ["No Stall", "Stall"])
    plt.ylim(-0.01, 1.01)     
    plt.grid(axis="x", alpha=0.3)

    plt.xlabel("Cycle")
    plt.title("Pipeline Stall Cycles")

    plt.tight_layout()
    plt.savefig("images/stall_cycles.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()