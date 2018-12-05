<template>
    <div>
        <b-alert dismissible variant="success" show>{{ message }}</b-alert>
        <br>
    </div>
</template>

<script>
export default {
    props: ['message'],
};
</script>