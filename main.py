import random
import requests
import re
from words import WORDS

# A pretty good start can be "soare".
DEFAULT_GUESS = "soare"
# DEFAULT_GUESS = random.choice(WORDS)
new_guess = list(DEFAULT_GUESS)
# Track letters that are present but not in the right spot
present_letters = {}
# Track letters that should not be included in future guesses
absent_letters = set()
# A flag to determine if we have the correct word
all_correct = False


def make_guess():
    """The make_guess function sends a request to the Wordle API and checks if the guess is correct."""
    global new_guess
    global present_letters
    global absent_letters
    global all_correct
    all_correct = True  # True at the start of each guess, update to False when a letter is 'present' or 'absent'

    # Define the url for sending requests to the Wordle API
    url = f"https://wordle.votee.dev:8000/daily?guess={''.join(new_guess)}"

    response = requests.get(url)

    if response.status_code == 200:  # If the response is 200
        results = response.json()
        # print(f"The guess is: {new_guess}")

        # Process each letter's feedback
        for result in results:
            letter_idx = result['slot']
            letter = result['guess']
            letter_result = result['result']
            print(f"Letter {letter} is {letter_result}")

            if letter_result == 'correct':
                new_guess[letter_idx] = letter  # Place the letter correctly
            elif letter_result == 'present':  # Letter is present but not in the correct slot
                if letter not in present_letters:
                    present_letters[letter] = set()
                # Add the current position to the set of positions to avoid in the future
                present_letters[letter].add(letter_idx)

                # Mark this slot as needing a new letter
                new_guess[letter_idx] = '_'

                all_correct = False  # Set to False if any letter is present

            elif letter_result == 'absent':  # Letter is completely absent in the correct word
                absent_letters.add(letter)
                # Also mark this slot as needing a new letter
                new_guess[letter_idx] = '_'
                all_correct = False  # Set to False if any letter is absent

    print(f"After checking, the new guess should be: {new_guess}")


def generate_pattern(new_guess, present_letters, absent_letters):
    pattern = ''
    for i, letter in enumerate(new_guess):
        if letter == '_':  # The letter is marked for updates
            # Exclude letters known to be absent globally and previously tried letters at this position
            excluded_letters = absent_letters.union(present_letters.get(letter, set()))
            pattern += f"[{''.join(set(alphabet) - excluded_letters)}]"
        else:
            pattern += letter
    return pattern


def fill_blanks_intelligently(temp_guess, present_letters, absent_letters):
    used_letters = set(temp_guess) - {'_'}


def refine_guess():
    """The refine_guess function will fill in the blanks in the new guess word, and then checks if it is a legit word."""
    global new_guess, present_letters, absent_letters, WORDS, alphabet
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    temp_guess = ['_'] * len(new_guess)

    # Generate patterns based on present and absent letters
    pattern = generate_pattern(new_guess, present_letters, absent_letters)

    # Attempt to find matching words
    matched_words = [word for word in WORDS if
                     re.match(pattern, word) and all(letter not in absent_letters for letter in word)]
    if matched_words:
        new_guess = list(random.choice(matched_words))  # Choose one of the matching words

    else:
        # If no matching words, fill with a heuristic approach or random valid letters
        fill_blanks_intelligently(temp_guess, present_letters, absent_letters)
