def extract_technique(cv_txt):
    """extract tech skill of candidate from text
                           :param cv_txt: list of string that extract from file cv
                           :type cv_txt : list string
                           :return: list of tech skills or None
                           :rtype list string or None
                           """
    if cv_txt:
        tech_voca = [line.rstrip('\n').lower() for line in open(DATA_TECH)]
        tech_skills = []
        try:
            for line in cv_txt:
                tech_in_line = ""
                # xóa các nội dung trong dấu () hoặc []
                if line != "":
                    if line.find(';') != -1:
                        line = line.replace(';', ',')
                    if line.find(':') != -1:
                        line = line.replace(':', ',')
                    if line.find(')') - line.find('(') > 3:

                        line_sub = line[line.find('(') + len('('):line.rfind(')')]
                        line_sub = line_process(line_sub)
                        words = line_sub.split(" ")
                        for word in words:
                            word = word.replace(',', '')
                            if word.lower() in tech_voca:
                                # tech_in_line = tech_in_line + word + ", "
                                posi = line_sub.find(word)
                                line_sub = line_sub[posi:]
                                tech_candidates = [x for x in line_sub.split(' ') if x != '']
                                for tech in tech_candidates:
                                    if tech[0] == ' ':
                                        tech = tech[1:]
                                    # if tech.lower() in tech_voca:
                                    if len(tech.split()) < 3 and any(item in tech.lower() for item in tech_voca):
                                        tech_in_line = tech_in_line + tech + ", "
                                break
                        if len(tech_in_line) / len(line_sub) > 0.4:
                            tech_skills += [remove_special_character_at_lead(s.lstrip().rstrip('.'))
                                            for s in tech_in_line.split(",") if s != '']

                    line = re.sub("[\(\[].*?[\)\]]", "", line)
                    line = line_process(line)
                    words = line.split(" ")
                    for word in words:
                        word = word.replace(',', '')
                        if word.lower() in tech_voca:
                            # tech_in_line = tech_in_line + word + ", "
                            posi = line.find(word)
                            line = line[posi:]
                            tech_candidates = [x for x in line.split(',') if x != '']
                            for tech in tech_candidates:
                                if tech[0] == ' ':
                                    tech = tech[1:]
                                # if tech.lower() in tech_voca:
                                if len(tech.split()) < 3 and any(item in tech.lower() for item in tech_voca):
                                    tech_in_line = tech_in_line + tech + ", "
                            break
                    if len(tech_in_line) / len(line) > 0.4:
                        tech_skills += [remove_special_character_at_lead(s.lstrip().rstrip('.'))
                                        for s in tech_in_line.split(",") if s != '']
        except Exception as ex:
            # err = Err.Failed
            msg = 'Error stopping process: {}'.format(ex)
            log.error('err at {}\n because:{}'.format(sys._getframe().f_code.co_name, msg))
        finally:
            log.info('End {}'.format(sys._getframe().f_code.co_name))
            return list(set(tech_skills))
    return None


def line_process(line):
    for i in range(0, len(line) - 1):
        if line[i] == ',' and line[i + 1] != " ":
            line = line.replace(',', ', ')
            line = line.replace('  ', ' ')
    if line.find('- ') != -1:
        line = line.replace('- ', ' ')
    return line
