""" lexer module:
Include The Lexer class responsible for The lexer analysis process of
Math expression.
The Lexer class produce token list if the expression has valid syntax.
In addition include SYNTAX_GROUP_A and SYNTAX_GROUP_B
dict that say what tokens can be inserted to token list while building it.
"""

from numbers_calc import *

EOF = '\n'

# constants to search in the
# SYNTAX_GROUP_A and SYNTAX_GROUP_B dictionary (Like Enum in c#)
CLOSER = 'Closer'
OPENER = 'Opener'
BINARY = 'Binary Operator'
PRE_UNARY = 'Pre Unary Operator'
POST_UNARY = 'Post Unary Operator'
NUMBER = 'Number'


# Full explanation about those dict is in Word file.
# dict that say which token can be inserted any moment to the tokens list
# include: Number, closer bracket and post UNARY
SYNTAX_GROUP_A = {NUMBER: False,
                  PRE_UNARY: False,
                  BINARY: True,
                  CLOSER: True,
                  OPENER: False,
                  POST_UNARY: True}

# include: Binary operator, opener bracket and pre UNARY
SYNTAX_GROUP_B = {NUMBER: True,
                  PRE_UNARY: True,
                  BINARY: False,
                  CLOSER: False,
                  OPENER: True,
                  POST_UNARY: False}


class Lexer(object):
    """ This class responsible of the tokenization process.
        Tokenization is the process of demarcating and possibly
        classifying sections of a string of input characters.
        In my program, the Lexer build list of tokens and then use this list
        in order to solve the expression.

        Attributes:
            expression str:  The math expression
            pos_expr int: current index to read from the expression
            current_char str: the last char scanned by the builder
            token_list list : the token list produced by the builder
            syntax_flags dict : dict with flag which determine what token can
            inserted in any moment to the token_list
    """
    def __init__(self, expression):
        # client string input: "4 + 12 * 3 "
        self.expression = expression
        # start scanning the text from zero index
        self.pos_expr = 0
        # the char in index self.pos
        self.current_char = self.expression[self.pos_expr]
        # init the token list
        self.token_list = []
        # init the syntax flag to SYNTAX_GROUP_B
        # because first token can be: NUMBER,PRE_UNARY or OPENER bracket
        self.syntax_flags = SYNTAX_GROUP_B

    def advance(self):
        """
        This function advance the pos index and update self.current_char
        to the next char in the expression
        """
        self.pos_expr += 1
        if self.pos_expr > len(self.expression) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.expression[self.pos_expr]

    def parity_minuses(self):
        """
        :return return True if the number of '-' in a row starts in
        self.current_char until meeting other char or end of string is even
        otherwise, return False
        :rtype: bool
        """
        minus_sign_parity = 0
        while self.current_char is not None \
                and self.current_char == '-':
            minus_sign_parity = (minus_sign_parity+1) % 2
            self.advance()
        return minus_sign_parity == 0

    def build_number_tok(self):
        """
        The function try to build a NumToken starting in index
        self.pos_expr of the expression
        :return NumToken with the value of the number
                 if error occurred while storing the number in float,
                return MEMORY_EXCEPTION ErrorCalc
        :rtype: NumToken or ErrorCalc
        """
        # create a str that will store the number begin in self.current_char
        number = ''
        # add all the digits left to the decimal point to number
        while self.current_char is not None \
                and self.current_char.isdigit():
            number += self.current_char
            self.advance()

        # add the digits right to the decimal point
        if self.current_char == '.':
            number += '.'
            self.advance()
            # add all the digits right to the decimal dot to the str
            while self.current_char is not None \
                    and self.current_char.isdigit():
                number += self.current_char
                self.advance()

        # convert the str in number to float
        convert_num_result = convert_str_to_number(number)

        if isinstance(convert_num_result, ErrorCalc):
            return convert_num_result

        return NumToken(convert_num_result)

    def get_next_token(self):
        """
        This function create instance of Token start in self.pos_expr
        and advance self.current_char to the next char in the expression
        The function builds to tokens in order
        to append them to the token list
        :return The instance of current Token,
                 if get to last of the expression return Token(EOF)
                 if tackled an error to create this Token return ErrorCalc
        :rtype: Token or ErrorCalc
        """
        current_token_val = self.current_char
        # check if we didn't get to the end of the expression
        if current_token_val is not None:
            # if we met a digit send it to a number creator function
            if current_token_val.isdigit():
                number_token = self.build_number_tok()
                return number_token

            if current_token_val == '-':
                # send to a function that handle with show of '-'
                return self.build_minus_tok()

            if current_token_val in BRACKETS_LIST:
                self.advance()
                return Token(current_token_val)

            if current_token_val in OPERATORS_PRECEDENCE.keys():
                if current_token_val in UNARY_OPERATORS:
                    current_token = UnaryToken(current_token_val)
                else:
                    current_token = BinaryToken(current_token_val)
                self.advance()
                return current_token

        # in order to determine we get to the end of the expression
        return Token(EOF)

    def get_tokens_list(self):
        """
        This function create the token list from
        self.expression and returns it.
        :return Complete Token list of the expression
        if occurred error while tokenize the expression (compile time error)
        return ErrorCalc with the specific error - Memory/Syntax Error
        :rtype: list or ErrorCalc
        """

        current_token = self.get_next_token()
        # loop over all the char in the expression
        # until we got to the end or have Error
        while isinstance(current_token, ErrorCalc) is False\
                and current_token.value != EOF:
            if self.valid_syntax(current_token) is True:
                # insert the current token in the end of the list
                self.token_list.append(current_token)
                # change the flags according the inserted token
                self.update_flags(current_token)
            else:
                # if we met problem with the syntax
                # check if this is the first token,
                # in order to give specific message
                token_val = current_token.value
                if not self.token_list:
                    error_mess = first_token_error(token_val)
                else:
                    # store the value of the last token in the list
                    # before current_token
                    pre_value = self.token_list[-1].value
                    error_mess = syntax_order_error(pre_value, token_val)
                return ErrorCalc(error_mess, SYNTAX_ORDER_ERROR)
            # get the next token
            current_token = self.get_next_token()

        # if we got outside the while and current_token
        # is instance of ErrorCalc return the Error
        if isinstance(current_token, ErrorCalc):
            return current_token

        # the token list is built
        return self.token_list

    def valid_syntax(self, token):
        """
        The function check if is it okay to insert the token in the
        end of self.token_list.
        Full explanation in Word file.
        :param Token token: last token scanned by the Lexer
        :return return True if is it okay to insert the token to the token list
                according to the syntax rules, else return False
        :rtype bool
        """

        # check what the type of the token and check his matched flag
        if token.value in CLOSER_BRACKETS:
            return self.syntax_flags[CLOSER]

        if token.value in OPENER_BRACKETS:
            return self.syntax_flags[OPENER]

        if isinstance(token, NumToken):
            return self.syntax_flags[NUMBER]

        # For operators: check the matched flag, if the flag is true
        # send to another function that check the token validity

        if token.value in PRE_UNARY_LIST:
            pre_flag = self.syntax_flags[PRE_UNARY]
            return pre_flag and self.validate_insert_pre(token.value)

        if token.value in POST_UNARY_LIST:
            post_flag = self.syntax_flags[POST_UNARY]
            return post_flag and self.validate_insert_post(token.value)

        if isinstance(token, BinaryToken):
            binary_flag = self.syntax_flags[BINARY]
            return binary_flag and self.validate_insert_binary(token.value)

        # for minus sign token
        return True

    def update_flags(self, inserted_token):
        """
        The function update the syntax_flags according
        to the last token inserted to the token list.
        :param Token inserted_token: the last token inserted to the token list
        """

        token_val = inserted_token.value
        if token_val in BINARY_OPERATORS or token_val in OPENER_BRACKETS \
                or isinstance(inserted_token, MinusSignToken)\
                or token_val in PRE_UNARY_LIST:
            self.syntax_flags = SYNTAX_GROUP_B
        else:
            self.syntax_flags = SYNTAX_GROUP_A

    def build_minus_tok(self):
        """
        The function return the next token we need to insert to the list
        when self.current_char is '-', it check if the minus is minus of
        sign or minus of simple Binary Operator
        :return Token we need to append in the end of the token list
        :rtype: Token
        """

        # get the last Token in the list
        pre_token = self.token_list[-1]
        # check if it minus sign or minus of an binary operator
        if isinstance(pre_token, BinaryToken) \
                or pre_token.value in PRE_UNARY_LIST:
            # this is minus of sign,
            # for example: '5*-6' or '~-4'
            # i use it only in the time to solve the operator before him

            # we check how much minus sign in a row we have
            if self.parity_minuses() is True:
                # if the number of times of '-' is even, return the next Token
                # because '6 / -- 6 ==> '6/6'
                return self.get_next_token()
            # if the counter_minus is odd ,create MinusSignToken
            current_token = MinusSignToken()
        else:
            # this is regular binary minus like in: '6 - 6' or '5! - 3'
            current_token = BinaryToken('-')
            self.advance()
        return current_token

    def validate_insert_binary(self, binary_op):
        """
        The function check The syntax condition:
        1. if binary operator come after post unary operator
        it has to be weak or equal precedence to him
        :param str binary_op: the binary operator need
        to be inserted to the token list
        :return if is valid to insert binary_op operator Token
        to the end of self.token_list
        :rtype bool
        """

        last_val = self.token_list[-1].value
        if last_val in POST_UNARY_LIST:
            # if new post unary '?' was weak than '&' in expression '4?&3'
            # this is syntax error because the
            # '&' don't have operand in his left side
            # when he will be calculate
            last_precedence = OPERATORS_PRECEDENCE[last_val]
            return last_precedence >= OPERATORS_PRECEDENCE[binary_op]
        return True

    def validate_insert_post(self, post_unary_op):
        """
        The function check The syntax condition:
        1. if unary operator come after unary operator
        he has to be weak or equal precedence than him
        :param str post_unary_op: the post unary operator
        need to be inserted to the token list
        :return if is valid to insert post_unary_op
         to the end of self.token_list
        :rtype bool
        """

        last_val = self.token_list[-1].value
        # for example if ';' will be strong than '!'
        # this expression will not be legal '5!;'
        # but this will be legal '5;!'
        if last_val in POST_UNARY_LIST:
            last_precedence = OPERATORS_PRECEDENCE[last_val]
            return OPERATORS_PRECEDENCE[post_unary_op] <= last_precedence
        return True

    def validate_insert_pre(self, pre_unary_op):
        """
        The function check The syntax condition:
        1. if pre unary come after pre unary he has to be
        stronger or equal precedence to him
        2. if pre unary come after binary operator
        he has to be stronger than him
        :param str pre_unary_op: the pre unary operator
        need to be inserted to the token list
        :return if is valid to insert pre_unary_op
        to the end of self.token_list
        :rtype bool
        """

        # pre unary can be the first character
        # check that the token list in not empty
        if self.token_list:
            # get the value of the last operator before him
            last_token = self.token_list[-1]
            if isinstance(last_token, MinusSignToken):
                # for case: '~-~3'
                last_token = self.token_list[-2]

            last_val = last_token.value

            if last_val in BINARY_OPERATORS or last_val in PRE_UNARY_LIST:
                last_precedence = OPERATORS_PRECEDENCE[last_val]
                if last_val in BINARY_OPERATORS:
                    # if '/' will be strong than '~' this
                    # expression would be illegal '5/~2'
                    return OPERATORS_PRECEDENCE[pre_unary_op] > last_precedence
                # if '#' will be pre unary that strong from '~'
                # that expression will be illegal '#~2'
                return OPERATORS_PRECEDENCE[pre_unary_op] >= last_precedence
        return True
