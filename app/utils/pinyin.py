from app.utils.pinyin_db import py_db


def get_all_pinyin(content=''):
    return ''.join([py_db.get('%X' % ord(c), c).split()[0][:-1].lower() for c in content])


def get_first_char(content=''):
    try:
        return py_db.get('%X' % ord(content[0]), content[0]).split()[0][:-1].upper()[0]
    except IndexError:
        return ''


def get_all_first_char(content=''):
    return ''.join([py_db.get('%X' % ord(c), c).split()[0][0].lower() for c in content])


if __name__ == "__main__":
    string = "龍行天"
    print("in: %s" % string)
    test_res = get_first_char(string)
    print("out: ", test_res, ' type -> ', type(test_res))
    print("out: ", get_all_pinyin(string))
    print("out: ", get_all_first_char(string))
