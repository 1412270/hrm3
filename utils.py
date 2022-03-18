def find_index_character_specical(txt):
    """find index of special character that is not alphabet,space,dot
            :param txt: a string need seach

            :type txt : string

            :return: index of character or -1 if cannot find
            """
    for i, letter in enumerate(txt):
        if not letter.isalpha() and not letter.isspace() and letter != '.':
            return i
    return -1


# @longtime
def remove_special_character_at_lead(txt, degital=False):
    """remove all special character at lead of string
        :param txt: a string need seach
        :param degital: option secial character contain number

        :type txt : string
        :type degital : bool

        :return: a string after removed
        """
    while True:
        if len(txt) < 1 or txt[0].isalpha() or (degital is False and txt[0].isdigit()):
            break
        else:
            txt = txt[1:]
    return txt


def remove_special_character_at_tail(txt, degital=False):
    """remove all special character at tail of string
        :param txt: a string need seach
        :param degital: option secial character contain number

        :type txt : string
        :type degital : bool

        :return: a string after removed
        """
    while True:
        if len(txt) < 1 or txt[-1].isalpha() or (degital is False and txt[-1].isdigit()) or (
                txt[-1] in [',', ':', ';', '-', '–', '?', '(', ')']):
            break
        else:
            txt = txt[:-1]
    return txt


def remove_mistake_icon_at_lead(txt):
    """remove a special character that is icon at lead
            :param txt: a string need seach

            :type txt : string

            :return: a string after removed
            """
    if len(txt) < 2:
        return txt
    if (txt[0].islower() and txt[1:].upper() == txt[1:]) or (txt.find(':') > 0 and len(txt.split()[0]) == 1):
        txt = txt[1:]
    return txt.lstrip()


# @longtime
def get_conten_at_center(line, index_key, lever=True):
    """get only conten (group of some special wolds) of string if lead or end of string is special character
            :param line: a string need process
            :param index_key: index begin of 'group of some special words'
            :param lever: option to check all character in word

            :type line : string
            :type index_key : int
            :type lever : bool

            :return: string after processed
            """
    # TODO fix while true
    while True:
        index = find_index_character_specical(line)
        if index == -1:
            break
        if index < index_key:
            line = line[index+1:]
            # while True:
            #     new_line = line[index:]
            #     index += 1
            #     if len(new_line) < 2 or new_line[0].isupper():
            #         line = new_line
            #         index_key -= index
            #         break
        else:
            line = line[:index]
            # if len(line[index:].split()) > 2:
            #     line = line[0:index]
            # else:
            #     line = line.replace(')', '')
            #     line = line.replace('(', '')
            #     line = line.replace('-', '')
            # if lever:
            #     words = line.split()
            #     new_line = ''
            #     for i in words:
            #         if i[0].isupper():
            #             new_line = new_line + ' ' + i
            #         else:
            #             line = new_line
            #             break
            #     break
    return line.rstrip().lstrip()
