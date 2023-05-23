import console_bot.ab_work as ab
from console_bot.handlers import no_command, instruction, show_all
import console_bot.Notes as Notes
import console_bot.sort as sort
import abc

MAIN_INSTRUCTION = 'instruction_for_menu.txt'


class UserInterface(abc.ABC):

    @abc.abstractmethod
    def show_help(self):
        pass

    @abc.abstractmethod
    def show_contacts(self):
        pass

    @abc.abstractmethod
    def show_notes(self):
        pass


class ConsoleInterface(UserInterface):

    def show_help(self):
        return instruction(MAIN_INSTRUCTION)

    def show_contacts(self):
        return show_all()

    def show_notes(self):
        return Notes.all("")


console_i = ConsoleInterface()


def good_bye(*args, **kwargs):
    return 'Good bye'


MAIN_COMMANDS = {
    'help': console_i.show_help,
    'address book': ab.main,
    'notes': Notes.main,
    'sort': sort.main,
    'show contacts': console_i.show_contacts,
    'show notes': console_i.show_notes,
    'exit': good_bye
}


MAIN_COMMANDS_WORDS = '|'.join(MAIN_COMMANDS)


def main():
    print(console_i.show_help())
    while True:
        user_input = input('Choose points: address book, notes, show contacts, show notes, sort: ')
        command, _ = ab.parser(user_input, MAIN_COMMANDS_WORDS)
        handler = MAIN_COMMANDS.get(command, no_command)
        output = handler()
        if output:
            print(output)
        if output == 'Good bye':
            break


if __name__ == '__main__':
    main()





