"""
    test_extra.py:
    In this file i wrote extra tests to my calculator program.
    Divided to some main parts:
    - Math Errors Tests (divide in zero, factorial, complex numbers)
    - Test with edge cases of minus (operator / sign)
    - Big results tests: expression that their result
                         will be inf or cause overflow exception
    - test spaces in expressions
    - test to the tokens_validation.py functions:
      valid brackets, unnecessary parentheses, last token validation
    - Decimal point place in expressions
    - pre and post unary operations
"""

from calculator_main_omega import *
from errors import *


# Math Errors Tests

def test_divide_in_zero_from_start():
    # test divide in zero in case that
    # we can see before solving
    expression = '56/0'
    result = main_evaluate(expression)
    assert result.error_type == DIVIDE_ZERO


def test_divide_in_zero_while_solve():
    # test divide in zero in case that
    # we can't see before solving
    expression = '56/(5-5)'
    result = main_evaluate(expression)
    assert result.error_type == DIVIDE_ZERO


def test_mod_in_zero():
    expression = '-3%0'
    result = main_evaluate(expression)
    # this result need to be none because we mod in zero
    assert result.error_type == DIVIDE_ZERO


def test_complex_number():
    expression = '(-7)^0.5'
    result = main_evaluate(expression)
    # check if get COMPLEX_ERROR when get complex result
    assert result.error_type == COMPLEX_ERROR


def test_factorial_negative():
    expression = '(-9)!'
    result = main_evaluate(expression)
    # the factorial operation on negative numbers is not legal
    assert result.error_type == FACTORIAL_ERROR


def test_factorial_not_round():
    expression = '2.404!+34'
    result = main_evaluate(expression)
    # the factorial operation on fraction numbers is not legal
    assert result.error_type == FACTORIAL_ERROR


def test_factorial_huge_number():
    expression = '600000!+4'
    result = main_evaluate(expression)
    assert result.error_type == MEMORY_EXCEPTION


# Minus tests:

def test_minus_start():
    # build expression that have '-' in the start
    expression = '-2^3'
    result = main_evaluate(expression)
    assert result == -8


def test_minus_after_binary():
    # test expression with minus after binary operator
    expression = '5*-2'
    result = main_evaluate(expression)
    assert result == -10


def test_minuses_row():
    # test expression with some minuses right after each other
    expression = '---(4+2)+8----8'
    result = main_evaluate(expression)
    assert result == 10


def test_huge_equation():
    expression = ('1+' * 10000) + '0'
    # i build expression with 10000 operators
    # i test this affect on my program
    result = main_evaluate(expression)
    assert result == 10000


def test_max_size_expression():
    # build expression with size bigger then the
    # MAX_EXPRESSION_SIZE
    expression = '5' * (MAX_EXPRESSION_SIZE + 1)
    result = main_evaluate(expression)
    assert result.error_type == MEMORY_EXCEPTION


# Big results tests:

def test_pow_overflow():
    expression = '225^225.6'
    result = main_evaluate(expression)
    assert result.error_type == MEMORY_EXCEPTION


def test_multiply_overflow():
    expression = '170!*444444'
    result = main_evaluate(expression)
    # the result of this expression is too big to store in float
    assert result.error_type == MEMORY_EXCEPTION


def test_minus_inf_number():
    expression = '-67675765675675675675897333333333' \
                 '09876767565656756745345543333335' \
                 '67567563453423423423436546333337' \
                 '47646767567576575675756756733335' \
                 '76578867864564534535423423413533' \
                 '32523523525235235235235352352433' \
                 '12412413523523535235241241241231' \
                 '24124421874126512561275126571323' \
                 '52352353523524124124121241244218' \
                 '52352353523524124124121241244218' \
                 '52352353523524124124121241244218' \
                 '52352353523524124124121241244218'\

    result = main_evaluate(expression)
    # python store it in float('inf'),
    # i test here if my program handle with that
    assert result.error_type == MEMORY_EXCEPTION


def test_plus_inf_number():
    expression = '67675765675675675675897333333333' \
                 '09876767565656756745345543333335' \
                 '67567563453423423423436546333337' \
                 '47646767567576575675756756733335' \
                 '76578867864564534535423423413533' \
                 '32523523525235235235235352352433' \
                 '12412413523523535235241241241231' \
                 '24124421874126512561275126571323' \
                 '52352353523524124124121241244218' \
                 '52352353523524124124121241244218' \
                 '52352353523524124124121241244218' \
                 '52352353523524124124121241244218'\

    result = main_evaluate(expression)
    # python store it in float('inf'),
    # i test here if my program handle with that
    assert result.error_type == MEMORY_EXCEPTION


# Space Test:

def test_space_inside_number():
    # we have illegal space inside the number '47'
    # in the real interpreter in python space inside
    # a expression is invalid syntax
    expression = '5*1^4+4  7+5'
    result = main_evaluate(expression)
    assert result.error_type == SPACE_IN_NUMBER


# Expression validations tests:
# Test to the validations that i do to
# expression before building the token list


def test_illegal_char_validation():
    expr = '454#f'
    validate = math_validations(expr)
    assert validate.error_type == ILLEGAL_CHAR


def test_unnecessary_brackets_validation():
    expr = '3^((4+4))'
    validate = math_validations(expr)
    # the double brackets around simple expression like: 4+4
    # is not legal do check if my calculator recognize it before solving
    assert validate.error_type == UNNECESSARY_PARENTHESES


def test_only_number_in_brackets():
    expr = '(6)'
    validate = math_validations(expr)
    # test only number in brackets
    assert validate is True


def test_opener_has_no_closer():
    expr = '((65+6)/6+(4+8/3'
    validate = math_validations(expr)
    # error that say the one of the opener '(' has no ')'
    assert validate.error_type == BRACKETS_ERROR


def test_closer_has_no_opener():
    expr = '(4+5)+9)+25^4'
    validate = math_validations(expr)
    # error that say the one of the closer ')' has no '(' matched
    assert validate.error_type == BRACKETS_ERROR


def test_last_token_pre_unary():
    expr = '4!+~'
    validate = math_validations(expr)
    assert validate.error_type == LAST_TOKEN_ERROR


def test_last_token_binary_operator():
    expr = '4!+'
    validate = math_validations(expr)
    assert validate.error_type == LAST_TOKEN_ERROR


# Test to the use of decimal point in expression

def test_double_dot_validation():
    expr = '4!+7..7'
    validate = math_validations(expr)
    # dot can't be after dot, because of that the specific error
    # will be 'dot after error'
    assert validate.error_type == DOT_ERROR


def test_first_dot_validation():
    expr = '.5+45*(65/7)'
    validate = math_validations(expr)
    # dot can't be the first char in expression
    assert validate.error_type == DOT_ERROR


def test_dot_after_operator_validation():
    expr = '45+.5'
    validate = math_validations(expr)
    # dot can't be after operator
    assert validate.error_type == DOT_ERROR


def test_valid_dot():
    expr = '45+0.5'
    result = main_evaluate(expr)
    assert result == 45.5


def test_no_fraction_after_dot():
    expr = '8.*2'
    # i decided to support expressions
    # like that like the real python interpreter
    result = main_evaluate(expr)
    assert result == 16


# Pre Unary Tests:
def test_tilda_before_minus():
    expr = '~~-(70)'
    result = main_evaluate(expr)
    assert result == -70


def test_pre_unary_in_a_row():
    expr = '~~~2'
    result = main_evaluate(expr)
    assert result == -2


def test_pre_unary_with_minuses():
    expr = '~-~--~-10'
    result = main_evaluate(expr)
    assert result == -10


# Post Unary Tests:
def test_post_unary_in_a_row():
    expr = '3!!+4'
    result = main_evaluate(expr)
    assert result == 724


def test_post_unary_on_brackets():
    expr = '(1+5&8$3)!+4'
    result = main_evaluate(expr)
    assert result == 724
