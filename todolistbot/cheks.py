interval_limit = 10000
text_limit = 250

days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

def check_numbers(number: str) -> bool:
    if number.isdigit():
        if number[0] != '0':
            if int(number) < interval_limit:
                return True
    return False


def days_check(day: str) -> bool:
    if day in days:
        return True
    else:
        return False


def time_check(time: str) -> bool:
    if ':' in time:
        a = time.split(':')
        if len(a) == 2:
            if a[0].isdigit() and a[1].isdigit():
                if 23 >= int(a[0]) >= 0:
                    if 59 >= int(a[1]) >= 0:
                        return True
    return False


def text_check(text: str) -> bool:
    if len(text) > text_limit:
        return False
    return True
