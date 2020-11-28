from question_generators import T5QuestionAnswerGenerator
from distractor_generators import Sense2VecDistractorGenerator

if __name__ == "__main__":
    qmodel = T5QuestionAnswerGenerator('../../saved_models/t5-base-qa-qg-hl')
    dmodel = Sense2VecDistractorGenerator()
    text = None
    with open('test.txt','r') as f:
        text = f.read()
    res = qmodel.generate_question_answer(text)
    # questions, answers = res['question']
    d = []
    for i,qa in enumerate(res):
        print(f"{i+1}){qa['question']}")
        print(f' A) {qa["answer"]}')
        distractors, ans_proc = dmodel.generate_distractors(qa['question'],qa["answer"], limit = 4)
        distractors.append(ans_proc)
        for i,x in enumerate(distractors):
            print(f' {chr(66 + i)}) {x}')
        print()
    