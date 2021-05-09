import hashlib
import requests
import re
import random
import time

algo = hashlib.sha1
encoding = 'utf-8'
line = 'from=danugener@gmail.com&name=Danya%20Generalov&to=schoolslon@gmail.com&amount=1.618033988749894&nonce={nonce}'
wordlist = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'
target_pattern = '^000[0-9a-f]{37}$'

words = requests.get(wordlist).text.split('\n')

while True:
    nonce = random.choice(words).replace(' ', '%20')
    phrase = line.format(nonce=nonce)
    phrase_bytes = bytes(phrase, encoding)
    phash = algo(phrase_bytes).hexdigest()
    if re.match(target_pattern, phash):
        print(nonce, phrase, phash, sep='\t')
        time.sleep(0.5)
