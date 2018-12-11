<template>
  <div>
    <b-alert v-if="message==('Duplicate template names not allowed.')" dismissible variant="danger" show>{{ message }}</b-alert>
    <b-alert v-if="message==('Can\'t swap goals of different levels.')" dismissible variant="danger" show>{{ message }}</b-alert>
    <b-alert v-else dismissible variant="success" show>{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
    props: ['message'],
};
</script>
