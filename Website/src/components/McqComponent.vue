<template>
  <div class="px-4 justify-start text-lg">
    <div>
      <span class="w-1/12 cursor-default font-mono">{{ qno + 1 + ". " }}</span
      ><input
        @input="
          event => {
            handleInput(0, event.target.value);
          }
        "
        :value="mcq.question"
        :readonly="!editMode"
        class="bg-gray-100 outline-none w-9/12"
        :class="!editMode ? 'cursor-default' : ''"
      />
      <span class="inline-flex mx-auto" :class="!editMode ? 'invisible' : ''">
        <button
          class="w-6 mt-3"
          title="Shuffle Options"
          @click="shuffleOptions"
        >
          <img src="../assets/shuffle.png" />
        </button>
      </span>
    </div>

    <div v-for="(option, ind) in mcq.options" :key="ind" class="px-4">
      <span class="w-1/12 cursor-default font-mono">{{
        String.fromCharCode(65 + ind) + ") "
      }}</span>
      <input
        :list="mcq.id"
        @input="
          event => {
            handleInput(ind + 1, event.target.value);
          }
        "
        class="bg-gray-100 outline-none w-9/12 inline-flex justify-start"
        :class="getClass(option.isanswer)"
        :value="option.value"
        :readonly="!editMode"
      />
      <span class="inline-flex mx-auto" :class="!editMode ? 'invisible' : ''">
        <button
          @click="() => makeAnswer(ind)"
          class="w-6"
          :title="option.isanswer ? 'UnMark Answer' : 'Mark Answer'"
        >
          <img src="../assets/correct.png" />
        </button>
        <button
          @click="() => deleteOption(ind)"
          class="w-6"
          title="Remove Option"
        >
          <img src="../assets/delete.png" />
        </button>
      </span>
    </div>

    <datalist :id="mcq.id">
      <option :key="option" v-for="option in mcq.otherOptions">{{
        option
      }}</option>
    </datalist>
    <div :class="!editMode ? 'invisible' : ''" class="w-full flex ">
      <button @click="addOption" class="w-8 mt-5 ml-4" title="Add Option">
        <img src="../assets/addoption.png" />
      </button>
    </div>
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
    },
    answerCount(): number {
      let count = 0;
      this.mcq.options.forEach(option => {
        if (option.isanswer) count++;
      });
      return count;
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
      this.$store.commit("updateMcq", { index: this.qno, mcq: temp });
    },
    addOption() {
      if (this.mcq.options.length < 26)
        this.$store.commit("addOption", this.qno);
    },
    deleteOption(curOption: number) {
      if (!this.mcq.options[curOption].isanswer || this.answerCount > 1) {
        this.$store.commit("deleteOption", {
          mcqIndex: this.qno,
          optionIndex: curOption
        });
      }
    },
    makeAnswer(curOption: number) {
      if (!this.mcq.options[curOption].isanswer || this.answerCount > 1) {
        this.$store.commit("toggleOptionAnswer", {
          mcqIndex: this.qno,
          optionIndex: curOption
        });
      }
    },
    shuffleOptions() {
      this.$store.dispatch("shuffleOptions", this.qno);
    }
  }
});
</script>

<style scoped>
[list]::-webkit-calendar-picker-indicator {
  display: none;
}
</style>
