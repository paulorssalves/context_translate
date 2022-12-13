from reverso_context_api import Client
import itertools as itt
import pandas as pd
import sys, time, random

LANGUAGE_TUPLE = ("en", "pt")
client = Client(LANGUAGE_TUPLE[0], LANGUAGE_TUPLE[1])

def get_translations(word, example_number, LANGUAGES=None):

    """
    Extrai traduções da palavra (String) direto do Reverso Context.
    O número de traduções corresponde ao (Inteiro) "example_number"
    """
    global LANGUAGE_TUPLE
    if LANGUAGES != None:
        LANGUAGE_TUPLE = LANGUAGES

    translation_list = list(client.get_translations(word.lower(), 
                            source_lang=LANGUAGE_TUPLE[0], 
                            target_lang=LANGUAGE_TUPLE[1]))[:example_number]

    return translation_list

def get_phrases_from_word(word, example_number, group_languages=True, LANGUAGES=None):
    """
    Extrai do Reverso Context frases (e traduções destas) que 
    contextualizam a palavra escolhida. A opção "group_languages=True" 
    separa as frases por língua (de modo que se temos 6 frases, 
    3 em língua estrangeira (E) e 3 na língua que conhecemos (C), elas virão
    agrupadas por idioma, e não por correspondência): EEE-CCC. "group_languages=False"
    resultaria em frases intercaladas: EC-EC-EC
    """
    global LANGUAGE_TUPLE
    if LANGUAGES != None:
        LANGUAGE_TUPLE = LANGUAGES

    phrase_list = list(itt.islice(client.get_translation_samples(word.lower(), 
        cleanup=True, 
        source_lang=LANGUAGE_TUPLE[0], 
        target_lang=LANGUAGE_TUPLE[1]), 
        example_number))

    if group_languages is False:
        return phrase_list

    input_language_example_list = []
    output_language_example_list = []

    for group in phrase_list:
        input_language_example_list.append(group[0])
        output_language_example_list.append(group[1])
    
    phrase_dict = {"input phrases": input_language_example_list,
                   "output phrases": output_language_example_list}

    return phrase_dict

def get_word_data(word, translation_number, example_number, LANGUAGES=None):
    """
    Adquire os dados relacionados à palavra inserida, isto é,
    suas traduções e exemplos dela em contexto. O número de traduções
    e de frases contextualizantes são definidos, respectivamente,
    pelos parâmetros "translation_number" e "example_number"
    """

    translations = get_translations(word.lower(), translation_number, LANGUAGES)

    if translations == []:
        return False

    data =  {
        "name": word.lower(),
        "translations": translations, 
        "examples": get_phrases_from_word(word.lower(), example_number, LANGUAGES)
        } 

    return data

def fetch_element_as_string(dict, element):
    """
    Transforma lista dentro do dicionário em string.
    Deste modo, o arquivo .csv final não fica cheio
    de colchetes.
    """
    if element == "name":
        return dict["name"]
    elif element == "translations":
        output = "" 
        for index in range(len(dict[element])):
            output += dict[element][index]
            if index < len(dict[element]) - 1:
                output+="<br><br>"
        return output
    elif (element == "input phrases") or (element == "output phrases"):
        output = ""
        for index in range(len(dict["examples"][element])):
            output += dict["examples"][element][index]
            if index < len(dict["examples"][element]) - 1:
                output+="<br><br>"
        return output
    else:
        return "There is no such element."

def produce_dataframe(dictionary):
    """
    produz um dataframe separando palavras da seguinte forma:
    PALAVRA ORIGINAL | TRADUÇÕES | EXEMPLOS NA LÍNGUA ESTRANGEIRA | EXEMPLOS TRADUZIDOS
    """
    data = dictionary
    final_dictionary = {
        "name": fetch_element_as_string(data, "name"),
        "traduções": fetch_element_as_string(data, "translations"),
        "exemplos": fetch_element_as_string(data, "input phrases"),
        "exemplos traduzidos": fetch_element_as_string(data, "output phrases"),
    }

    return pd.DataFrame(final_dictionary, index=[0])


def append_to_csv(DataFrame, OUTPUT_FILE_NAME):
    """
    Incrementa o dataframe a um .csv. Isso impede que qualquer progresso
    seja perdido caso por algum motivo o programa encontra um erro. A alternativa
    seria criar o .csv apenas quando o programa terminar de rodar, mas aí
    todos os dados seriam perdidos no caso de um erro.
    """
    DataFrame.to_csv(OUTPUT_FILE_NAME, encoding="utf-8", mode="a", header=False, index=False)
    
def time_log(DURATION):
    sys.stdout.write("\n")
    for second in range(DURATION):
        sys.stdout.write('Wait... %s/%s\r' % (second+1, DURATION))
        time.sleep(1)
        sys.stdout.flush()
    time.sleep(random.random())

def progress (count, total, suffix=""):
    # taken from Vladmir Ignatev on GitHub
    bar_len = 60
    filled_len = int(round(bar_len * count / float (total)))

    percents = round(100.0 * count / float(total), 1)
    bar = "=" * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush() # as suggested by Rom Ruben
