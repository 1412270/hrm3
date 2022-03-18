def is_cv_English(texts):
    """check a cv is writted by english
            :param texts: list of string in cv

            :type texts : list string

            :return: True - is cv english, False - vietnames
            """
    count = 0
    if texts is not None:
        for i in texts:
            s1, n1 = re.subn(
                r'[àáạảãâầấậẩẫăằắặẳẵÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪèéẹẻẽêềếệểễÈÉẸẺẼÊỀẾỆỂỄòóọỏõôồốộổỗơờớợởỡÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠìíịỉĩÌÍỊỈĨùúụủũưừứựửữƯỪỨỰỬỮÙÚỤỦŨỳýỵỷỹỲÝỴỶỸĐđ]',
                'a', i)
            count += n1
            if count > 15:
                return False
        return True
    return False
