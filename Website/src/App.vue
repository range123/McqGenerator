<template>
  <div class="h-screen bg-gray-200">
    <app-header />
    <div class="w-full flex">
      <router-view> </router-view>
    </div>
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
