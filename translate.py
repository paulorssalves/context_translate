from tools import (get_word_data, get_word_fallback, 
                   produce_dataframe, append_to_csv)
from time import sleep
import readline
import pandas as pd

# Variáveis numéricas
TRANSLATION_NUMBER = 3
EXAMPLE_NUMBER = TRANSLATION_NUMBER
ITERATION_CYCLE=20
WAIT_TIME=30
REQUEST_NUMBER=30

# filename autocompletion
readline.parse_and_bind("tab: complete")

# arquivos de entrada e saída
#INPUT_FILE=input("Insira o nome do arquivo de entrada: ")
#OUTPUT_FILE=input("Insira o nome do arquivo de saída: ")
INPUT_FILE="input.csv"
OUTPUT_FILE="output.csv"

# arquivo a ser lido
f = pd.read_csv(INPUT_FILE, header=None, names=['word(s)'])

# parte do arquivo a ser lido
head = f.head(REQUEST_NUMBER)

if __name__ == "__main__":
    iterations = 0
    for cell in head.iteritems():
        for word in cell[1]:
            if iterations == ITERATION_CYCLE:
                for i in range(1, WAIT_TIME+1): 
                    print("waiting... {}/{}".format(i, WAIT_TIME))
                    sleep(1)
            
            iterations += 1
            print(word)
            word_data = get_word_data(word, TRANSLATION_NUMBER, EXAMPLE_NUMBER)
            if word_data == False: # retorna falso quando não há exemplo objetivo de tradução (mesmo havendo exemplos em frases; isso é feito por medida de segurança)
                continue
            df = produce_dataframe(word_data)
            append_to_csv(df, OUTPUT_FILE)