import random

def play_guessing_game(user_input):
    correct = random.randint(1, 5)
    try:
        guess = int(user_input)
        return guess == correct, correct
    except ValueError:
        return False, correct
