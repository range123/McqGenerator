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
          @drop.prevent="loadMcqsFromFile($event)"
          @dragenter.prevent=""
          @dragover.prevent=""
        >
          <div class="justify-around flex w-full p-4 border-black">
            <button
              :class="isMcqEmpty ? 'opacity-25' : 'hover:bg-green-600'"
              :disabled="isMcqEmpty"
              @click="toggleAnswer"
              :title="!showAnswer ? 'Show Answers' : 'Hide Answers'"
              class="m-auto rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
            >
              <!-- {{ !showAnswer ? "Show Answers" : "Hide Answers" }} -->
              <img
                v-if="!showAnswer"
                src="../assets/Buttons/ans_show.png"
                alt="Show Answers"
              />
              <img
                v-else
                src="../assets/Buttons/ans_hide.png"
                alt="Hide Answers"
              />
            </button>
            <button
              :class="isMcqEmpty ? 'opacity-25' : 'hover:bg-gray-800'"
              :disabled="isMcqEmpty"
              @click="toggleEdit"
              :title="!editMode ? 'Edit' : 'Save'"
              class="m-auto rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
            >
              <!-- {{ !editMode ? "Edit" : "Save" }} -->
              <img
                v-if="!editMode"
                src="../assets/Buttons/edit.png"
                alt="Edit"
              />
              <img v-else src="../assets/Buttons/save.png" alt="Save" />
            </button>
            <button
              :class="isMcqEmpty ? 'opacity-25' : 'hover:gra'"
              :disabled="isMcqEmpty"
              @click="exportmcqs"
              title="Export as GIFT file"
              class="m-auto rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
            >
              <!-- Export -->
              <img src="../assets/Buttons/export.png" alt="Export" />
            </button>
            <br />
          </div>
          <p class="text-center text-gray-600" v-show="editMode">
            *Long click to delete a question
          </p>
          <!-- <div id="mcqs"> -->
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
          <!-- </div> -->
          <div class="w-full flex justify-around p-4">
            <button
              :disabled="isMcqEmpty"
              :class="isMcqEmpty ? 'opacity-25' : ''"
              @click="clearMcqs"
              title="Clear MCQs"
              class="my-5 rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
            >
              <img src="../assets/Buttons/clear.png" />
            </button>
            <button
              @click="addMcq"
              title="Add MCQ"
              class="my-5 rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
            >
              <img src="../assets/Buttons/question_add.png" />
            </button>
            <button
              :disabled="isMcqEmpty"
              :class="isMcqEmpty ? 'opacity-25' : ''"
              @click="saveMcqsToFile"
              title="Save to file"
              class="my-5 rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
            >
              <img src="../assets/Buttons/download.png" />
            </button>
          </div>
        </article>
      </section>
    </div>
  </div>
</template>

<script lang="ts">
import { defineAsyncComponent, defineComponent } from "vue";
import { Mcq } from "@/types";
// import McqComponent from "@/components/McqComponent.vue";
import {
  PDFDataRangeTransport,
  PDFDocumentProxy,
  PDFLoadingTask,
  PDFProgressData
} from "pdfjs-dist/webpack";
// import HelloWorld from "@/components/HelloWorld.vue"; // @ is an alias to /src
let getDocument: (
  data: Uint8Array | BufferSource,
  pdfDataRangeTransport?: PDFDataRangeTransport,
  passwordCallback?: (fn: (password: string) => void, reason: string) => string,
  progressCallback?: (progressData: PDFProgressData) => void
) => PDFLoadingTask<PDFDocumentProxy>;
let hash: (obj: any, options?: any) => string;
let saveAs: (
  data: Blob | string,
  filename?: string,
  disableAutoBOM?: boolean
) => void;

const main = async () => {
  getDocument = (await import("pdfjs-dist/webpack")).getDocument;
  hash = (await import("object-hash")).default;
  saveAs = (await import("file-saver")).saveAs;
};
main();

export default defineComponent({
  name: "Home",
  components: {
    McqComponent: defineAsyncComponent(() =>
      import("@/components/McqComponent.vue")
    )
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
    async readfile(e: DragEvent) {
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
    },
    clearMcqs() {
      this.$store.commit("setMcqs", []);
    },
    async saveMcqsToFile() {
      const mcqHash = await this.getHash(this.mcqs);
      const temp = JSON.stringify({ mcqs: this.mcqs, mcqHash });
      const blob = new Blob([temp], {
        type: "application/json;charset=utf-8"
      });
      saveAs(blob, "saveFile.json");
    },
    async loadMcqsFromFile(e: DragEvent) {
      const files = e.dataTransfer?.files ? e.dataTransfer.files : [];
      // if (files.length != 1) {
      //   window.alert("Accepts only one file");
      //   return;
      // }
      // const file = files[0];

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const txtreader = new FileReader();
        txtreader.onload = async f => {
          if (f.target?.result && typeof f.target.result === "string") {
            const res = JSON.parse(f.target.result);
            const mcqs: Mcq[] = res.mcqs;
            const GTHash: string = res.mcqHash;
            if (await this.verifyHash(mcqs, GTHash))
              this.$store.commit("extendMcqs", mcqs);
            else window.alert("Integrity Check Failed");
          }
        };
        if (!file.type.startsWith("application/json")) return;
        txtreader.readAsText(file);
      }
    },
    async getHash(mcqs: Mcq[]): Promise<string> {
      const options = {
        // excludeValues: true,
        unorderedArrays: true,
        encoding: "base64"
      };

      return hash(mcqs, options);
    },
    async verifyHash(mcqs: Mcq[], GTHash: string): Promise<boolean> {
      return (await this.getHash(mcqs)) === GTHash;
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

<style scoped>
/* img {
  width: 64px;
  height: 64px;
} */
</style>
