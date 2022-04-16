#List to string is a scipt that pastes in a list from the clipboard and converts
#it to an actual string.

import pyperclip

text = pyperclip.paste()

def convert_text(text):
    return " ".join(text.split())

pyperclip.copy(convert_text(text))        # Copy the joined list back to the clipboard



# Test script

import pytest

from list_to_string import convert_text

def test_convert_text():
    assert convert_text("""julian
                        bob
                        homies""") == 'julian bob homies'
