<template>
<div class="p-4">
    <div>
        <span>{{(qno +1) + '. '}}</span><span>{{state.question}}</span>
    </div>
    
    <div v-for="(option, ind) in state.options" :key="ind" class="px-4">
        <span>{{String.fromCharCode(65 + ind) + ') '}}</span>
        <span :class="showanswer && option.isanswer ? 'text-green-500 font-bold' : ''" > {{option.value}}</span>
    </div>


</div>
  
</template>

<script>
import {reactive} from 'vue'
export default {
    props : {
        'mcq' : {
            'question' : String,
            'answer' : String,
            'distractors' : Array
        },
        'qno' : Number,
        'showanswer' : Boolean
    },
    setup(props)
    {
        const state = reactive({...props.mcq})
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
        // state.distractors = shuffle(state.distractors)
        state.options = shuffle([{'value' : state.answer, 'isanswer' : true},
        {'value' : state.distractors[0], 'isanswer' : false},
        {'value' : state.distractors[1], 'isanswer' : false},
        {'value' : state.distractors[2], 'isanswer' : false}])

        return {state}
    
    }



}
</script>

<style>

</style>