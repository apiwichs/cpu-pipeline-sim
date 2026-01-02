# 🧠 CPU Pipeline Simulator
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Architecture](https://img.shields.io/badge/Computer%20Architecture-Pipeline%20Simulation-green)
![Status](https://img.shields.io/badge/Status-Complete-success)

A **cycle-accurate 5-stage CPU pipeline simulator** that models **instruction-level parallelism**, **RAW data hazards**, and **stall/bubble behavior**, with **quantitative performance analysis** using **NumPy**, **Pandas**, and **Matplotlib**.

---

## 🚀 Highlights

- ⏱️ **Cycle-accurate simulation**
- 🔁 **RAW data hazard detection**
- 🧱 **Pipeline stalls & bubble insertion**
- 📊 **CPI, stall rate, and pipeline utilization analysis**
- 📈 **Matplotlib performance visualizations**
- 🧪 **User-defined or hardcoded instruction streams**
- 💾 **CSV export of per-cycle pipeline trace**

---

## 🏗️ Pipeline Architecture

Classic **5-stage in-order pipeline**:

```
IF  →  ID  →  EX  →  MEM  →  WB
```

Each cycle, the simulator:
- Advances instructions through pipeline stages
- Detects **Read-After-Write (RAW)** hazards
- Inserts **bubbles (NOPs)** when required
- Logs the state of every stage

---

## 🧩 Instruction Format

Supported R-type ALU instructions:

```
OP dst src1 src2
```

Example:
```
ADD x1 x2 x3
SUB x9 x1 x8
```

- `OP`  : Arithmetic operation (`ADD`, `SUB`)
- `dst` : Destination register
- `src` : Source registers

> Bubbles are modeled internally as NOP-equivalent pipeline entries.

---

## ⚠️ Hazard Model

- Detects **RAW hazards** in the **ID stage**
- An instruction stalls if it reads a register written by an older instruction in:
  - **EX**
  - **MEM**
- **WB is treated as architecturally complete**, matching standard textbook timing
- Stall behavior:
  - IF & ID are frozen
  - A bubble is injected into EX
  - Older instructions continue to drain

---

## 🧪 Example Execution Trace

```
Cycle | IF               | ID               | EX               | MEM              | WB
------|------------------|------------------|------------------|------------------|----------------
1     | ADD x1<-x2,x3    | ----             | ----             | ----             | ----
2     | ADD x4<-x1,x5    | ADD x1<-x2,x3    | ----             | ----             | ----
3     | ADD x8<-x6,x7    | ADD x4<-x1,x5    | ADD x1<-x2,x3    | ----             | ----
4     | (stall)          | ADD x4<-x1,x5    | ----             | ADD x1<-x2,x3    | ----
```

---

## 📊 Performance Metrics

Derived **directly from the per-cycle trace**:

- **Total cycles**
- **Instructions retired**
- **Stall cycles & stall rate**
- **Cycles Per Instruction (CPI)**
- **Average pipeline occupancy**

All statistics are computed using **Pandas** and **NumPy**, not hardcoded counters.

---

## 📈 Visualizations

- **Pipeline occupancy vs. cycle**  
  Shows pipeline fill, stalls, and drain behavior over time

- **Stall cycles timeline**  
  Binary view of stall insertion across execution

*(Plots generated using Matplotlib)*

---

## 📁 Project Structure

```
cpu-pipeline-sim/
├── instruction.py      # Instruction data model
├── pipeline.py         # Pipeline + hazard logic
├── user_input.py       # Interactive instruction input
├── main.py             # Simulation driver & analysis
├── program_data.csv    # Exported per-cycle trace
└── README.md
```

---

## 🛠️ Requirements

- Python **3.10+**
- NumPy
- Pandas
- Matplotlib

Install dependencies:
```bash
pip install numpy pandas matplotlib
```

---

## ▶️ Running the Simulator

```bash
python main.py
```

- Supports **hardcoded** or **user-entered** instruction streams
- Automatically generates:
  - Console metrics
  - CSV trace
  - Performance plots

---

## 💡 Skills Demonstrated

- Computer Architecture & Pipeline Design
- Cycle-level performance modeling
- Hazard detection & stall control
- Python software engineering
- Data analysis with Pandas & NumPy
- Visualization with Matplotlib

---

## 🔮 Future Extensions

- 🔁 Data forwarding / bypassing
- 📦 Load/store instructions
- 🌿 Control hazards & branch modeling
- ⚙️ Configurable pipeline depth
- 📐 Comparative CPI analysis across designs

---

## © Copyright & Usage

© **Apiwich Sumeksri**. All rights reserved.

This repository and its contents are the intellectual property of **Apiwich Sumeksri**.  
No part of this project may be copied, modified, distributed, or used for commercial purposes without **explicit written permission** from the author.

This project is shared publicly **for portfolio and educational demonstration purposes only**.

---

