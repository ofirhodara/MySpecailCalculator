"""In solver module there is the Calculator class that responsible for
solving the result of math expression stored in token list.
first he eval all the expression inside the brackets
and then send the remain expression to evaluate_token_list function.
- evaluate_token_list: return result of token list without brackets
In addition 3 helper functions to the solving process:
- insert_post_result/insert_pre_result/insert_binary_result:
insert the result of operation to the token list and delete the operator
and 2 function that responsible for negate number after minus of sign:
negate_minus_sign and check_negation
"""


from tokens_validation import *


class Calculator(object):
    """
    Calculator is class that responsible to produce result from token list
    Attributes:
        token_list list -- Token list of math expression
    """
    def __init__(self, token_list):
        self.token_list = token_list

    def get_index_of_opener_bracket(self, closer_index):
        """
        The function return the index of the opener bracket token
        of the closer bracket token in index close_index in self.token_list
        :param int closer_index: the index of the closer
         bracket in the list of tokens
        :return return the index of the suit opener
        :rtype: int
        """
        pos_opener = closer_index - 1
        while self.token_list[pos_opener].value not in OPENER_BRACKETS:
            pos_opener -= 1
        return pos_opener

    def get_result(self):
        """
        The function target is to solve the math expression
        stored in self.token_list
        :return: if success to solve, the function return the result
                 otherwise return ErrorCalc with specific error message
        :rtype: float for the result or ErrorCalc
        """

        # first ,solve all the sub expressions inside the brackets
        solved_brackets = self.eval_all_brackets()
        # check if all the sub expression inside
        # the brackets was evaluated good
        if isinstance(solved_brackets, ErrorCalc):
            return solved_brackets

        # try to evaluate all the expression remain in the list
        result_token = evaluate_token_list(self.token_list)
        if isinstance(result_token, ErrorCalc):
            # return the error
            return result_token
        # return the float value of the NumToken
        return result_token.value

    def eval_all_brackets(self):
        """
        The function solve all the expression inside the brackets
        and insert their result to self.token_list in their
        place in the expression
        :return True if the Calculator success to solve
        all the sub expressions in the brackets
        Otherwise return ErrorCalc with specific Error type
        """

        # find the first index of an closer token
        index_of_closer = self.first_index_of_closer()
        # while there is bracket in the expression
        while index_of_closer != -1:
            # find the suit opener for the founded closer
            opener_index = self.get_index_of_opener_bracket(index_of_closer)
            # get sub list of the expression between the brackets
            expr_between = self.token_list[opener_index + 1:index_of_closer]
            # evaluate the expression inside the brackets
            result_inside = evaluate_token_list(expr_between)

            if isinstance(result_inside, ErrorCalc):
                return result_inside

            # delete the expression between the brackets (include them)
            # from the expression list
            del self.token_list[opener_index:index_of_closer + 1]
            # insert the result to the list
            self.token_list.insert(opener_index, result_inside)
            # search the next brackets need to solve
            index_of_closer = self.first_index_of_closer()

        # return true if we solved all the brackets
        return True

    def first_index_of_closer(self):
        """
        The function search in self.token_list token with
        value of closer bracket
        :return return the index of first token with value of closer bracket
                 if not found return -1
        :rtype int
        """
        # using list comprehension
        return next((tok_index for tok_index in range(0, len(self.token_list))
                     if self.token_list[tok_index].value
                     in CLOSER_BRACKETS), -1)


def insert_post_result(tokens_list, op_index):
    """
    The function solve the post unary operator in index op_index
    insert the result to the token list and delete the unary operator
    :param list tokens_list: Token list of math expression
    :param int op_index: the index of the token with
                         post_unary operator to solve
    :return if there was Error while solving return ErrorCalc
             else return the number of tokens deleted from
             the list in the solving
    """

    # get the number left to the operator
    left_num = tokens_list[op_index - 1].value

    result = solve_unary(left_num, tokens_list[op_index].value)
    # check if there was Math Error/Memory Error while solving
    if isinstance(result, ErrorCalc):
        return result

    # insert the result to the list
    tokens_list[op_index - 1].value = result
    # delete the operator from the list
    del tokens_list[op_index]
    # only one token was deleted so return 1
    return 1


def insert_pre_result(tokens_list, op_index):
    """
    The function solve the pre unary operator in index op_index
    insert the result to the token list and delete the pre unary operator
    :param list tokens_list: Token list of math expression
    :param int op_index: the index of the token with
    pre unary operator to solve
    :return if there was Error while solving return ErrorCalc
            else return the number of tokens deleted
            from the list in the solving
    """
    # in regular pre unary expression, only one token
    # delete from the list, '~2+3'(4 tokens) => '-2+3'(3 tokens)
    deleted_tokens_count = 1

    # negate the right operand
    # if we have minus sign token after the operator
    is_negated = check_negation(tokens_list, op_index)
    # if met error while negate
    if isinstance(is_negated, ErrorCalc):
        return is_negated

    if is_negated is True:
        # if negated, we deleted the minus sign so add
        # 1 to the counter of deleted tokens
        deleted_tokens_count += 1

    # calculate the result of the expression
    index_of_number = op_index + 1
    right_num = tokens_list[index_of_number].value
    operator = tokens_list[op_index].value
    result = solve_unary(right_num, operator)

    if isinstance(result, ErrorCalc):
        return result

    # insert the result in the list
    tokens_list[index_of_number].value = result
    # delete the operator
    del tokens_list[op_index]

    return deleted_tokens_count


def insert_binary_result(tokens_list, op_index):
    """
    This function solve the binary expression in tokens_list
    for the binary operator in index: (op_index)
    the function delete the left and right to the op
    numbers tokens from the list
    and insert the result instead the operator token
    :param list tokens_list: list of tokens present math expression
    :param int op_index: the index of the binary operator in tokens_list
    :return if there was Error while solving return ErrorCalc
             else return the number of tokens deleted
             from the list in the solving
    """

    # in regular binary expression
    # we delete two tokens from the list:
    # '3+4' (3 token) => '7' (1 token)
    deleted_tokens_count = 2

    # negate the right operand
    # if we have minus sign token after the operator
    is_negated = check_negation(tokens_list, op_index)

    # if met error while negate
    if isinstance(is_negated, ErrorCalc):
        return is_negated

    if is_negated is True:
        # if negated, we deleted the minus sign so add
        # 1 to the counter of deleted tokens, case: 8 * - 9
        deleted_tokens_count += 1

    # get the numbers of this binary expression
    left_num = tokens_list[op_index - 1].value
    right_num = tokens_list[op_index + 1].value

    # calculate the result
    operator = tokens_list[op_index].value
    result = solve_binary(left_num, operator, right_num)

    # check if there was error while solving
    if isinstance(result, ErrorCalc):
        return result

    # insert the result into the token list
    tokens_list[op_index] = NumToken(result)

    # delete the left number
    del tokens_list[op_index - 1]

    # delete the right number
    # notice that one element is already deleted
    del tokens_list[op_index]

    return deleted_tokens_count


def evaluate_token_list(tokens_list):
    """
    The function try solve to math expression stored in tokens_list
    :param tokens_list: list of tokens present math expression
                        without brackets Tokens
    :return if tackled with Run time Error while solving
             return ErrorCalc with specific Error Message
             else, return The NumToken with result of the expression
    """
    # get the list of precedence in this token list
    precedences = build_precedence_list(tokens_list)
    # calculate only once the len of the list
    token_list_len = len(tokens_list)

    # solve until the precedences list is empty
    while precedences:
        token_index = 0
        # get the current max precedence to solve
        max_precedence = precedences.pop(0)
        while token_index < token_list_len:
            curr_token = tokens_list[token_index]
            # check if current_token is token with max_precedence
            if isinstance(curr_token, OperatorToken) and\
                    OPERATORS_PRECEDENCE[curr_token.value] == max_precedence:
                # try to solve the operation in token_index
                # and get how much tokens deleted from the list
                del_tokens = solve_op_in_index(token_index, tokens_list)
                if isinstance(del_tokens, ErrorCalc):
                    # if we tackled with error while
                    # solving the current_token operator return it
                    return del_tokens
                # delete from token_list_len the number of tokens
                # deleted from the list in order to avoid calculate
                # len(tokens_list), after every operator solved
                token_list_len -= del_tokens
            else:
                token_index += 1

    # after solving all the operators the result will be in the first
    # token of the tokens_list
    return tokens_list[0]


def get_right_most_pre_unary(tokens_list, pre_index):
    """
    The function check if there is some pre unary operators in
    a row starting in pre_index in tokens_list,
    check what pre unary need to be solved in tokens_list
    :param tokens_list: list of tokens present math expression
    :param pre_index: index of pre unary token in tokens_list
    :return return the index of the first unary operator need
            to solve in tokens_list.
            from index: pre_index
            token indexes:  0 1 2 3
            For   example: '~ ~ ~ 2'
            if pre_index = 0, the function will return 2
    """

    number_index = pre_index
    # search the most right pre token operator
    while isinstance(tokens_list[number_index], NumToken) is False:
        number_index += 1

    # for cases: ~~-4
    if isinstance(tokens_list[number_index - 1], MinusSignToken):
        number_index -= 1

    # the pre unary index will be always in the number left side
    return number_index - 1


def solve_op_in_index(op_index, tokens_list):
    """
    The function call to the suitable function from:
    insert_binary_result
    insert_pre_result
    insert_post_result
    according to the operator token in op_index in tokens_list
    and return their result
    :param int op_index: get index of operator token in tokens_list
    :param list tokens_list: list of tokens present math expression
    :return if there was Error while solving the operator in op_index
     return ErrorCalc with specific error type
     else return the number of tokens deleted from the list in the solving
    """

    op_value = tokens_list[op_index].value
    # get which function we need to call in order to solve op_value
    if op_value in BINARY_OPERATORS:
        insert_result_func = insert_binary_result
    elif op_value in POST_UNARY_LIST:
        insert_result_func = insert_post_result
    else:
        # search the right most pre unary operator index
        op_index = get_right_most_pre_unary(tokens_list, op_index)
        insert_result_func = insert_pre_result

    # call the function that solve the operator in index op_index
    return insert_result_func(tokens_list, op_index)


def check_negation(tokens_list, op_index):
    """
    The function check if is there minus sign token after the operator
    in op_index in tokens_list, if yes: try negate the number right to him
    and delete the the minus sign from the tokens list and return True
    if not return False
    :param list tokens_list: Token list of math expression
    :param int op_index: index of Minus Sign Token in tokens_list
    :return False if not need to negate
            True if success to negate,
            ErrorCalc if not success negate
    """
    # check if the token after the operator is minus sign
    if isinstance(tokens_list[op_index + 1], MinusSignToken):
        is_negated = negate_minus_sign(tokens_list, op_index + 1)
        if is_negated is not True:
            # there was error while negate
            return is_negated
        # negated
        return True
    # not need to negate
    return False


def negate_minus_sign(tokens_list, minus_index):
    """
    The function negate the number after the minus sign token in index
    minus_index, and delete the minus sign token from tokens_list
    :param list tokens_list: Token list of math expression
    :param int minus_index: index of Minus Sign Token in tokens_list
    :return True if success to negate,
            ErrorCalc with MemoryException error type if not
    """

    # for cases: '4&-3'
    # the '-' sign has priority only on the '&' before him
    # so i negate the '3' when is the time to solve '&'

    num_to_negate = tokens_list[minus_index + 1].value
    # try to get the result of negation
    result = solve_binary(num_to_negate, '*', float(-1))

    # theoretically, because the limit of
    # negative and positive float number
    # is not equal we can met overflow error while negate a number
    if isinstance(result, ErrorCalc):
        return result

    # change the value to the result
    tokens_list[minus_index + 1].value = result
    # delete the minus sign token from the list
    del tokens_list[minus_index]
    return True
