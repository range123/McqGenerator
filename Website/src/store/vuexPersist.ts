import { State } from "@/types";
import VuexPersistence from "vuex-persist";

export const vuexLocal = new VuexPersistence<State>({
  storage: window.localStorage,
  reducer: (state: State) => ({
    mcqs: state.mcqs,
    text: state.text,
    showAnswer: state.showAnswer,
    editMode: state.editMode
  })
});
