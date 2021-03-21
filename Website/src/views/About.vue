<template>
  <div class="flex m-auto w-10/11 justify-center h-screen bg-white">
    <title>About</title>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
    />
    <div id="myPage">
      <br /><br />
      <div class="bgimg-1 w3-display-container w3-opacity-min" id="home">
        <div class="w3-display-middle" style="white-space:nowrap;">
          <span
            class="w3-center w3-padding-large w3-black w3-xlarge w3-wide w3-animate-opacity"
            >FINAL<span class="w3-hide-small"> YEAR </span> PROJECT
          </span>
        </div>
      </div>
      <br /><br />
      <!-- Container (About Section) -->
      <div class="">
        <h2 class="w3-center text-3xl font-bold">ABOUT THE PROJECT</h2>
        <p class="w3-center text-xs">
          <em
            >Multiple Choice Q&A and Distractor Generation using
            Text-Transformers</em
          >
        </p>
        <p class="text-justify m-12 text-xl w-8/12 mx-auto">
          With so much digital content to learn from, it is almost impossible to
          test one's understanding. It is also pretty difficult to ask someone
          to prepare questions based on the learned content, So we built this
          automatic MCQ generator which works with any form of text and provides
          candidate MCQ questions with suitable distractors with which one can
          test their understanding of the content. The question generator is a
          fine-tuned T5-base model for question generation task.
        </p>
        <center>
          <h6>
            <a
              href="https://www.overleaf.com/project/5f8628c048052f0001387df7"
              class="text-blue-500 underline"
              >More About This Project</a
            >
          </h6>
        </center>
      </div>

      <div class="w3-container w3-padding-64 w3-center">
        <h2 class="text-3xl font-bold">OUR TEAM</h2>
        <p class="w3-center text-xs">
          <em
            >SSN College of Engineering - Dept. of Computer Science &
            Engineering</em
          >
        </p>
        <br />
        <div class="w3-row">
          <br />

          <center>
            <div class="w3-third">
              <img
                src="../assets/Pictures/jayaraman.jpeg"
                alt="Jayaraman"
                style="width:45%"
                class="w3-circle w3-hover-opacity"
              />
              <h3>Jayaraman N R</h3>
              <p>Final Year</p>
            </div>

            <div class="w3-third">
              <img
                src="../assets/Pictures/gokul.jpg"
                alt="Gokul"
                style="width:45%"
                class="w3-circle w3-hover-opacity"
              />
              <h3>Gokul Sahar</h3>
              <p>Final Year</p>
            </div>

            <div class="w3-third">
              <img
                src="../assets/Pictures/dinesh.jpg"
                alt="Dinesh"
                style="width:45%"
                class="w3-circle w3-hover-opacity"
              />
              <h3>Dinesh K</h3>
              <p>Final Year</p>
            </div>
          </center>
        </div>
      </div>
      <footer class="w3-container w3-padding-32 w3-theme-d1 w3-center">
        <h4>Contact Us</h4>
        <div class="flex w-full justify-around mt-10">
          <div class="justify-between">
            <a
              class="w3-button w3-large"
              href="https://github.com/range123"
              title="Github"
              ><i class="fa fa-github"></i
            ></a>
            <a
              class="w3-button w3-large"
              href="https://www.linkedin.com/in/jayaraman-n-r-884818193/"
              title="Linkedin"
              ><i class="fa fa-linkedin"></i
            ></a>
          </div>
          <div class="justify-between">
            <a
              class="w3-button w3-large"
              href="https://github.com/gokulsahar"
              title="Github"
              ><i class="fa fa-github"></i
            ></a>
            <a
              class="w3-button w3-large"
              href="https://www.linkedin.com/in/gokulsahar/"
              title="Linkedin"
              ><i class="fa fa-linkedin"></i
            ></a>
          </div>
          <div class="justify-between">
            <a class="w3-button w3-large" href="" title="Github"
              ><i class="fa fa-github"></i
            ></a>
            <a
              class="w3-button w3-large"
              href="javascript:void(0)"
              title="Linkedin"
              ><i class="fa fa-linkedin"></i
            ></a>
          </div>
        </div>

        <div
          style="position:relative;bottom:100px;z-index:1;"
          class="w3-tooltip w3-right"
        >
          <span class="w3-text w3-padding w3-hide-small">Go To Top</span>
          <a class="w3-button w3-theme" @click.prevent="scrollTop"
            ><span class="w3-xlarge">
              <i class="fa fa-chevron-circle-up"></i></span
          ></a>
        </div>
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "About",
  methods: {
    async scrollTop() {
      window.scrollTo(0, 0);
    }
  }
});
</script>

<style scoped src="../assets/Styles/w3.css"></style>
