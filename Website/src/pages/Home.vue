<template>
<div class="bg-gray-300 w-full">
        <div class="flex w-full flex-wrap mt-5">

        <section class="flex m-auto w-11/12 h-screen">
            <article class="w-1/2 border">
                <textarea class="w-full h-full" v-model="text" ref="textref"></textarea>
            </article>
                    <button
        :disabled="isdisabled"
        :class="isdisabled ? 'opacity-25':'hover:bg-black hover:text-white '" 
        
        type="button"
        class="uppercase text-2xl font-bold border-solid border-black border-2 rounded-md px-4 py-2 m-2 transition duration-500 ease select-none focus:outline-none focus:shadow-outline"
       @click="generate">
        G<br>e<br>n<br>e<br>r<br>a<br>t<br>e
      </button>
        <article class="w-1/2 bg-gray-100 border-solid border-black border-2 overflow-auto divide-y-4">
            <div class="justify-around flex w-full p-4 border-black">
                <button class="border w-1/4 border-green-500 bg-green-500 text-white font-bold rounded-md px-4 py-2 m-2 transition duration-500 ease select-none hover:bg-green-600 focus:outline-none focus:shadow-outline" @click="showanswer=!showanswer">{{!showanswer ? "Show Answers" : "Hide Answers"}}</button>
                <button @click="editmode=!editmode" class="border w-1/4 border-gray-700 font-bold bg-gray-700 text-white rounded-md px-4 py-2 m-2 transition duration-500 ease select-none hover:bg-gray-800 focus:outline-none focus:shadow-outline">{{!editmode ? "Edit" : "Save" }}</button>
                <button @click="print" class="border w-1/4 border-indigo-500 bg-indigo-500 text-white font-bold rounded-md px-4 py-2 m-2 transition duration-500 ease select-none hover:bg-indigo-600 focus:outline-none focus:shadow-outline">Save & Print</button>
            </div>
        
            <div id="mcqs">
                <Mcq v-for="(mcq,ind) in mcqs" :key="mcq.question" :mcq="mcq" :qno="ind" :showanswer="showanswer" :contenteditable="editmode"> </Mcq>
            </div>
                
            </article>
        </section>
  </div>
</div>

</template>

<script>
import axios from 'axios'
import Mcq from '../components/Mcq'
export default {
     
    components : {Mcq},
    directives : { print }
    ,
    data()
    {
        const text = ''
        const mcqs = []
        const isdisabled= false
        const showanswer = false
        const editmode = false
        return {text, isdisabled, mcqs, showanswer, editmode}
    },
    mounted(){
        this.$refs.textref.focus()
    },
    methods : {
        generate()
        {
            this.isdisabled = true;
            const url = "https://wise-chicken-49.loca.lt/generate_mcqs"
            axios.post(url, {
                source : this.text
            }).then((res) => {
                console.log(res.data)
                const temp = res.data.filter((x) => {
                    return x.distractors.length >=3;
                })
                this.mcqs = temp
                this.isdisabled = false;
            })
        },
        print()
        {
            this.$htmlToPaper('mcqs')
        }

    }

}
</script>

<style>

</style>