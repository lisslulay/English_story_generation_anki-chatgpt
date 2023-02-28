from constant import *

def format_word(s:str) -> str:
    if not s:
        return s
    
    s = s.split(" ", 1)[0].strip()
    if s[-1] == '*':
        s = s[0:-1]
    return s

def read_file(file_name, group_num) -> list[list[list[str], str], ...]:
    with open(file_name, "r", encoding="utf-8") as f:
        count = 0
        group = []
        res = []
        voc = ""
        while True:
            vocabulary = f.readline()
            format_vocabulary = format_word(vocabulary)
            if vocabulary:
                group.append(format_vocabulary)
                voc += vocabulary
            count += 1
            
            # end of the file
            if not vocabulary:
                if group != []:
                    res.append([group, voc])
                break
            # group by GROUP_NUM
            elif count % group_num == 0:
                res.append([group, voc])
                group = []
                voc = ""
    return res

