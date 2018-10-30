<template>
<div>
<div class="container-fluid">
    <h3>Think of this as the main page of your application after {{ netid }} has been authenticated.</h3>
    <b-form @login="onLogin" class="w-100">
      <b-button href="https://fed.princeton.edu/cas/logout" variant="primary">Log me out of this website and CAS!</b-button>
      <b-button type="login" href="http://localhost:8080/" variant="primary">Home</b-button>
    </b-form>
</div>

<div class="container-fluid">
      <div class="col-med-12">
        <br>
        <h1>Goals</h1>
        <hr><br>
        <alert :message="message" v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.goal-modal>Add Goal</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Goal #</th>
              <th scope="col">Goal</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(Goal, index) in Goals" :key="index">
              <td>{{  }}</td>
              <td>{{  }}</td>
              <td>
                <button type="button" class="btn btn-warning btn-sm">Update</button>
                <button type="button" class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  </div>

  <b-modal ref="addGoalModal"
           id="goal-modal"
           title="Add a new goal"
           hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Goal Number:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addGoalForm.goalNum"
                        required
                        placeholder="Enter goal number">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-goalTitle-group"
                      label="Goal Title:"
                      label-for="form-goalTitle-input">
            <b-form-input id="form-goalTitle-input"
                          type="text"
                          v-model="addGoalForm.goalTitle"
                          required
                          placeholder="Enter goal title">
            </b-form-input>
          </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
  </b-modal>
</div>
</template>
<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      goals: [],
      addGoalForm: {
        goalNum: '',
        goalTitle: '',
      },
      netid: 'NETID HERE',
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    // This isn't firing
    onLogin(evt) {
      evt.preventDefault();
      const path = 'http://localhost:5000/';
      axios.get(path)
        .then((res) => {
          this.netid = res.data.netid;
        })
        .catch((error) => {
            // eslint-disable-next-line
          console.error(error);
        });
    },
    getGoals() {
      const path = 'http://localhost:5000/goals';
      axios.get(path)
        .then((res) => {
          this.goals = res.data.goals;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addGoal(payload) {
      const path = 'http://localhost:5000/books';
      axios.post(path, payload)
        .then(() => {
          this.getGoals();
          this.message = 'Goal added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getGoals();
        });
    },
    initForm() {
      this.addBookForm.goalNum = '';
      this.addBookForm.goalTitle = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addGoalModal.hide();
      // if (this.addGoalForm.read[0]) read = true;
      const payload = {
        goalNum: this.addGoalForm.goalNum,
        goalTitle: this.addGoalForm.goalTitle,
      };
      this.addGoal(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addGoalModal.hide();
      this.initForm();
    },
  },
  created() {
    this.onLogin();
  }
};
</script>