from datetime import datetime, timedelta
import re


def contains_money(*, title:str, description:str):
    """
        Checks if contains any amount of money in title and/or description 
        inputs: 
            str: title
            str: description
        outputs:
            bool: found_money
    """
    if not title or not description:
        return False
    
    money_pattern = r'\$[\d,.]+|\d+ (dollars|USD)'
    found_money = bool(re.search(money_pattern, title + description))
    
    return found_money


def count_search_phrases(*, title:str, description:str, phrase:str):
    """
        Count how many times the phrase appears in the title and/or description
        inputs:
            str: title
            str: description
            str: phrase
        outputs:
            int: count_phrase
    """
    if not title or not description:
        return None

    title_count = title.lower().count(phrase.lower())
    description_count = description.lower().count(phrase.lower())
    
    count_phrase = title_count + description_count
    return count_phrase


def get_previous_and_today_date(*, date_range:int):
    """
        Gets the previous and current date for the given date range
        input: 
            int: date_range
        outputs:
            error: tuple(status_code, status_message)
            success: previous_date, today_date
    """
    if not isinstance(date_range, int) or date_range < 0:
        return (-1, f'date_range is not a valid parameter. date_range: {date_range} type(data_range): {type(date_range)}')

    today_date = datetime.today().strftime('%m/%d/%Y')
    if date_range < 2:
        today_month = str(today_date).split('/')[0]
        today_year = str(today_date).split('/')[2]
        previous_date = f'{today_month}/01/{today_year}'
    else:
        previous_date = datetime.now() - timedelta(days=((date_range-1) * 30))
        previous_month = str(previous_date).split('-')[1]
        previous_year = str(previous_date).split('-')[0]
        previous_date = f'{previous_month}/01/{previous_year}'
    
    return previous_date, today_date

