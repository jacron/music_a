def get_common(lines):
    common = ''
    small = ''
    for line in lines:
        if len(small) < len(line):
            small = line
    temp_common = ''
    for c in small:
        temp_common += c
        for line in lines:
            if temp_common not in line:
                temp_common = str(c)
                for line2 in lines:
                    if temp_common not in line2:
                        temp_common = ''
                        break
                break
        if temp_common != '' and len(temp_common) > len(common):
            common = temp_common
    return common


def main():
    titles = [
        '04 - Fantasiestucke, Op. 73 I. Zart und mut Ausdruck.flac',
        '05 - Fantasiestucke, Op. 73 II. Lebhaft, leicht.flac',
        '06 - Fantasiestucke, Op. 73 III. Rasch, mut Feuer.flac',
    ]
    common = get_common(titles)
    print(common)


if __name__ == '__main__':
    main()
