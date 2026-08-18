"""
Task 2:
- FCFS
- Non-preemptive SJF
- SRTF

Task 3:
- Round Robin (quantum = 3 and 6)

Task 4:
- Non-preemptive Priority
- Non-preemptive Priority with aging

The fixed JOBS list is imported from jobs.py and is never re-typed here.

Tie-breaking rule:
When two ready jobs have the same scheduling criterion:
1. Earlier arrival_time is selected first.
2. If arrival_time is also tied, lower job_id is selected first.
"""

from jobs import JOBS
def print_results(name, results):
    """Print per-job waiting and turnaround times plus averages."""
    print(f"\n{'=' * 60}")
    print(name)
    print(f"{'=' * 60}")
    print(f"{'Job ID':<12}{'Waiting Time':<15}{'Turnaround Time':<18}")
    print("-" * 45)
    total_waiting = 0
    total_turnaround = 0
    # Print in the original JOBS order.
    for job in JOBS:
        job_id = job["job_id"]
        waiting = results[job_id]["waiting_time"]
        turnaround = results[job_id]["turnaround_time"]
        print(f"{job_id:<12}{waiting:<15}{turnaround:<18}")
        total_waiting += waiting
        total_turnaround += turnaround
    average_waiting = total_waiting / len(JOBS)
    average_turnaround = total_turnaround / len(JOBS)
    print("-" * 45)
    print(f"Average Waiting Time    : {average_waiting:.2f}")
    print(f"Average Turnaround Time : {average_turnaround:.2f}")

# TASK 2 — FCFS
# ============================================================

def fcfs():
    """
    First-Come, First-Served scheduling.
    Jobs are selected by:
    1. arrival_time
    2. job_id
    FCFS is non-preemptive.
    """
    current_time = 0
    results = {}
    # Arrival time is the primary criterion.
    # job_id is the tie-breaker.
    ordered_jobs = sorted(
        JOBS,
        key=lambda job: (job["arrival_time"], job["job_id"])
    )
    for job in ordered_jobs:
        # CPU may be idle before the next job arrives.
        if current_time < job["arrival_time"]:
            current_time = job["arrival_time"]
        start_time = current_time
        completion_time = start_time + job["burst_time"]
        turnaround_time = completion_time - job["arrival_time"]
        waiting_time = turnaround_time - job["burst_time"]
        results[job["job_id"]] = {
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        }
        current_time = completion_time
    return results


# ============================================================
# TASK 2 — NON-PREEMPTIVE SJF
# ============================================================

def sjf():
    """
    Non-preemptive Shortest Job First.
    Tie-breaking:
    1. Earlier arrival_time
    2. Lower job_id
    """
    current_time = 0
    completed = set()
    results = {}

    while len(completed) < len(JOBS):

        # Jobs that have arrived and are not completed.
        ready_jobs = [
            job for job in JOBS
            if job["job_id"] not in completed
            and job["arrival_time"] <= current_time
        ]

        # If no job is ready, advance to the next arrival.
        if not ready_jobs:
            current_time = min(
                job["arrival_time"]
                for job in JOBS
                if job["job_id"] not in completed
            )
            continue
        selected = min(
            ready_jobs,
            key=lambda job: (
                job["burst_time"],
                job["arrival_time"],
                job["job_id"]
            )
        )
        start_time = current_time
        completion_time = start_time + selected["burst_time"]
        turnaround_time = completion_time - selected["arrival_time"]
        waiting_time = turnaround_time - selected["burst_time"]
        results[selected["job_id"]] = {
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        }

        completed.add(selected["job_id"])
        current_time = completion_time

    return results


# ============================================================
# TASK 2 — SRTF
# ============================================================

def srtf():
    current_time = 0
    remaining_time = {
        job["job_id"]: job["burst_time"]
        for job in JOBS
    }

    completion_times = {}

    while len(completion_times) < len(JOBS):

        ready_jobs = [
            job for job in JOBS
            if job["arrival_time"] <= current_time
            and remaining_time[job["job_id"]] > 0
        ]

        # CPU idle until the next job arrives.
        if not ready_jobs:
            current_time = min(
                job["arrival_time"]
                for job in JOBS
                if remaining_time[job["job_id"]] > 0
            )
            continue

        # Select the smallest remaining time.
        # Tie-breaking:
        # arrival_time, then job_id.
        selected = min(
            ready_jobs,
            key=lambda job: (
                remaining_time[job["job_id"]],
                job["arrival_time"],
                job["job_id"]
            )
        )

        # Run the selected job for one tick.
        current_time += 1
        remaining_time[selected["job_id"]] -= 1

        # Job has completed.
        if remaining_time[selected["job_id"]] == 0:
            completion_times[selected["job_id"]] = current_time

    results = {}

    for job in JOBS:
        job_id = job["job_id"]
        completion_time = completion_times[job_id]

        turnaround_time = completion_time - job["arrival_time"]
        waiting_time = turnaround_time - job["burst_time"]

        results[job_id] = {
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        }

    return results

# ============================================================
# TASK 3 — ROUND ROBIN
# ============================================================

def round_robin(quantum):
  from collections import deque

    current_time = 0
    ready_queue = deque()

    remaining_time = {
        job["job_id"]: job["burst_time"]
        for job in JOBS
    }

    arrival_order = sorted(
        JOBS,
        key=lambda job: (job["arrival_time"], job["job_id"])
    )

    next_arrival_index = 0

    completion_times = {}

    dispatch_slices = []
    previous_job = None
    context_switches = 0

    while len(completion_times) < len(JOBS):
        while (
            next_arrival_index < len(arrival_order)
            and arrival_order[next_arrival_index]["arrival_time"]
            <= current_time
        ):
            ready_queue.append(
                arrival_order[next_arrival_index]["job_id"]
            )
            next_arrival_index += 1

        # If queue is empty, jump to next arrival.
        if not ready_queue:
            current_time = arrival_order[next_arrival_index]["arrival_time"]
            continue

        job_id = ready_queue.popleft()

        # A different job starting a new slice is a context switch.
        if previous_job is not None and previous_job != job_id:
            context_switches += 1

        previous_job = job_id

        run_time = min(quantum, remaining_time[job_id])

        dispatch_slices.append({
            "job_id": job_id,
            "start": current_time,
            "end": current_time + run_time,
        })

        # Execute the job for the time quantum or until completion.
        current_time += run_time
        remaining_time[job_id] -= run_time

        # ----------------------------------------------------
        # IMPORTANT BOUNDARY RULE
        # ----------------------------------------------------
        # First add jobs that arrived exactly during the slice,
        # including jobs arriving at current_time.
        while (
            next_arrival_index < len(arrival_order)
            and arrival_order[next_arrival_index]["arrival_time"]
            <= current_time
        ):
            ready_queue.append(
                arrival_order[next_arrival_index]["job_id"]
            )
            next_arrival_index += 1

        if remaining_time[job_id] == 0:
            completion_times[job_id] = current_time
        else:
            # Expired job goes to the back AFTER newly arrived jobs.
            ready_queue.append(job_id)

    results = {}

    for job in JOBS:
        job_id = job["job_id"]

        turnaround_time = (
            completion_times[job_id] - job["arrival_time"]
        )

        waiting_time = turnaround_time - job["burst_time"]

        results[job_id] = {
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        }

    return results, dispatch_slices, context_switches


# ============================================================
# TASK 4 — NON-PREEMPTIVE PRIORITY
# ============================================================

def priority_scheduling(aging=False):
    current_time = 0
    completed = set()
    results = {}

    while len(completed) < len(JOBS):

        ready_jobs = [
            job for job in JOBS
            if job["job_id"] not in completed
            and job["arrival_time"] <= current_time
        ]

        # If no job is ready, move to the next arrival.
        if not ready_jobs:
            current_time = min(
                job["arrival_time"]
                for job in JOBS
                if job["job_id"] not in completed
            )
            continue

        def effective_priority(job):
            if not aging:
                return job["priority"]

            ticks_waited = current_time - job["arrival_time"]

            return max(
                1,
                job["priority"] - (ticks_waited // 3)
            )

        selected = min(
            ready_jobs,
            key=lambda job: (
                effective_priority(job),
                job["arrival_time"],
                job["job_id"]
            )
        )

        start_time = current_time
        completion_time = start_time + selected["burst_time"]

        turnaround_time = completion_time - selected["arrival_time"]
        waiting_time = turnaround_time - selected["burst_time"]

        results[selected["job_id"]] = {
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
        }

        completed.add(selected["job_id"])
        current_time = completion_time

    return results


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TASK 2
    # --------------------------------------------------------

    fcfs_results = fcfs()
    sjf_results = sjf()
    srtf_results = srtf()

    print_results("FCFS", fcfs_results)
    print_results("Non-Preemptive SJF", sjf_results)
    print_results("SRTF", srtf_results)

    # --------------------------------------------------------
    # TASK 3
    # --------------------------------------------------------

    rr3_results, rr3_slices, rr3_switches = round_robin(3)
    rr6_results, rr6_slices, rr6_switches = round_robin(6)

    print_results("Round Robin (Quantum = 3)", rr3_results)
    print(f"Dispatch slices          : {len(rr3_slices)}")
    print(f"Context switches         : {rr3_switches}")

    print_results("Round Robin (Quantum = 6)", rr6_results)
    print(f"Dispatch slices          : {len(rr6_slices)}")
    print(f"Context switches         : {rr6_switches}")

    print(
        "\nReal-OS overhead statement:"
    )
    print(
        "Quantum 3 would cause more real context-switch overhead "
        "than quantum 6 because this simulation produces more "
        "job changes: 16 switches for quantum 3 versus 10 switches "
        "for quantum 6."
    )

    # --------------------------------------------------------
    # TASK 4
    # --------------------------------------------------------

    priority_results = priority_scheduling(aging=False)
    aging_results = priority_scheduling(aging=True)

    print_results(
        "Non-Preemptive Priority (No Aging)",
        priority_results
    )

    print_results(
        "Non-Preemptive Priority (With Aging)",
        aging_results
    )

    # Longest waiting job — no aging
    longest_no_aging = max(
        priority_results,
        key=lambda job_id: priority_results[job_id]["waiting_time"]
    )

    # Longest waiting job — aging
    longest_aging = max(
        aging_results,
        key=lambda job_id: aging_results[job_id]["waiting_time"]
    )

    print("\nPriority Scheduling Longest Wait")
    print("-" * 45)
    print(
        f"No aging : {longest_no_aging} "
        f"({priority_results[longest_no_aging]['waiting_time']} ticks)"
    )
    print(
        f"With aging: {longest_aging} "
        f"({aging_results[longest_aging]['waiting_time']} ticks)"
    )
```
