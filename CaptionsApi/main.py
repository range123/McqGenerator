
from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi

tags_metadata = [
    {
        "name": "mcqs",
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
# TODO Add known origins later and pass to allow_origins instead of *
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


res = [
    {
        'question': 'Is the backend not deployed?',
        'answer': 'Yes',
        'distractors': [
            "No",
            "Definitely Not",
            "Obviously"
        ]
    },
    {
        'question': 'Is the backend being tested?',
        'answer': 'sure',
        'distractors': [

        ]
    },
    {
        'question': 'Is this a dummy backend?',
        'answer': 'Obviously',
        'distractors': [
            "No",
            "Nah",
            "Bruh",
            "Yes"
        ]
    },
    {
        'question': 'Is this a PWA',
        'answer': 'Ofcourse',
        'distractors': [
            "No"
        ]
    }
]


@app.post('/generate_mcqs', tags=['mcqs'], response_model=List[MCQ])
async def generate_mcqs(inp: InputModel):

    return res

@app.get('/get_captions/{video_id}', tags=['Captions'])
async def get_captions(video_id : str):
    try:
        captions = YouTubeTranscriptApi.get_transcript(video_id)
        res : str =' '.join(map(lambda cap : cap['text'],captions))
        res = ' '.join(res.replace('\n',' ').split())
        print(res)
        return res
    except:
        return "<no captions found>"
    
