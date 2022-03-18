def extract_GPA(cv_txt):
    """extract GPA from text
                           :param cv_txt: list of string that extract from file cv
                           :type cv_txt : list string
                           :return: GPA or None
                           :rtype string or None
                           """
    if cv_txt:
        for i, line in enumerate(cv_txt):
            if any(x in line.lower() for x in
                   ['gpa', 'medium score', 'điểm trung bình']):
                if len(cv_txt) - i > 4:
                    check_end = 4
                else:
                    check_end = 0
                if i - 1 > 0:
                    check_begin = 1
                else:
                    check_begin = 0
                for j in range(i - check_begin, i + check_end):
                    gpa = re.search(r'[0-9]\.\d\d?\/?\d?\d?', cv_txt[j].lower())
                    if gpa:
                        return gpa[0]
    return None


# @longtime_root
def extract_cv(path, mode=False):
    """extract all infomation from text
                           :param path: path of file cv need extract info
                           :param mode: mode to extract text from file, by library reader or OCR scan
                           :type path : string path
                           :type mode : bool False-OCR, True- library reader
                           :return: dictionary of infomation
                           :rtype dictionary
                           """
    start_time = time.time()
    path = path.strip()

    language = 'vie'
    info_found = 0
    name = None
    email = None
    phone = None
    birthday = None
    gender = None
    address = None
    school = None
    season = None
    tech_skill = None
    face_image = None
    facebook = None
    gpa = None
    split_section = None
    if path.split('.')[-1].lower() != 'pdf' and path.split('.')[-1].lower() != 'docx':
        return None

    if path.split('.')[-1].lower() == 'pdf':
        cv_text, text_raw, language = extract_text_from_pdf_priority_pdf_reader(path)

        if len(cv_text) > 0:
            if count_space_sentence(cv_text) is True:
                name, email, phone, birthday, gender, address, school, season, tech_skill, face_image, facebook, gpa, \
                split_section = get_info_from_text(cv_text, text_raw, language, path)
                info_found = sum(x is not None for x in [name, email, phone, birthday, gender, address, school, tech_skill])
        if info_found < 5:
            cv_text, text_raw = pipline_extract_txt_by_ocr(path)
            if cv_text is not None:
                language = is_cv_English(cv_text)
                name, email, phone, birthday, gender, address, school, season, tech_skill, face_image, facebook, gpa, \
                split_section = get_info_from_text(cv_text, text_raw, language, path)

    if path.split('.')[-1].lower() == 'docx':
        cv_text, text_raw = convert_docx2txt(path)
        language = is_cv_English(cv_text)
        name, email, phone, birthday, gender, address, school, season, tech_skill, face_image, facebook, gpa, \
        split_section = get_info_from_text(cv_text, text_raw, language, path)

    if language == 1:
        language = 'eng'
    else:
        language = 'vie'
    if not mode:
        mod = 'OCR scan'
    else:
        mod = 'PDF reading'
    total_time = time.time() - start_time

    return {
        "name": name, "email": email, "phone": phone, "facebook": facebook, 'birthday': birthday, "gender": gender,
        "address": address, "face_image": face_image,
        "education": {"university": school, "season": season, "GPA": gpa}, "tech": tech_skill,
        "text_raw": split_section, "other": {"language": language, "mode": mod, "time_process": total_time}
    }
