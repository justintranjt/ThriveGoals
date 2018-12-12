<template>
    <b-container fluid id="aboutUsContainer">
        <b-navbar toggleable fixed="top" variant="light" type="light">
            <b-navbar-toggle target="nav_text_collapse"></b-navbar-toggle>
            <b-collapse is-nav id="nav_collapse">
                <b-navbar-brand>Thrive</b-navbar-brand>
                <b-navbar-nav class="ml-auto">
                    <b-nav-item v-bind:href="clientURI">Home</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
        <b-container class="mt-4 pt-5 pb-2 text-center" id="bv-r2c2">
            <h1 id="aboutUsText">About Thrive</h1>
            <p id="aboutUsText">Thrive is a COS 333 project advised by Mohamed El-Dirany and Robert Dondero. The creation of Thrive was motivated by assisting first generation college students in the Office of Access and Inclusion’s FSI Summer program. Our system provides users with modifiable templates created by learning specialists and other students to help them structure their work processes for major assignments like papers and coding projects.</p>
        </b-container>
        <b-container class="mt-4 text-center" id="bv-r2c2">
            <h1 id="aboutUsText">Team</h1>
            <b-card-group deck>
                <b-card class="border-0" img-src="https://placekitten.com/1000/300" img-top>
                    <h5 class="card-title">Josh Gardner</h5>
                    <p class="card-text">
                        COS '20
                    </p>
                    <a href="#"
               class="card-link">GitHub</a>
                    <a href="#"
               class="card-link">Website</a>
                </b-card>
                <b-card class="border-0" img-src="https://placekitten.com/1000/300" img-top>
                    <h5 class="card-title">Sonia Joseph</h5>
                    <p class="card-text">
                        NEU '19
                    </p>
                    <a href="#"
               class="card-link">GitHub</a>
                    <a href="#"
               class="card-link">Website</a>
                </b-card>
                <b-card class="border-0" img-src="https://placekitten.com/1000/300" img-top>
                    <h5 class="card-title">Hamza Mahmood</h5>
                    <p class="card-text">
                        COS '20
                    </p>
                    <a href="#"
               class="card-link">GitHub</a>
                    <a href="#"
               class="card-link">Website</a>
                </b-card>
                <b-card class="border-0" img-src="/static/JTran.jpg" img-top>
                    <h5 class="card-title">Justin Tran</h5>
                    <p class="card-text">
                        COS '20
                    </p>
                    <a href="https://github.com/justintranjt"
               class="card-link">GitHub</a>
                    <a href="https://justintranjt.me/"
               class="card-link">Website</a>
                </b-card>
                <b-card class="border-0" img-src="https://placekitten.com/1000/300" img-top>
                    <h5 class="card-title">Viktoria Zlatinova</h5>
                    <p class="card-text">
                        COS '19
                    </p>
                    <a href="#"
               class="card-link">GitHub</a>
                    <a href="#"
               class="card-link">Website</a>
                </b-card>
            </b-card-group>
        </b-container>
    </b-container fluid>
</template>
<script>
export default {
    data() {
        return {
            clientURI: process.env.URI_CLIENT_ROOT,
        };
    },
};
</script>