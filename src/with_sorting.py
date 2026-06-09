
# Built-in
from queue import SimpleQueue
from typing import List, Dict, Tuple, Set
from random import seed, shuffle
from heapq import heappush, heappop
from functools import reduce
from logging import Logger
from datetime import datetime

logger = Logger("LibrARiaN")

# Constants
CONSECUTIVE_SECTIONS_DICT: Dict[int, Set[int]] = {
    0: {1, 2, 14, 15, 16, 17},
    1: {0, 2, 3, 14, 15, 16, 17},
    2: {0, 1, 3, 4, 5, 14, 15, 16, 17, 18, 19},
    3: {0, 1, 2, 4, 5, 14, 15, 16, 17, 18, 19},
    4: {2, 3, 5, 6, 7, 16, 17, 18, 19, 20, 21},
    5: {2, 3, 4, 6, 7, 16, 17, 18, 19, 20, 21},
    6: {4,5,7,8,9,18,19,20,21,22,23},
    7: {4,5,6,8,9,18,19,20,21,22,23},
    8: {6,7,9,10,11,20,21,22,23,24,25},
    9: {6,7,8,10,11,20,21,22,23,24,25},
    10: {8,9,11,12,13,22,23,24,25,26},
    11: {8,9,10,12,13,22,23,24,25,30},
    12: {10,11,13,24,25,26,27,28,29,30},
    13: {10,11,12,24,25,26,27,28,29,30},
    14: {0, 1, 2, 15, 16, 17},
    15: {0, 1, 2, 3, 14, 16, 17},
    16: {0, 1, 2, 3, 4, 5, 14, 15, 17, 18, 19},
    17: {0, 1, 2, 3, 4, 5, 14, 15, 16, 18, 19},
    18: {2, 3, 4, 5, 6, 7, 16, 17, 19, 20, 21},
    19: {2, 3, 4, 5, 6, 7, 16, 17, 18, 20, 21},
    20: {4,5,6,7,8,9,18,19,21,22,23},
    21: {4,5,6,7,8,9,18,19,20,22,23},
    22: {6,7,8,9,10,11,20,21,23,24,25},
    23: {6,7,8,9,10,11,20,21,22,24,25},
    24: {8,9,10,11,12,13,22,23,25,26,27,28,29,30},
    25: {8,9,10,11,12,13,22,23,24,26,27,28,29,30},
    26: {10,12,13,24,25,27,28,29,30},
    27: {10,11,12,13,24,25,26,28,29,30},
    28: {10,11,12,13,24,25,26,27,29,30},
    29: {10,11,12,13,24,25,26,27,28,30},
    30: {10,12,13,24,25,26,27,28,29},
}
HAND_CAPACITY = 15

PICK_BOOK_S: int = 1
BETWEEN_CONSECUTIVE_S: int = 3
FINAL_STORAGE_S: int = 1

BITS_OF_VOLUME_NUM = 3
BITS_OF_VOLUME_SERIES = 7
TOTAL_OF_THEMES = len(CONSECUTIVE_SECTIONS_DICT)
TOTAL_OF_BOOKS = TOTAL_OF_THEMES * 2**(BITS_OF_VOLUME_SERIES +
                                       BITS_OF_VOLUME_NUM)

SEED = 1

# Functions
def floor_books_init(seed_number: int) -> SimpleQueue[int]:
    seed(seed_number)
    logger.warning("Creating list of books")
    random_books = list(range(TOTAL_OF_BOOKS))
    logger.warning("Shuffling...")
    before_shuffle = datetime.now()
    shuffle(random_books)
    logger.warning(f"Shuffling took {datetime.now() - before_shuffle}")
    logger.warning("Flooring books...")
    floor_books = SimpleQueue()
    before_flooring = datetime.now()
    for book in random_books:
        floor_books.put(book)
    del random_books
    logger.warning(f"Flooring took {datetime.now() - before_flooring}")
    return floor_books

def radix_once(buckets: int, bit_offset: int, books: SimpleQueue[int]) -> Tuple[List[SimpleQueue[int]], int]:
    book_pile_list = [SimpleQueue() for _ in range(buckets)]
    piling_seconds = 0
    hands = []
    current_section = 0
    while not books.empty():
        while len(hands) < 15 and not books.empty():
            piling_seconds += PICK_BOOK_S
            heappush(hands, books.get())
        logger.debug(f"Got {len(hands)} books.")
        while hands:
            book = heappop(hands)
            section = ((TOTAL_OF_BOOKS - 2**bit_offset) & book) >> bit_offset
            if current_section != section:
                piling_seconds += BETWEEN_CONSECUTIVE_S
                next_section_options = CONSECUTIVE_SECTIONS_DICT[current_section]
                while section not in next_section_options:
                    piling_seconds += BETWEEN_CONSECUTIVE_S
                    next_section_options |= reduce(Set.union, (CONSECUTIVE_SECTIONS_DICT.get(next_section, set()) 
                                                                for next_section in next_section_options))

            book_pile_list[section].put(book)
        logger.debug(f"Hands empty.")
            
    return (book_pile_list, piling_seconds)

def queue_iter(queue: SimpleQueue):
    while not queue.empty():
        yield queue.get()

# Main
def main():
    floor_books = floor_books_init(SEED)
        
    sorted_queues, recorded_time = radix_once(2, 14, floor_books)
    print(f"{recorded_time=}s == {recorded_time/3600.0}h")
    
    for queue in sorted_queues:
        print(queue)
        more_sorted_queues, aux_recorded_time = radix_once(TOTAL_OF_BOOKS, BITS_OF_VOLUME_SERIES + BITS_OF_VOLUME_NUM, queue)
        recorded_time += aux_recorded_time
        print(f"{recorded_time=}s == {recorded_time/3600.0}h")

if __name__ == "__main__":
    main()