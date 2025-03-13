class ParseError(Exception):
    pass


def parse(hours, minutes):
    if hours > 23 or hours < 0:
        raise ParseError

    if minutes > 59 or minutes < 0:
        raise ParseError
