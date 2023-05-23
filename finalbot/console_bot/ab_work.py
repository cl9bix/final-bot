import re

import console_bot.handlers as handlers


OPERATIONS = {
    'help': handlers.help,
    'add': handlers.adding,
    'change phone': handlers.changing_phone,
    'change': handlers.changing,
    'phone': handlers.get_phones,
    'show all': handlers.show_all,
    'show part': handlers.show_part,
    'remove contact': handlers.remove_contact,
    'remove phone': handlers.remove_phone,
    'days to birth': handlers.days_to_birth,
    'upcoming birthdays': handlers.upcoming_birth,
    'find': handlers.find_rec,
    'save': handlers.save,
    'no command': handlers.no_command,
    'main menu': handlers.main_menu,
    'return': handlers.main_menu,
}

COMMAND_WORDS = '|'.join(OPERATIONS)

def parser(message: str, commands: str) -> tuple[str|None, str|None, str|None]:
    '''Parse message to command and data'''
    message = message.lstrip()
    command_match = re.search(fr'^({commands})\b', message, re.IGNORECASE)
    if command_match:
        command = command_match.group(1)
        data = re.sub(rf'{command}\b', '', message, 1).strip()
        command = command.strip().lower()
        return command, data
    return 'no command', ''

def main():
    print(handlers.help())
    while True:
        inp = input('Write your command: ')
        command, data  = parser(inp, COMMAND_WORDS)
        handler = OPERATIONS.get(command, handlers.no_command)
        output = handler(data)
        print(output)
        if output == 'Return':
            break
    pass 

if __name__ == '__main__':
    main()

