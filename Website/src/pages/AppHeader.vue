<template>
  
  <nav class="flex  bg-black  flex-wrap ">
      <router-link to="/" class="p-2  items-center ">
        <span class="p-5 text-xl text-white font-bold uppercase tracking-wide"
          >Multi-Source MCQ Generator</span
        >
      </router-link>
      
      <div
        class="hidden top-navbar w-full lg:inline-flex lg:flex-grow lg:w-auto "
        id="navigation"
      >
        <div
          class="lg:inline-flex lg:flex-row lg:ml-auto lg:w-auto w-full lg:items-center items-start  flex flex-col lg:h-auto"
        >
          <router-link
            to="/about"
            class="lg:inline-flex lg:w-auto w-full px-3 py-2 rounded text-gray-400 items-center justify-center hover:bg-red-600 hover:text-white"
          >
            <span>About</span>
          </router-link>
          <a
            href="https://github.com/range123/FinalYearProject"
            class="lg:inline-flex lg:w-auto w-full px-3 py-2 rounded text-gray-400 items-center justify-center hover:bg-red-600 hover:text-white"
          >
            <span>GitHub</span>
          </a>                
        </div>
      </div>
    </nav>
</template>

<script>
export default {
    data()
    {
        return {
            routes : [
                { name : 'Home', to : '/'}
            ]
        }
    },

}
</script>

<style>

</style>