<template>
<div class="bg-gray-300 w-full">
        <div class="flex w-full flex-wrap mt-5">

        <section class="flex m-auto w-11/12 h-screen">
            <article class="w-1/2 border">
                <textarea class="w-full h-full" v-model.lazy="text" ref="textref"></textarea>
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
                <button :class="mcqs.length==0 ? 'opacity-25' : 'hover:bg-green-600' " :disabled="mcqs.length==0" @click="showanswer=!showanswer" class="border w-1/4 border-green-500 bg-green-500 text-white font-bold rounded-md px-4 py-2 m-2 transition duration-500 ease select-none  focus:outline-none focus:shadow-outline" >{{!showanswer ? "Show Answers" : "Hide Answers"}}</button>
                <button :class="mcqs.length==0 ? 'opacity-25' : 'hover:bg-gray-800'" :disabled="mcqs.length==0" @click="editmode=!editmode" class="border w-1/4 border-gray-700 font-bold bg-gray-700 text-white rounded-md px-4 py-2 m-2 transition duration-500 ease select-none  focus:outline-none focus:shadow-outline">{{!editmode ? "Edit" : "Save" }}</button>
                <button :class="mcqs.length==0 ? 'opacity-25' : 'hover:bg-indigo-600'" :disabled="mcqs.length==0" @click="print" class="border w-1/4 border-indigo-500 bg-indigo-500 text-white font-bold rounded-md px-4 py-2 m-2 transition duration-500 ease select-none  focus:outline-none focus:shadow-outline">Save & Print</button>
                <br>
            </div>
            <p class="text-center text-gray-600">*double click to delete a question</p>
            <div id="mcqs">
                <Mcq @dblclick="()=>(handledelete(ind))" v-for="(mcq,ind) in mcqs" :key="mcq.question" :mcq="mcq" :qno="ind" :showanswer="showanswer" :contenteditable="editmode"> </Mcq>
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
            function shuffle(array) {
                var currentIndex = array.length, temporaryValue, randomIndex;

                // While there remain elements to shuffle...
                while (0 !== currentIndex) {

                    // Pick a remaining element...
                    randomIndex = Math.floor(Math.random() * currentIndex);
                    currentIndex -= 1;

                    // And swap it with the current element.
                    temporaryValue = array[currentIndex];
                    array[currentIndex] = array[randomIndex];
                    array[randomIndex] = temporaryValue;
                }
                return array

            }
            this.isdisabled = true;
            const url = "http://localhost:8000/generate_mcqs"
            axios.post(url, {
                source : this.text.trim()
            }).then((res) => {
                // console.log(res.data)
                //Shuffle questions if necessary
                // const temp = shuffle(res.data.filter((x) => {
                //     return x.distractors.length >=3;
                // }))
                const temp = res.data.filter((x) => {
                    return x.distractors.length >= 3;
                })
                const data = []
                
                
                temp.forEach(element => {
                    const t = {
                        'question' : element.question,
                    }
                    // Shuffle the options before selecting if necessary
                    // element.distractors = shuffle(element.distractors)
                    t.options = shuffle([{'value' : element.answer, 'isanswer' : true},
                    {'value' : element.distractors[0], 'isanswer' : false},
                    {'value' : element.distractors[1], 'isanswer' : false},
                    {'value' : element.distractors[2], 'isanswer' : false}])
                    data.push(t)
                });
                this.mcqs = data
                this.isdisabled = false;
            }).catch((err) => {
                window.alert('Atleast 5 words required')
                console.log(err)
                this.isdisabled = false;
            })
        },
        print()
        {
            this.$htmlToPaper('mcqs')
        },
        handledelete(ind)
        {
            // console.log(ind)
            this.mcqs.splice(ind,1)
        }

    }

}
</script>

<style>

</style>