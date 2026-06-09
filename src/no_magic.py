# Built-in
from typing import List, Dict, Tuple, Set
from random import seed, shuffle
from heapq import heappush, heappop
from functools import reduce
from logging import Logger
from datetime import datetime
from math import log, ceil

logger = Logger("LibrARiaN")

# Constants
CONSECUTIVE_SECTIONS_DICT: Dict[int, Set[int]] = {
    0: {1, 2, 14, 15, 16, 17},
    1: {0, 2, 3, 14, 15, 16, 17},
    2: {0, 1, 3, 4, 5, 14, 15, 16, 17, 18, 19},
    3: {0, 1, 2, 4, 5, 14, 15, 16, 17, 18, 19},
    4: {2, 3, 5, 6, 7, 16, 17, 18, 19, 20, 21},
    5: {2, 3, 4, 6, 7, 16, 17, 18, 19, 20, 21},
    6: {4, 5, 7, 8, 9, 18, 19, 20, 21, 22, 23},
    7: {4, 5, 6, 8, 9, 18, 19, 20, 21, 22, 23},
    8: {6, 7, 9, 10, 11, 20, 21, 22, 23, 24, 25},
    9: {6, 7, 8, 10, 11, 20, 21, 22, 23, 24, 25},
    10: {8, 9, 11, 12, 13, 22, 23, 24, 25, 26},
    11: {8, 9, 10, 12, 13, 22, 23, 24, 25, 30},
    12: {10, 11, 13, 24, 25, 26, 27, 28, 29, 30},
    13: {10, 11, 12, 24, 25, 26, 27, 28, 29, 30},
    14: {0, 1, 2, 15, 16, 17},
    15: {0, 1, 2, 3, 14, 16, 17},
    16: {0, 1, 2, 3, 4, 5, 14, 15, 17, 18, 19},
    17: {0, 1, 2, 3, 4, 5, 14, 15, 16, 18, 19},
    18: {2, 3, 4, 5, 6, 7, 16, 17, 19, 20, 21},
    19: {2, 3, 4, 5, 6, 7, 16, 17, 18, 20, 21},
    20: {4, 5, 6, 7, 8, 9, 18, 19, 21, 22, 23},
    21: {4, 5, 6, 7, 8, 9, 18, 19, 20, 22, 23},
    22: {6, 7, 8, 9, 10, 11, 20, 21, 23, 24, 25},
    23: {6, 7, 8, 9, 10, 11, 20, 21, 22, 24, 25},
    24: {8, 9, 10, 11, 12, 13, 22, 23, 25, 26, 27, 28, 29, 30},
    25: {8, 9, 10, 11, 12, 13, 22, 23, 24, 26, 27, 28, 29, 30},
    26: {10, 12, 13, 24, 25, 27, 28, 29, 30},
    27: {10, 11, 12, 13, 24, 25, 26, 28, 29, 30},
    28: {10, 11, 12, 13, 24, 25, 26, 27, 29, 30},
    29: {10, 11, 12, 13, 24, 25, 26, 27, 28, 30},
    30: {10, 12, 13, 24, 25, 26, 27, 28, 29},
}
HAND_CAPACITY: int = 15

PICK_BOOK_S = 0.5
CONSECUTIVE_SERIES_TRAVEL_TIME_S = 3
FINAL_STORAGE_RANDOM_S = 10
FINAL_STORAGE_SAME_SERIES_S = 1

BITS_OF_VOLUME_NUM = 3
BITS_OF_VOLUME_SERIES = 4
TOTAL_OF_THEMES = len(CONSECUTIVE_SECTIONS_DICT)
TOTAL_OF_BOOKS: int = TOTAL_OF_THEMES * 2 ** (
    BITS_OF_VOLUME_SERIES + BITS_OF_VOLUME_NUM
)
BITS_OF_TOTAL_BOOKS = ceil(log(TOTAL_OF_BOOKS, 2))

SEED: int = 1


# Functions
def floor_books_init(seed_number: int) -> List[int]:
    seed(seed_number)
    logger.warning("Creating list of books...")
    floor_books = list(range(TOTAL_OF_BOOKS))
    logger.warning("Shuffling...")
    before_shuffle = datetime.now()
    shuffle(floor_books)
    logger.warning(f"Shuffling took {datetime.now() - before_shuffle}")
    return floor_books


def radix_once(
    buckets: int, bit_offset: int, books: List[int]
) -> Tuple[List[List[int]], float]:
    book_pile_list = [[] for i in range(buckets)]
    piling_seconds = 0
    hands = []
    current_section = 0
    while books:
        while len(hands) < HAND_CAPACITY and books:
            piling_seconds += PICK_BOOK_S
            heappush(hands, books.pop())
        logger.debug(f"Got {len(hands)} books.")
        while hands:
            book = heappop(hands)
            section = book >> bit_offset
            if current_section != section:
                piling_seconds += CONSECUTIVE_SERIES_TRAVEL_TIME_S
                next_section_options = CONSECUTIVE_SECTIONS_DICT[current_section]
                while section not in next_section_options:
                    piling_seconds += CONSECUTIVE_SERIES_TRAVEL_TIME_S
                    next_section_options |= reduce(
                        Set.union,
                        (
                            CONSECUTIVE_SECTIONS_DICT.get(next_section, set())
                            for next_section in next_section_options
                        ),
                    )

            book_pile_list[section].append(book)
            current_section = section
        logger.debug(f"Hands empty.")

    return (book_pile_list, piling_seconds)


# def queue_iter(queue: SimpleQueue):
#     while not queue:
#         yield queue.get()


def just_store_them(books: List[int]) -> float:
    piling_seconds = 0
    hands = []
    current_section = 0
    current_series = 0
    while books:
        while len(hands) < HAND_CAPACITY and books:
            piling_seconds += PICK_BOOK_S
            heappush(hands, books.pop())
        logger.debug(f"Got {len(hands)} books.")
        while hands:
            book = heappop(hands)
            section = book >> (BITS_OF_VOLUME_SERIES + BITS_OF_VOLUME_NUM)
            if current_section != section:
                piling_seconds += CONSECUTIVE_SERIES_TRAVEL_TIME_S
                next_section_options = CONSECUTIVE_SECTIONS_DICT[current_section]
                while section not in next_section_options:
                    piling_seconds += CONSECUTIVE_SERIES_TRAVEL_TIME_S
                    next_section_options |= reduce(
                        Set.union,
                        (
                            CONSECUTIVE_SECTIONS_DICT.get(next_section, set())
                            for next_section in next_section_options
                        ),
                    )
            series = book >> BITS_OF_VOLUME_NUM
            piling_seconds += (
                FINAL_STORAGE_SAME_SERIES_S
                if current_series == series
                else FINAL_STORAGE_RANDOM_S
            )
            current_series = series
        logger.debug(f"Hands empty.")
    return piling_seconds


# Main
def main():
    floor_books = floor_books_init(SEED)

    logger.error("Two radix")
    logger.warning("First radix")
    sorted_queues, recorded_time = radix_once(
        2, int(log(TOTAL_OF_BOOKS - 1, 2)), floor_books
    )
    print(f"{recorded_time=}s == {recorded_time/3600.0:.4f}h")

    for i, queue in enumerate(sorted_queues):
        logger.warning(f"Second radix, iter {i}")
        themed_book_queues, aux_recorded_time = radix_once(
            TOTAL_OF_THEMES, BITS_OF_VOLUME_SERIES + BITS_OF_VOLUME_NUM, queue
        )
        recorded_time += aux_recorded_time
        print(f"{recorded_time=}s == {recorded_time/3600.0:.4f}h")
        logger.warning("Fitting binned books...")
        while themed_book_queues:
            themed_books = themed_book_queues.pop()
            recorded_time += FINAL_STORAGE_RANDOM_S + FINAL_STORAGE_SAME_SERIES_S * len(
                themed_books
            )
            del themed_books
        print(f"{recorded_time=}s == {recorded_time/3600.0:.4f}h")

    floor_books = floor_books_init(SEED)

    sorted_queues, recorded_time = radix_once(
        TOTAL_OF_THEMES, BITS_OF_VOLUME_SERIES + BITS_OF_VOLUME_NUM, floor_books
    )
    print(f"{recorded_time=}s == {recorded_time/3600.0:.4f}h")
    logger.warning("Fitting binned books...")
    while sorted_queues:
        themed_books = sorted_queues.pop()
        recorded_time += FINAL_STORAGE_RANDOM_S + FINAL_STORAGE_SAME_SERIES_S * len(
            themed_books
        )
        del themed_books
    print(f"{recorded_time=}s == {recorded_time/3600.0:.4f}h")

    logger.error("Just store them.")
    recorded_time = just_store_them(floor_books_init(SEED))
    print(f"{recorded_time=}s == {recorded_time/3600.0:.4f}h")


if __name__ == "__main__":
    main()
