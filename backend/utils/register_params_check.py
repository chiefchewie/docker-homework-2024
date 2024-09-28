# -*- coding: utf-8 -*-

import re
import string


def validate_username(username: str):
    if type(username) is not str:
        return False

    if len(username) < 5 or len(username) > 12:
        return False

    # username must be (one or more alphas) followed by (one or more digits)
    if not re.match(r'^[A-Za-z]+\d+$', username):
        return False

    return True


def validate_password(password: str):
    if type(password) is not str:
        return False

    if len(password) < 8 or len(password) > 15:
        return False

    has_uppercase = False
    has_lowercase = False
    has_digit = False
    has_special = False

    for c in password:
        if c in string.ascii_uppercase:
            has_uppercase = True
        elif c in string.ascii_lowercase:
            has_lowercase = True
        elif c in string.digits:
            has_digit = True
        elif c in '-_*^':
            has_special = True
        else:
            return False

    return has_uppercase and has_lowercase and has_digit and has_special


def validate_mobile(mobile: str):
    if type(mobile) is not str:
        return False

    # match + then match a digit number then match a '.' then match a 12 digit number
    return re.match(r'^\+\d{2}\.\d{12}$', mobile)


def validate_url(url: str):
    if type(url) is not str:
        return False

    # check both the protocal and extract domain
    if url.startswith('http://'):
        domain = url[8:]
    elif url.startswith('https://'):
        domain = url[9:]
    else:
        return False

    if len(domain) > 48 or '.' not in domain:
        return False

    # domain is labels separated by '.'
    labels = domain.split('.')
    for i, l in enumerate(labels):
        # labels can't be empty, nor can they start/end with '-'
        if len(l) == 0 or l[0] == '-' or l[-1] == '-':
            return False

        # match the contents of the label with alphanumeric chars and '-'
        if not re.match(r'[-A-Za-z0-9]+', l):
            return False

        # last label can't be all digits
        if i == len(labels) - 1 and l.isdigit():
            return False

    return True


def register_params_check(content: dict):
    """
    TODO: 进行参数检查
    """
    if 'username' not in content or not validate_username(content['username']):
        return 'username', False

    if 'password' not in content or not validate_password(content['password']):
        return 'password', False

    if 'nickname' not in content or type(content['nickname']) is not str:
        return 'nickname', False

    if 'mobile' not in content or not validate_mobile(content['mobile']):
        return 'mobile', False

    if 'url' not in content or not validate_url(content['url']):
        return 'url', False

    if 'magic_number' in content:
        magic_num = content['magic_number']
        if type(magic_num) is not int or magic_num < 0:
            return 'magic_number', False
    else:
        content['magic_number'] = 0

    return "ok", True
