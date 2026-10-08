def check_adoption_cooldown(day_returned):
    if day_returned is None:
        return None
    if not isinstance(day_returned, int):
        raise TypeError("day_returned must be an integer.")
    if isinstance(day_returned, bool):
        raise TypeError("day_returned cannot be a boolean")
    if day_returned <= 0:
        raise ValueError("day_returned must be higher than 0")
        
    adoption_day = day_returned + 14
    return adoption_day

test_cases = [
    (1, 15),
    (5, 19),
    (10, 24),
    (100, 114)
]

for day_returned, expected in test_cases:
    result = check_adoption_cooldown(day_returned)
    assert result == expected, f"Day returned: {day_returned}| Expected is {expected} but is supposed to be {result}"

invalid_test_cases = [
    (0, ValueError),
    (-3, ValueError),
    (1.5, TypeError),
    ("Tuesday", TypeError),
    (True, TypeError),
    (False, TypeError)
]

for day_returned, expected_error in invalid_test_cases:
    try:
        check_adoption_cooldown(day_returned)
        assert False, f"Expected {expected_error.__name__} for {day_returned}, but no error was raised"
    except expected_error:
        pass