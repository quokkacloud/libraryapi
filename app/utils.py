"""
File with other functions
"""


def get_average_of_ratings(rating_dict):
    rating_sum = 0
    rating_num = 0
    for rating, times in rating_dict.items():
        rating_sum += rating*times
        rating_num += times
    try:
        avg_rate = float(rating_sum/rating_num)
    except ZeroDivisionError:
        return 0.0
    return '{0:.2f}'.format(avg_rate)

