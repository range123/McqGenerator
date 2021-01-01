import { Mcq, State } from "@/types";

export function setMcqs(state: State, mcqs: Mcq[]) {
  state.mcqs = mcqs;
}

export function toggleAnswer(state: State) {
  state.showAnswer = !state.showAnswer;
}

export function toggleEdit(state: State) {
  state.editMode = !state.editMode;
}

export function addMcq(state: State, mcq: Mcq) {
  state.mcqs.push(mcq);
}

export function deleteMcq(state: State, index: number) {
  state.mcqs.splice(index, 1);
}

interface Update {
  index: number;
  mcq: Mcq;
}
export function updateMcq(state: State, { index, mcq }: Update) {
  state.mcqs[index] = mcq;
}

export function setText(state: State, text: string) {
  state.text = text;
}
