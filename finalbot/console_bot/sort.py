import os
from pathlib import Path
import shutil

import console_bot.ab_work as ab
from console_bot.handlers import no_command, input_error, instruction

SORT_INSTRUCTION = 'instruction_for_sorter.txt'

extensions = {'Зображення': ['jpeg', 'png', 'jpg', 'svg'],
              "Відео": ['avi', 'mp4', 'mov', 'mkv'],
              "Документи": ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
              "Музика": ['mp3', 'ogg', 'wav', 'amr'],
              "Архіви": ['zip', 'gz', 'tar'],
              "Невідомі розширення": []}


def normalize(word):
    result_name = ''
    dicti = {'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v', 'Г': 'G', 'г': 'g', 'Д': 'D', 'д': 'd',
             'Е': 'E', 'е': 'e', 'Ё': 'E', 'ё': 'e', 'Ж': 'J', 'ж': 'j', 'З': 'Z', 'з': 'z', 'И': 'I', 'и': 'i',
             'Й': 'J', 'й': 'j', 'К': 'K', 'к': 'k', 'Л': 'L',
             'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n', 'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R',
             'р': 'r', 'С': 'S', 'с': 's', 'Т': 'T',
             'т': 't', 'У': 'U', 'у': 'u', 'Ф': 'F', 'ф': 'f', 'Х': 'H', 'х': 'h', 'Ц': 'TS', 'ц': 'c', 'Ч': 'CH',
             'ч': 'ch', 'Ш': 'SH', 'ш': 'sh',
             'Щ': 'SCH', 'щ': 'sch', 'Ъ': '', 'ъ': '', 'Ы': 'Y', 'ы': 'y', 'Ь': '', 'ь': '', 'Э': 'E', 'э': 'e',
             'Ю': 'YU',
             'ю': 'yu', 'Я': 'YA', 'я': 'ya', 'Є': 'JE', 'є': 'je', 'І': 'I', 'і': 'i', 'Ї': 'JI', 'ї': 'ji', 'Ґ': 'G',
             'ґ': 'g', '_': 'W', '__': 'w'}
    for i in word:
        if i not in dicti.values():
            if i in dicti.keys():
                result_name += dicti[i]
            elif '0' <= i <= '9':
                result_name += i
            else:
                result_name += '_'
        else:
            result_name += i
    return result_name


def create_dirs(path):
    path = Path(path)
    path.joinpath('Зображення').mkdir(exist_ok=True)
    path.joinpath('Відео').mkdir(exist_ok=True)
    path.joinpath('Документи').mkdir(exist_ok=True)
    path.joinpath('Музика').mkdir(exist_ok=True)
    path.joinpath('Архіви').mkdir(exist_ok=True)
    path.joinpath('Невідомі розширення').mkdir(exist_ok=True)


def get_subfolder_paths(path):
    subfolder_paths = [f.path for f in os.scandir(path) if f.is_dir()]
    return subfolder_paths


def get_file_paths(path):
    file_paths = [f.path for f in os.scandir(path) if not f.is_dir()]
    return file_paths


def sort_files(ls, path):
    file_paths = ls
    ext_list = list(extensions.items())
    lst = []
    for file_path in file_paths:
        lst.append(file_path)
        extension = file_path.split('.')[-1]
        file_name = file_path.split('\\')[-1]
        normalize_name = file_name.split('.')
        normal = normalize(normalize_name[0])
        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                os.replace(file_path, f'{path}\\{ext_list[dict_key_int][0]}\\{normal}.{extension}')
                lst.remove(file_path)
    for i in lst:
        file_name = i.split('\\')[-1]
        os.replace(i, f'{path}\\Невідомі розширення\\{file_name}')


def get_subfolders(path):
    subfolders = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            subfolders.append(item_path)
            subfolders.extend(get_subfolders(item_path))
    return subfolders


def full_sort(path):
    m = get_subfolders(path)
    for i in m:
        new_path = i
        sort = sort_files(get_file_paths(new_path), path)


def dearchivator(path):
    way = f'{path}\\Архіви'
    j = get_file_paths(way)
    for i in j:
        name = i.split('\\')[-1]
        name = name.split('.')
        (os.mkdir(way + f'\\{normalize(name[0])}'))
        shutil.unpack_archive(i, f'{way}\\{normalize(name[0])}')
        os.remove(i)


def folder_remover(path):
    list_with_folders = get_subfolders(path)
    list_with_folders.reverse()
    for i in list_with_folders:
        name = i.split('\\')[-1]
        if name not in extensions.keys():
            if len(os.listdir(i)) == 0:
                os.rmdir(i)


def organize_files(path):
    if not path:
        raise ValueError('You should write path')

    if os.path.isdir(path):
        create_dirs(path)
        sort_files(get_file_paths(path), path)
        full_sort(path)
        dearchivator(path)
        folder_remover(path)
        return "Done"
    else:
        raise ValueError("Not correct path")


def start(*args, **kwargs):
    return instruction(SORT_INSTRUCTION)


def no_command(*args, **kwargs):
    return 'There are no command like this'


def main_menu(*args, **kwargs) -> str:
    '''Return to the main menu'''
    output = 'Return'
    return output


SORT_COMMANDS = {
    'sort': organize_files,
    'return': main_menu,
    'help': start
}

SORT_COMMANDS_WORDS = '|'.join(SORT_COMMANDS)


def main():
    print(start())
    while True:
        user_input = input('Write your command: ')
        command, data = ab.parser(user_input, SORT_COMMANDS_WORDS)
        handler = SORT_COMMANDS.get(command, no_command)
        output = handler(data)
        print(output)
        if output == 'Return':
            break


if __name__ == '__main__':
    main()