from gensim import similarities
import pandas as pd

class Query:
    def __init__(self, model):
        self.model = model

    # consulta
    def search(self, query):
        query_string = query = query.lower().split()
        query = self.model.dictionary.doc2bow(query)
        query = self.model.lsi[query]
        
        # ranqueamento dos documentos
        index = similarities.MatrixSimilarity(self.model.corpus_lsi)
        sims = index[query]
        
        # criando um DataFrame com o ranqueamento, o índice dos documentos e o título
        ranking = pd.DataFrame({'similarity': sims, 'index': range(len(self.model.documents)), 'title': [document[1] for document in self.model.documents]})

        # ordenando o dataframe de forma decrescente
        ranking.sort_values(by=['similarity'], ascending=False, inplace=True)
        
        results = {}
        for i, row in ranking.iterrows():
            # encontrando a posição da query no documento

            query_pos = self.model.documents[int(row['index'])][2].lower().find(query_string[0])
            if query_pos == -1:
                continue

            results.setdefault(self.model.documents[int(row['index'])][1],[])
            results[self.model.documents[int(row['index'])][1]].append(self.model.documents[int(row['index'])][2])

        # retornando o ranqueamento dos documentos
        return results