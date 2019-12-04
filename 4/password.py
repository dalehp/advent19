def count_guesses(start_range: int, end_range: int) -> int:
    guesses = 0
    for num in range(start_range, end_range+1):
        if guess_valid(num):
            guesses += 1
    return guesses

def guess_valid(guess: int):
    code = str(guess)
    if len(code) != 6:
        return False
    group_len = 1
    double = False
    for i in range(len(code) - 1):
        if code[i] == code[i+1]:
            group_len += 1
        elif group_len == 2:
            double = True
        else:
            group_len = 1

        if code[i] > code[i+1]:
            return False
    if not double and group_len != 2:
        return False
    return True
        


if __name__ == "__main__":
    guesses = count_guesses(307237, 769058)
    print(f"Number of guesses: {guesses}")
