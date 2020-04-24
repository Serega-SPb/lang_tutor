import os
import zipfile

from core.decorators import try_except_wrapper


@try_except_wrapper
def get_file_reader(path):
    parts = os.path.normpath(path).split(os.sep)
    zip_index = [i for i, p in enumerate(parts, 1) if p.endswith('.zip')]
    if zip_index:
        zip_index = zip_index.pop()
        path_to_zip = os.sep.join(parts[:zip_index])
        path_in_zip = '/'.join(parts[zip_index:])

        zip_arch = zipfile.ZipFile(path_to_zip, 'r', zipfile.ZIP_DEFLATED)
        file = zip_arch.open(path_in_zip)
        return file
    else:
        reader = open(path, 'r', encoding='utf-8')
        return reader


@try_except_wrapper
def read_file(path):
    content = get_file_reader(path)
    if isinstance(content, bytes):
        content.decode()
    return content
