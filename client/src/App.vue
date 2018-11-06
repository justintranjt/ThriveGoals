<template>
  <div id="app">
<!--     <b-navbar toggleable fixed="top" variant="light" type="light">
      <b-navbar-toggle target="nav_text_collapse"></b-navbar-toggle>
      <b-navbar-brand>Thrive</b-navbar-brand>
      <b-nav-text>Logged in as {{ netID }}</b-nav-text>
    </b-navbar> -->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  // data() {
  //   return {
  //     netID: '',
  //   };
  // },
  // methods: {
  //   getLoginNetID() {
  //     const path = 'http://localhost:5000/loginNetID';
  //     axios.get(path)
  //       .then((res) => {
  //         this.netID = res.data.netID;
  //       })
  //       .catch((error) => {
  //         // eslint-disable-next-line
  //         console.error(error);
  //       });
  //     },
  //   },
  //   beforeMount() {
  //     this.getLoginNetID();
  //   },
};
</script>

<style>

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
