import { Mcq, Option, State } from "@/types";
import axios, { AxiosResponse } from "axios";
import { v4 as uuidv4 } from "uuid";
import { ActionContext } from "vuex";

function shuffle(array: Option[]): Option[] {
  let currentIndex: number = array.length;
  let temporaryValue;
  let randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }
  return array;
}

interface McqModel {
  question: string;
  answer: string;
  distractors: string[];
}
export async function generateMcqs(
  { commit }: ActionContext<State, State>,
  text: string
) {
  // const url = "http://localhost:8000/generate_mcqs";
  const url = "https://5evt4e.deta.dev/generate_mcqs"
  let res: AxiosResponse<any>;
  try {
    res = await axios.post(url, {
      source: text.trim()
    });
  } catch (error) {
    if (error.response && error.response.status === 422) {
      window.alert("Atleast 5 words required");
    } else {
      window.alert("Unexpected Error!");
      console.log(error);
    }
    return;
  }

  // let temp: McqModel[] = res.data;
  const temp: McqModel[] = res.data;

  // Uncomment to allow only questions with >=3 distractors

  // temp = temp.filter(x => {
  //   return x.distractors.length >= 3;
  // });

  const mcqs: Mcq[] = [];
  temp.forEach(element => {
    const t: Mcq = {
      question: element.question,
      id: uuidv4(),
      options: [],
      otherOptions: element.distractors
    };
    const options = [{ value: element.answer, isanswer: true }];
    element.distractors.forEach((distractor, ind) => {
      if (ind > 2) return;
      options.push({ value: distractor, isanswer: false });
    });
    t.options = shuffle(options);

    mcqs.push(t);
  });
  commit("setMcqs", mcqs);
}

export async function addMcq({ commit }: ActionContext<State, State>) {
  const mcq: Mcq = {
    question: "question",
    id: uuidv4(),
    otherOptions: [],
    options: shuffle([
      { value: "answer", isanswer: true },
      { value: "option1", isanswer: false },
      { value: "option2", isanswer: false },
      { value: "option3", isanswer: false }
    ])
  };
  commit("addMcq", mcq);
}

export async function shuffleOptions(
  { commit, state }: ActionContext<State, State>,
  mcqIndex: number
) {
  const mcq: Mcq = JSON.parse(JSON.stringify(state.mcqs[mcqIndex]));
  mcq.options = shuffle(mcq.options);
  commit("updateMcq", { index: mcqIndex, mcq });
}
