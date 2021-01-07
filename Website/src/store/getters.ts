import { State } from "@/types";

export function isMcqEmpty(state: State): boolean {
  return state.mcqs.length === 0;
}

export const getMcq = (state: State) => {
  (index: number) => {
    return state.mcqs[index];
  };
};
