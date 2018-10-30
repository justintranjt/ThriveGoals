<template>
  <div>
    <b-alert variant="success" show>{{ netid }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['netid'],
};
</script>
