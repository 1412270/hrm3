def split_sections(cv_txt, lang=None):
    """split content into different part in dictionary
                           :param cv_txt: list of string that extract from file cv
                           :type lang : language , 1 english, 0 vietnamese
                           :return: dictionary of imformation
                           :rtype dictionary

                           """
    if cv_txt:
        if lang is None:
            lang = is_cv_English(' '.join(cv_txt))
        dict_sections = {}
        key = 'INFOMATION'
        data = []
        for i, value in enumerate(cv_txt):
            index_check = check_index_section(value.replace(':', ''), lang)
            if index_check != 0:
                if i > 0:
                    dict_sections[key] = data
                data = []
                key = index_check
                cv_txt[i] = index_check.upper()
            else:
                data.append(value)
        dict_sections[key] = data
        return dict_sections, cv_txt
    return None


def get_info_from_text(cv_text, text_raw, language, path):
    split_section, cv_text = split_sections(cv_text, language)
    address = extract_address(cv_text, language)
    school, season = extract_university(cv_text)
    name = extract_name(text_raw, language, address, school)
    email = extract_email(cv_text)
    phone = extract_phone_number(cv_text)
    birthday = extract_birthday(cv_text)
    gender = extract_gender(cv_text, language)
    # school, season = extract_university(cv_text)
    tech_skill = extract_technique(cv_text)
    face_image = str(extract_face(path))
    facebook = extract_facebook_profile(cv_text)
    gpa = extract_GPA(cv_text)
    return name, email, phone, birthday, gender, address, school, season, tech_skill, face_image, facebook, gpa, \
           split_section


# Đếm số dòng có quá nhiều khoảng trắng(space)
def count_space_sentence(cv_text):
    line_found = 0
    for line in cv_text:
        count_space = line.count(' ')
        if float(count_space/len(line)) > 0.4:
            line_found = line_found + 1
    if line_found > 1:
        return False
    return True
