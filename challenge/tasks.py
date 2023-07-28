from robocorp import workitems
from robocorp.tasks import task

from models.excel import Excel
from models.nytimes import NyTimes

import json


def main(*, work_items:dict):
    ny = NyTimes(search_phrase=work_items['search_phrase'])
    ny.open()
    
    ny.apply_filters(
        date_range=work_items['date_range'], 
        categories=work_items['categories'], 
        sections=work_items['sections']
    )

    results = ny.get_results()
    if isinstance(results, tuple) and results[0] == 0:
        return 0

    output_json_path = "output/data.json"
    json_file = open(output_json_path, "w")

    json.dump(results, json_file, indent=2)
    json_file.close()

    excel = Excel()
    excel.fill_excel(data=results, search_phrase=work_items['search_phrase'])
    
    return 1


@task
def solve_challenge():
    try:
        with open("config.json", "r") as f:
            config_data = json.load(f)
    except Exception as error:
        msg_error = f'Error reading configuration file. error: {error}'
        raise Exception(msg_error)
    
    env = config_data["env"]
    if env == "dev":
        work_items = config_data["work_items"]
    else:
        work_items = dict()
        for item in workitems.inputs:
            keys = ['categories', 'date_range', 'search_phrase', 'sections']
            for key in keys:
                try:
                    work_items[key] = item.payload[key]
                except KeyError as error:
                    work_items[key] = None
            item.done()

    try:
        main(work_items=work_items)
    except Exception as error:
        msg_error = f'Exception while solving challenge. error: {error}'
        raise Exception(msg_error)
            