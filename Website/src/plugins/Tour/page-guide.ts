import VPageGuide from "./VPageGuide.vue";
import { App } from "vue";

const PageGuide = {
  install(app: App) {
    app.directive("page-guide", {
      beforeMount(el, binding) {
        el.setAttribute("v-page-guide", binding.value);

        const modifiers = Object.getOwnPropertyNames(binding.modifiers);
        if (modifiers.length > 0) {
          el.setAttribute("v-page-guide-placement", modifiers[0]);
        }
      }
    });

    // app.component("v-page-guide", VPageGuide);
    // app.component(VPageGuide)
  }
};

export default PageGuide;
