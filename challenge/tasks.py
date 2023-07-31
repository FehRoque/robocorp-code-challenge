from robocorp import log
from robocorp import workitems
from robocorp.tasks import task

from models.excel import Excel
from models.nytimes import NyTimes

import json


def main(*, env:str, work_items:dict):
    log.info("Starting main...")

    ny = NyTimes(
        env=env, 
        search_phrase=work_items['search_phrase']
    )
    
    log.info("Opening nytimes...")
    ny.open()

    log.info("Applying filters...")
    ny.apply_filters(
        date_range=work_items['date_range'], 
        types=work_items['types'], 
        sections=work_items['sections']
    )

    log.info("Getting results...")
    results = ny.get_results()

    if isinstance(results, tuple) and results[0] == 0:
        log.warn("No results found...")
        return 0

    output_json_path = "output/output.json"
    json_file = open(output_json_path, "w")

    json.dump(results, json_file, indent=2)
    json_file.close()

    excel = Excel()

    log.info("Filling excel with results...")
    excel_filled = excel.fill_excel(
        data=results, 
        search_phrase=work_items['search_phrase']
    )

    return 1


@task
def solve_challenge():
    log.info("Starting task...")
    try:
        with open("config.json", "r") as f:
            config_data = json.load(f)
    except Exception as error:
        msg_error = f'Error reading configuration file. error: {error}'
        log.exception(msg_error)
        raise Exception(msg_error)
    
    env = config_data["env"]
    if env == "dev":
        work_items = config_data["work_items"]
    else:
        work_items = dict()
        for item in workitems.inputs:
            keys = config_data["keys"]
            for key in keys:
                try:
                    work_items[key] = item.payload[key]
                except KeyError as error:
                    log.warn(f"Error getting key value for key {key}: {error}")
                    work_items[key] = None
            item.done()

    try:
        main(env=env, work_items=work_items)
    except Exception as error:
        msg_error = f'Exception while solving challenge. error: {error}'
        log.exception(msg_error)
        raise Exception(msg_error)
            