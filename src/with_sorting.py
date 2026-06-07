
# Built-in
from queue import SimpleQueue
from typing import List, Dict, Tuple, Set
from random import seed, shuffle
from heapq import heappush, heappop
from functools import reduce

# Constants
CONSECUTIVE_SECTIONS_DICT: Dict[int, Set[int]] = {
    0: {1, 2, 16, 18},
    1: {0, 3, 17, 19},
    2: {0, 3, 4, 16, 18, 20},
    3: {1, 2, 5, 17, 19, 21},
    4: {2, 5, 6, 18, 20, 22},
    5: {3, 4, 7, 19, 21, 23},
}
HAND_CAPACITY = 15

PICK_BOOK_S: int = 1
BETWEEN_CONSECUTIVE_S: int = 3 
FINAL_STORAGE_S: int = 5

BITS_OF_VOLUME_NUM = 1
BITS_OF_VOLUME_SERIES = 1
BITS_OF_THEME = 1
BITS_OF_FLOOR = 1
TOTAL_OF_BOOKS = 2**(BITS_OF_FLOOR + 
                     BITS_OF_THEME +
                     BITS_OF_VOLUME_SERIES +
                     BITS_OF_VOLUME_NUM)
TOTAL_OF_THEMES = 2**(BITS_OF_FLOOR + BITS_OF_THEME)

SEED = 1

# Functions
def floor_books_init(seed_number: int) -> SimpleQueue[int]:
    seed(seed_number)
    random_books = list(range(TOTAL_OF_BOOKS))
    shuffle(random_books)
    floor_books = SimpleQueue()
    for book in random_books:
        floor_books.put(book)
    del random_books
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
            
    return (book_pile_list, piling_seconds)


# Main
def main():
    floor_books = floor_books_init(SEED)
        
    sorted_queues, recorded_time = radix_once(TOTAL_OF_THEMES, BITS_OF_VOLUME_SERIES + BITS_OF_VOLUME_NUM, floor_books)
    for i, queue in enumerate(sorted_queues):
        aux_list = []
        while not queue.empty():
            aux_list.append(queue.get())
        print(i, aux_list)
    print(f"{recorded_time=}")

if __name__ == "__main__":
    main()