# zone-job-scheduler-deadlock-engine

## Production Scheduling Choice

Based on the results I got from Tasks 2–4, I would choose the SJF/SRTF family, specifically SRTF, for the zone-controller jobs. SRTF gave the best overall performance in my testing, with an average waiting time of 11.50 ticks and an average turnaround time of 17.00 ticks. These were the lowest values among the scheduling algorithms I tested.

The other three scheduling families are less suitable for this workload:

1. **FCFS:** FCFS had an average waiting time of 17.12 ticks and an average turnaround time of 22.62 ticks. Both values are higher than SRTF, so jobs would generally have to wait longer before completing.
2. **Round Robin:** With a quantum of 3, Round Robin produced 16 context switches, while a quantum of 6 produced 10 context switches. The quantum-6 version still had an average waiting time of 20.38 ticks, which is much higher than SRTF's 11.50 ticks. This makes Round Robin less suitable for this workload.
3. **Priority Scheduling:** Priority scheduling without aging had an average waiting time of 14.12 ticks, while priority scheduling with aging had 17.12 ticks. In the no-aging case, Z3-J02 waited for 33 ticks, which shows that some lower-priority jobs can experience a long wait.

Therefore, I would use SRTF in production for these zone-controller jobs because it provided the lowest average waiting time and turnaround time in my measured results.

## Part 1 — Program Outputs

The following outputs were produced by running the Part 1 programs using the fixed `JOBS` list from `jobs.py`.

### Task 2–4 — Scheduling Algorithms

```text
============================================================
FCFS
============================================================
Job ID      Waiting Time   Turnaround Time
---------------------------------------------
Z1-J01      0              8
Z1-J02      7              11
Z2-J01      10             19
Z2-J02      18             23
Z3-J01      22             24
Z3-J02      23             29
Z1-J03      28             31
Z2-J03      29             36
---------------------------------------------
Average Waiting Time    : 17.12
Average Turnaround Time : 22.62

============================================================
Non-Preemptive SJF
============================================================
Job ID      Waiting Time   Turnaround Time
---------------------------------------------
Z1-J01      0              8
Z1-J02      12             16
Z2-J01      33             42
Z2-J02      14             19
Z3-J01      4              6
Z3-J02      17             23
Z1-J03      4              7
Z2-J03      20             27
---------------------------------------------
Average Waiting Time    : 13.00
Average Turnaround Time : 18.50

============================================================
SRTF
============================================================
Job ID      Waiting Time   Turnaround Time
---------------------------------------------
Z1-J01      20             28
Z1-J02      0              4
Z2-J01      33             42
Z2-J02      7              12
Z3-J01      1              3
Z3-J02      10             16
Z1-J03      1              4
Z2-J03      20             27
---------------------------------------------
Average Waiting Time    : 11.50
Average Turnaround Time : 17.00

============================================================
Round Robin (Quantum = 3)
============================================================
Job ID      Waiting Time   Turnaround Time
---------------------------------------------
Z1-J01      26             34
Z1-J02      19             23
Z2-J01      32             41
Z2-J02      24             29
Z3-J01      11             13
Z3-J02      26             32
Z1-J03      14             17
Z2-J03      29             36
---------------------------------------------
Average Waiting Time    : 22.62
Average Turnaround Time : 28.12
Dispatch slices          : 17
Context switches         : 16

============================================================
Round Robin (Quantum = 6)
============================================================
Job ID      Waiting Time   Turnaround Time
---------------------------------------------
Z1-J01      26             34
Z1-J02      5              9
Z2-J01      32             41
Z2-J02      13             18
Z3-J01      17             19
Z3-J02      18             24
Z1-J03      23             26
Z2-J03      29             36
---------------------------------------------
Average Waiting Time    : 20.38
Average Turnaround Time : 25.88
Dispatch slices          : 11
Context switches         : 10

Real-OS overhead statement:
Quantum 3 would cause more real context-switch overhead than quantum 6 because this simulation produces more job changes: 16 switches for quantum 3 versus 10 switches for quantum 6.

============================================================
Non-Preemptive Priority (No Aging)
============================================================
Job ID      Waiting Time   Turnaround Time
---------------------------------------------
Z1-J01      0              8
Z1-J02      7              11
Z2-J01      27             36
Z2-J02      11             16
Z3-J01      8              10
Z3-J02      33             39
Z1-J03      13             16
Z2-J03      14             21
---------------------------------------------
Average Waiting Time    : 14.12
Average Turnaround Time : 19.62

============================================================
Non-Preemptive Priority (With Aging)
============================================================
Job ID      Waiting Time   Turnaround Time
---------------------------------------------
Z1-J01      0              8
Z1-J02      7              11
Z2-J01      10             19
Z2-J02      18             23
Z3-J01      22             24
Z3-J02      23             29
Z1-J03      28             31
Z2-J03      29             36
---------------------------------------------
Average Waiting Time    : 17.12
Average Turnaround Time : 22.62

Priority Scheduling Longest Wait
---------------------------------------------
No aging : Z3-J02 (33 ticks)
With aging: Z2-J03 (29 ticks)
```

### Task 5 — Race Condition and Peterson's Algorithm

```text
============================================================
Zone-B Compute-Credit Counter
============================================================

Initial counter: 100
Correct final value: 85

Without synchronization:
Run 1: 125
Run 2: 125
Run 3: 125
Run 4: 125
Run 5: 125

Race condition observed: YES

With Peterson's Algorithm:
Run 1: 85
Run 2: 85
Run 3: 85
Run 4: 85
Run 5: 85

Peterson's Algorithm correct: YES
```

### Task 6 — Banker's Algorithm

```text
============================================================
Banker's Algorithm
============================================================

Need Matrix:
P0: [7, 4, 3]
P1: [1, 2, 2]
P2: [6, 0, 0]
P3: [0, 1, 1]

Initial Available: [3, 3, 2]

Initial system safety check:
SAFE

Safe sequence:
P1 -> P3 -> P0 -> P2

------------------------------------------------------------
Request 1
------------------------------------------------------------
Process: P1
Request: [1, 0, 2]

Safety check after hypothetical allocation:
SAFE

RESULT: GRANT request from P1.

------------------------------------------------------------
Request 2
------------------------------------------------------------
Process: P0
Request: [2, 0, 2]

Safety check after hypothetical allocation:
UNSAFE

RESULT: DENY request from P0 because granting it would leave
the system in an unsafe state.

Both requests were evaluated independently against the original state.
```

### Task 7 — Paging Address Translation

```text
============================================================
Paging Address Translation
============================================================

Page size: 1024 bytes

Logical Address: 260
Page Number: 0
Offset: 260
Frame Number: 5
Physical Address: 5380

Logical Address: 1500
Page Number: 1
Offset: 476
Frame Number: 2
Physical Address: 2524

Logical Address: 3000
Page Number: 2
Offset: 952
Frame Number: 9
Physical Address: 10168

Logical Address: 5000
Page Number: 4
Offset: 904
Page Fault: Page 4 is not present in PAGE_TABLE.
```

### Task 7 — Segmentation Address Translation

```text
============================================================
Segmentation Address Translation
============================================================

Logical Address: (0, 150)
Base: 1000
Limit: 400
Physical Address: 1150

Logical Address: (1, 350)
Base: 2200
Limit: 300
Segmentation Fault: Offset 350 >= limit 300.

Logical Address: (2, 100)
Base: 500
Limit: 150
Physical Address: 600
```

### Part 1 Verification Summary

| Task | Result |
|---|---|
| Task 1  | PASS |
| Task 2 — FCFS, SJF, SRTF | PASS |
| Task 3 — Round Robin Q=3 and Q=6 | PASS |
| Task 4 — Priority with/without aging | PASS |
| Task 5 — Race condition + Peterson's Algorithm | PASS |
| Task 6 — Banker's Algorithm | PASS |
| Task 7 — Paging + Segmentation | PASS |
| Task 8 — Production algorithm justification | PASS |
