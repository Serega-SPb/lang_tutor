import os

TEMPLATES_DIR = 'templates'
CUR_DIR = os.path.abspath(os.path.dirname(__file__))


def get_page(name, context=None):
    file_path = os.path.join(CUR_DIR, TEMPLATES_DIR, f'{name}.html')
    if not os.path.isfile(file_path):
        return None

    with open(file_path, 'r', encoding='utf-8') as reader:
        page = reader.read()

    page = page.replace('\n', '')
    return eval(f"f'{page}'", {}, context)
