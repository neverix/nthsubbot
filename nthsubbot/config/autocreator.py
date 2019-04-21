""" Automatically creates the config. """
import getpass


def auto_create(source, keymaps):
    """
    Automatically creates the config.
    :param source: source config, new keys will be added.
    :param keymaps: the "key maps" for creating the config.
    Key map example:
        {
           "name": "reddit features",
           "type": "dict",
           "keymaps": {
               "username": {
                   "name": "username",
                   "type": "str"
               }
               "password": {
                   "name": "reddit password",
                   "type": "secret"
               },
               "version": {
                   "name": "bot version",
                   "default": 1,
                   "type": "int"
               }
            }
        }
    """
    # output config
    target = {}
    # iterate every property in the source config
    for key, keymap in keymaps.items():
        # example
        # {
        #   "name": "reddit features",
        #   "type": "dict",
        #   "keymaps": {
        #       "username": {
        #           "name": "username",
        #           "type": "str"
        #       }
        #       "password": {
        #           "name": "reddit password",
        #           "type": "secret"
        #       },
        #       "version": {
        #           "name": "bot version",
        #           "default": 1,
        #           "type": "int"
        #       }
        #    }
        # }
        # get the name of the property
        name = keymap["name"]
        # check if there is a default value for keymap
        try:
            keymap["default"]
        except KeyError:
            pass
        else:
            # ask the user if they want to customize the property
            change = bool_input("customize " + name)
            # use defaults if the user doesn't want to customize it
            if not change:
                target[key] = keymap["default"]
                continue
        # handle dictionaries, recurse
        if keymap["type"] == "dict":
            target[key] = auto_create(source[key] if key in source else {}, keymap["keymaps"])
        # check if it already exists
        if key in source:
            target[key] = source[key]
            continue
        # prompt for asking
        prompt = name + ": "
        # handle strings, ask user
        if keymap["type"] == "str":
            target[key] = input(prompt)
        # handle secrets, use getpass
        if keymap["type"] == "secret":
            target[key] = getpass.getpass(prompt)
        # handle integers, ask user and convert to int
        if keymap["type"] == "int":
            target[key] = int(input(prompt))
        # handle booleans, ask user using bool_input
        if keymap["type"] == "bool":
            target = bool_input(prompt)
    return target


# ask user a yes/no question
def bool_input(prompt):
    # get input
    yes_no = input(f"\"{prompt}\"? (Y/N) ")
    if yes_no.lower() in "no":
        # user said "no" or "n"
        return False
    if yes_no.lower() not in "yes":
        # user said neither, interpreted as "yes"
        print("?")
        print("I'll interpret that as a \"yes\".")
    return True
