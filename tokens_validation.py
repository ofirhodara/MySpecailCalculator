"""tokens_validation module:
In this file there is all the expression validation
functions before trying to build token list:
size_validation, legal chars, dot errors,
valid brackets, dot errors and unnecessary_parentheses
In addition there is 2 function that change
the expression before sending him to solve:
delete spaces and handle_minus_start
"""

from numbers_calc import *


def legal_chars(expression):
    """
    The function check if all the character in
    expression is valid in our calculator
    :param str expression: expression input for solving
    :return return true if all the characters in the
    expression are legal otherwise return ErrorCalc with ILLEGAL_CHAR
    error type
    :rtype: bool or ErrorCalc
    """

    # only for display to user the specific
    # index of illegal char if found one
    index_tok = 0
    for char_tok in expression:
        if char_tok.isdigit() is False \
                and char_tok not in OPERATORS_PRECEDENCE.keys() \
                and char_tok not in BRACKETS_LIST and char_tok != '.':
            # found illegal char build error message of ILLEGAL_CHAR error
            error_message = illegal_char(index_tok, expression[index_tok])
            return ErrorCalc(error_message, ILLEGAL_CHAR)
        index_tok += 1
    return True


def delete_spaces(expr):
    """
    The function build a new expression without the legal spaces
    :param str expr: expression input for solving
    :return ErrorCalc instance if:
    SPACE_IN_NUMBER: found illegal space
    EMPTY_EXPRESSION: after delete the spaces the expression is empty
    otherwise return the expr without spaces
    """

    non_space_expr = ''
    pos_expr = len(expr) - 1
    while pos_expr >= 0:
        if expr[pos_expr].isspace():
            if pos_expr != 0 and pos_expr != len(expr)-1:
                after_space = expr[pos_expr+1]
                before_space = expr[pos_expr-1]
                if (after_space.isdigit() or after_space == '.') and\
                        (before_space.isdigit() or before_space == '.'):
                    # for cases we have space inside a number
                    # like: '4 4+4' or '4. 6 + 4'
                    error_message = space_inside_number(before_space,
                                                        after_space)
                    return ErrorCalc(error_message, SPACE_IN_NUMBER)
            # delete the space from the original expression
            expr = expr[:pos_expr] + expr[pos_expr + 1:]
        else:
            # add this character the new expression
            non_space_expr = expr[pos_expr] + non_space_expr
        pos_expr -= 1

    # if after delete all the spaces the expression is empty
    if not non_space_expr:
        error_message = only_spaces_expression()
        return ErrorCalc(error_message, EMPTY_EXPRESSION)
    return non_space_expr


def dot_errors(expression):
    """
    This function check all the edge cases for '.'
    characters in my expression
    1. first in the expression
    2. after operator
    :param str expression: not empty expression input for solving
    :return false if all the dots are in legal positions
             else, return ErrorCalc with DOT_ERROR error type
    """

    # '.' can't be the first Character
    if expression[0] == '.':
        error_mess = first_token_error('.')
        return ErrorCalc(error_mess, DOT_ERROR)

    for expr_pos in range(1, len(expression)):
        if expression[expr_pos] == '.':
            if expression[expr_pos-1].isdigit() is False:
                error_mess = error_dot_after_operator(expression[expr_pos-1])
                return ErrorCalc(error_mess, DOT_ERROR)
    return False


def last_token(expression):
    """
    The function check if the last char in the expression
    can be in the end of math expression
    :param str expression: not empty expression input for solving
    :return return True if the last token is last legal char in expression
             otherwise return ErrorCalc with LAST_TOKEN_ERROR error type
    :rtype: bool/ErrorCalc
    """

    last_char = expression[-1]
    # last char can be: digit/post unary/closer bracket/Decimal point
    if last_char.isdigit() is False and last_char not in POST_UNARY_LIST \
            and last_char not in CLOSER_BRACKETS and last_char != '.':
        error_message = last_token_error(last_char)
        return ErrorCalc(error_message, LAST_TOKEN_ERROR)
    return True


def valid_brackets(expression):
    """
    This function check if for every bracket there is match other bracket
    :param str expression: string represent math expression without spaces
    :return return True if the brackets is valid
             otherwise return ErrorCalc with BRACKETS_ERROR error type
    :rtype: bool/ErrorCalc
    """

    # build stack for brackets
    stack = []
    # only for show the specific index of error
    expr_index = 0
    for expr_char in expression:
        if expr_char in OPENER_BRACKETS:
            stack.append(expr_char)
        elif expr_char in CLOSER_BRACKETS:
            # check if the stack is not empty before pop
            if len(stack) > 0:
                # if in the future will support '}' or ']'
                # we need to check that the closer is match to the
                # opener in the top of the stack, '{6+6)' is not legal
                opener_index_openers_list = OPENER_BRACKETS.index(stack.pop())
                closer_index_closers_list = CLOSER_BRACKETS.index(expr_char)
                if closer_index_closers_list != opener_index_openers_list:
                    return ErrorCalc(not_match_bracket(), BRACKETS_ERROR)
            else:
                # that means that one of the closer brackets
                # has not suitable opener
                error_message = closer_has_no_opener_error(expr_index)
                return ErrorCalc(error_message, BRACKETS_ERROR)
        expr_index += 1

    # check if the stack is empty
    # if not that means that one of the opener brackets
    # has not suitable closer
    if len(stack) != 0:
        error_message = opener_has_no_closer_error()
        return ErrorCalc(error_message, BRACKETS_ERROR)
    return True


def math_validations(expression):
    """
    The function do all the validation on math exercise in: expression
    before sending it to the calculator to solving
    :param str expression: string represent math expression without spaces
    :return return True if the expression is Valid
             else, return ErrorCalc with the specific error type
    :rtype: bool or ErrorCalc
    """

    # build list with all the math validations functions
    validations_funcs = [legal_chars, valid_brackets,
                         unnecessary_parentheses,
                         dot_errors, last_token]

    for validity_func in validations_funcs:
        is_valid = validity_func(expression)
        if isinstance(is_valid, ErrorCalc):
            # found error
            return is_valid

    # if we get here the expression is passed all the validations
    return True


def handle_minus_start(expression):
    """
    The function handle cases that there is - in the start of expression or
    after opener bracket by put 0 before this minus
    for cases like: -(4+6) => 0-(4+6) and 8*(-6^2) => 8*(0-6^2)
    :param str expression: not empty string represent math expression
    :return return the expression after put 0 before in the places mentioned
    :rtype: str
    """

    if expression[0] == '-':
        expression = '0' + expression
    # i loop over all the OPENER_BRACKETS in order to be generic and
    # not only write '(-' and '(0-' also '{-' and '{0-'
    for opener in OPENER_BRACKETS:
        expression = expression.replace(opener + '-', opener + '0-')
    return expression


def unnecessary_parentheses(expression):
    """
    The function check if there is unnecessary parentheses in the expression
    for example: ((6+6))*3
    :param str expression: string represent math expression
                           after passed valid_brackets validation
    :return return False if there are not
            unnecessary parentheses in the expression
            else, return ErrorCalc with UNNECESSARY_PARENTHESES error type
    :rtype: bool/ErrorCalc
    """

    # build stack for brackets
    stack_brackets = []
    for expr_char in expression:
        if expr_char not in CLOSER_BRACKETS:
            stack_brackets.append(expr_char)
        else:
            if stack_brackets[-1] in OPENER_BRACKETS:
                # if expr_char = ')' and the char in the top of the stack
                # is '(', there is unnecessary parentheses
                error_message = error_extra_brackets()
                return ErrorCalc(error_message, UNNECESSARY_PARENTHESES)

            # pop all the chars from the stack until
            # met the matched '('
            del stack_brackets[-1]
            while stack_brackets[-1] not in OPENER_BRACKETS:
                del stack_brackets[-1]
            # pop the opener
            del stack_brackets[-1]
    return False


def size_validations(expression):
    """
    do the size validation to the expression
    Expression can't be empty and cant be over the max size
    :param str expression: arithmetic expression
    :return if one of the condition not passed return ErrorCalc
             with inductive message
             else return True
    """

    size_expr = len(expression)
    # check if input is empty
    if size_expr == 0:
        return ErrorCalc(empty_expression(), EMPTY_EXPRESSION)

    if size_expr >= MAX_EXPRESSION_SIZE:
        return ErrorCalc(max_size_error(size_expr), MEMORY_EXCEPTION)
    return True
