def remove_accent_vietnamese(s):
    """remove all accent in string if it is written by vietnames
                :param s: a string need process
                :type s : string
                :return: string after processed
                """
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s


# @longtime
def continues_line(cv_txt):
    """link to line if those are the same sentence
                    :param cv_txt: list of string
                    :param eng: language using write
                    :type cv_txt : list string
                    :return: list string after processed
                    """

    txt_continues = []
    check = 0
    for i, line in enumerate(cv_txt):
        if i == 0 or len(line) < 1:
            txt_continues.append(line)
        elif (line[0].isalpha() and line[
            0].islower() and '@' not in line and 'facebook' not in line and 'fb' not in line) or line[
            0] == '/' or line[
            0] == ',' or check == 1:
            txt_continues[-1] = txt_continues[-1] + ' ' + line
            check = 0
        elif (line[-1] == '-' or line[-1] == ',' or line[-1] == '/' or line[-1] == '–') and i + 1 < len(cv_txt) + 1:
            txt_continues.append(line)
            check = 1
        else:
            txt_continues.append(line)
    return txt_continues


# @longtime
def check_index_section(line, eng=True):
    """check a sentence is a name of index section in CV
        :param line: string need check
        :param eng: language using write
        :type line :string
        :type eng : bool , True if english, 0- vietnamese
        :return: 1 if sentence is index section and 0 is not
        """
    line = remove_special_character_at_lead(line, degital=True)
    if eng:
        index_voca = [line.rstrip('\n').lower() for line in
                      open(DATA_INDEX_ENG, encoding='cp932', errors='ignore')]
        if len(line.split()) > 3:
            return 0
        else:
            for idx in index_voca:
                # if line.lower() == idx:
                if float(SequenceMatcher(None, line.lower(), idx).ratio()) > 0.85:
                    return idx.upper()

            return 0
    else:
        index_voca = [line.rstrip('\n').lower() for line in
                      open(DATA_INDEX_VN, encoding='utf-8', errors='ignore')]
        if len(line.split()) > 6:
            return 0
        else:
            for idx in index_voca:
                # if line.lower() == idx:
                if float(SequenceMatcher(None, line.lower(), idx).ratio()) > 0.85:
                    return idx.upper()
            return 0
