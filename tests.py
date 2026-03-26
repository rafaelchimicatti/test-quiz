import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

from model import Question


def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    assert len(question.choices) == 2
    assert question.choices[0].id == 1
    assert question.choices[1].id == 2


def test_remove_choice_by_id():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')

    question.remove_choice_by_id(c1.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == c2.id


def test_remove_choice_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert len(question.choices) == 0


def test_set_correct_choices():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')

    question.set_correct_choices([c1.id])

    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct


def test_set_correct_choices_invalid_id():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.set_correct_choices([999])


def test_correct_selected_choices_valid():
    question = Question(title='q1')
    c1 = question.add_choice('a', True)

    result = question.correct_selected_choices([c1.id])

    assert result == [c1.id]


def test_correct_selected_choices_exceeds_limit():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', True)

    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])


def test_choice_text_validation():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('')

    with pytest.raises(Exception):
        question.add_choice('a' * 101)


def test_points_out_of_range():
    with pytest.raises(Exception):
        Question(title='q1', points=0)

    with pytest.raises(Exception):
        Question(title='q1', points=101)