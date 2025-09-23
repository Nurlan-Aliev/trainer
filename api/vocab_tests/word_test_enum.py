from enum import Enum


class Test(str, Enum):
    spelling = "spelling"
    translate = "translate"
    reverse_translate = "reverse_translate"
