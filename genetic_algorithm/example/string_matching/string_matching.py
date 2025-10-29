import random

SEARCHED_TEXT = "Ana are mere"
CHROMOSOME_LENGTH = len(SEARCHED_TEXT)

def create_string_individual() -> list[chr]:
    return [random.randint(0, 0x10ffff) for _ in range(CHROMOSOME_LENGTH)]

