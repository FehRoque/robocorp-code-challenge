from robocorp import excel

from utils import gvars
import os

# TODO: CREATE CLASS FOR THIS MODEL

def set_headers(*, worksheet):
    headers = gvars.excel_headers
    for header in headers:
        values_header = headers[header] 
        worksheet.set_cell_value(row=1, column=values_header['column'], value=values_header['value'])


def fill_excel(*, phrase, data, excel_name, excel_folder):
    excel_path = f'{excel_folder}{excel_name}'
    if os.path.isfile(excel_path):
        wb = excel.open_workbook(path=excel_path)
        move_excel = False
    else:
        file = excel_name.split('.')
        wb = excel.create_workbook(fmt=file[1], sheet_name=phrase)
        move_excel = True

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
            return (-99, f'error: {error} saving excel file excel_path: {excel_path}')
    else:
        try:
            wb.save(name=excel_name, overwrite=True)
        except Exception as error:
            return (-99, f'error: {error} saving excel file excel_name: {excel_name}')
        try:
            os.makedirs(excel_folder)
        except:
            pass
        try:
            os.rename(excel_name, excel_path)
        except Exception as error:
            return(0, f'failed to move excel file. error: {error}')

    return (1, 'excel filled successfully')

