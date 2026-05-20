def round_ans(val):
    """
    Rounds currency to 2 decimal places
    :param val: Number to be rounded
    :return: Number rounded to 2 decimal places
    """
    var_rounded = round(val, 2)
    return "{:.2f}".format(var_rounded)


def to_ils(to_convert):
    """
    Converts from NZD to ILS
    :param to_convert: Amount to be converted in NZD
    :return: Converted amount in ILS
    """
    answer = to_convert * 2.07
    return round_ans(answer)


def to_nzd(to_convert):
    """
    Converts from ILS to NZD
    :param to_convert: Amount to be converted in ILS
    :return: Converted amount in NZD
    """
    answer = to_convert / 2.07
    return round_ans(answer)


# Main Routine / Testing starts here
# to_ils_test = [1, 50, 100, 500]
# to_nzd_test = [1, 50, 100, 500]
#
# for item in to_ils_test:
#     ans = to_ils(item)
#     print(f"{item} NZD is {ans} ILS")
#
# print()
#
# for item in to_nzd_test:
#     ans = to_nzd(item)
#     print(f"{item} ILS is {ans} NZD")
