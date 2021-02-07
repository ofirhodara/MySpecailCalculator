"""errors.py module:
the file includes str constants of all the error types
we have in the calculator
In addition, it includes the ErrorCalc class
stored The information of an error
we tackled during solving attempt to math expressions
"""

# Math errors:
COMPLEX_ERROR = 'Complex Number Error'
DIVIDE_ZERO = 'Divide in zero Error'
FACTORIAL_ERROR = 'Factorial Error'

# Memory:
# if get OverFlow Exception or +-inf
# or expression is to large
MEMORY_EXCEPTION = 'Memory Exception Error'

# 7 Validations error before building the token list Error
ILLEGAL_CHAR = 'Illegal Char Error'
BRACKETS_ERROR = 'Valid brackets Error'
SPACE_IN_NUMBER = 'Space in number Error'
DOT_ERROR = 'Decimal point Error'
LAST_TOKEN_ERROR = 'Last token Error'
UNNECESSARY_PARENTHESES = 'Unnecessary Parentheses Error'
EMPTY_EXPRESSION = 'Empty Expression Error'

# Syntax error while build the Token list
SYNTAX_ORDER_ERROR = 'Syntax Order Error'


class ErrorCalc(object):
    """
    ErrorCalc is class stored The information of an error
    we tackled during solving the math expression
    Attributes:
         error_message str -- Specific message about the error
         error_type str -- The type of the error
    """
    def __init__(self, error_message, error_type):
        self.error_message = error_message
        self.error_type = error_type

    def __str__(self):
        error_str = "ERROR TYPE: " + str(self.error_type) + "\n"
        error_str += self.error_message
        return error_str

    def __repr__(self):
        return self.__str__()
