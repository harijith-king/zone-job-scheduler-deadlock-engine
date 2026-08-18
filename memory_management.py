"""
Task 7 — Paging and Segmentation Address Translator
Paging:
- Page size = 1024 bytes
- PAGE_TABLE maps page numbers to frame numbers.
"""

PAGE_SIZE = 1024
PAGE_TABLE = {
    0: 5,
    1: 2,
    2: 9,
    3: 1
}
# SEGMENTATION CONFIGURATION
# {segment: (base, limit)}
SEGMENT_TABLE = {
    0: (1000, 400),
    1: (2200, 300),
    2: (500, 150)
}
# PAGING TRANSLATOR
def translate_paged_address(logical_address):
    page_number = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE
    # Check whether the page exists in the page table.
    if page_number not in PAGE_TABLE:
        return (
            f"Page fault: page {page_number} is not present "
            f"in PAGE_TABLE."
        )
    frame_number = PAGE_TABLE[page_number]
    physical_address = (
        frame_number * PAGE_SIZE + offset
    )
    return (
        f"Logical address {logical_address}: "
        f"page={page_number}, offset={offset}, "
        f"frame={frame_number}, "
        f"physical address={physical_address}"
    )
# SEGMENTATION TRANSLATOR
def translate_segmented_address(segment, offset):
    # Check whether the segment exists.
    if segment not in SEGMENT_TABLE:
        return (
            f"Segmentation fault: segment {segment} "
            f"is not present in SEGMENT_TABLE."
        )
    base, limit = SEGMENT_TABLE[segment]
    # Check segment boundary.
    if offset >= limit:
        return (
            f"Segmentation fault: segment={segment}, "
            f"offset={offset} exceeds limit={limit}."
        )
    physical_address = base + offset
    return (
        f"Logical address ({segment}, {offset}): "
        f"base={base}, limit={limit}, "
        f"physical address={physical_address}"
    )
# ============================================================
# MAIN PROGRAM
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("TASK 7 — PAGING AND SEGMENTATION ADDRESS TRANSLATOR")
    print("=" * 65)
    print("\n" + "-" * 65)
    print("PAGING TRANSLATION")
    print("-" * 65)
    print(f"Page size: {PAGE_SIZE}")
    print(f"Page table: {PAGE_TABLE}")
    paged_addresses = [
        260,
        1500,
        3000,
        5000
    ]
    for address in paged_addresses:
        print(translate_paged_address(address))
    print("\n" + "-" * 65)
    print("SEGMENTATION TRANSLATION")
    print("-" * 65)
    print(f"Segment table: {SEGMENT_TABLE}")
    segmented_addresses = [
        (0, 150),
        (1, 350),
        (2, 100)
    ]
    for segment, offset in segmented_addresses:
        print(
            translate_segmented_address(
                segment,
                offset
            )
        )
