from random import sample, shuffle

from api.models import WordsToLearn, Word
from api.vocab_tests.custom_enum import Test
from api.vocab_tests.schemas import TranslateSchemas


def remove_item(item_list, my_item):
    return [item for item in item_list if item != my_item]


def question(word: Word, test: Test):
    if test == Test.translate.value:
        return {'word_en': word.word_en}
    else:
        return {'word_ru': word.word_ru, 'word_az': word.word_az}


def answer(word: Word, test: Test):
    if test == Test.translate.value:
        return {'word_ru': word.word_ru, 'word_az': word.word_az}
    else:
        return {'word_en': word.word_en}


def crete_question_and_options(
    first: list[WordsToLearn], second: list[Word], test: Test
):

    second = [question(word, test) for word in second]
    result = []
    for word in first:
        available = remove_item(second, question(word.word, test))
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
