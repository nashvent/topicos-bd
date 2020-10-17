import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import json

lemmatizer = WordNetLemmatizer()


class InvertedIndex:
    documents = []
    index = {}
    process_content = ""
    custom_separator = "1111111111111111111111111"

    def __init__(self, array_content):
        self.docIds = array_content[:,0]
        self.content = array_content[:,1] # [[textKey, content]]
        print("self.docIds len", len(self.docIds))
        print("self.content", len(self.content))
        self.preprocessing_content()
        self.create_documents()

    def preprocessing_content(self):
        self.add_separator()
        self.remove_blank_spaces()
        self.remove_special_chars()
        self.remove_stop_words()
        self.lemmatizer_all()    

    def add_separator(self):
        # self.content = self.content.replace("*       *       *       *       *", custom_separator)
        self.process_content = self.custom_separator.join(self.content)
        self.process_content = self.process_content.replace("\n", " ")
        print("separator added")

    def remove_blank_spaces(self):
        self.process_content = re.sub(" +", " ", self.process_content)
        print("remove blank spaces")

    def remove_special_chars(self):
        # return re.sub('[^A-ZÜÖÄa-z0-9\s ]+', '', content)
        self.process_content = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,\*\n]", "", self.process_content)
        print("remove special chars")

    def remove_stop_words(self):
        stop_words = stopwords.words('english')
        tokens_without_sw = [w.lower() for w in self.process_content.split(
            " ") if w.lower() not in stop_words]
        self.process_content = " ".join(tokens_without_sw)
        print("remove stop words")

    def lemmatizer_all(self):
        lemmas_list = [lemmatizer.lemmatize(w)
                                            for w in self.process_content.split(" ")]
        
        self.process_content = " ".join(lemmas_list)
        print("finish lemmatizer")



    def create_documents(self):
        self.documents = self.process_content.split(self.custom_separator)
        print("self.documents len", len(self.documents))


    def mapper(self, document):
        current_map = {}
        array_doc = document.split(" ")
        for item in array_doc:
            if(item!=""):
                if item in current_map:
                    current_map[item] += 1
                else:
                    current_map[item] = 1
        return current_map

    def reducer(self, mapper, docId):
        for item in mapper:
            if item not in self.index:
                self.index[item] = []
            self.index[item].append({"docId": docId, "value": mapper[item]})

    def process(self):
        print("init process")
        count = 0
        for document in self.documents:
            if( len(self.docIds)> count ):
                current_map = self.mapper(document)
                self.reducer(current_map, self.docIds[count])
                count += 1
        print("finish proccess")

    def saveIndexInDisc(self):
        with open('../output/index.json', 'w') as outfile:
            json.dump(self.index, outfile)
