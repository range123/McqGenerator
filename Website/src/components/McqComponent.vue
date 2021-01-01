<template>
  <div class="p-4">
    <div>
      <span class="w-1/12 cursor-default">{{ qno + 1 + ". " }}</span
      ><input
        @input="
          event => {
            handleInput(0, event.target.value);
          }
        "
        :value="mcq.question"
        :readonly="!editMode"
        class="bg-gray-100 outline-none w-11/12"
        :class="!editMode ? 'cursor-default' : ''"
      />
    </div>

    <div v-for="(option, ind) in mcq.options" :key="ind" class="px-4">
      <span class="w-1/12 cursor-default">{{
        String.fromCharCode(65 + ind) + ") "
      }}</span>
      <input
        :list="mcq.id"
        @input="
          event => {
            handleInput(ind + 1, event.target.value);
          }
        "
        class="bg-gray-100 outline-none w-11/12"
        :class="getClass(option.isanswer)"
        :value="option.value"
        :readonly="!editMode"
      />
    </div>

    <datalist :id="mcq.id">
      <option :key="option" v-for="option in mcq.otherOptions">{{
        option
      }}</option>
    </datalist>
  </div>
</template>

<script lang="ts">
import { Mcq } from "@/types";
import { defineComponent } from "vue";

export default defineComponent({
  name: "Mcq",
  props: {
    qno: Number
  },
  computed: {
    editMode(): boolean {
      return this.$store.state.editMode;
    },
    showAnswer(): boolean {
      return this.$store.state.showAnswer;
    },
    mcq(): Mcq {
      return this.$store.state.mcqs[this.qno as number];
    },
    getClass() {
      return (isAnswer: boolean) => {
        let res = "";
        if (this.showAnswer && isAnswer) res += "text-green-500 font-bold ";
        if (!this.editMode) res += "cursor-default";

        return res;
      };
    }
  },
  methods: {
    handleInput(type: number, value: string) {
      const temp: Mcq = this.mcq;
      if (type === 0) temp.question = value;
      else
        temp.options[type - 1] = {
          value,
          isanswer: temp.options[type - 1].isanswer
        };
      // this.updateMcq({ index: this.qno, mcq: temp });
      this.$store.commit("updateMcq", { index: this.qno, mcq: temp });
    }
  }
});
</script>

<style scoped>
[list]::-webkit-calendar-picker-indicator {
  display: none;
}
</style>
