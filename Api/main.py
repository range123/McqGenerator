
from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import Path
from json import load, dumps
from requests import post, get

tags_metadata = [
    {
        "name": "Mcqs",
        "description": "Generate **MCQs** from given text ",
    },
    {
        "name": "Captions",
        "description": "Get **Captions** for given youtube video id ",
    }
]
app = FastAPI(
    title="API for NLP App",
    description="API which exposes endpoints for MCQ generation from text and other NLP tasks",
    version="0.0.1",
)

origins = [
    "http://mcq-generator.surge.sh",
    "https://mcq-generator.surge.sh",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MCQ(BaseModel):
    question: str
    answer: str
    distractors: List[str]


class InputModel(BaseModel):
    source: str = Field(..., title='Source Text',
                        description='The text from which MCQs will be generated'
                        )
    max_questions: Optional[int] = Field(None, title='Maximum Questions',
                                         description='Maximum number of questions to generate', ge=1)
    max_distractors: Optional[int] = Field(None, title='Maximum Distractors',
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
                'max_questions': 5,
                'max_distractors': 5
            }
        }


# url = "http://localhost:5000/{}"
url = "http://mcq-generator.eastus.azurecontainer.io:8000/{}"


@app.post('/generate_mcqs', tags=['Mcqs'], response_model=List[MCQ])
async def generate_mcqs(inp: InputModel):
    try:
        get(url.format('ping'), timeout=5).json()
        res = post(url.format('generate_mcqs'), data=dumps(inp.dict())).json()
        return res
    except Exception as e:
        print(e)
        with open('./tempData.json', 'r') as f:
            res = load(f)
            return res


@app.get('/get_captions/{video_id}', tags=['Captions'], response_model=str)
async def get_captions(video_id: str = Path(..., example="MT6M_sqAuZo")):
    try:
        captions = YouTubeTranscriptApi.get_transcript(video_id)
        res: str = ' '.join(map(lambda cap: cap['text'], captions))
        res = ' '.join(res.replace('\n', ' ').split())
        return res
    except:
        return "<no captions found>"
