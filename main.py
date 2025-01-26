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

all_correct = False

