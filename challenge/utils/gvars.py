env = "dev"

excel_path = "output/excel/output.xlsx"
output_json_path = "output/data.json"
url_nytimes = "https://nytimes.com/"

sections_type = {
    '1': 'Arts', 
    '2': 'Business',
    '3': 'Movies',
    '4': 'New York',
    '5': 'Opinion',
    '6': 'Sports',
    '7': 'Travel',
    '8': 'U.S.',
    '9': 'World',
}

types_categories = {
    '1': 'Article',
    '2': 'Audio',
    '3': 'Image Slideshow',
    '4': 'Interative Graphics',
    '5': 'Recipe',
    '6': 'Video',
    '7': 'Wirecutterarticle',
}

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
