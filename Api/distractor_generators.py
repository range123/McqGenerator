# import nlp2go
# import spacy
# from sense2vec import Sense2VecComponent
import requests
import json
from typing import List, Optional
import nltk
import string


class DistractorGenerator:
    
    def __init__(self, model_path : str):
        pass
    def generate_distractors(self, question : str, answer : str):
        pass

# class BertDistractorGenerator(DistractorGenerator):
    
#     def __init__(self, BDG_model_path : str, BDG_ANPM_model_path : str, BDG_PM_model_path : str):
#         self.bdg = nlp2go.Model(model_path = BDG_model_path)
#         self.bdg_anpm = nlp2go.Model(model_path = BDG_ANPM_model_path)
#         self.bdg_pm = nlp2go.Model(model_path = BDG_PM_model_path)
#     def generate_distractors(self, text : str, question : str, answer : str):
#         temp = {'input' : text + ' [SEP] ' + question + ' [SEP] ' + answer}
#         res = []
#         res += self.bdg.predict(temp)['result']
#         res += self.bdg_anpm.predict(temp)['result']
#         res += self.bdg_pm.predict(temp)['result']
#         return res

# class Sense2VecDistractorGenerator(DistractorGenerator):

#     def __init__(self, model_path : str):
#         self.spacy_nlp = spacy.load("en_core_web_lg")
#         s2v = Sense2VecComponent(self.spacy_nlp.vocab).from_disk(model_path)
#         self.spacy_nlp.add_pipe(s2v)

#     def generate_distractors(self, question : str, answer : str, limit : int = 3):
#         doc = self.spacy_nlp(answer)
#         ans = [doc]
#         for ent in doc:
#             try:
#                 assert ent._.in_s2v
#                 most_similar = ent._.s2v_most_similar(10)
#                 for m in most_similar:
#                     text = m[0][0].lower()
#                     if text not in ans:
#                         ans.append(text)
#             except:
#                 continue
#         return ans

class Sense2VecDistractorGenerator(DistractorGenerator):
    def __init__(self):
        self.url = "https://api.explosion.ai/sense2vec2/find"

        # self.payload= '{"word":{},"sense":{},"model":"2019"}'
        self.headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'DNT': '1',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://explosion.ai',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }
        self.st = list(string.punctuation)
        self.st += nltk.corpus.stopwords.words("english")
        self.l = ["CD","FW","JJ","NN","NNS","NNP","NNPS","POS","RB","RP","VB","VBD","VBG","VBN","VBP","VBZ"]
    
    def _preprocess(self, text : str) -> str:
        
        if len(text.split())>1 :
            ind = text.find(",")
            text = text[:ind if ind >=0 else len(text)].split()

            text = ' '.join(filter(lambda x : x not in self.st,text))
            tokens = nltk.word_tokenize(text)
            res = nltk.pos_tag(tokens)
            ans = list(filter(lambda x : x[1] in self.l,res))
            ans = ' '.join(map(lambda x : x[0], ans))
            ans = ans.strip()
            return ans
        else:
            return text
        # return ' '.join(text.split()).strip()
    
    def _postprocess(self, distractors : List[str], answer : str, limit : Optional[int] = None) -> List[str] :
        # TODO shuffle the distractors ?
        # TODO code this function better
        s = set()
        ans = []
        filtered = filter(lambda x : answer.lower().strip() not in x.lower().strip(), distractors)
        for dist in filtered:
            if dist.lower().strip not in s:
                s.add(dist.lower().strip)
                ans.append(dist.lower().strip())
        limit = min(limit if limit else float('inf'), len(ans))
        return ans[:limit] 

    def generate_distractors(self, question : str, answer : str, limit : int = 3) -> List[str]:
        sense  = 'auto'
        answer = self._preprocess(answer)
        
        data = json.dumps({
            'word' : answer,
            'sense' : sense,
            'model' : '2019'
        })
        response = requests.request("POST", self.url, headers=self.headers, data=data, timeout=60)
        distractors = []
        for dist in json.loads(response.text)['results']:
            distractors.append(dist['text'])
        return self._postprocess(distractors, answer, limit), answer


        

class ConceptNetDistractorGenerator(DistractorGenerator):
    def __init__(self, BDG_model_path : str, BDG_ANPM_model_path : str, BDG_PM_model_path : str):
        pass
    def generate_distractors(self, question : str, answer : str):
        pass

if __name__ == "__main__":
    pass
    # model = Sense2VecDistractorGenerator('../../saved_models/s2v_reddit_2019_lg/s2v_reddit_2019_lg')
    # print(model.generate_distractors('', 'cricket ball',5))


    

    # print(response.text)

    