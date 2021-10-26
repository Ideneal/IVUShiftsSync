import re
from datetime import datetime, timedelta


def remove_control_chars(str):
    """
    Removes the control chars '\n\t\r' from a string.
    @param str: The string
    """
    regex = re.compile(r'[\n\t\r]')
    str = regex.sub('', str)
    return str


def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def str2datetime(str):
    d = str.split('+')[0] if '+' in str else str
    d = d.replace('Z', '')
    return datetime.strptime(d, '%Y-%m-%dT%H:%M:%S')


def str2date(str):
    return str2datetime(str).date()


def date2datetime(date):
    return datetime.combine(date, datetime.min.time())


def add_days(date, days):
    return date + timedelta(days=days)
