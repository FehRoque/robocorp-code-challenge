from robocorp import http
from RPA.Browser.Selenium import Selenium

from utils import lib

import time


# TODO: Create class and implement its methods using these functions 


def open_nytimes(*, browser:Selenium, url_nytimes:str, search_phrase:str):
    """
    """
    if not url_nytimes:
        return (-1, 'url_nytimes not specified!')
    elif not isinstance(url_nytimes, str):
        return (-1, f'url_nytimes not str! type(url_nytimes): {type(url_nytimes)}')
    
    search = search_phrase.replace(' ', '%20')
    url_search = f'{url_nytimes}/search?query={search}&sort=newest'

    try:
        browser.open_available_browser(url=url_search)
    except Exception as error:
        return (-2, f'error opening available browser. error: {error}')
    
    try:
        button_locator = "xpath://button[contains(text(), 'Continue')]"
        browser.wait_until_element_is_visible(locator=button_locator, timeout=5)

        webelement = browser.get_webelement(locator=button_locator)
        browser.click_button(locator=webelement)
    except:
        pass

    try:
        page_locator = 'id:searchTextField'
        browser.find_element(locator=page_locator)
    except Exception as error:
        return (-99, f'Exception while finding element {page_locator}, page may not be available! error: {error}')
    
    return (1, 'browser opened successfully!')


def apply_filter(*, browser:Selenium, filter_type:str, filters:list[str]):
    """
    """
    if not isinstance(filter_type, str):
        return (-1, f'filter_type is not str. type(filter_type): {type(filter_type)}' )
    elif filter_type.lower() != 'section' and filter_type.lower() != 'type':
        return (-1, f'filter_type unknown. filter_type: {filter_type}' )
    
    if not isinstance(filters, list):
        return (-1, f'filters is not list!. type(filters): {type(filters)}' )
    elif not filters or len(filters) == 0:
        return (0, f'no filters to apply. filters: {filters}')

    locator_filter_type_button = f"xpath://button//label[contains(text(), '{filter_type.capitalize()}')]"
    try:    
        browser.wait_until_element_is_enabled(locator=locator_filter_type_button, timeout=15)
        webelement = browser.get_webelement(locator=locator_filter_type_button)
        browser.click_element(locator=webelement)
    except Exception as error:
        return (-1, f"error: {error} filter_type: {filter_type} locator: {locator_filter_type_button}")

    for section in filters:
        xpath_element = f"xpath://span[contains(text(), '{section.capitalize()}')]"
        try:
            webelement = browser.get_webelement(locator=xpath_element)
            browser.click_element(locator=webelement)
        except:
            continue
                    
    try:    
        webelement = browser.get_webelement(locator=locator_filter_type_button)
        browser.click_element(locator=webelement)
    except:
        return (-2, f"error clicking '{filter_type}' element. locator: {locator_filter_type_button}")
    
    return (1, 'filter applied OK')


def apply_filters(*, browser:Selenium, date_range:int, categories:list[str], sections:list[str]):
    """
    """
    filters = [
        'date_range',
        'section',
        'type',
    ]
    
    for filter in filters:
        if filter == 'date_range':
            previous_date, today_date = lib.get_previous_and_today_date(date_range=date_range)
            filter_applied = filter_dates(browser=browser, previous_date=previous_date, today_date=today_date)
        elif filter == 'section':
            filter_applied = apply_filter(browser=browser, filter_type=filter, filters=sections)
        elif filter == 'type':
            filter_applied = apply_filter(browser=browser, filter_type=filter, filters=categories)
        
        if filter_applied[0] < 0:
            return (-1, f'error applying filter. filter: {filter} filter_applied: {filter_applied}')

    button_locator = 'xpath://*[@id="site-content"]/div/div[1]/div[1]/form/div[1]/button'
    try:
        webelement = browser.get_webelement(locator=button_locator)
        browser.click_button_when_visible(locator=webelement)
    except Exception as error:
        return (-2, f'error submitting filters. locator: {button_locator} error: {error}')
    
    return (1, 'filters applied OK')


def filter_dates(*, browser:Selenium, previous_date:str, today_date:str):
    """
    """
    elements = {
        'date_range': "xpath://button//label[contains(text(), 'Date Range')]",
        'specific_dates': "xpath://button[contains(text(), 'Specific Dates')]",
        'start_date': "id:startDate",
    }

    for element in elements.values():
        try:
            webelement = browser.get_webelement(locator=element)
            browser.click_button_when_visible(locator=webelement)
        except Exception as error:
            return (-2, f'error: {error} element: {element} ')
    
    elements = {
        'start_date': "id:startDate",
        'end_date': "id:endDate",
    }

    for key_element in elements.keys():
        element = elements[key_element] 
        if key_element == 'start_date':
            try:
                browser.input_text(element, previous_date)
            except Exception as error:
                return (-2, f'error: {error} element: {element} ')
        elif key_element == 'end_date':
            try:
                webelement = browser.get_webelement(locator=element)
                browser.click_button_when_visible(locator=webelement)

                browser.input_text(webelement, today_date)
                browser.press_keys(webelement, 'ENTER')
            except Exception as error:
                return (-2, f'error: {error} element: {element} ')
            
    return (1, 'date filters OK')


def get_search_results(*, browser:Selenium, search_phrase:str):
    """
    """
    button_locator = "xpath://button[contains(text(), 'Show More')]"
    try:
        show_more_button = browser.get_webelement(button_locator)
        show_more = True
    except:
        show_more = False

    while show_more:
        try:
            show_more_button = browser.get_webelement(button_locator)
            browser.click_element_when_clickable(show_more_button, timeout=3)
            time.sleep(1)
        except:
            show_more = False

    results_locator = "xpath://p[contains(text(), 'results for')]"
    try:
        browser.wait_until_page_contains_element(locator=results_locator)
        webelement = browser.get_webelement(locator=results_locator)
        results = webelement.text
        results_number = results.split()[1]
    except Exception as error:
        return (-1, f'error getting results. error: {error} locator: {results_locator}')
    
    if int(results_number) < 1:
        return (0, f'There is no results for this search. results: {results} results_number: {results_number}')

    table_results_locator = 'tag:ol'
    try:
        browser.wait_until_page_contains_element(locator=table_results_locator)
        table_elements = browser.get_webelements(locator=table_results_locator)
    except Exception as error:
        return (-2, f'error getting table results elements. error: {error} locator: {table_results_locator}')

    values_search = dict()
    for table in table_elements:
        news = 0

        list_elements = browser.find_elements(locator='tag:li', parent=table)
        for list_item in list_elements:
            elements = {
                'date': 'tag:span',
                'title': 'tag:h4',
                'description': 'tag:p',
                'img': 'tag:img',
            }

            for key_element in elements.keys():
                element = elements[key_element]

                element_finded = browser.find_elements(locator=element, parent=list_item)
                if not element_finded:
                    break

                if key_element == 'date':
                    try:
                        date = element_finded[0].text
                    except:
                        date = 'error'
                elif key_element == 'title':
                    try:
                        title = element_finded[0].text
                    except:
                        title = 'error'
                elif key_element == 'description':
                    try:
                        description = element_finded[1].text
                    except:
                        description = 'error'
                elif key_element == 'img':
                    try:
                        src_img = browser.get_element_attribute(element_finded[0], 'src')
                    except:
                        src_img = 'error'

            if not element_finded:
                continue

            if src_img == 'error':
                img_filename = 'error'
            else:
                try:
                    img_path = str(src_img.split('images')[1]).split('?')[0]
                    img_filename = img_path.split('/')[-1]
                    http.download(url=src_img, target_file=f'output/images/{img_filename}')
                except:
                    img_filename = 'error'

            count_phrase = lib.count_search_phrases(title=title, description=description, phrase=search_phrase)
            has_money = lib.contains_money(title=title, description=description)

            news += 1
            values_search[news] = {
                'date': date,
                'title': title,
                'description': description,
                'img_filename': img_filename,
                'count_phrase': count_phrase,
                'has_money': has_money,
            }

    return values_search

