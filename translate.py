from tools import (get_word_data, 
                   produce_dataframe, append_to_csv)
import time, random, datetime, sys
import readline
import pandas as pd

# Variáveis numéricas
TRANSLATION_NUMBER = 3
EXAMPLE_NUMBER = TRANSLATION_NUMBER
WAIT_TIME=5

# filename autocompletion
readline.parse_and_bind("tab: complete")

INPUT_FILE=""

try:
    if sys.argv[1]:
        INPUT_FILE = str(sys.argv[1])
except IndexError:
    print("Defaulting to 'words.csv' as input file")
    INPUT_FILE="words.csv"

OUTPUT_FILE = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".csv"

# arquivo a ser lido
f = pd.read_csv(INPUT_FILE, header=None, names=['word(s)'])

REQUEST_NUMBER = len(f)

# parte do arquivo a ser lido
head = f.head(REQUEST_NUMBER)

if __name__ == "__main__":
    for cell in head.iteritems():
        for word in cell[1]:
            print(word)
            word_data = get_word_data(word, TRANSLATION_NUMBER, EXAMPLE_NUMBER)
            for sec in range(1,WAIT_TIME+1):
                if sec == WAIT_TIME:
                    print(f"wait... {sec}/5")
                    time.sleep(1+(2*random.random()))
                else:
                    print(f"wait... {sec}/5")
                    time.sleep(1)
            if word_data == False: # retorna falso quando não há exemplo objetivo de tradução (mesmo havendo exemplos em frases; isso é feito por medida de segurança)
                continue
            df = produce_dataframe(word_data)
            append_to_csv(df, OUTPUT_FILE)

