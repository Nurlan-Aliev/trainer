from enum import Enum


class Test(str, Enum):
    constructor = "constructor"
    translate = "translate"
    rev_translate = "rev_translate"
