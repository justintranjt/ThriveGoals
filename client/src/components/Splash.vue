<template>
    <b-container fluid class="container-fluid" id="splashContainer">
        <b-navbar toggleable fixed="top" variant="light" type="light">
            <b-navbar-toggle target="nav_text_collapse"></b-navbar-toggle>
            <b-navbar-brand>Thrive</b-navbar-brand>
        </b-navbar>
        <b-row id="intro">
            <b-col>
                <h3 id="hometitle">THRIVE</h3>
                <h2 id="row1-1">Set goals and track <br> your progress every <br> step of the way.</h2>
                <b-form id="loginButton">
                    <b-button variant="secondary lg" size="lg" v-bind:href="serverURI + '/loginPage'">Login via CAS</b-button>
                </b-form>
            </b-col>
        </b-row>
        <b-row id="aboutText">
                <b-col id="bv-r2c2">
                    <h1>About Thrive</h1>
                    <!-- eslint-disable -->
                    Our software helps you break down large projects into manageable subgoals in a goal hierarchy, reducing procrastination and making work more enjoyable and intrinsically motivating. Our modifiable templates are created by learning specialists and other students with the purpose of guiding you through major assignments.
                </b-col>
        </b-row>
    </b-container>
</template>
<script>
import axios from 'axios';

export default {
    data() {
        return {
            netID: '',
            serverURI: process.env.URI_SERVER_ROOT,
        };
    },
    methods: {
        getLoginNetID() {
            const path = process.env.URI_SERVER_ROOT + '/loginNetID';
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
    },
};
</script>
