from collections import UserDict, defaultdict
import re
import pickle
import os

from console_bot.handlers import instruction

NOTES_INSTRUCTION = 'instruction_for_notes.txt'


class HashTags:
    def __init__(self, hashtags):
        self.value = hashtags


class NoteRecord:
    def __init__(self, record, hashtags: HashTags = None):
        self.record = record
        if hashtags:
            self.hashtags = hashtags
        else:
            self.hashtags = []


class Notes(UserDict):

    def add_note(self, note_record: NoteRecord):
        theme = note_record.record.split(' ')
        key = []
        for i in range(1):
            key.append(theme[i])
        self.data[' '.join(key)] = note_record
        return self.data

    def edit_note(self, note_key, new_record):
        if note_key in self.data:
            self.data[note_key].record = new_record
            return 'You edit note'
        else:
            return f'No note found with key "{note_key}"'

    def remove_note(self, note_key):
        if note_key in self.data:
            del self.data[note_key]
            return f'You remove note'
        else:
            return f'No note found with key "{note_key}"'

    def save_in_file(self):
        if os.path.isfile('notes.bin'):
            with open('notes.bin', 'wb') as fh:
                pickle.dump(self, fh)
        else:
            with open('notes.bin', 'wb') as fh:
                pickle.dump(self, fh)

    @staticmethod
    def open_from_file():
        if os.path.isfile('notes.bin'):
            with open('notes.bin', 'rb') as fh:
                return pickle.load(fh)
        else:
            return Notes()

    def search_by_tag(self, key):
        matching_notes = []
        for name, note in self.data.items():
            if key in note.hashtags:
                matching_notes.append(f"{name} : {note.record}")
        return matching_notes

    def sort_by_tag(self):
        sorted_notes = defaultdict(list)
        for name, note in self.data.items():
            if not note.hashtags:
                sorted_notes["without hashtags"].append(name)
            for tag in note.hashtags:
                sorted_notes[tag].append(name)
        return sorted_notes


notes = Notes.open_from_file()


def add(result):
    if (result[1]) == None:
        return "Print your note"
    elif len(result) == 3:
        hashtags = result[2]
        record = NoteRecord(result[1], hashtags)
        notes.add_note(record)
    else:
        record = NoteRecord(result[1])
        notes.add_note(record)
    return 'You add note'


def all(result):
    result = ''
    for k, v in notes.items():
        result += f'Theme:{k},\n {v.record}\n\n'
    return result if result else 'There are no notes'


def change(result):
    if (result[1]) == None:
        return "Need information "
    else:
        theme = result[1].split(' ')
        key = theme[0]
        note = " ".join(theme[1:])
        message = notes.edit_note(key, note)
        return message


def remove(result):
    if (result[1]) == None:
        return "Need information "
    else:
        key = result[1]
        message = notes.remove_note(key)
        return message


def find(result):
    word = result[1]
    if word:
        result = []
        for i in notes:
            res = re.findall(word, notes[i].record)
            if len(res) > 0:
                result.append(f'Note :{notes[i].record}')
        if not result:
            return 'There are no notes like this'
        return '\n'.join(result)
    return f"Enter the keyword you want to search"

def search(result):
    tag = result[1]
    if tag:
        result = notes.search_by_tag(tag)
        if len(result) == 0:
            return f"No matches"
        return "\n".join(result)
    return f"Enter the tag you want to search"


def sort(*args):
    sorted = notes.sort_by_tag()
    result = ""
    for tag, names in sorted.items():
        result += f"{tag} : {', '.join(names)} \n"
    return result


def help(*args):
    return instruction(NOTES_INSTRUCTION)

commands_dict ={'add': add, 
                'show all': all, 
                'change': change, 
                'remove': remove, 
                'find': find, 
                'search': search, 
                'sort': sort,
                'help': help}

def message_parser(text):
    command=None
    note = None
    hashtags = None
    str=text.lower()
    for i in commands_dict:
        res = re.findall(i,str)
        if len(res)>0:
            command = i
            break
    info = []
    flag = False
    for i in str.split():
        if flag:
            info.append(i)
        elif i == command:
            flag = True
    if len(info)>0:
        note=' '.join(info)
    if note:
        mess = note.split(' ')
        tags =[]
        for i in mess:
            if i.startswith('#'):
                tags.append(i)
        if len(tags)>0:
            hashtags = tags
    if hashtags:
        return [command, note, hashtags]
    else:
        if command:
            return [command, note]


def main():
    print(help())
    while True:
        text = input('Write your command: ')
        if text == 'return':
            notes.save_in_file()
            print('return')
            break
        res = message_parser(text)
        if res:
            if res[0] in commands_dict:
                print(commands_dict[res[0]](res))
        else:
            print("There no command")




if __name__ == '__main__':
    main()


