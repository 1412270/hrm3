def extract_gender(cv_txt, lang=None):
    """extract gender from text
                           :param lang: language in text
                           :param cv_txt: list of string that extract from file cv
                           :type cv_txt : list string
                           :return: gender or None
                           :rtype int -1 boy, 0 girl or None
                           """
    if cv_txt:
        if lang is None:
            lang = is_cv_English(' '.join(cv_txt))
        if lang:

            for line in cv_txt:
                char_first = line.split()[0]
                if len(char_first) == 1:
                    line = line[1:].lstrip()
                line = line.lower()
                if line.find('female') != -1:
                    return 0
                elif line.find('male') != -1:
                    return 1
            return None
        else:
            for line in cv_txt:
                char_first = line.split()[0]
                if len(char_first) == 1:
                    line = line[1:].lstrip()
                line = line.lower()
                line = line.lower()
                if line.find('giới tính') != -1:
                    if line.find('nam') != -1:
                        return 1
                    elif line.find('nữ') != -1:
                        return 0
                else:
                    result = line.find(':')
                    if result < 0:
                        result = -1
                    line = line[result + 1:].lstrip()
                    if line.find('nam') != -1 and len(line) < 5:
                        return 1
                    elif line.find('nữ') != -1 and len(line) < 5:
                        return 0
    return None
