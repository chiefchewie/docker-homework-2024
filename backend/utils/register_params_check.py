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


def validate_password(psswd: str):
    if type(psswd) is not str:
        return False

    if len(psswd) < 8 or len(psswd) > 15:
        return False

    # at least 1 uppercase
    if len(filter(lambda c: c in string.ascii_uppercase, psswd)) < 1:
        return False

    # at least 1 lowercase
    if len(filter(lambda c: c in string.ascii_lowercase, psswd)) < 1:
        return False

    # at least 1 digit
    if len(filter(lambda c: c in string.digits, psswd)) < 1:
        return False

    # at least 1 special character
    if len(filter(lambda c: c in '-_*^', psswd)) < 1:
        return False

    return True


def validate_mobile(mobile: str):
    if type(mobile) is not str:
        return False

    # match + then match a digit number then match a '.' then match a 12 digit number
    return re.match(r'^\+\d{2}\.\d{12}$')


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

    if len(domain) > 48:
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

    if 'nickname' not in content:
        return 'nickname', False

    if 'mobile' not in content or not validate_mobile(content['mobile']):
        return 'mobile', False

    if 'url' not in content or not validate_url(content['url']):
        return 'url', False

    if 'magic_number' in content:
        magic_num = content['magic_number']
        return type(magic_num) is int and magic_num >= 0
    else:
        content['magic_number'] = 0

    return "ok", True
