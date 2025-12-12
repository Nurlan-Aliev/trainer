from enum import Enum


class Test(str, Enum):
    constructor = "constructor"
    translate = "translate"
    rev_translate = "rev_translate"


class Language(str, Enum):
    word_ru = 'word_ru'
    word_az = 'word_az'
