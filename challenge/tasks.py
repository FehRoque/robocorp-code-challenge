from robocorp import workitems
from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium

from models import excel, nytimes
from utils import gvars

import json


def main(*, browser:Selenium, config_data:dict):
    url_nytimes = gvars.url_nytimes
    search_phrase = config_data['search_phrase']

    nytimes_opened = nytimes.open_nytimes(
        browser=browser,
        url_nytimes=url_nytimes,
        search_phrase=search_phrase,
    )
    
    if nytimes_opened[0] < 0:
        return (-1, nytimes_opened[1])

    filters_applied = nytimes.apply_filters(
        browser=browser,
        date_range=config_data['date_range'], 
        categories=config_data['categories'], 
        sections=config_data['sections']
    )

    if filters_applied[0] < 0:
        return (-2, filters_applied[1])

    search_results = nytimes.get_search_results(
        browser=browser,
        search_phrase=search_phrase
    )

    if isinstance(search_results, tuple) and search_results[0] == 0:
        return (0, 'no results for the search phrase')
    elif not isinstance(search_results, dict):
        return (-3, search_results[1])
    
    output_json_path = gvars.output_json_path
    json_file = open(output_json_path, "w")

    json.dump(search_results, json_file, indent=2)
    json_file.close()

    excel_path = gvars.excel_path
    path = excel_path.split('/')
    
    excel_name = path[-1]
    excel_folder = excel_path.replace(excel_name, '')

    excel_filled = excel.fill_excel(
        phrase=search_phrase, 
        data=search_results, 
        excel_name=excel_name, 
        excel_folder=excel_folder
    )

    if excel_filled[0] < 0:
        return (-4, excel_filled[1])
    
    return (1, 'Success')


# TODO: USE OOP


@task
def solve_challenge():
    env = gvars.env
    if env == "dev":
        try:
            with open("config.json", "r") as f:
                config_data = json.load(f)
        except Exception as error:
            msg_error = f'Error reading configuration file. error: {error}'
            raise Exception(msg_error)
    else:
        config_data = dict()
        for item in workitems.inputs:
            try:
                config_data["categories"] = item.payload["categories"]
                config_data["date_range"] = item.payload["date_range"]
                config_data["search_phrase"] = item.payload["search_phrase"]
                config_data["sections"] = item.payload["sections"]
                item.done()
            except KeyError as error:
                item.fail(code="MISSING_VALUE", message=str(error))
                msg_error = f"MISSING_VALUE error: {error}"
                raise Exception(msg_error)

    try:
        browser = Selenium()
        main(browser=browser, config_data=config_data)
    except Exception as error:
        msg_error = f'Exception while solving challenge. error: {error}'
        raise Exception(msg_error)
    finally:
        browser.close_all_browsers()
            