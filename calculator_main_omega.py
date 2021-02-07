"""This calculator_main_omega module include The main function of the program.
the function ask from the user math expressions
try to solve them, and print result until the user ask to stop.
In addition, there is main_evaluate that take math expression str
and return the result of the solving attempt
"""

from lexer import *
from solver import Calculator
from tokens_validation import *


def main_evaluate(expression):
    """
    This function try to solve the expression
    according to the math rules by doing:
    - Validations
    - Tokenize
    - Evaluation
    :param str expression: arithmetic expression
    :return if succeed to solve return the result,
             otherwise return ErrorCalc with specific error type
    :rtype: float or ErrorCalc
    """

    # step 1: Validations
    valid_size = size_validations(expression)
    if isinstance(valid_size, ErrorCalc):
        return valid_size

    # try to delete the spaces
    expression = delete_spaces(expression)
    # check if success to delete the spaces
    if isinstance(expression, ErrorCalc):
        return expression

    # print to the user the expression without spaces
    print_expression(expression)

    # do math validation on expression
    math_valid = math_validations(expression)
    if isinstance(math_valid, ErrorCalc):
        return math_valid

    expression = handle_minus_start(expression)

    # step 2: Build Token list, Tokenize process
    lexer = Lexer(expression)
    token_list = lexer.get_tokens_list()

    if isinstance(token_list, ErrorCalc):
        return token_list

    # step 3: Evaluation
    interpreter = Calculator(token_list)
    return interpreter.get_result()


def main():
    running = True
    # the program keep running until the user ask to stop
    while running:
        ask_expression()
        expression = calculator_input()
        # check if the input NOT cause to exception
        if expression is not None:
            result = main_evaluate(expression)
            print_result(result)

        # check if the user want to insert more expressions
        ask_if_another()
        is_another = calculator_input()
        while is_another is None or is_another not in 'YNny' or not is_another:
            ask_if_another()
            is_another = calculator_input()

        running = is_another in 'yY'


if __name__ == '__main__':
    main()
