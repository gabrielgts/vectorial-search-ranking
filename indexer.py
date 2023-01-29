from bs4 import BeautifulSoup
import re

base_path = './corpus'

class Indexer:
    def __init__(self, mainUrl):
        self.mainUrl = mainUrl
        self.documents = []
        self.index_site()

    def getHTMLdocument(self, url):
        with open('{}/{}'.format(base_path, url), encoding='ISO-8859-1') as fp:
            return BeautifulSoup(fp, 'html.parser')

    def index_site(self):
        id = 1
        site_index = self.getHTMLdocument(self.mainUrl)
        self.documents.append((id, 'homepage', self.preprocess_document(site_index.get_text())))

        for item in site_index.select('a'):
            id += 1
            item_link = item.get('href') if item else None
            try:
                content = self.getHTMLdocument(item_link)
                self.documents.append((id, ' '.join(item.contents), self.preprocess_document(content.get_text())))
            except FileNotFoundError:
                continue
        return self.documents

    def preprocess_document(self, document):
        return re.sub(r'[^\w\s]','', document.lower()).replace('\n', ' ').replace('\xa0', ' ')


