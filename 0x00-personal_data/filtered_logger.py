#!/usr/bin/env python3
""" PII Module """

import re


def filter_datum(fields, redaction, message, separator):
    """ Returns log message obfuscated """
    pattern = fr'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, f'\\1={redaction}', message)
