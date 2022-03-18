stop_word = ["đại học", "cao đẳng", "thành phố", "tỉnh", "huyện", "hồ sơ", "học viện", "hồ chí minh", "hcm", "tp",
                 "tham gia", "sinh viên", "học vấn", "công ty", "cty"]

    words = input.split()
    if any(s in input.lower() for s in stop_word):
        return None
    loop = len(input.split()) - long + 1
    for i in range(0, loop):
        candicate = words[i:i + long]
        print(candicate)
        name = " ".join(candicate)
        if address is not None:
            if address.find(name) != -1:
                break
        if school is not None:
            if school.find(name) != -1:
                break
        if candicate_test(candicate) is False:
            continue

        for item in candicate:
            if remove_accent_vietnamese(item).title() not in vn_words:
                name = None
                break

        if name is not None:
            check_vn = re.findall(
                r'\b\S*[ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]+\S*\b',
                name)
            if len(check_vn) > 0:
                if len(set(must_have_words) & set(candicate)) != 0:
                    return name
            if len(check_vn) == 0:
                if len(set(must_have_words_2) & set(candicate)) != 0:
                    return name

    return None


def candicate_test(candicate):
    name_maybe = " ".join(candicate)
    name_title = name_maybe.title()
    name_upper = name_maybe.upper()
    if name_maybe != name_title and name_maybe != name_upper:
        return False
    check_vn = re.findall(r"[$&+,:;=?@#|'<>.^*()%!-]", name_maybe)
    if len(check_vn) > 0:
        return False
    return True
