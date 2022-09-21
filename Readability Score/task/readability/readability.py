import math
import re
import sys

def syllable_cnt(word):
    word = re.sub(r'([.!?]|, )', '', word.lower())
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e") or word.endswith("led"):
        count -= 1
    if count == 0:
        count += 1
    p_cnt = 1 if count > 2 else 0
    res = (count, p_cnt)
    return res

def words(text):
    words = list(filter(None, re.split(r'[ \n\t]', text)))
    return words

def dif_words(text):
    wrds = words(text)
    wrds = [re.sub(r'[)(.!?,]', '', w.lower()) for w in wrds]
    dw = [w for w in wrds if w not in words_lst]
    return dw

def sentences(text):
    return list(filter(None, re.split(r'[!.?\n]', text)))

def chars(text):
    return list(filter(None, re.findall(r'[\S]', text)))

def f_ari(s, w, ch):
    return 4.71 * len(ch) / len(w) + 0.5 * len(w) / len(s) - 21.43

def f_fk(s, w, syl):
    return 11.8 * syl / len(w) + 0.39 * len(w) / len(s) - 15.59

def f_cl(s, w, ch):
    return 5.89 * len(ch) / len(w) - 30 * len(s) / len(w) - 15.8

def f_smog(psyl, s):
    return 1.043 * math.sqrt(psyl * 30 / len(s)) + 3.1291

def f_dc(s, w, dw):
    score = 15.79 * len(dw) / len(w) + 0.0496 * len(w) / len(s)
    if len(dw) / len(w) >= 0.05:
        score += 3.6365
    return score

dic = {'1': '7', '2': '8', '3': '9', '4': '10', '5': '11', '6': '12', '7': '13',
       '8': '14', '9': '15', '10': '16', '11': '17', '12': '18', '13': '24', '14': '24'}
dic_dc = {0: '10', 5: '12', 6: '14', 7: '16', 8: '18', 9: '24'}
args = sys.argv[1:]

if '--infile' in args and '--words' in args :
    i = args.index('--infile')
    fn = args[i + 1]
    with open(fn, 'r') as f:
        text = f.read()

    i = args.index('--words')
    fn = args[i + 1]
    with open(fn, 'r') as f:
        wrds = f.read()
    words_lst = wrds.split()

    ss = sentences(text)
    ww = words(text)
    ch = chars(text)
    dww = dif_words(text)

    syl = sum([syllable_cnt(w)[0] for w in ww])
    p_syl = sum([syllable_cnt(w)[1] for w in ww])
    score = 4.71 * len(ch) / len(ww) + 0.5 * len(ww) / len(ss) - 21.43
    age = dic[str(round(score))] if score < 15 else '22'

    print('The text is:\n', text)
    print(f'Words: {len(ww)}')
    print(f'Difficult words: {len(dww)}')
    print(f'Sentences: {len(ss)}')
    print(f'Characters: {len(ch)}')
    print(f'Syllables: {syl}')
    print(f'Polysyllables: {p_syl}')

    cmd = input('Enter the score you want to calculate (ARI, FK, SMOG, CL, DC, all): ').lower()
    print()
    sum_age = 0
    cnt = 0
    if cmd == 'all' or 'ari' in cmd:
        score = math.ceil(f_ari(ss, ww, ch))
        age = dic[str(score)] if score < 15 else '22'
        print(f'Automated Readability Index: {score} (about {age} year olds).')
        sum_age += int(age)
        cnt += 1
    if cmd == 'all' or 'fk' in cmd:
        score = math.ceil(f_fk(ss, ww, syl))
        age = dic[str(score)] if score < 15 else '22'
        print(f'Flesch–Kincaid readability tests: {score} (about {age} year olds).')
        sum_age += int(age)
        cnt += 1
    if cmd == 'all' or 'smog' in cmd:
        score = round(f_smog(p_syl, ss))
        age = dic[str(score)] if score < 15 else '22'
        print(f'Simple Measure of Gobbledygook: {score} (about {age} year olds).')
        sum_age += int(age)
        cnt += 1
    if cmd == 'all' or 'cl' in cmd:
        score = round(f_cl(ss, ww, ch))
        age = dic[str(score)] if score < 15 else '22'
        print(f'Coleman–Liau index: {score} (about {age} year olds).')
        sum_age += int(age)
        cnt += 1
    if cmd == 'all' or 'dc' in cmd:
        score = f_dc(ss, ww, dww)
        idx = 0 if score < 5 else int(score)
        age = dic_dc[idx] if score < 10 else '24'
        print(f'Dale-Chall: {round(score, 2)} (about {age} year olds).')
        sum_age += int(age)
        cnt += 1

    print(f'\nThis text should be understood in average by {round(sum_age/cnt, 1)} year olds.')
else:
    print(args)
