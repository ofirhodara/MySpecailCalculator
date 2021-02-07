"""numbers_calc module:
This module is responsible of all the calculations
and the mathematical evaluation of expressions.
It includes, find the precedence list: build_precedence_list
Calculations functions: factorial, result_binary, result_unary
                        solve_binary, solve_unary
and math errors validations:
divide or mod in zero, factorial rules (can_factorial function)
"""


from errors import *
from input_output import *
from token_consts import *
from tokens import *


def factorial(num):
    """
    This function calculate the factorial of num
    :param int num: The number that i do the factorial on
                    round non negative number between [0-170]
    :return the factorial of this num, for example: 4! = (4*3*2*1)
    :rtype: float
    :raises OverFlow Exception if num > 170
            TypeError if num is not round
    """

    fact_result = 1
    for num_part in range(1, num + 1):
        fact_result = fact_result * num_part

    return float(fact_result)


def result_binary(left_num, right_num, op):
    """
    This function calculate the result of left_num op right_num
    :param float left_num: number left to the op
    :param float right_num: number right to the op
    :param str op: binary operator
    :return return the result of the expression left_num op right_num
    if the result is: Divide in zero (Nan) or complex number return ErrorCalc
    with the specific error type, else return the result
    :raise OverFlow exception if the result is too big/small to be stored
    """

    if op == '+':
        return left_num + right_num
    if op == '-':
        return left_num - right_num
    if op == '*':
        return left_num * right_num
    if op == '@':
        return (left_num + right_num) / 2
    if op == '$':
        return max(left_num, right_num)
    if op == '&':
        return min(left_num, right_num)
    if op == '^':
        return calc_pow(left_num, right_num)
    # op is '/' or '%'
    return calc_divide_mod(left_num, op, right_num)


def result_unary(op, num):
    """
    The function calculate the result of [num op]
    :param float num: num to do the operator on
    :param str op: unary operator str
    :return the result of the expression
             or ErrorCalc if tackle with math error
    """

    if op == '!':
        valid_fact = can_factorial(num)
        if valid_fact is True:
            return factorial(int(num))
        else:
            error_message = factorial_error(num)
            # build ErrorCalc with type of valid_fact
            return ErrorCalc(error_message, valid_fact)

    if op == '~':
        # for the '~' operator
        return -1 * num


def can_factorial(number):
    """
    This function check if we can do factorial on number
    :param float number: The number that i do the factorial on
    :return True if the operator '!' is legal on num else return str
             with the specific error type
    :rtype: bool or str
    """

    # check if the number is not negative and he is round
    if number >= 0 and number.is_integer():
        # my calculator do factorial only for numbers below 170
        # for avoid overflow Exception
        if number <= 170:
            return True
        else:
            return MEMORY_EXCEPTION
    return FACTORIAL_ERROR


def solve_binary(left_num, operator, right_num):
    """
    The function try to solve the expression [left_num op right_num]
    :param float left_num: the number left to the operator in the expression
    :param str operator: binary operator of the expression
    :param float right_num: the number right to the operator in the expression
    :return return the result of the expression [left_num op right_num]
             if tackled with Math Error/Memory Exception return ErrorCalc
    """
    is_too_big = False
    try:
        # calculate the binary expression
        result = result_binary(left_num, right_num, operator)
    except OverflowError:
        is_too_big = True

    # check if the result cause to OverFlow exception or +-Inf result
    # with some operators it give overflow and others give inf
    if is_too_big is True or is_inf(result) is True:
        # build expression str for print message to the user
        expression = str(left_num) + " " + str(operator) + " " + str(right_num)
        error_message = too_big_exception(expression)
        return ErrorCalc(error_message, MEMORY_EXCEPTION)
    return result


def solve_unary(number, operator):
    """
    The function try to solve the expression [number op]
    :param float number: the number to the operator on
    :param str operator: unary operator of the expression
    :return return the result of the expression [number op]
             if tackled with Math Error/Memory Exception return ErrorCalc
    """
    is_too_big = False
    try:
        result = result_unary(operator, number)
    except OverflowError:
        is_too_big = True

    if is_too_big is True or is_inf(result) is True:
        expression = "Number: " + str(number) + ", Operator:" + str(operator)
        error_message = too_big_exception(expression)
        return ErrorCalc(error_message, MEMORY_EXCEPTION)
    return result


def convert_str_to_number(num_str):
    """
    The function try to convert the str num_str to float
    :param str num_str: str represent number in math expression
    :return return float with num_str value
             if the number is too big/small to be stored in float
             return ErrorCalc with MEMORY_EXCEPTION error type
    """

    too_big_size = False

    try:
        float_num = float(num_str)
    except OverflowError:
        too_big_size = True

    if too_big_size is True or is_inf(float_num) is True:
        error_message = too_big_exception(num_str)
        return ErrorCalc(error_message, MEMORY_EXCEPTION)

    return float_num


def is_inf(number):
    """
    :param number: float number
    :return return True if the number is float
    with value of +/-inf else return False
    :rtype: bool
    """
    return number == float('inf') or number == float('-inf')


def build_precedence_list(tokens_list):
    """
    The function build list that include what operators
    precedences there is in the token list
    :param list tokens_list: math expression token list
    :return list including all the precedences of operators in
    the list in descending order without duplicates
    :rtype: list
    """

    precedences = []
    precedences_count = 0
    token_index = 0
    # while we get to the end of the list or
    # the precedences_count is equal to MAX_OPERATOR_GRADE:
    # that means that all the precedences is already in the list
    while token_index in range(0, len(tokens_list)) \
            and precedences_count < MAX_OPERATOR_GRADE:
        current_token = tokens_list[token_index]
        if isinstance(current_token, OperatorToken):
            op_precedence = OPERATORS_PRECEDENCE[current_token.value]
            # avoid duplicated in the precedences list
            if op_precedence not in precedences:
                precedences.append(op_precedence)
                precedences_count += 1
        token_index += 1

    # sort the precedences list because we need to solve
    # the highest precedences first
    precedences.sort(reverse=True)
    return precedences


def calc_pow(left_num, right_num):
    """
    the function calculate the expression left_num ^ right_num
    :param float left_num: the number left to the pow in the expression
    :param float right_num: the number right to the pow in the expression
    :return if the result of left_num ^ right_num is complex
    return ErrorCalc with COMPLEX_ERROR type
    else, return the result
    :raise OverFlow Exception when left_num ** right_num is too big/small
           to be stored
    """
    pow_result = left_num ** right_num
    if isinstance(pow_result, complex):
        # check if result of the calculation is complex number
        expr = str(left_num) + '^' + str(right_num)
        error_message = imaginary_number(expr, pow_result)
        return ErrorCalc(error_message, COMPLEX_ERROR)
    return pow_result


def calc_divide_mod(left_num, op, right_num):
    """
    the function calculate the expression left_num op right_num
    op can be '/' or '%'
    :param float left_num: the number left to the operator in the expression
    :param str op: '%' or '/'
    :param float right_num: the number right to the operator in the expression
    :return return the result if the expression
    left_num op right_num not include divide in zero
    else, return ErrorCalc with specific error Message and DIVIDE_ZERO type
    """
    if right_num == 0:
        # build inductive error message
        if op == '/':
            error_message = div_zero_error(left_num)
        else:
            error_message = mod_zero_error(left_num)
        return ErrorCalc(error_message, DIVIDE_ZERO)
    if op == '%':
        return left_num % right_num
    return left_num / right_num
