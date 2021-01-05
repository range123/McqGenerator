<template>
  <div class="justify-around w-full h-full">
    <input
      type="text"
      @keyup="getYoutube"
      v-model="link"
      class="w-full h-full focus:bg-green-100"
      placeholder="Youtube Link"
      @blur="$emit('blur')"
      ref="ytref"
    />
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent } from "vue";
import { useToast } from "vue-toastification";

export default defineComponent({
  emits: ["yttext", "blur"],
  name: "YTComponent",
  data() {
    return { link: "", toast: useToast() };
  },
  mounted() {
    (this.$refs.ytref as any).focus();
  },
  methods: {
    async getYoutube(e: KeyboardEvent) {
      if (e.key === "Enter") {
        let temp = this.link.split("v=")[1];
        const ampersandPosition = temp.indexOf("&");
        if (ampersandPosition != -1) {
          temp = temp.substring(0, ampersandPosition);
        }
        const url = "https://5evt4e.deta.dev/get_captions/";
        try {
          const text = await axios.get(url + temp);
          if (text.data === "<no captions found>") {
            this.toast.error("Captions Not Found!");
            this.$emit("yttext", null);
            return;
          }

          this.$emit("yttext", text.data);
        } catch (error) {
          this.toast.error("Unexpected Error!");
        }
      }
    }
  }
});
</script>

<style></style>
