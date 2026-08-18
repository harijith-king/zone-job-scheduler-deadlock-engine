# zone-job-scheduler-deadlock-engine

## Production Scheduling Choice

Based on the results I got from Tasks 2–4, I would choose the SJF/SRTF family, specifically SRTF, for the zone-controller jobs. SRTF gave the best overall performance in my testing, with an average waiting time of 11.50 ticks and an average turnaround time of 17.00 ticks. These were the lowest values among the scheduling algorithms I tested.

The other three scheduling families are less suitable for this workload:

1. **FCFS:** FCFS had an average waiting time of 17.12 ticks and an average turnaround time of 22.62 ticks. Both values are higher than SRTF, so jobs would generally have to wait longer before completing.
2. **Round Robin:** With a quantum of 3, Round Robin produced 16 context switches, while a quantum of 6 produced 10 context switches. The quantum-6 version still had an average waiting time of 20.38 ticks, which is much higher than SRTF's 11.50 ticks. This makes Round Robin less suitable for this workload.
3. **Priority Scheduling:** Priority scheduling without aging had an average waiting time of 14.12 ticks, while priority scheduling with aging had 17.12 ticks. In the no-aging case, Z3-J02 waited for 33 ticks, which shows that some lower-priority jobs can experience a long wait.

Therefore, I would use SRTF in production for these zone-controller jobs because it provided the lowest average waiting time and turnaround time in my measured results.
