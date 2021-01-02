import { Mcq, State } from "@/types";

export function setMcqs(state: State, mcqs: Mcq[]) {
  state.mcqs = mcqs;
}

export function extendMcqs(state: State, mcqs: Mcq[]) {
  state.mcqs.push(...mcqs);
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

interface SpecifyOption {
  mcqIndex: number;
  optionIndex: number;
}
export function deleteOption(
  state: State,
  { mcqIndex, optionIndex }: SpecifyOption
) {
  state.mcqs[mcqIndex].options.splice(optionIndex, 1);
}

export function toggleOptionAnswer(
  state: State,
  { mcqIndex, optionIndex }: SpecifyOption
) {
  state.mcqs[mcqIndex].options[optionIndex].isanswer = !state.mcqs[mcqIndex]
    .options[optionIndex].isanswer;
}

export function addOption(state: State, mcqIndex: number) {
  state.mcqs[mcqIndex].options.push({ value: "New Option", isanswer: false });
}
