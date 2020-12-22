<template>
<div class="bg-gray-300 w-full">
        <div class="flex w-full flex-wrap mt-5">

        <section class="flex m-auto w-11/12 h-screen">
            <article class="w-1/2 border" @drop.prevent="readfile($event)">
                <textarea class="w-full h-full" v-model.lazy="text" ref="textref"></textarea>
            </article>
                    <button
        :disabled="isdisabled"
        :class="isdisabled ? 'opacity-25':'hover:bg-black hover:text-white '" 
        
        type="button"
        class="uppercase text-2xl font-bold border-solid border-black border-2 rounded-md px-4 py-2 m-2 transition duration-500 ease select-none focus:outline-none focus:shadow-outline"
       @click="generate"
       title="Generate MCQs">
        G<br>e<br>n<br>e<br>r<br>a<br>t<br>e
      </button>
        <article class="w-1/2 bg-gray-100 border-solid border-black border-2 overflow-auto divide-y-4">
            <div class="justify-around flex w-full p-4 border-black">
                <button :class="mcqs.length==0 ? 'opacity-25' : 'hover:bg-green-600' " :disabled="mcqs.length==0" @click="showanswer=!showanswer" class="border w-1/4 border-green-500 bg-green-500 text-white font-bold rounded-md px-4 py-2 m-2 transition duration-500 ease select-none  focus:outline-none focus:shadow-outline" >{{!showanswer ? "Show Answers" : "Hide Answers"}}</button>
                <button :class="mcqs.length==0 ? 'opacity-25' : 'hover:bg-gray-800'" :disabled="mcqs.length==0" @click="editmode=!editmode" class="border w-1/4 border-gray-700 font-bold bg-gray-700 text-white rounded-md px-4 py-2 m-2 transition duration-500 ease select-none  focus:outline-none focus:shadow-outline">{{!editmode ? "Edit" : "Save" }}</button>
                <button :class="mcqs.length==0 ? 'opacity-25' : 'hover:bg-indigo-600'" :disabled="mcqs.length==0" @click="exportmcqs" class="border w-1/4 border-indigo-500 bg-indigo-500 text-white font-bold rounded-md px-4 py-2 m-2 transition duration-500 ease select-none  focus:outline-none focus:shadow-outline">Save & Print</button>
                <br>
            </div>
            <p class="text-center text-gray-600">*Long click to delete a question</p>
            <div id="mcqs">
                <Mcq  @onmcqchange="handlechange(ind,$event)" @mousedown="()=>(handledown(ind))" @mouseup="handleup" v-for="(mcq,ind) in mcqs" :key="mcq.id" :mcq="mcq" :qno="ind" :showanswer="showanswer" class="shadow-sm" :editable="editmode"> </Mcq>
            </div>
            <div class="w-full flex justify-around">
                <button @click="addmcq" :class="editmode ? 'hover:bg-blue-300' :''" :disabled="!editmode" title="Add MCQ" class="border bg-gray-400 text-white text-4xl w-16 font-bold h-16 shadow my-5">
                    +</button>
            </div>
                
            </article>
        </section>
  </div>
</div>

</template>

<script>
import axios from 'axios'
import Mcq from '../components/Mcq'
import { saveAs } from 'file-saver'
import { v4 as uuidv4 } from 'uuid';
var PDFJS;
import('pdfjs-dist/webpack').then(pdfjs => {
  PDFJS = pdfjs})
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
        const timer = ''
        const editmode = false
        return {text, isdisabled, mcqs, showanswer, timer, editmode}
    },
    mounted(){
        this.$refs.textref.focus()
    },
    methods : {
        generate()
        {
            
            this.isdisabled = true;
            // const url = "http://localhost:8000/generate_mcqs"
            // const url = "https://mcq-generator.loca.lt/generate_mcqs"
            const url = "http://mcq-generator.eastus.azurecontainer.io:8000/generate_mcqs"
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
                        id : uuidv4()
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
                if (err.response){
                    if (err.response.status == '422'){
                        window.alert('Atleast 5 words required')
                    }
                    else{
                        console.log(err)
                    }
                }
                this.isdisabled = false;
            })
        },
        print()
        {
            this.$htmlToPaper('mcqs')
        },
        exportmcqs()
        {

            function exportmcq(qno, mcq)
            {
                const temp = {...mcq}
                const quest = `::Q${qno}:: ${mcq.question}`
                let ans = '{'
                for (let i = 0; i< temp.options.length; i++) {
                  const ele = temp.options[i]; 
                    if (ele.isanswer)
                        ans += ' ='+ele.value
                    else
                        ans += ' ~'+ele.value
                
                }
                return quest + '\n' + ans + ' }'

            }
            const temp = []
            this.mcqs.forEach((mcq, ind) => {
                temp.push(exportmcq(ind+1,mcq))
            })
            var blob = new Blob([temp.join('\n\n')], {type: "text/plain;charset=utf-8"});
            saveAs(blob, "MCQs")
            

        }
        ,
        handledown(ind)
        {
            // console.log(ind)
            this.timer = setTimeout( () => {
                this.mcqs.splice(ind,1)
            },1000)
            
        },
        handleup()
        {
            if (this.timer)
                clearInterval(this.timer);
        },
        readfile(e)
        {
            const files = e.dataTransfer.files
            if (files.length != 1) {
                window.alert('Accepts only one file')
                return
            }
            const file = files[0]
            var txtreader = new FileReader()
            txtreader.onload = f => {
                this.text = f.target.result
            }


            const getPageText = async (pdf, pageNo) => {
                const page = await pdf.getPage(pageNo);
                const tokenizedText = await page.getTextContent();
                const pageText = tokenizedText.items.map(token => token.str).join("");
                return pageText;
            };

            const getPDFText = async (source) => {
                const pdf = await PDFJS.getDocument(source).promise;
                const maxPages = pdf.numPages;
                const pageTextPromises = [];
                for (let pageNo = 1; pageNo <= maxPages; pageNo += 1) {
                    pageTextPromises.push(getPageText(pdf, pageNo));
                }
                const pageTexts = await Promise.all(pageTextPromises);
                return pageTexts.join(" ");
            };

            var pdfreader = new FileReader()
            PDFJS.disableTextLayer = true;
            pdfreader.onload = async f => {
                this.text = await getPDFText(f.target.result)
            }

            if (file.type.startsWith('text/'))
            {
                txtreader.readAsText(file)
            }
            else if (file.type.startsWith('application/pdf'))
            {
                pdfreader.readAsArrayBuffer(file)
            }
            else{
                window.alert('Currently Accepts only PDF and TXT files')
            }

        },
        handlechange(ind,value)
        {
            this.mcqs[ind] = value
        },
        addmcq()
        {
            const temp = {
                question : "question",
                id : uuidv4(),
                options : shuffle([
                    {value : "answer", isanswer : true},
                    {value : "option1", isanswer : false},
                    {value : "option2", isanswer : false},
                    {value : "option3", isanswer : false}
                ])
            }
            this.mcqs.push(temp)
        }

    }

}
</script>

<style>

</style>