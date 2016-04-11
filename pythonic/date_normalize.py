from datetime import date
import datetime


class IndefinitePast(date):
    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return False

INDEFINITE_PAST = IndefinitePast(datetime.MINYEAR, 1, 1)

class IndefiniteFuture(date):
    def __lt__(self, other):
        return False

    def __le__(self, other):
        if other is INDEFINITE_PAST:
            return True
        return False

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True


INDEFINITE_FUTURE = IndefiniteFuture(datetime.MAXYEAR, 12, 31)

def process_start_date(d):
     if d is None:
         return INDEFINITE_PAST
     return d

def process_end_date(d):
     if d is None:
         return INDEFINITE_FUTURE
     return d

class ValidationError(Exception):
    pass


def validate_end_date_later_than_start(start_date, end_date):
    if process_end_date(end_date) <= process_start_date(start_date):
        raise ValidationError("The end date should be later than the start date.")

if __name__ == '__main__':
    print INDEFINITE_FUTURE <= INDEFINITE_PAST
    # print None <= None
    validate_end_date_later_than_start(datetime.datetime, None)