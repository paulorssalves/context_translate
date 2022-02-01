import pandas as pd
import itertools
from wiktionaryparser import WiktionaryParser
from reverso_context_api import Client
from time import sleep
import readline

parser = WiktionaryParser()
# número de itens a serem lidos
# interessante não fazer mais do que trinta, no máximo. Mas idealmente, cerca de 15.
REQUEST_NUMBER=int(input("Insira o número de palavras a buscar: "))
# REQUEST_NUMBER=278

# filename autocompletion
readline.parse_and_bind("tab: complete")

# arquivos de entrada e saída
INPUT_FILE=input("Insira o nome do arquivo de entrada: ")
OUTPUT_FILE=input("Insira o nome do arquivo de saída: ")
# INPUT_FILE="russian-words.csv"
# OUTPUT_FILE="out.csv"

# línguas
client = Client("ru", "en")

# arquivo a ser lido
f = pd.read_csv(INPUT_FILE, header=None, names=['word(s)'])

# parte do arquivo a ser lido
head = f.head(REQUEST_NUMBER)

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

iterations = 0 
for cell in head.iteritems():
    print(cell)
    for words in cell[1]:
        iterations += 1
        data = []
        l = []
        l.append(words)
        print(words)
        filter_list = list(list(client.get_translations(words, source_lang="ru", target_lang="en")))[:5]
        if filter_list == []:
            word = parser.fetch(words)
            if word == []:
                continue
            elif word[0]['definitions'] == []: 
                # checando se a palavra existe no Wiktionary
                # se não existe, ignorá-la
                continue 
            else: 
                # se existe, separar dados sobre ela em uma lista .csv separada 
                word_data = word[0]['definitions'][0]['text'] 
                organized_word_data= {'word': [word_data[0]], 'details': [word_data[1]]}
                word_dataframe = pd.DataFrame(organized_word_data)
                word_dataframe.set_index('word',inplace=True)
                word_dataframe.to_csv(OUTPUT_FILE+".alt.csv", encoding="utf-8", mode="a", header=False)

        else:
            l += list(itertools.islice(client.get_translation_samples(words, cleanup=True, source_lang="ru", target_lang="en"), 3))
            l.append(filter_list)
            data.append(l)
            organized_data = gen_translations(data) # dados obtidos no context reverso separados em quatro diferentes colunas
            df = pd.DataFrame(organized_data)
            df.set_index('col0', inplace=True)
            df.to_csv(OUTPUT_FILE, encoding="utf-8", mode="a", header=False)
        if iterations >= 20:
            for i in range(1,31):
                print("sleeping... {}/30".format(i))
                sleep(1)
            iterations = 0
