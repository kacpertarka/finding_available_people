import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname} {message}",
    style='{'
)


def no_directory_found(dir_name) -> None:
    """
    This function display a warning that dir_name does not exist and then ends the programme
    :param dir_name:
    """
    logging.warning(f'{dir_name} does not exits!!!')
    sys.exit(0)


def lack_off_free_time() -> None:
    """
    This function display information that number of person are not available on that day and then ends the programme
    """
    logging.info('There are not available person on this day!!')
    sys.exit(0)


def ending_message() -> None:
    logging.info('There is no available person on that day!!!')
    sys.exit(0)


def show_result(dict_: dict) -> None:

    if dict_:
        print("We've found matches person: ", end='')
        people = ', '.join(*dict_.values())
        print(people, '\nThe suitable time is: ', *dict_.keys())
        sys.exit(0)
    ending_message()
