<template>
<div class="p-4">
    <div>
        <span>{{(qno +1) + '. '}}</span><span>{{mcq.question}}</span>
    </div>
    
    <div v-for="(option, ind) in mcq.options" :key="ind" class="px-4">
        <span>{{String.fromCharCode(65 + ind) + ') '}}</span>
        <span :class="showanswer && option.isanswer ? 'text-green-500 font-bold' : ''" > {{option.value}}</span>
    </div>


</div>
  
</template>

<script>
// import {reactive} from 'vue'
export default {
    props : {
        'mcq' : {
            'question' : String,
            'options' : Array
        },
        'qno' : Number,
        'showanswer' : Boolean
    },
    setup()
    {
    
    }



}
</script>

<style>

</style>