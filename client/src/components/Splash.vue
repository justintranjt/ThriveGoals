<template>
    <div class="container-fluid p-5" id="splashContainer">
        <h3>Welcome to Thrive</h3>
        <h2>Logged in as {{ netID }}</h2>
        <b-form>
            <b-button variant="primary" href="http://localhost:5000/loginPage">Login via CAS</b-button>
        </b-form>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    data() {
        return {
            netID: '',
        };
    },
    methods: {
        getLoginNetID() {
            const path = 'http://localhost:5000/loginNetID';
            axios.get(path)
                .then((res) => {
                    this.netID = res.data.netID;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
    },
    beforeMount() {
        this.getLoginNetID();
    }
};
</script>