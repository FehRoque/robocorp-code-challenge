from robocorp import excel
from robocorp.excel.worksheet import Worksheet

from utils import gvars

import os


# TODO: Create class and implement its methods using these functions 


def set_headers(*, worksheet: Worksheet):
    """ Set the excel headers
        inputs: workheet object
        outputs: ([status_code, status_message])
            status_code == 1  == success
            status_code < 0   == error
                status_code -1: 'error getting excel headers' 
                status_code -2: 'error setting excel headers'
    """
    try:
        headers = gvars.excel_headers
    except: 
        msg_error = f'Error setting cell value for the header. error: {error}'
        return (-1, msg_error)

    try:
        for header in headers:
            values_header = headers[header] 
            worksheet.set_cell_value(row=1, column=values_header['column'], value=values_header['value'])
    except Exception as error:
        msg_error = f'Error setting cell value for the header. error: {error}'
        return (-2, msg_error)

    return (1, 'headers set correctly')


def fill_excel(*, phrase:str, data:dict, excel_name:str, excel_folder:str):
    """ Fill excel with input values
        inputs: phrase, data, excel_name, excel_folder
        outputs: ([status_code, status_message])
            status_code == 1  == success
            status_code < 0   == error
    """    
    excel_path = f'{excel_folder}{excel_name}'
    if os.path.isfile(excel_path):
        wb = excel.open_workbook(path=excel_path)
    else:
        file = excel_name.split('.')
        wb = excel.create_workbook(fmt=file[1], sheet_name=phrase)

    worksheet = wb.create_worksheet(name=phrase, exist_ok=True)
    set_headers(worksheet=worksheet)

    for news in data.keys():
        try:
            news_value = data[news]
        except:
            continue

        values = [
            news_value['date'],
            news_value['title'],
            news_value['description'],
            news_value['img_filename'],
            news_value['count_phrase'],
            news_value['has_money'],
        ] 

        row = int(news) + 1
        column = 1

        for value in values:
            try:
                worksheet.set_cell_value(row=row, column=column, value=value)
            except:
                worksheet.set_cell_value(row=row, column=column, value='error')
            column += 1

    if os.path.isfile(excel_path):
        try:
            wb.save(name=excel_path, overwrite=True)
        except Exception as error:
            msg_error = f'error: {error} saving excel file excel_path: {excel_path}'
            return (-99, msg_error)
    else:
        try:
            wb.save(name=excel_name, overwrite=True)
        except Exception as error:
            msg_error = f'error: {error} saving excel file excel_name: {excel_name}'
            return (-99, msg_error)
        try:
            os.makedirs(excel_folder)
        except:
            pass
        try:
            os.rename(excel_name, excel_path)
        except Exception as error:
            msg_error = f'failed to move excel file. error: {error}'
            return(0, msg_error)

    return (1, 'excel filled successfully')

