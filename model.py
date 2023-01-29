from gensim import corpora, models
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords

class Model:
    def __init__(self, documents):
        self.documents = documents
        self.corpus_lsi = None
        self.lsi = None
        self.dictionary = None
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words("portuguese"))
        self.create_model()

    def create_model(self):
        # pré-processamento de texto
        texts = [[word for word in self.preprocess_document(document[2])] for document in self.documents]
        self.dictionary = corpora.Dictionary(texts)
        corpus = [self.dictionary.doc2bow(text) for text in texts]

        # criação do modelo vetorial
        self.lsi = models.LsiModel(corpus, id2word=self.dictionary, num_topics=2)
        self.corpus_lsi = self.lsi[corpus]

    def preprocess_document(self, document):
        tokens = word_tokenize(document.lower())
        tokens = [token for token in tokens if not token in self.stop_words]
        
        return tokens