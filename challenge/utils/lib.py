from datetime import datetime, timedelta
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
    if date_range <= 2:
        today_month = str(today_date).split('/')[0]
        today_year = str(today_date).split('/')[2]
        previous_date = f'{today_month}/01/{today_year}'
    else:
        previous_date = datetime.now() - timedelta(days=((date_range-1) * 30))
        previous_month = str(previous_date).split('-')[1]
        previous_year = str(previous_date).split('-')[0]
        previous_date = f'{previous_month}/01/{previous_year}'
    
    return previous_date, today_date

