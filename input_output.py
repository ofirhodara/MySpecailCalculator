"""input_output module:
In this file i handle the input and output of the program.
Output:
    in order to give the user the most inductive messages
    i build function that build specific
    str error message about the any error
    and return the message in order to print it to the user
Input:
    calculator_input function is responsible for all the
    input from the user in my the program.
"""

from token_consts import *


def illegal_char(index_illegal, char_illegal):
    """
    build error message to that the character
    in index_illegal of the expression is illegal
    :param int index_illegal: the index of the illegal char
    :param str char_illegal: the illegal char in the expression
    :return illegal char error message
    :rtype str
    """
    error_message = "This char: " + str(char_illegal)
    error_message += "\nin index: " + str(index_illegal)
    error_message += "\nis not valid in my interpreter!"
    return error_message


def space_inside_number(left_tok, right_tok):
    """
    build error message to the user about illegal space in expression
    because he inside a number for example : '6 6+6'
    :param str left_tok: the char left to the illegal space in expression
    :param str right_tok: the char right to the illegal space in expression
    :return space inside number error message
    :rtype str
    """
    error_message = "You can't have space inside a number:\n"
    error_message += "between:" + str(left_tok) + " and " + str(right_tok)
    error_message += "\nThe same Syntax error examples:\n"
    error_message += "45 + 4 5 or 5.55 + 2"
    return error_message


def factorial_error(error_num):
    """
    build error message to the user about number that can't do factorial on
    :param error_num: The illegal number to do factorial on
    :return factorial error error message
    :rtype str
    """
    error_message = "You can't do factorial to: " + str(error_num) + "\n"
    if error_num < 0:
        error_message += "This is negative number"
    elif error_num > 170:
        error_message += "this number is higher than the max number\n"
        error_message += "i do factorial On: 170"
    else:
        error_message += "the number is not round"

    return error_message


def div_zero_error(num):
    """
    build error message to the user that he can't divide
    num in zero
    :param float num: the number that cause to divide in zero
                      for example 7 in expression: 7/0
    :return divide in zero error message
    :rtype str
    """
    return "You can't DIV " + str(num) + " in zero"


def mod_zero_error(num):
    """
    build error message to the user that he can't mod
    num in zero
    :param float num: the number that cause to mod in zero
                      for example 7 in expression: 7%0
    :return mod in zero error message
    :rtype str
    """
    return "You can't MOD " + str(num) + " in zero"


def error_extra_brackets():
    """
    :return unnecessary Brackets error message
    :rtype str
    """
    error_message = "There is unnecessary Brackets in the expression!\n"
    error_message += "Another example for this Error is: ((44*3))+5 "
    return error_message


def too_big_exception(expression):
    """
    build error message
    that say that the result of expression is too big/small
    to the calculator.
    the result of it is inf or cause overflow.
    :param str expression: math expression cause to the error
    :return memory exception error message
    :rtype str
    """
    error_message = "I can't Store the result of:\n"
    error_message += str(expression)
    return error_message


def calculator_input():
    """
    The function get input from the user.
    :return The input.
             if error caused while get the input return None.
    """
    try:
        expression = input()
    except Exception:
        # i read that this can be EOFError but not found
        # if there is more so write Exception for safety
        print("Sorry, the calculator can't store this input!")
        return None
    return expression


def syntax_order_error(pre, current):
    """
    build error message to the user while getting
    syntax error in expression that
    current can't be after pre
    for example: '8/*8'
    '*' (current) can't be after '/' (pre)
    :param str current: the token that caused to the error
    :param str pre: the token placed before current in expression
    :return syntax error message
    :rtype str
    """

    return str(current) + " can't come after the " + str(pre)


def first_token_error(token):
    """
    build error message say that token can't be the first
    token in expression
    :param str token: illegal first token in math expression, like: '/','!',')'
    :return first token error message
    """
    return str(token) + " can't be the first token in expression!"


def last_token_error(token):
    """
    build error message say that token can't be the last
    token in expression
    :param str token: illegal last token in math expression, like: '+','^'
    :return last token error message
    :rtype str
    """
    return str(token) + " can't be the last token in expression!"


def closer_has_no_opener_error(index_closer):
    """
    build error message that one of the closer brackets
    has not opener
    :param index_closer: the index of closer bracket
    in the math expression
    :return closer has no opener error message
    """
    error_message = "the closer bracket in index: " + str(index_closer)
    error_message += "\nhas no opener bracket"
    return error_message


def opener_has_no_closer_error():
    """
    build error message that one of the opener brackets
    has not matched closer
    in the math expression
    :return opener has no closer error message
    """
    return "one of the opener brackets hasn't closer"


def imaginary_number(expression, result):
    """
    build error message that the complex number are not legal in my calculator
    I use it to return message with the specific part that caused to the error
    for example: '6 + ((-9)^0.5) * 5'
    i return only the -9^0.5 part
    :param expression: math expression caused to complex result
    :param result: the complex number result
    :return complex number error message
    """
    error_message = "The result of : " + str(expression) + " is: \n"
    error_message += str(result)
    error_message += "\nComplex Number in my calculator is illegal!"
    return error_message


def empty_expression():
    """
    :return error message that the math expression inserted is empty
    """
    return "Sorry, empty expression in not legal"


def print_result(result):
    """
    the function print inductive message to the user about
    the result of the solving attempt
    :param float/ErrorCalc result: The result of solving
    attempt for a math equation
    """

    if isinstance(result, float):
        # if success to solve
        print("The Result of The expression is:")
    print(str(result))


def only_spaces_expression():
    """
    :return error message that his expression
    is only whitespaces
    :rtype str
    """
    return "Sorry, your expression in build with only whitespaces!"


def error_dot_after_operator(operator):
    """
    build error message to user that he has '.' after operator
    and that is not legal, for example: '9+.*9'
    :param str operator: the operator before the dot
    :return error dot after operator error message
    :rtype str
    """
    return "dot after: " + str(operator) + " is not legal"


def ask_expression():
    """
    print message to user ask to insert math expression
    """
    print("Please Enter your Math Expression:")


def ask_if_another():
    """
    print message to user ask if he want to insert another math expression
    """
    print("Do you want to insert another expression ? (Y: YES, N:NO)")


def print_expression(expression):
    """
    print math expression
    :param expression: math expression
    """
    print("Your expression: " + str(expression))


def not_match_bracket():
    """
    build error message to user that
    he has closer bracket that not matched to his opener
    Notice this function is only for future use:
    when we will add another brackets
    :return error not match bracket error message
    :rtype str
    """
    error_message = "There is brackets that not match to each other!\n"
    error_message += "for example: (5+5}"
    return error_message


def max_size_error(size_expr):
    """
    build error message to the user about
    expression that over the legal size of char in expression
    in my calculator
    :param str size_expr: the len of the illegal expression inserted
    :return max size of expression error message
    :rtype str
    """
    error_mess = "Your expression size is: " + str(size_expr)
    error_mess += "\nThe max size of legal expression"
    error_mess += "in my calculator is: " + str(MAX_EXPRESSION_SIZE)
    return error_mess
