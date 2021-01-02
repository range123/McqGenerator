<template>
  <div class="bg-gray-200 w-full">
    <div class="flex w-full flex-wrap mt-5">
      <section class="flex m-auto w-11/12 h-screen">
        <article class="w-1/2 border" @drop.prevent="readfile($event)">
          <textarea
            class="w-full h-full"
            v-model.trim="text"
            ref="textref"
          ></textarea>
        </article>
        <button
          :disabled="isdisabled"
          :class="
            isdisabled ? 'opacity-25' : 'hover:bg-black hover:text-white '
          "
          type="button"
          class="uppercase text-2xl font-bold border-solid border-black border-2 rounded-md px-4 py-2 m-2 transition duration-500 ease select-none focus:outline-none focus:shadow-outline"
          @click="generateMcqs"
          title="Generate MCQs"
        >
          G<br />e<br />n<br />e<br />r<br />a<br />t<br />e
        </button>
        <article
          class="w-1/2 bg-gray-100 border-solid border-black border-2 overflow-auto divide-y-4"
        >
          <div class="justify-around flex w-full p-4 border-black">
            <button
              :class="isMcqEmpty ? 'opacity-25' : 'hover:bg-green-600'"
              :disabled="isMcqEmpty"
              @click="toggleAnswer"
              class="border w-1/4 border-green-500 bg-green-500 text-white font-bold rounded-md px-4 py-2 m-2 transition duration-500 ease select-none  focus:outline-none focus:shadow-outline"
            >
              {{ !showAnswer ? "Show Answers" : "Hide Answers" }}
            </button>
            <button
              :class="isMcqEmpty ? 'opacity-25' : 'hover:bg-gray-800'"
              :disabled="isMcqEmpty"
              @click="toggleEdit"
              class="border w-1/4 border-gray-700 font-bold bg-gray-700 text-white rounded-md px-4 py-2 m-2 transition duration-500 ease select-none  focus:outline-none focus:shadow-outline"
            >
              {{ !editMode ? "Edit" : "Save" }}
            </button>
            <button
              :class="isMcqEmpty ? 'opacity-25' : 'hover:bg-indigo-600'"
              :disabled="isMcqEmpty"
              @click="exportmcqs"
              class="border w-1/4 border-indigo-500 bg-indigo-500 text-white font-bold rounded-md px-4 py-2 m-2 transition duration-500 ease select-none  focus:outline-none focus:shadow-outline"
            >
              Save & Print
            </button>
            <br />
          </div>
          <p class="text-center text-gray-600">
            *Long click to delete a question (Edit Mode)
          </p>
          <div id="mcqs">
            <mcq-component
              @mousedown="() => handledown(ind)"
              @mouseleave="handleup"
              @mouseup="handleup"
              v-for="(mcq, ind) in mcqs"
              :key="mcq.id"
              :qno="ind"
              class="shadow-sm"
            >
            </mcq-component>
          </div>
          <div class="w-full flex justify-around">
            <button @click="addMcq" title="Add MCQ" class="w-16 font-bold my-5">
              <img src="../assets/addmcq.png" />
            </button>
          </div>
        </article>
      </section>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { PDFDocumentProxy, getDocument } from "pdfjs-dist/webpack";
import { saveAs } from "file-saver";
import { Mcq } from "@/types";
import McqComponent from "@/components/McqComponent.vue";
// import HelloWorld from "@/components/HelloWorld.vue"; // @ is an alias to /src

export default defineComponent({
  name: "Home",
  components: {
    McqComponent
  },
  data() {
    const isdisabled = false;
    const timer = 0;
    return { isdisabled, timer };
  },
  mounted() {
    (this.$refs.textref as any).focus();
  },
  methods: {
    async generateMcqs() {
      this.isdisabled = true;
      await this.$store.dispatch("generateMcqs", this.text);
      this.isdisabled = false;
    },
    readfile(e: DragEvent) {
      const files = e.dataTransfer?.files ? e.dataTransfer.files : [];
      if (files.length != 1) {
        window.alert("Accepts only one file");
        return;
      }
      const file = files[0];
      const txtreader = new FileReader();
      txtreader.onload = f => {
        if (f.target?.result && typeof f.target.result === "string")
          this.text = f.target.result;
      };
      const getPageText = async (pdf: PDFDocumentProxy, pageNo: number) => {
        const page = await pdf.getPage(pageNo);
        const tokenizedText = await page.getTextContent();
        const pageText = tokenizedText.items.map(token => token.str).join("");
        return pageText;
      };
      const getPDFText = async (source: string | ArrayBuffer) => {
        const pdf = await getDocument(source as any).promise;
        const maxPages = pdf.numPages;
        const pageTextPromises = [];
        for (let pageNo = 1; pageNo <= maxPages; pageNo += 1) {
          pageTextPromises.push(getPageText(pdf, pageNo));
        }
        const pageTexts = await Promise.all(pageTextPromises);
        return pageTexts.join(" ");
      };
      const pdfreader = new FileReader();
      // PDFJS.disableTextLayer = true;
      pdfreader.onload = async f => {
        if (f.target?.result) {
          this.text = await getPDFText(f.target.result);
        }
      };
      if (file.type.startsWith("text/")) {
        txtreader.readAsText(file);
      } else if (file.type.startsWith("application/pdf")) {
        pdfreader.readAsArrayBuffer(file);
      } else {
        window.alert("Currently Accepts only PDF and TXT files");
      }
    },
    exportmcqs() {
      function exportmcq(qno: number, mcq: Mcq) {
        const temp = { ...mcq };
        const quest = `::Q${qno}:: ${temp.question}`;
        let ans = "{";
        for (let i = 0; i < temp.options.length; i++) {
          const ele = temp.options[i];
          if (ele.isanswer) ans += " =" + ele.value;
          else ans += " ~" + ele.value;
        }
        return quest + "\n" + ans + " }";
      }
      const temp: string[] = [];
      this.mcqs.forEach((mcq: Mcq, ind: number) => {
        temp.push(exportmcq(ind + 1, mcq));
      });
      const blob = new Blob([temp.join("\n\n")], {
        type: "text/plain;charset=utf-8"
      });
      saveAs(blob, "MCQs");
    },
    handleup() {
      if (this.editMode && this.timer) clearTimeout(this.timer);
    },
    handledown(ind: number) {
      if (this.editMode) {
        this.timer = setTimeout(() => {
          this.deleteMcq(ind);
        }, 1000);
      }
    },
    toggleEdit() {
      this.$store.commit("toggleEdit");
    },
    toggleAnswer() {
      this.$store.commit("toggleAnswer");
    },
    deleteMcq(ind: number) {
      this.$store.commit("deleteMcq", ind);
    },
    async addMcq() {
      await this.$store.dispatch("addMcq");
    }
  },
  computed: {
    mcqs() {
      return this.$store.state.mcqs;
    },
    editMode() {
      return this.$store.state.editMode;
    },
    showAnswer() {
      return this.$store.state.showAnswer;
    },
    isMcqEmpty() {
      return this.$store.getters.isMcqEmpty;
    },
    text: {
      get() {
        return this.$store.state.text;
      },
      set(text: string) {
        this.$store.commit("setText", text);
      }
    }
  }
});
</script>
