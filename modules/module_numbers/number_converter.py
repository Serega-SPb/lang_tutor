""" Convert range (0, 10^12) with including 10^12"""

from collections import namedtuple


Number = namedtuple('Number', 'value hiragana, kanji')


base_numbers = {
    0: Number(0, 'れい', '零'),
    1: Number(1, 'いち', '一'),
    2: Number(2, 'に', '二'),
    3: Number(3, 'さん', '三'),
    4: Number(4, 'よん', '四'),
    5: Number(5, 'ご', '五'),
    6: Number(6, 'ろく', '六'),
    7: Number(7, 'なな', '七'),
    8: Number(8, 'はち', '八'),
    9: Number(9, 'きゅう', '九'),
    10: Number(10, 'じゅう', '十'),
    100: Number(100, 'ひゃく', '百'),
    1000: Number(1000, 'せん', '千'),
    10000: Number(10000, 'まん', '万'),
    100000000: Number(100000000, 'おく', '億')
}

exceptions = {
    10: Number(10, 'じゅう', '十'),
    100: Number(100, 'ひゃく', '百'),
    300: Number(300, 'さんびゃく', '三百'),
    600: Number(600, 'ろっぴゃく', '六百'),
    800: Number(800, 'はっぴゃく', '八百'),
    1000: Number(1000, 'いっせん', '一千'),
    3000: Number(3000, 'さんぜん', '三千'),
    8000: Number(8000, 'はっせん', '八千')
}


def __convert_man(num, end_num=None):
    if num == 0:
        return
    kan, hir = '', ''
    for i in range(len(str(num))):
        ord_num = 10 ** i
        ch = num % (10 * ord_num) // ord_num
        if ch == 0:
            continue
        ch_num = base_numbers[ch]
        check_val = ch * ord_num
        if check_val in exceptions:
            if check_val == 1000 and end_num is None:
                ch_num = base_numbers[ord_num]
            else:
                ch_num = exceptions[check_val]
        else:
            if ord_num > 1:
                kan = f'{base_numbers[ord_num].kanji}{kan}'
                hir = f'{base_numbers[ord_num].hiragana}{hir}'
        kan = f'{ch_num.kanji}{kan}'
        hir = f'{ch_num.hiragana}{hir}'
    if end_num:
        kan += end_num.kanji
        hir += end_num.hiragana
    return Number(num, hir, kan)


def convert(num):
    oku_sep = 10 ** 8
    man_sep = 10 ** 4

    oku_num = base_numbers[100000000]
    man_num = base_numbers[10000]

    len_of_num = len(str(num))

    if num == 0:
        return base_numbers[0]

    oku_s, man_s, kaz_s = None, None, None
    if len_of_num >= 9:
        oku_s = __convert_man(num // oku_sep, oku_num)
    if len_of_num >= 5:
        man_s = __convert_man(num % oku_sep // man_sep, man_num)
    kaz_s = __convert_man(num % man_sep)

    parts = [oku_s, man_s, kaz_s]
    return Number(num,
                  ''.join([p.hiragana for p in parts if p is not None]),
                  ''.join([p.kanji for p in parts if p is not None]))
