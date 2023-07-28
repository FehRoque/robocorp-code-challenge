from robocorp import excel
from robocorp.excel.worksheet import Worksheet

import os


class Excel:
    path_excel = "output/excel/output.xlsx"
    path = path_excel.split('/')
    
    excel_name = path[-1]
    excel_folder = path_excel.replace(excel_name, '')
    
    excel_headers = {
        'news_date': {
            'column': 1,
            'value': 'News Date',
        },
        'news_title': {
            'column': 2,
            'value': 'News Title',
        },
        'news_description': {
            'column': 3,
            'value': 'News Description',
        },
        'news_picture_filename': {
            'column': 4,
            'value': 'Picture Filename',
        },
        'phrase_count': {
            'column': 5,
            'value': 'Phrase Count',
        },
        'contains_money': {
            'column': 6,
            'value': 'Contains Money',
        },
    }


    def __init__(self) -> None:
        pass


    def set_headers(self, worksheet: Worksheet):
        """ 
            Set the excel headers
        """
        try:
            for header in self.excel_headers:
                values_header = self.excel_headers[header] 
                worksheet.set_cell_value(
                    row=1, 
                    column=values_header['column'], 
                    value=values_header['value']
                )
        except Exception as error:
            msg_error = f'Error setting cell value for the header. error: {error}'
            raise Exception(msg_error)


    def fill_excel(self, data:dict, search_phrase:str):
        """ 
            Fill excel with data
        """    
        excel_path = f'{self.excel_folder}{self.excel_name}'
        if os.path.isfile(excel_path):
            wb = excel.open_workbook(path=excel_path)
        else:
            file = self.excel_name.split('.')
            wb = excel.create_workbook(fmt=file[1], sheet_name=search_phrase)

        worksheet = wb.create_worksheet(name=search_phrase, exist_ok=True)
        self.set_headers(worksheet=worksheet)

        for news in data.keys():
            try:
                value_news = data[news]
            except:
                continue

            values = [
                value_news['date'],
                value_news['title'],
                value_news['description'],
                value_news['img_filename'],
                value_news['count_phrase'],
                value_news['has_money'],
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
                raise Exception(msg_error)
        else:
            try:
                wb.save(name=self.excel_name, overwrite=True)
            except Exception as error:
                msg_error = f'error: {error} saving excel file excel_name: {self.excel_name}'
                raise Exception(msg_error)
            try:
                os.makedirs(self.excel_folder)
            except:
                pass
            try:
                os.rename(self.excel_name, excel_path)
            except Exception as error:
                msg = f'failed to move excel file. error: {error}'
                return(0, msg)

