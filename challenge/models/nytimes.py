from robocorp import log
from robocorp import http
from RPA.Browser.Selenium import Selenium
from utils import lib

import time


class NyTimes:
    url = "https://nytimes.com/"


    def __init__(self, env:str, search_phrase:str):
        self.browser = Selenium()
        self.env = env
        self.search_phrase = search_phrase


    def open(self):
        """
            Open the nytimes website using url and search phrase
        """
        if not self.search_phrase:
            msg_error = 'search_phrase not specified!'
            log.exception(msg_error)
            raise Exception(msg_error)
        elif not isinstance(self.search_phrase, str):
            msg_error = f'search_phrase not str! type(search_phrase): {type(self.search_phrase)}'
            log.exception(msg_error)
            raise Exception(msg_error)
        
        search_query = self.search_phrase.replace(' ', '%20')
        url_search = f'{self.url}/search?query={search_query}&sort=newest'

        try:
            self.browser.open_available_browser(url=url_search)
        except Exception as error:
            msg_error = f'error opening available browser. error: {error}'
            log.exception(msg_error)
            raise Exception(msg_error)
        
        close_popup_button_locator = "xpath://button[contains(text(), 'Continue')]"
        try:
            self.browser.wait_until_element_is_visible(locator=close_popup_button_locator)
            webelement = self.browser.get_webelement(locator=close_popup_button_locator)
            self.browser.click_button(locator=webelement)
        except:
            log.warn("Could not close initial popup window!")
            pass

        page_locator = 'id:searchTextField'
        try:
            self.browser.find_element(locator=page_locator)
        except Exception as error:
            msg_error = f'error: {error} while finding element {page_locator} after opening page, page may not be available!'
            log.exception(msg_error)
            raise Exception(msg_error)
        

    def apply_date(self, previous_date:str, today_date:str):
        """
            Apply date filter
        """
        elements_to_interact = {
            'date_range': "xpath://button//label[contains(text(), 'Date Range')]",
            'specific_dates': "xpath://button[contains(text(), 'Specific Dates')]",
            'start_date': "id:startDate",
        }

        for element in elements_to_interact.values():
            try:
                webelement = self.browser.get_webelement(locator=element)
                self.browser.click_button_when_visible(locator=webelement)
            except Exception as error:
                msg_error = f'error: {error} interacting with element: {element}'
                log.exception(msg_error)
                raise Exception(msg_error)
        
        elements_to_interact = {
            'start_date': "id:startDate",
            'end_date': "id:endDate",
        }

        for key_element in elements_to_interact.keys():
            element = elements_to_interact[key_element] 
            if key_element == 'start_date':
                try:
                    self.browser.input_text(element, previous_date)
                except Exception as error:
                    msg_error = f'error: {error} interacting with element: {element}'
                    log.exception(msg_error)
                    raise Exception(msg_error)
            elif key_element == 'end_date':
                try:
                    webelement = self.browser.get_webelement(locator=element)
                    self.browser.click_button_when_visible(locator=webelement)
                    time.sleep(1)
                    self.browser.input_text(webelement, today_date)
                    self.browser.press_keys(webelement, 'ENTER')
                except Exception as error:
                    msg_error = f'error: {error} interacting with element: {element}'
                    log.exception(msg_error)
                    raise Exception(msg_error)
                
    
    def apply_filter(self, type_filter:str, filters:list[str]):
        """
            Apply specific filter (Section or Type)
        """
        if not isinstance(type_filter, str):
            msg_error = f'type_filter is not str. type(type_filter): {type(type_filter)}'
            log.exception(msg_error)
            raise Exception(msg_error)
        elif type_filter.lower() != 'section' and type_filter.lower() != 'type':
            msg_error = f'type_filter unknown. type_filter: {type_filter}'
            log.exception(msg_error)
            raise Exception(msg_error)
        
        if not filters or len(filters) == 0:
            msg = 'no filters to apply!'
            log.warn(msg)
            return msg

        type_filter_button_locator = f"xpath://button//label[contains(text(), '{type_filter.capitalize()}')]"
        try:    
            self.browser.wait_until_element_is_enabled(locator=type_filter_button_locator)
            button_type_filter = self.browser.get_webelement(locator=type_filter_button_locator)
            self.browser.click_element(locator=button_type_filter)
            time.sleep(1)
        except Exception as error:
            msg_error = f"error: {error} clicking element. locator: {type_filter_button_locator}"
            log.exception(msg_error)
            raise Exception(msg_error)

        for filter in filters:
            xpath_element = f"xpath://span[contains(text(), '{filter.capitalize()}')]"
            try:
                button_filter = self.browser.get_webelement(locator=xpath_element)
                self.browser.click_element(locator=button_filter)
            except Exception as error:
                msg_error = f"error: {error}\nfilter: {filter}\nlocator: {xpath_element}"
                log.warn(msg_error)
                continue
                        
        try:    
            button_type_filter = self.browser.get_webelement(locator=type_filter_button_locator)
            self.browser.click_element(locator=button_type_filter)
        except Exception as error:
            msg_error = f"error: {error} clicking element. locator: {type_filter_button_locator}"
            log.exception(msg_error)
            raise Exception(msg_error)
        

    def apply_filters(self, date_range:int, types:list[str], sections:list[str]):
        """
            Apply all filters
        """
        filters = [
            'date_range',
            'section',
            'type',
        ]
        
        for filter in filters:
            if filter == 'date_range':
                previous_date, today_date = lib.get_previous_and_today_date(date_range=date_range)
                self.apply_date(previous_date=previous_date, today_date=today_date)
            elif filter == 'section':
                self.apply_filter(type_filter=filter, filters=sections)
            elif filter == 'type':
                self.apply_filter(type_filter=filter, filters=types)

        submit_button_locator = 'xpath://*[@id="site-content"]/div/div[1]/div[1]/form/div[1]/button'
        try:
            submit_button = self.browser.get_webelement(locator=submit_button_locator)
            self.browser.click_button_when_visible(locator=submit_button)
        except Exception as error:
            msg_error = f'error: {error} submitting filters. locator: {submit_button_locator}'
            log.exception(msg_error)
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
            log.exception(msg_error)
            raise Exception(msg_error)
        
        if results_number == '0':
            msg = f'There is no results for this search. results: {results} results_number: {results_number}'
            log.info(msg)
            return 0
            
        self.show_more_results_if_possible()
         
        table_results_locator = 'tag:ol'
        try:
            table_elements = self.browser.get_webelements(locator=table_results_locator)
        except Exception as error:
            msg_error = f'error getting table results elements. error: {error} locator: {table_results_locator}'
            log.exception(msg_error)
            raise Exception(msg_error)

        search_values = dict()
        for table in table_elements:
            list_itens_locator = 'tag:li'
            try: 
                list_elements = self.browser.find_elements(locator=list_itens_locator, parent=table)
                len_list = len(list_elements)
            except Exception as error:
                msg_error = f'error getting elements inside table. error: {error} locator: {list_itens_locator}'
                log.exception(msg_error) 
                raise Exception(msg_error)
            
            if len_list == 0:
                continue

            news_index = 0
            for list_item in list_elements:
                news_index += 1
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
                        log.warn(f'Could not find element: {element}')
                        continue

                    if key_element == 'date':
                        try:
                            date = element_finded[0].text
                        except:
                            log.warn(f'Could not get date from element key_element: {key_element}')
                            continue
                    elif key_element == 'title':
                        try:
                            title = element_finded[0].text
                        except:
                            log.warn(f'Could not get title from element key_element: {key_element}')
                            continue
                    elif key_element == 'description':
                        try:
                            description = element_finded[1].text
                        except:
                            log.warn(f'Could not get description from element key_element: {key_element}')
                            continue
                    elif key_element == 'img':
                        try:
                            src_img = self.browser.get_element_attribute(element_finded[0], 'src')
                        except:
                            log.warn(f'Could not get src from img key_element: {key_element}')
                            continue

                try:
                    if self.env == "dev":
                        img_filename = None
                    else:
                        img_path = str(src_img.split('images')[1]).split('?')[0]
                        img_filename = img_path.split('/')[-1]
                        http.download(url=src_img, target_file=f'output/{img_filename}')
                except Exception as error:
                    log.warn(f'error: {error} dowloading image')
                    img_filename = None
        
                count_phrase = lib.count_search_phrases(title=title, description=description, phrase=self.search_phrase)
                has_money = lib.contains_money(title=title, description=description)

                search_values[news_index] = {
                    'date': date,
                    'title': title,
                    'description': description,
                    'img_filename': img_filename,
                    'count_phrase': count_phrase,
                    'has_money': has_money,
                }

        return search_values


    def show_more_results_if_possible(self, timeout:int=15):
        """
            This function uses the show more button to show more results to the search
        """
        show_more_button_locator = "class:css-vsuiox"
        results_locator = 'tag:h4'

        show_more_results = True
        while show_more_results:
            try:
                results_before_click = len(self.browser.find_elements(locator=results_locator))
            except:
                results_before_click = None

            try:
                button_class = self.browser.get_webelements(locator=show_more_button_locator)
                if not button_class:
                    break
                # MOST OF THE TIME THIS BUTTON STOPS WORKING FOR A WHILE AFTER TOO MANY CLICKS
                button_element = self.browser.get_webelement('tag:button', parent=button_class[0])
                self.browser.wait_until_element_is_enabled(locator=button_element, timeout=timeout)
                self.browser.click_element(locator=button_element)
                # TRIED TO WAIT SOME SECONDS AFTER EVERY CLICK
                time.sleep(1)
            except:
                pass

            try:
                results_after_click = len(self.browser.find_elements(locator=results_locator))
            except:
                results_after_click = None

            if results_after_click == results_before_click:
                show_more_results = False

        return results_after_click
    
