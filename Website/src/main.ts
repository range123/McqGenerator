import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import "./assets/Styles/index.css";
import Toast, { PluginOptions, POSITION } from "vue-toastification";
// Import the CSS or use your own!
import "vue-toastification/dist/index.css";

const options: PluginOptions = {
  // You can set your default options here
  position: POSITION.TOP_CENTER
};
const app = createApp(App);
app.use(store);
app.use(router);

app.use(Toast, options);
app.directive("click-outside", {
  beforeMount(el, binding, vnode) {
    el.clickOutsideEvent = function(event: MouseEvent) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event, el);
      }
    };
    document.body.addEventListener("click", el.clickOutsideEvent);
  },
  unmounted(el) {
    document.body.removeEventListener("click", el.clickOutsideEvent);
  }
});
app.mount("#app");
