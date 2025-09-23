from random import sample, shuffle

from api.models import WordsToLearn, Word
from api.vocab_tests.word_test_enum import Test
from api.vocab_tests.schemas import TranslateSchemas


def question(word: Word, test: Test):
    if test == Test.translate.value:
        return word.word_en
    else:
        return word.word_ru


def answer(word: Word, test: Test):
    if test == Test.translate.value:
        return word.word_ru
    else:
        return word.word_en


def crete_question_and_options(
    first: list[WordsToLearn], second: list[Word], test: Test
):

    second = [question(word, test) for word in second]
    result = []

    for word in first:
        available = list(set(second) - {question(word.word, test)})
        random_choices = sample(available, 3)
        new_list = [question(word.word, test)] + random_choices
        shuffle(new_list)
        new_question = TranslateSchemas(
            word_id=word.word_id,
            question=answer(word.word, test),
            options=new_list,
        )
        result.append(new_question)
    return result
