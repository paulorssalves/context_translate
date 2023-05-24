from tools import (get_word_data, 
                   produce_dataframe, append_to_csv,
                   time_log, progress)
import datetime, sys
import readline
import pandas as pd

# Variáveis numéricas
TRANSLATION_NUMBER = 3
EXAMPLE_NUMBER = 3 
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

    wordlist = list(head.items())[0][1]

    for index in range(len(wordlist)):
        word_data = get_word_data(wordlist[index], TRANSLATION_NUMBER, EXAMPLE_NUMBER)

        if word_data == False: # retorna falso quando não há exemplo objetivo de tradução (mesmo havendo exemplos em frases; isso é feito por medida de segurança)
            print ("Sem traduções disponíveis para \"{}\". Pulando...".format(wordlist[index]))
            continue

        progress(index+1, REQUEST_NUMBER, "{} ({}/{})".format(word_data["name"], index+1, REQUEST_NUMBER))

        df = produce_dataframe(word_data)
        append_to_csv(df, OUTPUT_FILE)

        time_log(WAIT_TIME) 
