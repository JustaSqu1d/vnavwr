from math import floor, log


def re_format(number):
    units = ["", "k", "m", "g", "t", "p"]
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return "%.2f%s" % (number / k**magnitude, units[magnitude])
