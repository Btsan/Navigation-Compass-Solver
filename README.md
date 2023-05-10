# Navigation-Compass-Solver
Brute-force solver for Navigation Compass puzzles

<sub>Initial upload (May 9, 2023)</sub>

---

### Requirements

- python 3.8+
- numpy 1.23+

### Problem 

The Navigation Compass problem is a game involving 3 rings, $A, B,$ and $C$, which each have their own initial angle and rotation per step, rings may rotate in multiples of $\frac{\pi}{3}$ either clockwise or counter-clockwise. Additionally, the rings only rotate in 3 groups, e.g. ring $A$ may move simultaneously as a group with ring $B$ and/or with ring $C$ or as a group by itself. These patterns are not known prior to starting the problem. The goal of the player is to rotate the rings such that they are all oriented $\pi$ radians or $180\degree$. This can be formulated as solving the following system of equations.

$$ \cos(a_1 x_1 + a_2 x_2 + a_3 x_3 + a_0) = -1 $$

$$ \cos(b_1 x_1 + b_2 x_2 + b_3 x_3 + b_0) = -1 $$

$$ \cos(c_1 x_1 + c_2 x_2 + c_3 x_3 + c_0) = -1 $$

The solution to this, $x_1, x_2,$ and $x3$, are the number of times to rotate each group of rings. The python script `navigation_compass.py` attempts to brute-force a solution.

### Usage

`navigation_compass.py` has several arguments to specify the configuration of a navigation compass puzzle.

| Flag | Required | Valid Argument | Description |
| :--------: | :---: | :----: | ----: |
| `--inner` | Yes | Number that is a multiple of 60 | Degree of the inner axis | 
| `--middle` | Yes | Number that is a multiple of 60 | Degree of the middle axis | 
| `--outer` | Yes | Number that is a multiple of 60 | Degree of the outer axis | 
| `--marks-inner` | Yes | Natural number | Number of marks on inner ring, indicating rotation per step | 
| `--marks-middle` | Yes | Natural number | Number of marks on middle ring, indicating rotation per step | 
| `--marks-outer` | Yes | Natural number | Number of marks on outer ring, indicating rotation per step | 
| `--inner-cw` | No | None | Specify flag only if inner ring rotates clockwise | 
| `--middle-cw` | No | None | Specify flag only if middle ring rotates clockwise | 
| `--outer-cw` | No | None | Specify flag only if outer ring rotates clockwise | 
| `-a`, `--group-a` | Yes | At least one of `inner`, `middle,` and  `outer` | First group of rings that rotate together | 
| `-b`, `--group-b` | Yes | At least one of `inner`, `middle,` and  `outer` | Second group of rings that rotate together |  
| `-c`, `--group-c` | Yes | At least one of `inner`, `middle,` and  `outer` | Third group of rings that rotate together | 
| `-N`, `--maxit` | No | Natural number | Maximum number of brute-force attempts (default 100) | 

Example
```
python navigation_compass.py --inner 60 --middle 0 --outer 180 --marks-inner 4 --marks-middle 3 --marks-outer 1 --inner-cw --middle-cw --outer-cw -a inner -b middle outer -c inner outer
>>>
         answer = [20.  1. 11.] % 6 = [2 1 5]
         rotate group A ['inner'] 2 times
         rotate group B ['middle', 'outer'] 1 times
         rotate group C ['inner', 'outer'] 5 times
Solved in 11 brute-force iterations
```

If no solution is found, check if the arguments are correct.
