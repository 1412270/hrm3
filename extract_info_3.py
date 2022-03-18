def extract_facebook_profile(cv_txt):
    """extract facebook from text
                           :param cv_txt: list of string that extract from file cv
                           :type cv_txt : list string
                           :return: facebook or None
                           :rtype string or None
                           """
    if cv_txt:
        for i, line in enumerate(cv_txt):
            line = line.replace(' ', '')
            facebookprofile = re.search(r'(?:(?:https):\/\/)?(?:www.)?facebook.com\/\S*', line)
            if facebookprofile:
                return facebookprofile.group(0)
    return None

def extract_birthday(cv_txt):
    if cv_txt:
        birthday = None
        for line in cv_txt:
            # dd/mm/yy
            birthday_1 = re.findall(r'(0?[1-9]|[12][0-9]|3[01])[-/.](0?[1-9]|1[012])[-/.](19[7-9]\d|200\d)(?=\D|$)',
                                    line)
            if birthday_1:
                birthday = (birthday_1[0][0], birthday_1[0][1], birthday_1[0][2])
                return birthday
            else:
                # mm/dd//yy
                birthday_1 = re.findall(r'(0?[1-9]|1[012])[-/.](0?[1-9]|[12][0-9]|3[01])[-/.](19[7-9]\d|200\d)(?=\D|$)',
                                        line)
                if birthday_1:
                    birthday = (birthday_1[0][1], birthday_1[0][0], birthday_1[0][2])
                    return birthday
                else:
                    # dd/month/yy
                    birthday_1 = re.findall(
                        r'(0?[1-9]|[12][0-9]|3[01])[ ,]?[ ]?(\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?))[ ,]?[ ]?(19[7-9]\d|200\d)(?=\D|$)',
                        line)
                    if birthday_1:
                        birthday = (birthday_1[0][0], birthday_1[0][1], birthday_1[0][3])
                    else:
                        birthday_1 = re.findall(
                            r'(\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?))[ ,]?[ ]?(0?[1-9]|[12][0-9]|3[01])[ ,]?[ ]?(19[7-9]\d|200\d)(?=\D|$)',
                            line)
                        if birthday_1:
                            birthday = (birthday_1[0][2], birthday_1[0][0], birthday_1[0][3])
        if birthday is not None:
            if len(birthday[1]) >= 3:
                b = birthday[1].strip()
                a = strptime(str(b)[:3], '%b').tm_mon
                birthday = (birthday[0], str(a), birthday[2])
        return birthday
    return None


def extract_name(cv_txt, lang, address, school):
    if cv_txt:
        name = None
        try:
            for i, line in enumerate(cv_txt):
                # if line.find(':') != -1:
                #     line = line.split(':')[1]
                if len(cv_txt[i].split()) < 3 and len(cv_txt[i + 1].split()) < 3:
                    line = cv_txt[i] + " " + cv_txt[i + 1]
                # print(line)
                stop_key = 5
                while stop_key > 1 and name is None:
                    name = name_checker(line, stop_key, address, school)
                    stop_key = stop_key - 1
                if name is not None:
                    break
        except Exception as ex:
            msg = 'Error stopping process: {}'.format(ex)
            log.error('err at {}\n because:{}'.format(sys._getframe().f_code.co_name, msg))
        finally:
            log.info('End {}'.format(sys._getframe().f_code.co_name))
            return name

    return None
