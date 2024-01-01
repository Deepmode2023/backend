

def count_sum_day(count_day: int, accumulator: int = 0):
    if count_day == 0:
        return accumulator if accumulator > 0 else 1

    next_count_day = count_day - 1
    return count_sum_day(next_count_day, accumulator + count_day)


def formula_spaced_repetition(last_repetition: int):
    return count_sum_day(last_repetition) + last_repetition
