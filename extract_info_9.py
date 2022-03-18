
def extract_university(cv_txt, range_end=5, range_begin=3):
    if cv_txt:
        name_school = None
        year_graduate = None
        for i, line in enumerate(cv_txt):
            if any(x in line for x in
                   ['Education', 'EDUCATION', 'Học Vấn', 'Học vấn', 'HỌC TẬP', 'HỌC VẤN', 'TRÌNH ĐỘ', 'Trình độ',
                    'Trình Độ', 'BẰNG CẤP CHỨNG CHỈ']) and len(line.split()) < 6:
                for j, line_after in enumerate(cv_txt[i:], start=i):
                    index_colon = line_after.find(':')
                    if index_colon < 0:
                        index_colon = 0
                    line_after = line_after[index_colon:]
                    if any(x in line_after.lower() for x in
                           ['fpt polytechnic', 'đại học', 'university', 'unive', 'cao đẳng', 'cđ', 'đh', 'college',
                            'học viện',
                            'institute']):
                        name_school = line_after
                        index_univers = []
                        for k in ['fpt polytechnic', 'đại học', 'university', 'unive', 'cao đẳng', 'college',
                                  'học viện', 'cđ', 'đh',
                                  'institute']:
                            index_univer = line_after.lower().find(k)
                            if index_univer >= 0:
                                index_univers.append(index_univer)

                        if j < len(cv_txt) - 1:
                            continues_school_name = cv_txt[j + 1]
                            words = continues_school_name.split()
                            if len(words) < 4 and check_index_section(continues_school_name) is False and any(
                                    char.isdigit() for char in continues_school_name) is False and any(
                                x in continues_school_name.lower() for x in ['major', ':']) is False:
                                for word in words:
                                    if word[0].islower():
                                        continues_school_name = ''
                                        break
                                name_school = line_after + ' ' + continues_school_name
                        index_univer = max(index_univers)
                        name_school = get_conten_at_center(name_school, index_univer, False)
                        if name_school is not None:
                            if len(cv_txt) - j > range_end:
                                check_end = range_end
                            else:
                                check_end = 0
                            if j - range_begin > 0:
                                check_begin = range_begin
                            else:
                                check_begin = 0
                            for l in range(j - check_begin, j + check_end):
                                year_graduate = re.search(
                                    r'((?:(?:0?[1-9]|1[012])|\b(?:an(?:uary)?|(feb(?:ruary))?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|(nov|dec)(?:ember)?))?[-/ ]? ?(19[7-9]\d|20\d\d) ?[-–—] ?(?:(?:(?:0?[1-9]|1[012])|\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|(nov|dec)(?:ember)?))?[-/ ]? ?(19[7-9]\d|20\d\d))?\b(?:now|present|hiện nay|hiện tại)?)',
                                    cv_txt[l].lower())
                                if year_graduate:
                                    year_graduate = year_graduate[0].lstrip().rstrip()
                                    break
                            return name_school, year_graduate
        return name_school, year_graduate
    return None, None
