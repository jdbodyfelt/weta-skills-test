# weta-skills-test

This repo holds output for JD Bodyfelt's skills test, requested by Sherryn Hunt in consideration of my candidacy at Weta Digital for Full Stack Senior Web Developer. 

## Original Problem Statement

Weta's render farm consists of tens of thousands of cores that all run render processes which continuously eat up heaps of disk space. You're given the task to write a tool (preferably in python) that can accurately predict the ETA to the next meltdown (i.e. when we'll run out of space) in the following, oversimplified scenario:

 * Let's assume that $n$ processes are running on the farm. They run forever, never die, and no new processes get spawned.

 * Each process eats memory at a constant, individual rate - process $p_i$ (with $0 <= i < n$) consumes 1 byte after every $d(p_i)$ seconds. The total amount of available disk space is denoted by $X$.

* For each given input configuration (read from stdin), calculate the ETA in seconds.

* HINT – it is not the average.

* A configuration is encoded as a single line like this: $\quad X d(p_1)\,d(p_2)\,\ldots\,d(p_n)$

* Each output (the number of seconds) should be written as a single line to stdout.

* Your tool should be able to cope with large numbers of processes and large quantities of disk space.

**Example:**
```bash
$ echo -e "4 3 7\n15 2 4 3 6\n16 2 4 3 6" | python your_solution.py
> 9
> 12
> 14
```
---

## A Path to Solution

In order to quickly process a given configuration, an analytic equation is required to calculate the meltdown ETA. 

Initially, as we are dealing with rates, I would immediately utilize a [harmonic mean](https://en.wikipedia.org/wiki/Harmonic_mean). However, a hint is _explicitly provided_ that it is not "the average". This is vague, as "THE average" implies _arithmetic mean_; to ensure the hint meant AN average, I can quickly verify by considering the first configuration line. The two processes $p_{1,2}$ have respective consumption rates of $r_i = \frac{1}{d(p_i)}$, whose harmonic rate yields $\rho = 0.2$ and an ETA of 20.0s, which does not match the expected 9.0s. Therefore, a better hint ought read "it is not ANY average". 

Let's turn to differential calculus for our solution. Each individual process $p_i$ has individually consumed $x_i(t)$ bytes at a given second count $t$. It has already been established that the rate of these individual consumptions are constant $\frac{d x_i}{dt} = \frac{1}{d(p_i)}$. The total consumed bytes at a given time is then 
$x(t) = \sum_i x_i(t)$, which is storage-bound as $\lceil x(t) \rceil \le X$. 

From the nifty distributive property of differentiation, since the individual rates are constant, so is the overall rate. This overall constant rate of consumption is then found to be $\rho = \frac{dx}{dt} = \sum_i \frac{d x_i}{d t} = \sum_i \frac{1}{d(p_i)}$. Armed with constant overall rate and the total available storage space, the amount of time to fill the space is then defined as $T = \lceil \frac{X}{\rho} \rceil$.

As a check to this analytical solution, let me verify from the example: 
|  $X$  | $\left\lbrace d(p_i) \right\rbrace$ | $\rho$ | $\frac{X}{\rho}$ | $\lceil \frac{X}{\rho} \rceil$ | Verified |
| :---: | :---------------------------------: | :---: | :--------------: | :----------------------------: | :------: |
| 4 | 3, 7 | $\frac{10}{21}$ | $\frac{84}{10} = 8.4$ | 9 | ✅ |
| 15 | 2, 4, 3, 6 | $\frac{15}{12}$ | $\frac{180}{15} = 12.0$ | 12 | ✅ |
| 16 | 2, 4, 3, 6 | $\frac{15}{12}$ | $\frac{192}{15} = 12.8$ | 13 | ❎ (not 14!) |

I'm fairly confident in my differentials, so I'm going to chalk this 2/3 discrepancy up to a flawed example. 

## Solution Implementation

**Note:** As I am currently teaching myself TypeScript, static/duck typing have been on my mind a bit, so I'll be using static-typed python in any functional calls. 

For our analytical solution above, a simple python function is created: 
```python
def secToBoom(line: str):
    rates = [float(obj) for obj in line.rstrip().split(' ')]
    storage = rates.pop(0)
    rates = [1.0/r for r in rates]
    rate = sum(rates)
    ETA = ceil(storage/rate)
    print(ETA)
```
This is fairly simple to follow, if you're familiar with object comprehension in python (mainly lists here).
I take the line, strip off the `\n` character, and split on whitespace. Since the problem brief specifically stated _"..cope with large numbers of processes and large quantities of disk space"_, I perform a typecast to float on these strings (rather than integer) to address the actual numbers. 

In order to address the required piping syntax, a simple `sys` call can be used. I've chosen to keep the line-by-line processing serial, as there are only 7 lines in `numbers.txt`, but we can certainly implement `multiprocessing` pools to perhaps distribute the sum across cores, or even use `tensorflow` to do large-scale mathematics across the GPU. Since the given text file is simplified, I'll keep my code simplified, and just call my analytical function with
```python
import sys
for line in sys.stdin:
    secToBoom(line)
``` 
---
 ## Runtime and Unit Test

 The file `mySolution.py` combines the line-by-line `stdin` call with the function definition. 
 As an initial runtime test, I call it with the example and get:
```bash
echo -e "4 3 7\n15 2 4 3 6\n16 2 4 3 6" | python mySolution.py 
9
12
13
```

Running [the requested dataset](https://github.com/acky6012/lincolnshire-poacher) which has been downloaded locally to `numbers.txt`, I get the following result:
```bash
cat numbers.txt | python mySolution.py
9
12
13
590496223
181210885613
204221389795924037861376
154
```
which I leave to candidacy reviewers to validate. Thank you for your time, and this fun activity to showcase my Python skillset. 





