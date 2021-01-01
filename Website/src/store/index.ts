import { createStore } from "vuex";
import { State } from "../types";
import * as Mutations from "./mutations";
import * as Actions from "./actions";
import * as Getters from "./getters";
import { vuexLocal } from "./vuexPersist";

const initState: State = {
  mcqs: [],
  showAnswer: false,
  editMode: false,
  text: ""
};
export default createStore({
  state: initState,
  mutations: Mutations,
  actions: Actions,
  getters: Getters,
  modules: {},
  plugins: [vuexLocal.plugin]
});
