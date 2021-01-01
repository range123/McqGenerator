<template>
  <app-header />
  <div class="w-full flex">
    <router-view> </router-view>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AppHeader from "./components/AppHeader.vue";
export default defineComponent({
  name: "App",
  components: { AppHeader }
});
</script>
