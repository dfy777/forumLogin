def writeSplit(str, index):
    res = []
    left = 0
    right = 0+index
    while True:
        if right >= len(str):
            if left >= len(str):
                break
            res.append(str[left:len(str)])
            break
        res.append(str[left:right])
        left = right
        right = left + index
    return res

def writeInfo(response):
    with open("cookies.log", 'w', encoding="utf-8") as f:
        res = ""


        f.write('cookie:\n\n')
        res = writeSplit(response.getheader('Set-Cookie'), 80)
        for i in res:
            f.write(i+'\n')
        f.write("\n\n================================================\n\n")


        f.write('headers:\n\n')
        res = writeSplit(str(response.headers), 80)
        for i in res:
            f.write(i+'\n')
        f.write("\n\n================================================\n\n")

        f.write('data:\n\n')
        res = writeSplit(response.data.decode('utf-8'), 80)
        for i in res:
            f.write(i+'\n')
        f.write(response.data.decode('utf-8'))
        f.write("\n\n================================================\n\n")