# ChessAI

This project aims to develop a chess playing ai bot<br>
Made using [pygame](https://www.pygame.org/) ([docs](https://www.pygame.org/docs/)).
<br>

## 🤖 Current Bot Performance
![Example](https://raw.githubusercontent.com/SudevOP1/ChessAI/main/code/analysis/bot_performance_comparison.png)<br> 

### bot1_random
Makes completely random legal moves without any evaluation or strategy<br>
### bot2_classic_depth
Uses a basic minimax search up to a fixed depth without pruning or optimizations, evaluating positions purely by material balance<br>
### bot3_alpha_beta
Implements the alpha-beta pruning algorithm to skip evaluation of branches that can’t affect the final decision, greatly improving search efficiency<br>
### bot4_move_ordering
Enhances alpha-beta pruning by sorting moves (e.g., captures first) to increase pruning effectiveness and reduce search time<br>
### bot5_pos_caching
Adds a transposition table (position caching) to store and reuse previously evaluated board states, minimizing redundant computations<br>
### bot6_square_heuristics
Evaluates positional strength by rewarding pieces placed on strategically valuable squares and adjusts king safety based on the game phase (middle game vs endgame)<br>
### bot7_active_square
Rewards positions where pieces control or attack more squares on the board, emphasizing overall piece activity and mobility over static placement<br>
### bot8_super_powerful
Combines both square-based heuristics and active-square evaluation to balance positional understanding with piece activity, making it the strongest and most adaptive bot<br>

## 🚀 How to run it locally

### 1. Clone the repo
```bash
git clone https://github.com/SudevOP1/ChessAI.git
cd ChessAI
```
### 2. Initialize venv
```powershell
python -m venv venv
venv\Scripts\activate
```
### 3. Install packages
```powershell
pip install -r requirements.txt
```
### 4. Run code
```powershell
python -m code.game
```
<br>
