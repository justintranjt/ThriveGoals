<template>
    <div>
        <b-alert v-if="message==('Duplicate template names not allowed.')" dismissible variant="danger" show>{{ message }}</b-alert>
        <b-alert v-else-if="message==('Can\'t swap topmost goal.')" dismissible variant="danger" show>{{ message }}</b-alert>
        <b-alert v-else-if="message==('Can\'t swap bottommost goal.')" dismissible variant="danger" show>{{ message }}</b-alert>
        <b-alert v-else dismissible variant="success" show>{{ message }}</b-alert>
        <br>
    </div>
</template>
<script>
export default {
    props: ['message'],
};
</script>