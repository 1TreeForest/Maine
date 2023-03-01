# Maine
A directed fuzzing tool for PHP applications. 

## Plan for now

1. The first step is to generate Control Flow Graph (CFG) and Call Graph (CG) to represent the dependencies between code blocks.

2. The next step involves pre-computing basic block distances using the Dijkstra algorithm. During the process, loops and recursions are treated as conditional statements with a 50% execution probability for each. If a branch can reach the target, its possibility is assigned a value of 1; otherwise, it is set to 0. The distance of a code block should be the inverse of the average of its successor blocks' possibility to reach the target block.

3. Appropriate seed inputs are added to a tuple and an input queue as the initial state.

4. The input distances are computed based on the covered basic blocks, and the **average [AFLGo] / shortest [SelectFuzz]** block distance is selected as an input's input distance. If the input discovers a path-divergent code that leads to a smaller input distance, the input distance should be updated accordingly. This improved input should be enqueued, and more energy should be allocated to it with a proper power schedule strategy. 

   > **possible minor contribution:** the average and shortest could perhaps be used in combination (e.g., dynamically adjusting the weights or adopting the shortest strategy if the seed input adopted the average strategy), as the average is somewhat similar to the breadth-first search and the shortest is somewhat similar to the depth-first search. Also, maybe I could adopt another power schedule strategy if time permits.

5. If the input queue becomes empty after a specific run, it should be refilled with the seed inputs so the fuzzing process is reset to the initial state, and the refill should be recorded. Some parameters or random seeds should be adjusted.

6. Early termination for path pruning could be implemented if time permits. Additionally, there may be other challenges encountered during the development process particularly due to the unique features of PHP.
