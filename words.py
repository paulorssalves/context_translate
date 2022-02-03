from wiktionaryparser import WiktionaryParser

INPUT_LANGUAGE="ru", "Russian"
parser = WiktionaryParser()

class DataNotAvailable(Exception):
    pass
class EtymologyNotAvailable(Exception):
    pass
class DefinitionsNotAvailable(Exception):
    pass 

def fetch_word(word, language=INPUT_LANGUAGE[1]):
   return parser.fetch(word, language)

class WordBase:
    def extract_item(self, word, selection):
        if word[0] != []:
            if word[0][selection]:
               return word[0][selection]
        else:
            raise DataNotAvailable

class Word(WordBase):
    def __init__(self, name):
        self.name = name
        self.data = fetch_word(name)
        self.definitions = self.get_definitions()
         
    def get_etymology(self):
        try:
            etymology = super().extract_item(self.data, "etymology")
            if (not etymology) or (etymology == []):
                raise EtymologyNotAvailable
            return etymology
        except EtymologyNotAvailable:
            print("Etymology not available.") 

    def get_definitions(self):
        try:
            definitions = super().extract_item(self.data, "definitions")
            if (not definitions) or (definitions == []):
                raise DefinitionsNotAvailable 
            return definitions 
        except DefinitionsNotAvailable:
            print("Definitions not available.")

    def get_word_class(self):
        if self.definitions is not None:
            return [item['partOfSpeech'] for item in self.definitions] 
        else:
            return ""

    def get_text(self):
        if self.definitions is not None:
            return [item['text'] for item in self.definitions]
        else:
            return ""

    def get_related_words(self):
        if self.definitions is not None:
            return [item['relatedWords'] for item in self.definitions]
        else: 
            return ""

    def get_examples(self):
        if self.definitions is not None:
            return [item['examples'] for item in self.definitions] 
        else:
            return ""