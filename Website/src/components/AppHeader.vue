<template>
  <nav class="flex  bg-black  flex-wrap justify-between">
    <router-link to="/" class="p-2  items-center ">
      <span class="lg:p-5 text-xl text-white font-bold uppercase tracking-wide"
        >Multi-Source MCQ Generator</span
      >
    </router-link>
    <button
      class="lg:hidden m-2 focus:outline-none hover:bg-gray-700 rounded-sm shadow-md"
      @click="() => (showBar = !showBar)"
    >
      <img src="../assets/Buttons/hamburger.png" alt="hamburger" />
    </button>
    <div
      class="top-navbar w-full lg:inline-flex lg:flex-grow lg:w-auto "
      :class="!showBar ? 'hidden' : ''"
    >
      <div
        class="lg:inline-flex lg:flex-row lg:ml-auto lg:w-auto w-full lg:items-center items-start  flex flex-col lg:h-auto"
      >
        <a
          @click="() => (showGuide = true)"
          class="lg:inline-flex lg:w-auto w-full px-3 py-2 rounded text-gray-300 items-center justify-center hover:bg-red-600 hover:text-white cursor-pointer"
        >
          <span>Guide</span>
        </a>
        <a
          v-if="deferedPrompt"
          @click="install"
          class="lg:inline-flex lg:w-auto w-full px-3 py-2 rounded text-gray-300 items-center justify-center hover:bg-red-600 hover:text-white cursor-pointer"
        >
          <span>Install</span>
        </a>
        <router-link
          to="/about"
          class="lg:inline-flex lg:w-auto w-full px-3 py-2 rounded text-gray-300 items-center justify-center hover:bg-red-600 hover:text-white"
        >
          <span>About</span>
        </router-link>
        <a
          href="https://github.com/range123/FinalYearProject"
          class="lg:inline-flex lg:w-auto w-full px-3 py-2 rounded text-gray-300 items-center justify-center hover:bg-red-600 hover:text-white"
        >
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "AppHeader",
  data() {
    return { deferedPrompt: null as Event | null, showBar: false };
  },
  created() {
    window.addEventListener("beforeinstallprompt", e => {
      e.preventDefault();
      this.deferedPrompt = e;
    });
    window.addEventListener("appinstalled", () => {
      this.deferedPrompt = null;
    });
  },
  methods: {
    install() {
      if (this.deferedPrompt) (this.deferedPrompt as any).prompt();
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
    }
  }
});
</script>

<style scoped>
img {
  width: 28px;
  height: 28px;
}
</style>
