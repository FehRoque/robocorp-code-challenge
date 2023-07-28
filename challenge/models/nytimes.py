from robocorp import http
from RPA.Browser.Selenium import Selenium
from utils import lib

import time


class NyTimes(Selenium):
    url = "https://nytimes.com/"


    def __init__(self, search_phrase:str):
        super()
        self.browser = Selenium()
        self.search_phrase = search_phrase


    def open(self):
        """
            Open the nytimes website using url and search phrase
        """
        if not self.search_phrase:
            msg_error = 'search_phrase not specified!'
            raise Exception(msg_error)
        elif not isinstance(self.search_phrase, str):
            msg_error = f'search_phrase not str! type(search_phrase): {type(self.search_phrase)}'
            raise Exception(msg_error)
        
        search_query = self.search_phrase.replace(' ', '%20')
        url_search = f'{self.url}/search?query={search_query}&sort=newest'

        try:
            self.browser.open_available_browser(url=url_search)
        except Exception as error:
            msg_error = f'error opening available browser. error: {error}'
            raise Exception(msg_error)
        
        close_popup_button_locator = "xpath://button[contains(text(), 'Continue')]"
        try:
            self.browser.wait_until_element_is_visible(locator=close_popup_button_locator)
            webelement = self.browser.get_webelement(locator=close_popup_button_locator)
            self.browser.click_button(locator=webelement)
        except:
            pass

        page_locator = 'id:searchTextField'
        try:
            self.browser.find_element(locator=page_locator)
        except Exception as error:
            msg_error = f'Exception while finding element {page_locator}, page may not be available! error: {error}'
            raise Exception(msg_error)
        

    def apply_date(self, previous_date:str, today_date:str):
        """
            Apply date filter
        """
        elements = {
            'date_range': "xpath://button//label[contains(text(), 'Date Range')]",
            'specific_dates': "xpath://button[contains(text(), 'Specific Dates')]",
            'start_date': "id:startDate",
        }

        for element in elements.values():
            try:
                webelement = self.browser.get_webelement(locator=element)
                self.browser.click_button_when_visible(locator=webelement)
            except Exception as error:
                msg_error = f'error: {error} element: {element}'
                raise Exception(msg_error)
        
        elements = {
            'start_date': "id:startDate",
            'end_date': "id:endDate",
        }

        for key_element in elements.keys():
            element = elements[key_element] 
            if key_element == 'start_date':
                try:
                    self.browser.input_text(element, previous_date)
                except Exception as error:
                    msg_error = f'error: {error} element: {element}'
                    raise Exception(msg_error)
            elif key_element == 'end_date':
                try:
                    webelement = self.browser.get_webelement(locator=element)
                    self.browser.click_button_when_visible(locator=webelement)

                    self.browser.input_text(webelement, today_date)
                    self.browser.press_keys(webelement, 'ENTER')
                except Exception as error:
                    msg_error = f'error: {error} element: {element}'
                    raise Exception(msg_error)
                

    def apply_filter(self, type_filter:str, filters:list[str]):
        """
            Apply specific filter (Section or Type)
        """
        if not isinstance(type_filter, str):
            msg_error = f'type_filter is not str. type(type_filter): {type(type_filter)}'
            raise Exception(msg_error)
        elif type_filter.lower() != 'section' and type_filter.lower() != 'type':
            msg_error = f'type_filter unknown. type_filter: {type_filter}'
            raise Exception(msg_error)
        
        if not filters or len(filters) == 0:
            msg= f'no filters to apply. filters: {filters}'
            return msg

        type_filter_button_locator = f"xpath://button//label[contains(text(), '{type_filter.capitalize()}')]"
        try:    
            self.browser.wait_until_element_is_enabled(locator=type_filter_button_locator, timeout=15)
            button_type_filter = self.browser.get_webelement(locator=type_filter_button_locator)
            self.browser.click_element(locator=button_type_filter)
        except Exception as error:
            msg_error = f"error: {error} clicking element. locator: {type_filter_button_locator}"
            raise Exception(msg_error)

        for filter in filters:
            xpath_element = f"xpath://span[contains(text(), '{filter.capitalize()}')]"
            try:
                button_filter = self.browser.get_webelement(locator=xpath_element)
                self.browser.click_element(locator=button_filter)
            except:
                continue
                        
        try:    
            button_type_filter = self.browser.get_webelement(locator=type_filter_button_locator)
            self.browser.click_element(locator=button_type_filter)
        except Exception as error:
            msg_error = f"error: {error} clicking element. locator: {type_filter_button_locator}"
            raise Exception(msg_error)
        

    def apply_filters(self, date_range:int, types:list[str], sections:list[str]):
        """
            Apply all filters
        """
        type_filters = [
            'date_range',
            'section',
            'type',
        ]
        
        for filter in type_filters:
            if filter == 'date_range':
                previous_date, today_date = lib.get_previous_and_today_date(date_range=date_range)
                self.apply_date(previous_date=previous_date, today_date=today_date)
            elif filter == 'section':
                self.apply_filter(type_filter=filter, filters=sections)
            elif filter == 'type':
                self.apply_filter(type_filter=filter, filters=types)

        button_locator = 'xpath://*[@id="site-content"]/div/div[1]/div[1]/form/div[1]/button'
        try:
            webelement = self.browser.get_webelement(locator=button_locator)
            self.browser.click_button_when_visible(locator=webelement)
        except Exception as error:
            msg_error = f'error submitting filters. locator: {button_locator} error: {error}'
            raise Exception(msg_error)
        

    def get_results(self):
        """
            Get all of the results for that search phrase
        """
        results_locator = "xpath://p[contains(text(), 'results for')]"
        try:
            self.browser.wait_until_page_contains_element(locator=results_locator)
            webelement = self.browser.get_webelement(locator=results_locator)
            results = webelement.text
            results_number = results.split()[1]
        except Exception as error:
            msg_error = f'error getting results for this search. error: {error} locator: {results_locator}'
            raise Exception(msg_error)
        
        if results_number == '0':
            msg = f'There is no results for this search. results: {results} results_number: {results_number}'
            return (0, msg)
            
        show_more_button_locator = "xpath://button[contains(text(), 'Show More')]"
        show_more_results = True

        while show_more_results:
            try:
                results_before_click = self.browser.find_elements(locator='tag:h4')
            except:
                results_before_click = None
            try:
                self.browser.click_element(locator=show_more_button_locator)
                time.sleep(1)
            except:
                show_more_results = False
            try:
                results_after_click = self.browser.find_elements(locator='tag:h4')
            except:
                results_after_click = None
            if results_after_click == results_before_click:
                show_more_results = False

        table_results_locator = 'tag:ol'
        try:
            table_elements = self.browser.get_webelements(locator=table_results_locator)
        except Exception as error:
            msg_error = f'error getting table results elements. error: {error} locator: {table_results_locator}'
            raise Exception(msg_error)

        search_values = dict()
        for table in table_elements:
            list_itens_locator = 'tag:li'
            try: 
                list_elements = self.browser.find_elements(locator=list_itens_locator, parent=table)
                len_list = len(list_elements)
            except Exception as error:
                msg_error = f'error getting elements inside table. error: {error} locator: {list_itens_locator}' 
                raise Exception(msg_error)
            
            if len_list == 0:
                continue

            news_index = 0
            for list_item in list_elements:
                elements_to_interact = {
                    'date': 'tag:span',
                    'title': 'tag:h4',
                    'description': 'tag:p',
                    'img': 'tag:img',
                }

                for key_element in elements_to_interact.keys():
                    element = elements_to_interact[key_element]
                    try:
                        element_finded = self.browser.find_elements(locator=element, parent=list_item)
                    except:
                        element_finded = None

                    if key_element == 'date':
                        try:
                            date = element_finded[0].text
                        except:
                            date = None
                    elif key_element == 'title':
                        try:
                            title = element_finded[0].text
                        except:
                            title = None
                    elif key_element == 'description':
                        try:
                            description = element_finded[1].text
                        except:
                            description = None
                    elif key_element == 'img':
                        try:
                            src_img = self.browser.get_element_attribute(element_finded[0], 'src')
                        except:
                            src_img = None

                if src_img:
                    try:
                        img_path = str(src_img.split('images')[1]).split('?')[0]
                        img_filename = img_path.split('/')[-1]
                        http.download(url=src_img, target_file=f'output/images/{img_filename}')
                    except:
                        img_filename = None
                else:
                    img_filename = None

                count_phrase = lib.count_search_phrases(title=title, description=description, phrase=self.search_phrase)
                has_money = lib.contains_money(title=title, description=description)

                news_index += 1
                search_values[news_index] = {
                    'date': date,
                    'title': title,
                    'description': description,
                    'img_filename': img_filename,
                    'count_phrase': count_phrase,
                    'has_money': has_money,
                }

        return search_values

