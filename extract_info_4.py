def name_checker(input, long, address, school):
    # input = re.sub('^.*\\.|ten|name|:', '', input, flags=re.IGNORECASE)
    if len(input.split()) < long:
        return None
    if input.lower().find('chi minh') != -1 or input.lower().find('ha noi') != -1:
        return None
    check_number = re.findall(r"[0123456789]", input)
    if len(check_number) > 1:
        return None
    if input.find('.') != -1:
        input = input.split('.')[0]
    if input.find(':') != -1:
        input = input.split(':')[1]
    if input.find(',') != -1:
        input = input.replace(',', '')
    f = open(DATA_NAME, "r")
    vn_words = f.read()
    vn_words = vn_words.split("\n")
    f.close()
