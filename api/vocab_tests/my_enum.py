from enum import Enum


class Test(str, Enum):
    spelling = "spelling"
    translate_ru = "translate_ru"
    reverse_translate_ru = "reverse_translate_ru"
