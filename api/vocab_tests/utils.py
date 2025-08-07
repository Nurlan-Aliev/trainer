from random import sample, shuffle
from api.vocab_tests.schemas import TranslateSchemas


def crete_question_and_options(first: list, second: list):
    result = []

    for word in first:

        random_choices = sample(second, 3)
        new_list = [word.word.word] + random_choices
        shuffle(new_list)
        new_question = TranslateSchemas(
            word_id=word.word_id,
            word_ru=word.word.translate_ru,
            options=new_list,
        )
        result.append(new_question)
    return result
