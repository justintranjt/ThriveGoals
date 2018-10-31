<template>
    <div>
        <div class="container-fluid p-5">
            <h3>Think of this as the main page of your application after {{ netid }} has been authenticated.</h3>
            <b-form @login="onLogin">
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
                        <tr v-for="(goal, index) in goals" :key="index">
                            <td>{{ goal.goalNum }}</td>
                            <td>{{ goal.goalTitle }}</td>
                            <td>
                                <button type="button" class="btn btn-warning btn-sm" v-b-modal.goal-update-modal @click="editGoal(goal)">Update</button>
                                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">Delete</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <b-modal ref="addGoalModal" id="goal-modal" title="Add a new goal" hide-footer>
            <b-form @submit="onSubmit" @reset="onReset" class="w-100">
                <b-form-group id="form-goalNumber-group" label="Goal Number:" label-for="form-goalNumber-input">
                    <b-form-input id="form-goalNumber-input" type="number" v-model.number="addGoalForm.goalNum" required placeholder="Enter goal number">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-goalTitle-group" label="Goal Title:" label-for="form-goalTitle-input">
                    <b-form-input id="form-goalTitle-input" type="text" v-model="addGoalForm.goalTitle" required placeholder="Enter goal title">
                    </b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="updateGoalModal" id="goal-update-modal" title="Update" hide-footer>
            <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                <b-form-group id="form-goalNumber-update-group" label="Goal Number:" label-for="form-goalNumber-update-input">
                    <b-form-input id="form-goalNumber-update-input" type="number" v-model.number="updateGoalForm.goalNum" required placeholder="Enter goal number">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-goalTitle-update-group" label="Goal Title:" label-for="form-goalTitle-update-input">
                    <b-form-input id="form-goalTitle-update-input" type="text" v-model="updateGoalForm.goalTitle" required placeholder="Enter goal title">
                    </b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Update</b-button>
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
                goalNum: 0,
                goalTitle: '',
            },
            updateGoalForm: {
                rowNum: 0, // This is the goal number BEFORE we update it
                goalNum: 0, // This is the goal number we are updating it TO
                goalTitle: '',
            },
            message: '',
            showMessage: false,
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
            const path = 'http://localhost:5000/modGoals';
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
            const path = 'http://localhost:5000/modGoals';
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
        deleteGoal(goalNum) {
            const path = `http://localhost:5000/modGoals/${goalNum}`;
            axios.delete(path)
                .then(() => {
                    this.getGoals();
                    this.message = 'Goal deleted!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals();
                });
        },
        updateGoal(payload, goalNum) {
            const path = `http://localhost:5000/modGoals/${goalNum}`;
            axios.put(path, payload)
                .then(() => {
                    this.getGoals();
                    this.message = 'Goal updated!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals();
                });
        },
        editGoal(goal) {
            this.updateGoalForm = goal;
            this.updateGoalForm.rowNum = goal.goalNum;
        },
        initForm() {
            this.addGoalForm.goalNum = 0;
            this.addGoalForm.goalTitle = '';
            this.updateGoalForm.rowNum = 0;
            this.updateGoalForm.goalNum = 0;
            this.updateGoalForm.goalTitle = '';
        },
        onDeleteGoal(goal) {
            this.deleteGoal(goal.goalNum);
        },
        onSubmitUpdate(evt) {
            evt.preventDefault();
            this.$refs.updateGoalModal.hide();
            const payload = {
                goalNum: this.updateGoalForm.goalNum,
                goalTitle: this.updateGoalForm.goalTitle,
            };
            this.updateGoal(payload, this.updateGoalForm.rowNum);
        },
        onResetUpdate(evt) {
            evt.preventDefault();
            this.initForm();
            this.getGoals();
        },
        onSubmit(evt) {
            evt.preventDefault();
            this.$refs.addGoalModal.hide();
            const payload = {
                goalNum: this.addGoalForm.goalNum,
                goalTitle: this.addGoalForm.goalTitle,
            };
            this.addGoal(payload);
            this.initForm();
        },
        onReset(evt) {
            evt.preventDefault();
            this.initForm();
        },
    },
    created() {
        // It appears that only the first method listed in created() is called. For now, onLogin is commented out so getGoals will load the table first 
        // this.onLogin();
        this.getGoals();
    },
};
</script>