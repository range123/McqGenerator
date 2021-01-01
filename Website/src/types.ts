export interface Option {
  value: string;
  isanswer: boolean;
}
export interface Mcq {
  question: string;
  options: Option[];
  id: string;
  otherOptions: string[];
}
export interface State {
  mcqs: Mcq[];
  showAnswer: boolean;
  editMode: boolean;
  text: string;
}
