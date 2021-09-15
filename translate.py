import pandas as pd
import itertools
import csv
from reverso_context_api import Client
from time import sleep

REQUEST_NUMBER=2
OUTPUT_FILE="slujenie_out.csv"
INPUT_FILE="slujenie.csv"

client = Client("ru", "en")

f = pd.read_csv(INPUT_FILE, header=None, names=['word(s)'])
head = f.head(REQUEST_NUMBER)

data = []
for cell in head.iteritems():
    for words in cell[1]:
        l = []
        l.append(words)
        l += list(itertools.islice(client.get_translation_samples(words, cleanup=True), 3))
        l.append(list(list(client.get_translations(words)))[:5])
        data.append(l)
        sleep(5)
        #data += list(list(itertools.islice(client.get_translation_samples(words, cleanup=True), 3)))


def gen_translations(data):
    word_list = []
    phrase_list= []
    originals = []
    trans_list=[]

    for group in data:
        break_n=0
        p = ""
        t = ""
        wt = ""

        for phrase in group[1:5]:
            break_n+=1
            try:
                t+=phrase[1]
                p+=phrase[0]
                if break_n <= 2:
                    p+="\n"
                    t+="\n"
            except IndexError:
                pass
                    
        try:
            t_break_n=0
            for item in group[4]:
                t_break_n += 1
                if t_break_n <= 4: 
                    wt+="\n"
                wt+=item
        except IndexError:
            pass

        originals.append(group[0])
        trans_list.append(wt)
        word_list.append(p)
        phrase_list.append(t)

    g = {'col0':originals, 'col1': trans_list,'col2':word_list, 'col3':phrase_list}

    return g

k = gen_translations(data)
df = pd.DataFrame(k)
df.set_index('col0', inplace=True)
df.to_csv(OUTPUT_FILE, encoding="utf-8", mode="w", header=False)

