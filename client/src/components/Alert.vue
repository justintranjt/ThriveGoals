<template>
  <div>
    <b-alert v-if="message==('Duplicate template names not allowed.')" variant="danger" show>{{ message }}</b-alert>
    <b-alert v-else variant="success" show>{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
