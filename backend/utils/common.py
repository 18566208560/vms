import datetime
from .constant import TIME_TO_LAB,TIME_BUKET


def time_to_lab(hour):

    for k in TIME_TO_LAB.keys():
        for item in k:
            if hour ==item:
                v = TIME_TO_LAB[k]

                return v




