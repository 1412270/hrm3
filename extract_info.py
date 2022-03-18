def extract_address(cv_txt, lang=None):
    """extract address from text
               :param lang: lanuage of text in cv
               :param cv_txt: list of string that extract from file cv
               :type cv_txt : list string
               :type lang : bool, 0 vietnam, 1 - english
               :return: address or None
               :rtype string or None
               """
    if len(cv_txt) < 1:
        return None
    district_hcm_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    distric_hcm_name = ['Thủ Đức', 'Gò Vấp', 'Bình Thạnh',
                        'Tân Bình', 'Tân Phú', 'Phú Nhuận', 'Bình Tân']
    district_hcm_englisgh = [remove_accent_vietnamese(name) for name in distric_hcm_name]
    if lang is None:
        lang = is_cv_English(' '.join(cv_txt))
    # nếu là cv bản tiếng anh thì check các key tiếng anh
    if lang:
        scores = []
        res_address = []
        for i, line in enumerate(cv_txt):
            score = 0
            words = re.split('[ ,]', line)
            if any(x in line for x in ['/']) and any(char.isdigit() for char in line):
                score += 1.5
            if any(x in words for x in ['Dist', 'dist', 'D.', 'District']):
                score += 3.5
                if any(x in line for x in district_hcm_englisgh):
                    score += 3
                elif any(x in line for x in district_hcm_num):
                    score += 3
            else:
                if any(x in line for x in district_hcm_englisgh):
                    score += 2.5
            if any(x in words for x in ['Ward', 'W.', 'ward']):
                score += 3.5
                if any(char.isdigit() for char in line):
                    score += 2
            if line.lower().find('street') != -1:
                score += 3.5
                if any(char.isdigit() for char in line):
                    score += 2
            if line.lower().find('city') != -1:
                score += 1
            if any(x in words for x in ['HCM', 'Ho Chi Minh', 'HCMC']):
                score += 1
            if score >= 3:
                scores.append(score)
                res_address.append(i)
        # print(scores, res_address)
        if len(scores) > 0:
            index_max = scores.index(max(scores))
            res = cv_txt[res_address[index_max]]
            if index_max > 0 and abs(res_address[index_max] - res_address[index_max - 1]) == 1:
                res = cv_txt[res_address[index_max - 1]] + res
            if index_max < len(scores) - 1 and abs(res_address[index_max] - res_address[index_max + 1]) == 1:
                res = res + cv_txt[res_address[index_max + 1]]
            result = res.find(':')
            if result < 0:
                result = -1
            res = res[result + 1:].lstrip()
            return res
        else:
            return None
    else:
        scores = []
        res_address = []
        for i, line in enumerate(cv_txt):
            result = line.find(':')
            if result < 0:
                result = -1
            line = line[result + 1:].lstrip()
            words = re.split('[ ,]', line)
            score = 0
            if any(x in line for x in ['/']) and any(char.isdigit() for char in line):
                score += 1.5
            if any('Q{}'.format(x) in words for x in district_hcm_num):
                score += 1.5
            if any(x in words for x in ['Quận', 'quận', 'Q.', 'QUẬN']):
                score += 3.5
                if any(x in line for x in distric_hcm_name):
                    score += 3
                if any(x in line for x in district_hcm_num):
                    score += 2
            if line.lower().find('số') != -1:
                score += 1
                if any(char.isdigit() for char in line):
                    score += 2
            
       
