"""
Task 6 — Banker's Algorithm
Resource types:
R0 = Compute slots
R1 = Network channels
R2 = Storage buffers
"""

from copy import deepcopy
# ============================================================
# ORIGINAL SYSTEM STATE — DO NOT MODIFY
# ============================================================
AVAILABLE = [3, 3, 2]
MAX_NEED = {
    "P0": [7, 5, 3],
    "P1": [3, 2, 2],
    "P2": [9, 0, 2],
    "P3": [2, 2, 2],
}
ALLOCATION = {
    "P0": [0, 1, 0],
    "P1": [2, 0, 0],
    "P2": [3, 0, 2],
    "P3": [2, 1, 1],
}
PROCESSES = ["P0", "P1", "P2", "P3"]
# ============================================================
# COMPUTE NEED MATRIX
# ============================================================
def calculate_need(max_need, allocation):
    need = {}
    for process in PROCESSES:
        need[process] = [
            max_need[process][i] - allocation[process][i]
            for i in range(3)
        ]
    return need
  
# ============================================================
# SAFETY ALGORITHM
# ============================================================
def safety_algorithm(available, allocation, need):
    work = available.copy()
    finish = {
        process: False
        for process in PROCESSES
    }
    safe_sequence = []
    while len(safe_sequence) < len(PROCESSES):
        found_process = False
        for process in PROCESSES:
            if finish[process]:
                continue
            # A process can finish if its remaining Need
            # can be satisfied by the current Work vector.
            can_finish = all(
                need[process][i] <= work[i]
                for i in range(3)
            )
            if can_finish:
                # Simulate process completion and resource release.
                for i in range(3):
                    work[i] += allocation[process][i]
                finish[process] = True
                safe_sequence.append(process)
                found_process = True
        # No unfinished process can proceed.
        if not found_process:
            return False, []
    return True, safe_sequence
# ============================================================
# RESOURCE REQUEST ALGORITHM
# ============================================================
def evaluate_request(process, request):
    available = AVAILABLE.copy()
    allocation = deepcopy(ALLOCATION)
    need = calculate_need(MAX_NEED, allocation)
    print("\n" + "-" * 65)
    print(f"Evaluating request from {process}: {request}")
    print("-" * 65)
    print(f"Current Available: {available}")
    print(f"{process} Need       : {need[process]}")
  
    # Check 1 — Request must not exceed Need.
    if any(
        request[i] > need[process][i]
        for i in range(3)
    ):
        print("DENIED: Request exceeds the process's remaining Need.")
        return False
    print("Check 1: Request does not exceed Need.")
  
    # Check 2 — Request must not exceed Available.
    if any(
        request[i] > available[i]
        for i in range(3)
    ):
        print("DENIED: Request exceeds Available resources.")
        return False
    print("Check 2: Request does not exceed Available resources.")

    # Hypothetically grant the request.
    for i in range(3):
        available[i] -= request[i]
        allocation[process][i] += request[i]
        need[process][i] -= request[i]
    print("Hypothetical allocation performed.")
    print(f"New Available: {available}")

    # Check 3 — Resulting state must remain safe.
    safe, sequence = safety_algorithm(
        available,
        allocation,
        need
    )
    if safe:
        print("Safety check: SAFE.")
        print(f"Safe sequence after granting: {sequence}")
        print(f"RESULT: GRANT request from {process}.")
        return True
    print("Safety check: UNSAFE.")
    print(
        f"RESULT: DENY request from {process} because "
        "granting it would leave the system in an unsafe state."
    )
    return False

# ============================================================
# MAIN PROGRAM
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("TASK 6 — BANKER'S ALGORITHM")
    print("=" * 65)
    need = calculate_need(MAX_NEED, ALLOCATION)
    print("\nResource Types:")
    print("R0 = Compute slots")
    print("R1 = Network channels")
    print("R2 = Storage buffers")
    print("\nInitial Available:")
    print(AVAILABLE)
    print("\nNeed Matrix:")
    print(f"{'Process':<10}{'R0':<8}{'R1':<8}{'R2':<8}")
    print("-" * 34)

    for process in PROCESSES:
        print(
            f"{process:<10}"
            f"{need[process][0]:<8}"
            f"{need[process][1]:<8}"
            f"{need[process][2]:<8}"
        )
    safe, safe_sequence = safety_algorithm(
        AVAILABLE,
        ALLOCATION,
        need
    )

    print("\nInitial Safety Check:")
    print(f"Safe state: {'YES' if safe else 'NO'}")
    if safe:
        print(f"One valid safe sequence: {safe_sequence}")
    else:
        print("No safe sequence exists.")
    evaluate_request(
        "P1",
        [1, 0, 2]
    )
    evaluate_request(
        "P0",
        [2, 0, 2]
    )
    print("\n" + "=" * 65)
    print("REQUESTS WERE EVALUATED INDEPENDENTLY")
    print("=" * 65)
    print(
        "Each request started from the original Available, "
        "Allocation, and Need state."
    )
