"""This module include the classes of the Token represent the
small parts of math expression,
The relationship between the classes are
full explained in my Word File.
    Token class: base class for all the tokens
    OperatorToken class: base class of operators tokens
    BinaryToken: token of binary operators : '*','+' and more
    UnaryToken: token of binary operators : '!','~'
    NumToken: token of the numbers in expressions
    MinusSignToken: class to minus sign '-' after
                    binary/pre unary operations
"""


class Token(object):
    """ Basic class of token in math expression
        A lexical token or simply token is a string with an assigned
        and thus identified meaning. It is structured as a pair
        consisting of a token name and an optional token value.

       Attributes:
           value str -- The token value
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Token({value})'.format(
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class OperatorToken(Token):
    """
    Class of Operator Token inherit from base class Token
    Attributes:
        value str -- The token value
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Operator Token({value})'.format(
            value=repr(self.value),
        )

    def __repr__(self):
        return self.__str__()


class BinaryToken(OperatorToken):
    """
    Class of binary Token inherit from base class OperatorToken

    Attributes:
        value str -- The token value (like: '%','+','-')
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Binary Token({value})'.format(
            value=repr(self.value),
        )

    def __repr__(self):
        return self.__str__()


class UnaryToken(OperatorToken):
    """
    Class of unary operator Token inherit from base class OperatorToken

    Attributes:
        value str -- The token value (like: '!','~')

    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Unary Token({value})'.format(
            value=repr(self.value),
        )

    def __repr__(self):
        return self.__str__()


class MinusSignToken(Token):
    """
    Class of Minus Sign Token inherit from base class Token
    Attributes:
        value str -- The token value '-'
    """
    def __init__(self):
        self.value = '-'

    def __str__(self):
        return 'Minus Sign Token({value})'.format(
            value=repr(self.value),
        )

    def __repr__(self):
        return self.__str__()


class NumToken(Token):
    """
    Class of operator Token inherit from base class Token
        Attributes:
        value float -- The token value (like: 2.4,100)
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Number Token({value})'.format(
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
