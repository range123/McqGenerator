<template>
<div class="p-4">
    <div>
        <span class="w-1/12">{{(qno +1) + '. '}}</span><input @input="handleinput(0,$event.target.value)" :value="mcq.question" :readonly="!editable" class="bg-gray-100 outline-none w-11/12" >
    </div>
    
    <div v-for="(option, ind) in mcq.options" :key="ind" class="px-4">
        <span class="w-1/12">{{String.fromCharCode(65 + ind) + ') '}}</span>
        <input @input="handleinput(ind+1,$event.target.value)" class="bg-gray-100 outline-none w-11/12" :class="showanswer && option.isanswer ? 'text-green-500 font-bold' : ''" :value="option.value" :readonly="!editable">
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
        'showanswer' : Boolean,
        'editable' : Boolean
    },
    emits : ['onmcqchange']
    ,
    data()
    {
        const timer = null
        return {timer}
    },
    methods : {
        handleinput(type, value)
        {
            if (this.timer)
            {
                clearTimeout(this.timer)
                this.timer =null
            }
            this.timer = setTimeout(() => {
                            if (type === 0)
                            {
                                const temp = {...this.mcq}
                                temp.question = value
                                this.$emit('onmcqchange', temp)

                            }
                            else{
                                const temp = {...this.mcq}
                                temp.options[type-1] = {value,isanswer : temp.options[type-1].isanswer} 
                                this.$emit('onmcqchange', temp)

                            }

            },100)

        }
    }



}
</script>

<style>

</style>