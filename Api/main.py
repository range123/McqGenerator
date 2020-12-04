from question_generators import T5QuestionAnswerGenerator
from distractor_generators import Sense2VecDistractorGenerator
from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import yaml
import logging

logger = logging.getLogger()

tags_metadata = [
    {
        "name": "mcqs",
        "description": "Generate **MCQs** from given text ",
    }
]
app = FastAPI(
    title="API for NLP App",
    description="API which exposes endpoints for MCQ generation from text and other NLP tasks",
    version="0.0.1",
)
# TODO Add known origins later and pass to allow_origins instead of *
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_config(fpath):
    '''
    Reads a yaml file and returns it as a dict
    Args:
        fpath (str) : The path to the yaml file.
    Returns:
        dict (dict) : Dictionary containing the contents of the yaml file. 
    '''
    try:
        with open(fpath) as f:
            return yaml.safe_load(f)
    except:
        logger.error('Cannot open ./config.yml, using default model path')
        return {'T5ModelPath' : 'valhalla/t5-small-qa-qg-hl'}

class MCQ(BaseModel):
    question : str
    answer : str
    distractors : List[str]

class InputModel(BaseModel):
    source : str = Field(..., title='Source Text', 
                    description='The text from which MCQs will be generated'
                    )
    max_questions : Optional[int] = Field(None, title='Maximum Questions',
                                    description= 'Maximum number of questions to generate', ge=1)
    max_distractors : Optional[int] = Field(None, title='Maximum Distractors',
                                        description='Maximum number of distractors to generate per question', ge=0)
    @validator('source')
    def should_have_min_words(cls, v):
        if len(v.split()) < 5:
            raise ValueError('Should contain atleast 5 words')
        return v
    class Config:
        schema_extra = {
            "example": {
                "source": 'Simple is better than complex.',
                'max_questions' : 5,
                'max_distractors' : 5
            }
        }

qmodel, dmodel = None, None 

@app.on_event('startup')
def load_models():
    global qmodel, dmodel
    config = load_config('./config.yml')
    logger.info('Loading Model...')
    try:
        qmodel = T5QuestionAnswerGenerator(config['T5ModelPath'])
    except:
        logger.error('Invalid model path provided, using default path')
        qmodel = T5QuestionAnswerGenerator('valhalla/t5-small-qa-qg-hl')
    dmodel = Sense2VecDistractorGenerator()


@app.post('/generate_mcqs', tags = ['mcqs'], response_model = List[MCQ])
async def generate_mcqs(inp : InputModel):
    res = qmodel.generate_question_answer(inp.source, max_questions= inp.max_questions)
    for i,mcq in enumerate(res):
        distractors, ans = dmodel.generate_distractors(mcq['question'], mcq['answer'], limit = inp.max_distractors)
        res[i]['distractors'] = distractors 
    return res

if __name__ == "__main__":
    config = load_config('./config.yml')
    qmodel = T5QuestionAnswerGenerator('../saved_models/t5-small-qa-qg-hl')
    dmodel = Sense2VecDistractorGenerator()
    uvicorn.run(app,host='0.0.0.0',port=8000)
    # text = None
    # with open('test.txt','r') as f:
    #     text = f.read()
    # res = qmodel.generate_question_answer(text)
    # # questions, answers = res['question']
    # d = []
    # for i,qa in enumerate(res):
    #     print(f"{i+1}){qa['question']}")
    #     print(f' A) {qa["answer"]}')
    #     distractors, ans_proc = dmodel.generate_distractors(qa['question'],qa["answer"], limit = 4)
    #     distractors.append(ans_proc)
    #     for i,x in enumerate(distractors):
    #         print(f' {chr(66 + i)}) {x}')
    #     print()
    