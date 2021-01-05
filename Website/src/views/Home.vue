<template>
  <div class="bg-gray-200 w-full">
    <div class="flex w-full flex-wrap my-5">
      <transition-group name="list">
        <QAComponent
          class=" bg-gray-800 flex ml-20 transition-all ease-in"
          @answer="highlightAnswer"
          style="height:1.5rem;width:20%;"
          v-if="showQA"
          @blur="() => (showQA = !showQA)"
          :text="text"
        />
      </transition-group>

      <section class="flex m-auto w-11/12" style="height:54rem;">
        <article
          class="w-1/2 border"
          @drop.prevent="readfile($event)"
          v-page-guide.left="'You can also Drag & Drop files here!'"
        >
          <textarea
            class="w-full h-full"
            v-model.trim="text"
            ref="textref"
            v-page-guide.bottom="
              'This is where you type text for generating mcqs'
            "
            :readonly="isReading"
            :class="isReading ? 'bg-gray-300 cursor-default' : ''"
          >
          </textarea>
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
          @contextmenu.prevent="
            () => {
              showQA = !showQA;
            }
          "
        >
          G<br />e<br />n<br />e<br />r<br />a<br />t<br />e
        </button>
        <article
          class="w-1/2 bg-gray-100 border-solid border-black border-2 divide-y-4"
          @drop.prevent="loadMcqsFromFile($event)"
          @dragenter.prevent=""
          @dragover.prevent=""
          v-page-guide.bottom="
            'You can import MCQs by dropping save files (json) here! '
          "
        >
          <div class="justify-around flex w-full p-4 border-black">
            <button
              :class="isMcqEmpty ? 'opacity-25' : 'hover:bg-green-600'"
              :disabled="isMcqEmpty"
              @click="toggleAnswer"
              :title="!showAnswer ? 'Show Answers' : 'Hide Answers'"
              class="m-auto rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
              v-page-guide.bottom="'For Toggling view answer'"
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
              v-page-guide.bottom="'For Editing MCQs'"
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
              :class="isMcqEmpty ? 'opacity-25' : 'hover:bg-indigo-600'"
              :disabled="isMcqEmpty"
              @click="exportmcqs"
              title="Export as GIFT file"
              class="m-auto rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
              v-page-guide.bottom="'For Exporting MCQs'"
            >
              <!-- Export -->
              <img src="../assets/Buttons/export.png" alt="Export" />
            </button>
            <br />
          </div>
          <p
            class="text-center text-gray-600"
            :class="!editMode ? 'invisible' : ''"
          >
            *Long click to delete a question
          </p>
          <!-- <div id="mcqs"> -->
          <draggable
            v-model="mcqs"
            class="divide-gray-200 divide-y overflow-x-hidden overflow-y-auto h-2/3 "
            ghost-class="ghost"
            drag-class="drag"
            chosen-class="chosen"
            v-page-guide.bottom="
              'This is the MCQ workspace, you can rearrange MCQs using drag & drop, delete MCQs on long press'
            "
          >
            <transition-group name="list">
              <mcq-component
                @mousedown="() => handledown(ind)"
                @mouseleave="handleup"
                @mouseup="handleup"
                @drag="handleup"
                v-for="(mcq, ind) in mcqs"
                :key="mcq.id"
                :qno="ind"
                class="shadow-sm bg-gray-100"
              >
              </mcq-component>
            </transition-group>
          </draggable>
          <div class="flex justify-around p-4 sticky ">
            <button
              :disabled="isMcqEmpty"
              :class="isMcqEmpty ? 'opacity-25' : ''"
              @click="clearMcqs"
              title="Clear MCQs"
              class="my-5 rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
              v-page-guide.bottom="'Clear MCQs '"
            >
              <img src="../assets/Buttons/clear.png" />
            </button>
            <button
              @click="addMcq"
              title="Add MCQ"
              class="my-5 rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
              v-page-guide.bottom="'Add a MCQ '"
            >
              <img src="../assets/Buttons/question_add.png" />
            </button>
            <button
              :disabled="isMcqEmpty"
              :class="isMcqEmpty ? 'opacity-25' : ''"
              @click="saveMcqsToFile"
              title="Save to file"
              class="my-5 rounded-xl focus:outline-none focus:shadow-outline shadow-lg"
              v-page-guide.bottom="
                'Generate a Save file which can be imported later'
              "
            >
              <img src="../assets/Buttons/download.png" />
            </button>
          </div>
        </article>
      </section>
    </div>
    <PageGuide :value="showGuide" @input="showGuide = false" />
  </div>
</template>

<script lang="ts">
import { defineAsyncComponent, defineComponent } from "vue";
import { Mcq } from "@/types";
import McqComponent from "@/components/McqComponent.vue";
import {
  PDFDataRangeTransport,
  PDFDocumentProxy,
  PDFLoadingTask,
  PDFProgressData
} from "pdfjs-dist/webpack";
import { VueDraggableNext } from "vue-draggable-next";
import { useToast } from "vue-toastification";
import { Worker } from "tesseract.js";

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
let ocrWorker: Worker;
const main = async () => {
  getDocument = (
    await import(
      /* webpackPrefetch: true */
      /* webpackPreload: true */
      /* webpackChunkName: "PDFjs" */
      "pdfjs-dist/webpack"
    )
  ).getDocument;
  hash = (
    await import(
      /* webpackPrefetch: true */
      /* webpackChunkName: "Hash" */
      "object-hash"
    )
  ).default;
  saveAs = (
    await import(
      /* webpackPrefetch: true */
      /* webpackChunkName: "file-saver" */
      "file-saver"
    )
  ).saveAs;
  const createWorker = (
    await import(
      /* webpackPrefetch: true */
      /* webpackChunkName: "OCR" */
      "tesseract.js"
    )
  ).createWorker;
  ocrWorker = createWorker({
    workerPath: "/js/worker.min.js",
    corePath: "/js/tesseract-core.wasm.js"
  });
  await ocrWorker.load();
  await ocrWorker.loadLanguage("eng");
  await ocrWorker.initialize("eng");
};
main();
export default defineComponent({
  name: "Home",
  components: {
    McqComponent,
    draggable: VueDraggableNext,
    PageGuide: defineAsyncComponent(() =>
      import("../plugins/Tour/VPageGuide.vue")
    ),
    QAComponent: defineAsyncComponent(() =>
      import("../components/QAComponent.vue")
    )
  },
  data() {
    const isdisabled = false;
    const timer = 0;
    return {
      isdisabled,
      timer,
      Toast: useToast(),
      isReading: false,
      showQA: false
    };
  },
  mounted() {
    const textarea = this.$refs.textref as any;
    textarea.focus();
  },
  methods: {
    highlightAnswer(data: { start: number; end: number }) {
      const textarea = this.$refs.textref as any;
      textarea.focus();
      textarea.setSelectionRange(data.start, data.end);
    },
    async doOcr(file: File) {
      this.text = (await ocrWorker.recognize(file)).data.text;
      this.isReading = false;
    },
    async generateMcqs() {
      this.isdisabled = true;
      await this.$store.dispatch("generateMcqs", this.text);
      this.isdisabled = false;
    },
    async readfile(e: DragEvent) {
      this.isReading = true;
      const files = e.dataTransfer?.files ? e.dataTransfer.files : [];
      if (files.length != 1) {
        this.Toast.error("Accepts only one file");
        return;
      }
      const file = files[0];
      const txtreader = new FileReader();
      txtreader.onload = f => {
        if (f.target?.result && typeof f.target.result === "string") {
          this.text = f.target.result;
          this.isReading = false;
        }
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
          this.isReading = false;
        }
      };
      if (file.type.startsWith("text/")) {
        txtreader.readAsText(file);
      } else if (file.type.startsWith("application/pdf")) {
        pdfreader.readAsArrayBuffer(file);
      } else if (file.type.startsWith("image/")) {
        await this.doOcr(file);
      } else {
        this.Toast.warning("Currently Accepts only PDF, Image and TXT files");
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
            else this.Toast.error("Integrity Check Failed");
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
    showGuide: {
      get() {
        return this.$store.state.showGuide;
      },
      set(g: boolean) {
        this.$store.commit("setGuide", g);
      }
    },
    mcqs: {
      get() {
        return this.$store.state.mcqs;
      },
      set(mcqs: Mcq[]) {
        this.$store.commit("setMcqs", mcqs);
      }
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
.list-enter-active {
  transition: all 1s ease;
}
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
.ghost {
  opacity: 25%;
}
/* .chosen{
  border: 3px solid green;
} */
.drag {
  background-color: #e0e0e0;
}

textarea::selection {
  color: #388e3c;
  font-weight: bold;
}
</style>
