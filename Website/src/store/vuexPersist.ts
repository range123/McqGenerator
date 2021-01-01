import { State } from "@/types";
import VuexPersistence from "vuex-persist";

export const vuexLocal = new VuexPersistence<State>({
  storage: window.localStorage
});
