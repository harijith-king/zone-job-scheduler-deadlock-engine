"""
Task 5 — Race Condition and Peterson's Algorithm
"""
import threading
import time
# ============================================================
# UNSYNCHRONIZED RACE CONDITION
# ============================================================
def run_without_synchronization():
    counter = [100]
    def consume_credits():
        # Read the shared value.
        value = counter[0]
        time.sleep(0.01)
        counter[0] = value - 40
    def reimburse_credits():
        # Read the shared value.
        value = counter[0]
        time.sleep(0.01)
        counter[0] = value + 25
    thread_1 = threading.Thread(target=consume_credits)
    thread_2 = threading.Thread(target=reimburse_credits)
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()
    return counter[0]

# ============================================================
# PETERSON'S ALGORITHM
# ============================================================

def run_with_peterson():
    counter = [100]
    # Standard Peterson shared variables.
    flag = [False, False]
    turn = 0
    def enter_critical_section(thread_id):
        other = 1 - thread_id
        flag[thread_id] = True
        turn = other
        while flag[other] and turn == other:
            pass
    def leave_critical_section(thread_id):
        flag[thread_id] = False
    def consume_credits():
        thread_id = 0
        enter_critical_section(thread_id)
        try:
            # Critical section:
            # read -> modify -> write must happen together.
            value = counter[0]
            time.sleep(0.01)
            counter[0] = value - 40
        finally:
            leave_critical_section(thread_id)
    def reimburse_credits():
        thread_id = 1
        enter_critical_section(thread_id)
        try:
            # Critical section:
            # read -> modify -> write must happen together.
            value = counter[0]
            time.sleep(0.01)
            counter[0] = value + 25
        finally:
            leave_critical_section(thread_id)
    thread_1 = threading.Thread(target=consume_credits)
    thread_2 = threading.Thread(target=reimburse_credits)
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()
    return counter[0]

# ============================================================
# MAIN PROGRAM
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("TASK 5 — RACE CONDITION AND PETERSON'S ALGORITHM")
    print("=" * 65)
    print("\nInitial Zone-B compute-credit counter: 100")
    print("Thread 0: subtract 40")
    print("Thread 1: add 25")
    print("Correct final value: 85")

    # --------------------------------------------------------
    # UNSYNCHRONIZED RUNS
    # --------------------------------------------------------

    print("\n" + "-" * 65)
    print("WITHOUT SYNCHRONIZATION")
    print("-" * 65)
    unsynchronized_results = []
    for run in range(1, 6):
        final_value = run_without_synchronization()
        unsynchronized_results.append(final_value)
        print(
            f"Run {run}: final counter = {final_value}"
        )

    # Check whether the race condition was observable.
    race_observed = any(
        value != 85
        for value in unsynchronized_results
    )
    print(
        f"\nRace condition observed: "
        f"{'YES' if race_observed else 'NO'}"
    )
    # --------------------------------------------------------
    # PETERSON'S ALGORITHM RUNS
    # --------------------------------------------------------
    print("\n" + "-" * 65)
    print("WITH PETERSON'S ALGORITHM")
    print("-" * 65)
    peterson_results = []
    for run in range(1, 6):
        final_value = run_with_peterson()
        peterson_results.append(final_value)
        print(
            f"Run {run}: final counter = {final_value}"
        )
    # Check whether all protected runs produced the correct value.
    all_correct = all(
        value == 85
        for value in peterson_results
    )
    print(
        f"\nAll Peterson runs produced 85: "
        f"{'YES' if all_correct else 'NO'}"
    )
    # --------------------------------------------------------
    # FINAL VERIFICATION
    # --------------------------------------------------------
    print("\n" + "=" * 65)
    print("TASK 5 VERIFICATION")
    print("=" * 65)
    print(
        f"Unsynchronized results: {unsynchronized_results}"
    )
    print(
        f"Peterson results       : {peterson_results}"
    )
    if race_observed and all_correct:
        print(
            "\nPASS: The unsynchronized version demonstrates "
            "the race condition, while Peterson's Algorithm "
            "consistently produces the correct final value of 85."
        )
    else:
        print(
            "\nCHECK: Repeat the experiment if the required "
            "race-condition behavior was not observed."
        )
