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
        class="bg-gray-100 outline-none w-9/12 "
        :class="!editMode ? 'cursor-default' : ''"
      />
      <span class="inline-flex" :class="!editMode ? 'invisible' : ''">
        <button
          class="mt-3 focus:outline-none focus:shadow-outline rounded-full shadow ml-2"
          title="Shuffle Options"
          @click="shuffleOptions"
        >
          <img src="../assets/Buttons/ans/shuffle.png" />
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
      <span class="inline-flex" :class="!editMode ? 'invisible' : ''">
        <button
          @click="() => makeAnswer(ind)"
          class="focus:outline-none focus:shadow-outline rounded-full shadow"
          id="temp"
          :title="option.isanswer ? 'UnMark Answer' : 'Mark Answer'"
        >
          <img
            v-if="option.isanswer"
            src="../assets/Buttons/ans/ans_unmark.png"
            alt="UnMark Answer"
          />
          <img
            v-else
            src="../assets/Buttons/ans/ans_mark.png"
            alt="Mark Answer"
          />
        </button>
        <button
          @click="() => deleteOption(ind)"
          class="focus:outline-none focus:shadow-outline rounded-full shadow ml-1"
          title="Remove Option"
        >
          <img src="../assets/Buttons/ans/dis_delete.png" />
        </button>
      </span>
    </div>

    <datalist :id="mcq.id">
      <option :key="option" v-for="option in mcq.otherOptions">{{
        option
      }}</option>
    </datalist>
    <div :class="!editMode ? 'invisible' : ''" class="w-full flex ">
      <button
        @click="addOption"
        class="mt-3 mb-2 ml-4 focus:outline-none focus:shadow-outline rounded-full shadow"
        title="Add Option"
      >
        <img src="../assets/Buttons/ans/dis_add.png" />
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
/* img {
  width: 28px;
  height: 28px;
} */
</style>
