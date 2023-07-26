from datetime import datetime
import re


def contains_money(*, title:str, description:str):
    """
    """
    if not title or not description:
        return False
    money_pattern = r'\$[\d,.]+|\d+ (dollars|USD)'
    return bool(re.search(money_pattern, title + description))


def count_search_phrases(*, title:str, description:str, phrase:str):
    """
    """
    if not title or not description:
        return None
    title_count = title.lower().count(phrase.lower())
    description_count = description.lower().count(phrase.lower())
    return title_count + description_count


def get_previous_and_today_date(*, date_range:int):
    """
    """
    if not isinstance(date_range, int) or date_range < 0:
        return (-1, f'date_range is not a valid parameter. date_range: {date_range} type(data_range): {type(date_range)}')

    today_date = datetime.today().strftime('%m/%d/%Y')
    month = str(today_date).split('/')[0]
    year = str(today_date).split('/')[2]

    if date_range > 1:
        month = int(month) - (date_range-1)
        # TODO: fix this when month is negative 
        if month == 0:
            month = "12"
            year = int(year) - 1
        elif len(str(month)) == 1:
            month = f'0{month}'

    previous_date = f'{month}/01/{year}'
    return previous_date, today_date

