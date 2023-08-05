from decimal import Decimal
import json, requests
from re import match
from flask import url_for

# this the fall back currency convert function, which uses the converion table stored on rates.json file
def currency_convert(rates, from_currency_code, to_currency_code, from_amount):

    if from_currency_code == 'USD':
        to_amount = Decimal(from_amount) * Decimal(rates[to_currency_code])
    else:
        to_amount = Decimal(from_amount) * Decimal(rates[to_currency_code]) / Decimal(rates[from_currency_code])

    return to_amount


# uses regex, returns true if string is a number
def is_num(s):
    if match("^\d+?\.\d+?$", s) is None:
        return s.isdigit()
    return True
