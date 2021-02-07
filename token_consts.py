"""token_consts module include:
 - dict of operators precedence
- lists of:
1. unary operators
2. pre unary operators
3. post unary operators
4. binary operators
6. closer and opener brackets and all brackets
- MAX_OPERATOR_GRADE: The highest precedence in our calculator
- MAX_EXPRESSION_SIZE: The max size of expression our the calculator
"""

# The highest precedence in our calculator
MAX_OPERATOR_GRADE = 6

UNARY_OPERATORS = ['~', '!']
PRE_UNARY_LIST = ['~']
POST_UNARY_LIST = ['!']
BINARY_OPERATORS = ['+', '-', '/', '*', '%', '@', '&', '$', '^']

BRACKETS_LIST = ['(', ')']
OPENER_BRACKETS = ['(']
CLOSER_BRACKETS = [')']

# dict with all the operators of the calculator and their precedences
OPERATORS_PRECEDENCE = {'+': 1, '-': 1,
                        '/': 2, '*': 2,
                        '^': 3,
                        '%': 4,
                        '@': 5, '$': 5, '&': 5,
                        '!': 6, '~': 6}

# max size of legal expression in my calculator
MAX_EXPRESSION_SIZE = 100000


