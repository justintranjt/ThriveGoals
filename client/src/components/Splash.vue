<template>
    <div class="container">
        <h3>Welcome to Thrive</h3>
        <h2>Logged in as {{ netid }}</h2>
        <b-form @login="onLogin" class="w-100">
            <b-button type="login" variant="primary" href="http://localhost:5000/goals">Login via CAS</b-button>
            <!-- <b-button type="login" variant="primary">Login via CAS</b-button> -->
        </b-form>
    </div>
</template>

<script>
import axios from 'axios';

// This isn't firing
export default {
  data() {
    return {
      netid: 'NETID HERE',
    };
  },
  methods: {
    onLogin(evt) {
      evt.preventDefault();
      const path = 'http://localhost:5000/goals';
      axios.get(path)
        .then((res) => {
          this.netid = res.data.netid;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.onLogin();
  }
};
</script>