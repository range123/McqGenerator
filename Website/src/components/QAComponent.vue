<template>
  <div class="justify-around w-full h-full">
    <input
      type="text"
      @keyup="doAnswering"
      v-model="question"
      class="w-full h-full focus:bg-green-100"
      placeholder="Ask Question"
      @blur="$emit('blur')"
      ref="qaref"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { load } from "@tensorflow-models/qna";
import { useToast } from "vue-toastification";
let model: any | null = null;
const main = async () => {
  model = await load({
    modelUrl: "/assets/mobilebert/model.json"
  });
};
main();

export default defineComponent({
  props: {
    text: String
  },
  emits: ["answer", "blur"],
  name: "QAComponent",
  data() {
    return { question: "", toast: useToast() };
  },
  mounted() {
    (this.$refs.qaref as any).focus();
  },
  methods: {
    async doAnswering(e: KeyboardEvent) {
      if (e.key === "Enter") {
        if (!model) {
          this.toast.warning("Model is loading Please wait!");
          return;
        }
        const result = await model?.findAnswers(
          this.question,
          this.text as string
        );
        if (result && result[0]) {
          // this.$emit("answer", { start: result[0].startIndex, end: result[0].endIndex });
          this.$emit("answer", {
            start: result[0].startIndex,
            end: result[0].startIndex + result[0].text.length
          });
        } else {
          this.$emit("answer", { start: 0, end: 0 });
        }
      }
    }
  }
});
</script>

<style></style>
