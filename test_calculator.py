"""
    This file include tests functions to my program :
    - 6 simple syntax error
    - 15 simple equations
    - 20 complicated equations
    - gibberish expression
    - empty and white spaces equations
    Notice: that are more tests in test_extra.py file
"""

from calculator_main_omega import *
from errors import *


# simple syntax errors
def test_syntax_error_brackets():
    # expression with problem with brackets
    expression = '(1*1%3^2)+(2+8'
    result = main_evaluate(expression)
    assert result.error_type == BRACKETS_ERROR


def test_syntax_error_illegal_operators_neighbors():
    # expression with neighbors binary operators
    expression = '1%*6+5'
    result = main_evaluate(expression)
    assert result.error_type == SYNTAX_ORDER_ERROR


def test_opener_after_number():
    # there is not operator between 7(7!)
    expression = '45+7(7!)%-8.6'
    result = main_evaluate(expression)
    assert result.error_type == SYNTAX_ORDER_ERROR


def test_syntax_error_last_illegal_operator():
    # test to the use of binary operator in end of
    # expression
    expression = '4-4+(5.4*0)^'
    result = main_evaluate(expression)
    assert result.error_type == LAST_TOKEN_ERROR


def test_syntax_error_first_illegal_operator():
    # test to the use of binary operator in start of
    # expression
    expression = '/4*63$0$2'
    result = main_evaluate(expression)
    assert result.error_type == SYNTAX_ORDER_ERROR


def test_no_operator_after_post_unary():
    # after post unary operator have to be another post unary
    # or binary operator
    expression = '~2-1!4'
    result = main_evaluate(expression)
    assert result.error_type == SYNTAX_ORDER_ERROR


def test_no_num_after_pre_unary():
    # after post unary operator have to be another post unary
    # or binary operator
    expression = '~+6*6'
    result = main_evaluate(expression)
    assert result.error_type == SYNTAX_ORDER_ERROR


# 15 simple equations
def test_equation1():
    expression = '4+4*7.6'
    result = main_evaluate(expression)
    assert result == 34.4


def test_equation2():
    expression = '4+2^1*3!'
    result = main_evaluate(expression)
    assert result == 16


def test_equation3():
    expression = '4!-2*-4@2'
    result = main_evaluate(expression)
    assert result == 30


def test_equation4():
    expression = '4%3!+~3+12/1.5'
    result = main_evaluate(expression)
    assert result == 9


def test_equation5():
    expression = '-(~3^2 +4!  - - - (- -2  /--1))'
    result = main_evaluate(expression)
    assert result == -31


def test_equation6():
    expression = ' 4* 5@6$--4'
    result = main_evaluate(expression)
    assert result == 22


def test_equation7():
    expression = '--((9-6)/-2^2)&2'
    result = main_evaluate(expression)
    assert result == -0.75


def test_equation8():
    expression = ' -(1--8)   % ~(-3)+2 *2  '
    result = main_evaluate(expression)
    assert result == 4


def test_equation10():
    expression = '5$~2+(8/(-2)^2)!'
    result = main_evaluate(expression)
    assert result == 7


def test_equation11():
    expression = ' 8.5 + 4 - - 4*2^  \r  ( 2/-2 )'
    result = main_evaluate(expression)
    assert result == 14.5


def test_equation12():
    expression = '(4*2)*2/~~4'
    result = main_evaluate(expression)
    assert result == 4


def test_equation13():
    expression = '9*\n--(\n4+4)$5'
    result = main_evaluate(expression)
    assert result == 72


def test_equation14():
    expression = '27/3*4*4%3-(-2)'
    result = main_evaluate(expression)
    assert result == 38


def test_equation15():
    expression = '(~(80%60+6&(-0008)))'
    result = main_evaluate(expression)
    assert result == -12


def test_empty():
    # test to empty expression
    expression = ''
    result = main_evaluate(expression)
    assert result.error_type == EMPTY_EXPRESSION


def test_only_spaces():
    # test to whitespaces expression
    expression = '\r\r\t'
    result = main_evaluate(expression)
    assert result.error_type == EMPTY_EXPRESSION


def test_gibberish():
    expression = 'a<<b5%2+2}}.2sd'
    result = main_evaluate(expression)
    assert result.error_type == ILLEGAL_CHAR


# 20 complicated equation with at least 20 characters
# in every equation i use few operators and the math rules for many times
# it was very important to me the build equations with:
# negative, round, positive, floating point and big numbers results

def test_complicated_equation1():
    expression = '6!-41*(2+3%-3)+~5*~2-6@(9+1)'
    result = main_evaluate(expression)
    assert result == 640


def test_complicated_equation2():
    expression = '((1+1)!^2)*5$6+(21&-(1+4)^3)'
    result = main_evaluate(expression)
    assert result == -101


def test_complicated_equation3():
    expression = '005*2^2&2-7&88+224@26-(43-44+66&2----45*(321&2))'
    result = main_evaluate(expression)
    assert result == 47


def test_complicated_equation_big_answer():
    expression = '10000^2+500000+8&554445+4!-9696+(~--~3!!+90000@36000000)'
    result = main_evaluate(expression)
    assert result == 118536056.0


def test_complicated_equation5():
    expression = '----(8*--8)$5+2%456+9*9*~(6+6)+2^(-(1+1))'
    result = main_evaluate(expression)
    assert result == -905.75


def test_complicated_equation6():
    expression = '3^2^~~(4+1)+5---3+2$2^3+1+4*2'
    result = main_evaluate(expression)
    assert result == 59068


def test_complicated_equation7():
    expression = '(87^3%2&66@45%((22%4$2^2)+7*~(6!))^2 *6)+2*2'
    result = main_evaluate(expression)
    assert result == 4


def test_complicated_equation8():
    expression = '(-1--1-1-1-1)*--2-2*4/(4*2)+3.100+4!+-1'
    result = main_evaluate(expression)
    assert result == 19.1


def test_complicated_equation9():
    expression = '3!+--(---6&22%(2+6-5)^2-2&21$221@00)+51@2@3+(40/2)'
    result = main_evaluate(expression)
    assert result == -69.75


def test_complicated_equation10():
    expression = '(5^5+32.3*-30@10)+(-(-(-(-7*(2)!!))))+2200@-2000+15*5'
    result = main_evaluate(expression)
    assert result == 2668


def test_complicated_equation11():
    expr = '~(-(3^2.00+ ~~21+(400/  2^2+(3+ (5+6) *2)))+(5%2@5$20))/2^2@2'
    result = main_evaluate(expr)
    assert result == 37.5


def test_complicated_equation12():
    expression = '18-6^2+5%4$3+2+4+5+6-------9+7&5/3.2%4.2'
    result = main_evaluate(expression)
    assert result == -7.4375


def test_complicated_equation13():
    expression = '4*(-8--4+(2*3)+(-(((1+2)-4)^2))+5@10^4&--3)'
    result = main_evaluate(expression)
    assert result == 1691.5


def test_complicated_equation14():
    expression = '24%12^2-7*9&(2+3-4+6$22--8--~9+8!)+25&(--5!+2)/~~5+((3+3)%5)'
    result = main_evaluate(expression)
    assert result == -57


def test_complicated_equation15():
    expression = '5&6@(5*20/10)+~5^3+3$--4-4*(---(2+2)!)%5'
    result = main_evaluate(expression)
    assert result == -117.5


def test_complicated_equation16():
    expression = '5%2^4+((1+3^3!)+40$(2+5))+(-20/-4&~(-5))'
    result = main_evaluate(expression)
    assert result == 776


def test_complicated_equation_small_fraction():
    expression = '7&8*22^3!-7^3+((22%2 * 7)+3$5 ^3&~7)'
    result = main_evaluate(expression)
    assert result == 793658985.0000128


def test_complicated_equation18():
    expression = '((1+2)^((-1+-2)*-1)!+(3-1)!)$3^2'
    result = main_evaluate(expression)
    assert result == 534361


def test_complicated_equation19():
    expr = '-20000&-5^(~-3)+2000000+30.00+(50/2@8)'
    result = main_evaluate(expr)
    assert result == 2000165.0


def test_complicated_equation20():
    expr = '(140*2*(5%3))/((-5%2)+(9^(2*(5/(5.0))))+((100$--99)*2))*22000'
    result = main_evaluate(expr)
    assert result == 44000
