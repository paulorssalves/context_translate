import pandas as pd
import itertools
import csv
from reverso_context_api import Client
from time import sleep

# TODO: dar a esse programa prompts para não precisar deixar nada hard-coded

# número de itens a serem lidos
# interessante não fazer mais do que trinta, no máximo. Mas idealmente, cerca de 15.
REQUEST_NUMBER=2

# arquivos de entrada e saída
INPUT_FILE="slujenie.csv"
OUTPUT_FILE="slujenie_out.csv"

# línguas
client = Client("ru", "en")

# arquivo a ser lido
f = pd.read_csv(INPUT_FILE, header=None, names=['word(s)'])

# parte do arquivo a ser lido
head = f.head(REQUEST_NUMBER)

# TODO: adicionar sleep a cada 20 iterações
data = []
for cell in head.iteritems():
    for words in cell[1]:
        l = []
        l.append(words)
        l += list(itertools.islice(client.get_translation_samples(words, cleanup=True), 3))
        l.append(list(list(client.get_translations(words)))[:5])
        data.append(l)
        #data += list(list(itertools.islice(client.get_translation_samples(words, cleanup=True), 3)))


def gen_translations(data):
    # palavras 
    originals = []
    originals_translated=[]

    # frases 
    target_phrases = []
    translated_phrases= []

    # a partir daqui, estamos juntando todas as strings em uma só e separando-as
    # apenas com uma newline. Por quê? Pra vincular todas as (cinco) traduções
    # da palavra e suas frases e as traduções desta a uma mesma célula
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

            # pode ser que não haja exemplo
            except IndexError:
                pass
                    
        try:
            t_break_n=0
            for item in group[4]:
                t_break_n += 1
                if t_break_n <= 4: 
                    wt+="\n"
                wt+=item

        # pode ser que não haja exemplo
        except IndexError:
            pass

        originals.append(group[0])
        originals_translated.append(wt)
        target_phrases.append(p)
        translated_phrases.append(t)

    g = {'col0':originals, 'col1': originals_translated,'col2':target_phrases, 'col3':translated_phrases}

    return g

k = gen_translations(data)
df = pd.DataFrame(k)
df.set_index('col0', inplace=True)
df.to_csv(OUTPUT_FILE, encoding="utf-8", mode="w", header=False)

