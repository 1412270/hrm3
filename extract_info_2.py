            if line.lower().find('đường') != -1:
                score += 2.5
            if any(x in line for x in ['Phường', 'phường', 'P.']):
                score += 3.5
            if any('P{}'.format(x) in line for x in district_hcm_num):
                score += 1.5
            if any(x in line for x in ['Thành Phố', 'thành phố', 'Tp', 'tp', 'TP']):
                score += 1
            if any(x in line for x in ['Hồ Chí Minh', 'HCM']):
                score += 1
            if score >= 3.5:
                scores.append(score)
                res_address.append(i)
        if len(scores) > 0:
            index_max = scores.index(max(scores))
            res = cv_txt[res_address[index_max]]
            if index_max > 0 and abs(res_address[index_max] - res_address[index_max - 1]) == 1:
                res = cv_txt[res_address[index_max - 1]] + res
            if index_max < len(scores) - 1 and abs(res_address[index_max] - res_address[index_max + 1]) == 1:
                res = cv_txt[res_address[index_max + 1]] + res
            result = res.find(':')
            if result < 0:
                result = -1
            res = res[result + 1:].lstrip()
            return res
        else:
            return None


# @longtime_root
def extract_email(cv_txt):
    """extract email from text
                   :param cv_txt: list of string that extract from file cv
                   :type cv_txt : list string
                   :return: email or None
                   :rtype string or None
                   """
    if cv_txt:
        for i, line in enumerate(cv_txt):
            line = line.replace('@ g', '@g')
            email = re.findall(r'[\w.-]+@[\w.-]+', line)
            if email:
                return email[0]
    return None


# @longtime_root
# get phone number
def extract_phone_number(cv_txt):
    """extract phone from text
                       :param cv_txt: list of string that extract from file cv
                       :type cv_txt : list string
                       :return: phone or None
                       :rtype string or None
                       """
    if cv_txt:
        for i, line in enumerate(cv_txt):
            line = line.replace(' ', '')
            line = line.replace('.', '')
            phone_number = re.search(r'(?:[(]?\+?\d?\d?[)]?)?\d{9}\d?', line)
            if phone_number:
                return phone_number.group(0)
    return None
