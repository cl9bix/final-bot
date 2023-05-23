from collections import UserDict
from functools import reduce
from datetime import date, datetime
import re
import pickle
from pathlib import Path

CONTACTS_FILE = Path('data.bin')

class Field():
    '''Common field characters'''

    def __init__(self, value) -> None:
        self.value = value
        pass

    def __eq__(self, __obj: object) -> bool:
        return self.value == __obj.value and type(self) == type(__obj)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    '''Name characters'''

    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            self.__value = value
        else:
            raise ValueError('Cant save contact with empty name')


class Phone(Field):
    '''Phone characters'''

    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        pattern = r"^(039|050|063|066|067|068|091|092|093|094|095|096|097|098|099)\d{7}$"
        if re.match(pattern, value):
            self.__value = value
        else:
            raise ValueError(f'Invalid phone number: {value} example number 0971111111')


class Birthday(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = datetime.strptime(value, '%d.%m.%Y').date()

    def __str__(self):
        return self.value.strftime('%B %d')

class Address(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        """Accept string with format is 'City, street, house number, number of flat(optional)'"""
        value = value.replace(' ', '')
        arr = value.split(',')
        if len(arr) >= 2 and len(arr) <= 4 and arr[0].isalpha() and arr[1].isalpha():
            self.__value = value
        else:
            raise ValueError('Adress should be in format: city, street, house, flat')

class Email(Field):

    '''Email characters'''
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter 
    def value(self, value: str):
        if not re.match(r"^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$", value):
            raise ValueError(f'{value} is not a valid email address')
        self.__value = value
          
class Record():
    '''Represent record with fields'''

    def __init__(self, name, *phones, birthday:Birthday=None, address:Address=None, email:Email=None):
        self.name = name
        self.phones = [phone for phone in filter(lambda phone: phone, phones)]
        self.birthday = birthday
        self.address = address
        self.email = email

    def __str__(self):
        output = f'name: {self.name.value}'

        phones = self.phones
        if phones:
            numbers = ', '.join(self.get_numbers())
            output += f' numbers: {numbers}'

        if self.birthday:
            output += f' birthday: {self.birthday}'

        if self.address:
            output += f' address: {self.address}'

        if self.email:
            output += f' email: {self.email}'

        return output

    def raise_nonumber(func):
        '''
        Decorator to raise exeption if there are no phone
        with such number in the phones
        '''

        def inner(self, phone, *args, **kwargs):
            if phone not in self.phones:
                raise ValueError('There are no phone with such number in the phones')
            return func(self, phone, *args, **kwargs)

        return inner

    def raise_same_number(func):
        '''
        Decorator to raise exeption if already there is phone
        with such number in the phones
        '''

        def inner(self, *args, **kwargs):
            phone = args[-1]
            if phone in self.phones:
                raise ValueError('Already there is phone with such number in the phones')
            return func(self, *args, **kwargs)

        return inner

    def raise_empty_number(func):
        '''Decorator to raise exeption if phone has empty number'''

        def inner(self, *args, **kwargs):
            for phone in args:
                if not phone.value:
                    raise ValueError('There no number in the command')
            return func(self, *args, **kwargs)

        return inner
    
    def add_data(self, element, new_data):
        
            try:
                parametr = getattr(self, element)
            except AttributeError:
                raise ValueError(f'There are no field {element} in record')

            if parametr:
                raise ValueError(f'This contact already has {element} data')
            setattr(self, element, new_data)

    def change_data(self, element, new_data):
            try:
                getattr(self, element)
            except AttributeError:
                raise ValueError(f'There are no field {element} in record')
            setattr(self, element, new_data)


    @raise_empty_number
    @raise_same_number
    def add_phone(self, phone: Phone) -> list[Phone]:
        '''Add new phone to phones'''
        self.phones.append(phone)
        return self.phones

    @raise_empty_number
    @raise_nonumber
    def remove_phone(self, phone: Phone) -> list[Phone]:
        '''Remove phone with number from phones'''
        for s_phone in filter(lambda s_phone: s_phone.value == phone.value, self.phones):
            self.phones.remove(s_phone)
        return self.phones

    @raise_empty_number
    @raise_nonumber
    @raise_same_number
    def change_phone(self, old_phone: Phone, new_phone: Phone) -> list[Phone]:
        '''Change phone number'''
        for phone in filter(lambda phone: phone == old_phone, self.phones):
            phone.value = new_phone.value
        return self.phones

    def get_numbers(self) -> list[str]:
        '''Return list with numbers'''
        numbers = [str(phone) for phone in self.phones]
        return numbers

    def days_to_birthday(self):
        '''Return number days to next birthday'''
        today = date.today()
        next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
        if today > next_birthday:
            next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
        days = (next_birthday - today).days
        return days


class AdressBook(UserDict):
    '''Represent adress book with records'''

    def add_record(self, record: Record) -> dict[str:Record]:
        '''Add new record to the adress book'''
        key = record.name.value
        self.data[key] = record
        return self.data

    def show_records(self) -> str:
        '''Show all records in the adress book data'''
        if not self.data:
            return 'There are no contacts in list'
        output = reduce(lambda s, t: str(s) + '\n' + str(t),
                        self.data.values(), 'Your contacts:')
        return output

    def find_records(self, symbols: str) -> str:
        '''Find all records with such symbols'''

        output = '\n'.join(
            str(record) for record in self.data.values()
            if symbols in record.name.value.lower()
            or symbols in ' '.join(record.get_numbers())
            or (record.birthday and symbols in str(record.birthday).lower())
            or (record.address and symbols in str(record.address).lower())
            or (record.email and symbols in str(record.email).lower())
        )
        if output:
            return output
        return 'No matches found'

    def __iter__(self):
        return self.iterator()

    def iterator(self, n=2):
        'Return generator that show next n records'
        current = 0
        while current < len(self.data):
            group_number = current // n + 1
            output = reduce(
                lambda s, t: str(s) + '\n' + str(t),
                list(self.data.values())[current:current + n],
                f'{group_number} group:'
            )
            yield output
            current += n

    def upcoming_birthdays(self, days):
        res = ""
        for rec in self.data.values():
            try:
                difference = rec.days_to_birthday()
            except AttributeError:
                continue
            else:
                if 0 <= difference <= days:
                    res += f"{rec} -> {difference} days left \n"
        return res

    def dump_file(self):
        with open(CONTACTS_FILE, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_data():
        if CONTACTS_FILE.exists():
            with open(CONTACTS_FILE, 'rb') as file:
                address_book = pickle.load(file)
        else:
            address_book = AdressBook()
        return address_book
    
    if __name__ == '__main__':
        a = Record(Name('SDASD'))
        a.change_data('sdfs', 'dsf')