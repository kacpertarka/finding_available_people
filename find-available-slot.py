import os
from datetime import datetime, timedelta
from dateutil import rrule
import click
from message import *


def get_list_of_file_from_dir(dir_name: str) -> list:
    """
    Function takes a list of file named <name>.txt from directory
    :param dir_name:
    :return list:
    """
    # if dir_name != None - change dictionary
    if dir_name:
        if not os.path.isdir(dir_name) or not os.path.exists(dir_name):
            no_directory_found(dir_name)
        os.chdir(dir_name)
    list_of_file = os.listdir()
    return [el for el in list_of_file if el.endswith('.txt')]


def get_available_time_of_day(dict_: dict) -> dict:
    """
    This function converts a dictionary with occupied time into a dictionary with available time
    :param dict_:
    :return dict of available time:
    """
    # if dict_ is empty use lac_off_free_time function
    if not dict_:
        lack_off_free_time()
    # available_dict - dictionary with available time, returned
    available_dict = {}
    # temp_list - temporary list with <key, value> elements from dict_
    temp_list = dict_to_list(dict_)
    # time_0 & time_24 - time 00:00 and 23:59
    time_0 = datetime(year=int(str(temp_list[0])[:4]),
                      month=int(str(temp_list[0])[5:7]),
                      day=int(str(temp_list[0])[8:10]), hour=0, minute=0, second=0)
    time_24 = datetime(year=int(str(temp_list[0])[:4]),
                       month=int(str(temp_list[0])[5:7]),
                       day=int(str(temp_list[0])[8:10]), hour=23, minute=59, second=59)
    # adding_1_sek - 1 second to add to time: 12:59:59 -> 13:00:00
    adding_1_sek = timedelta(seconds=1)
    # loop which completes the dictionary with the relevant times
    available_dict[time_0] = temp_list[0]
    for i in range(1, len(temp_list)-1, 2):
        available_dict[temp_list[i] + adding_1_sek] = temp_list[i+1]
    available_dict[time_24] = temp_list[-1]
    return available_dict


def get_time_from_file(line_date: str, is_whole_line: bool = True) -> tuple:
    """
    This functions converts strings with date from line from file to datetime type and returns time of start and end
    :param line_date:
    :param is_whole_line:
    :return:
    """
    if is_whole_line:
        s_date: str = line_date[:19]
        e_date: str = line_date[22:].strip('\n')
        try:
            start_date = datetime.strptime(s_date, '%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(e_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None, None
    else:
        """
        if line has length 11 - it's mean person is available whole day
        for example: 2030-12-24
        """
        year = line_date[:4]
        month = line_date[5:7]
        day = line_date[8:10]
        try:
            # at first start date begins at 00:00:00 but it was for tests only :)
            start_date = datetime.strptime(f'{year}-{month}-{day} 00:00:00', '%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(f'{year}-{month}-{day} 23:59:59', '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None, None
    return start_date, end_date


def read_file(file: str, date: datetime = datetime.today()) -> dict:
    """
    This function reads lines from a file and for each lines converts line to time in dictionary
    :param file:
    :param date:
    :return dict:
    """
    non_available_time = {}
    with open(file, 'r') as file:
        for line in file.readlines():
            # empty line
            if line == '\n':
                continue
            # length of date + '\n'
            if len(line) == 11:
                key, val = get_time_from_file(line, False)
                # if get_time_from_file function returns None type
                if not key or not val:
                    continue
                non_available_time[key] = val
                continue
            key, val = get_time_from_file(line)
            # if get_time_from_file function returns None type
            if not key or not val:
                continue
            # if second date is earlier than now
            if val < datetime.now():
                continue
            # if day of date from file is different to today
            if str(val)[:11] != str(date)[:11]:
                continue
            non_available_time[key] = val
    return get_available_time_of_day(non_available_time)


def find_available_time_(dict_: dict, available_time: int) -> dict:
    """
    This function iterates through the day from now to end of the day and checks for matches
    :param dict_:
    :param available_time:
    :return:
    """
    # name_list - list of name from dict_
    name_list = list(dict_.keys())
    # now - as the name says :0
    now = datetime.today()
    now = datetime.strptime(f'{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:00', '%Y-%m-%d %H:%M:%S')
    # finish_time - time to finish loop
    finish_time = now+timedelta(hours=24-now.hour, minutes=59-now.minute)
    # available_time - minimum available time for all
    available_time = timedelta(minutes=available_time)
    returned_dict = {}
    # looping through the day
    for time in rrule.rrule(rrule.MINUTELY, dtstart=now, until=finish_time):
        # adding empty list to <key> time in dictionary
        returned_dict[time] = []
        # looping through the name in name_list
        for name in name_list:
            # if time suits the person it will be adding to the list
            if is_available(time, available_time, dict_[name]):
                returned_dict[time].append(name[:-4])
        # if list is empty - delete the list
        if not returned_dict[time]:
            del returned_dict[time]
    return returned_dict


def is_available(time: datetime, diff_time: timedelta, dict_: dict) -> bool:
    """
    This function checks whether a given time matches
    :param time:
    :param diff_time:
    :param dict_:
    :return:
    """
    for key, val in dict_.items():
        if key <= time <= val and key <= time+diff_time <= val:
            return True
    return False


def first_available_time(dict_: dict, min_num_of_people: int) -> dict:
    """
    This function search first time when minimum number of people matches
    :param dict_:
    :param min_num_of_people:
    :return:
    """
    for k, v in dict_.items():
        if len(v) == min_num_of_people:
            time = ':'.join([str(k.hour), str(k.minute) if len(str(k.minute)) == 2 else '0' + str(k.minute)])
            return {time: v}
    return {}


def dict_to_list(dict_: dict) -> list:
    """
    This function converts dict to list
    :param dict_:
    :return:
    """
    returned_list = []
    [returned_list.extend([key, val]) for key, val in dict_.items()]
    return returned_list


@click.command()
@click.option('--calendars', type=str, default=None)
@click.option('--duration', type=int, default=45)
@click.option('--minimum_people', type=int, default=1)
def main(calendars: str, duration: int, minimum_people: int) -> None:

    file_list = get_list_of_file_from_dir(calendars)
    main_dict = {}

    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day

    for file_name in file_list:
        main_dict[file_name] = read_file(file_name, date=datetime(year=year, month=month, day=day))

    available_time = find_available_time_(main_dict, duration)

    first_available = first_available_time(available_time, minimum_people)

    show_result(first_available)


if __name__ == '__main__':

    main()


