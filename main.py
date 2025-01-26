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
        print(f"The guess is: {new_guess}")
