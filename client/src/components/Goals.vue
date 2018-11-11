<template>
    <div>
        <b-navbar toggleable fixed="top" variant="light" type="light">
            <b-navbar-toggle target="nav_text_collapse"></b-navbar-toggle>
            <b-navbar-brand>Thrive</b-navbar-brand>
            <b-nav-text>Logged in as {{ netID }}</b-nav-text>
            <b-navbar-nav class="ml-auto">
                <b-nav-item href="http://localhost:8080/">Home</b-nav-item>
                <b-nav-item-dropdown right>
                    <!-- Using button-content slot -->
                    <template slot="button-content">
                        <em>Templates</em>
                    </template>
                    <b-dropdown-item href="#">Template 1</b-dropdown-item>
                    <b-dropdown-item href="#">Template 2</b-dropdown-item>
                </b-nav-item-dropdown>
                <b-nav-item href="https://fed.princeton.edu/cas/logout">Logout</b-nav-item>
            </b-navbar-nav>
        </b-navbar>
        <div class="container">
            <div class="col-md-12">
                <h1>Goals</h1>
                <hr>
                <alert :message="message" v-if="showMessage"></alert>
                <h5>Overall Goal Progress</h5>
                <b-progress v-if="numCompleted!==0" :value="numCompleted/goals.length" :max=1 :precision="2" show-progress class="mb-3" variant="success"></b-progress>
                <b-progress v-else :value="0" :max=1 :precision="2" show-progress class="mb-3" variant="success"></b-progress>
                <button type="button" class="btn btn-success btn-med" v-b-modal.goal-modal>Add Goal</button>
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
                            <!-- Every cell has a green background if goal.completed=True. Perhaps there's a cleaner way to implement this -->
                            <td v-if=goal.completed v-bind:style="{backgroundColor: '#28a745c4'}">{{ goal.goalNum }}</td>
                            <td v-else>{{ goal.goalNum }}</td>
                            <td v-if=goal.completed v-bind:style="{backgroundColor: '#28a745c4'}">{{ goal.goalTitle }}</td>
                            <td v-else>{{ goal.goalTitle }}</td>
                            <td v-if=goal.completed v-bind:style="{backgroundColor: '#28a745c4'}">
                                <div class="btn-toolbar float-right" role="toolbar">
                                    <div class="btn-group mr-2" role="group">
                                        <button type="button" class="btn btn-success btn-sm" @click="onCompleteGoal(goal)">Complete</button>
                                    </div>
                                    <div class="btn-group mr-2" role="group">
                                        <button type="button" class="btn btn-warning btn-sm" v-b-modal.goal-update-modal @click="editGoal(goal)">Update</button>
                                    </div>
                                    <div class="btn-group" role="group">
                                        <button type="button" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">Delete</button>
                                    </div>
                                </div>
                            </td>
                            <td v-else>
                                <div class="btn-toolbar float-right" role="toolbar">
                                    <div class="btn-group mr-2" role="group">
                                        <button type="button" class="btn btn-success btn-sm" @click="onCompleteGoal(goal)">Complete</button>
                                    </div>
                                    <div class="btn-group mr-2" role="group">
                                        <button type="button" class="btn btn-warning btn-sm" v-b-modal.goal-update-modal @click="editGoal(goal)">Update</button>
                                    </div>
                                    <div class="btn-group" role="group">
                                        <button type="button" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">Delete</button>
                                    </div>
                                </div>
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
                <b-form-checkbox class="mb-3" id="form-completed-group" label="Completed?" label-for="form-goalTitle-input" v-model="addGoalForm.completed">
                    Completed?
                </b-form-checkbox>
                <br>
                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>
        <b-modal ref="updateGoalModal" id="goal-update-modal" title="Update this goal" hide-footer>
            <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                <b-form-group id="form-goalNumber-update-group" label="Goal Number:" label-for="form-goalNumber-update-input">
                    <b-form-input id="form-goalNumber-update-input" type="number" v-model.number="updateGoalForm.goalNum" required placeholder="Enter goal number">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-goalTitle-update-group" label="Goal Title:" label-for="form-goalTitle-update-input">
                    <b-form-input id="form-goalTitle-update-input" type="text" v-model="updateGoalForm.goalTitle" required placeholder="Enter goal title">
                    </b-form-input>
                </b-form-group>
                <b-form-checkbox class="mb-3" id="form-completed-update-group" label="Completed?" label-for="form-goalTitle-update-input" v-model="updateGoalForm.completed">
                    Completed?
                </b-form-checkbox>
                <br>
                <b-button type="submit" variant="primary">Save Updates</b-button>
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
            netID: '',
            goals: [],
            addGoalForm: {
                goalNum: 0,
                goalTitle: '',
                completed: false,
            },
            updateGoalForm: {
                rowNum: 0, // This is the goal number BEFORE we update it
                goalNum: 0, // This is the goal number we are updating it TO
                goalTitle: '',
                completed: false,
            },
            message: '',
            showMessage: false,
            numCompleted: 0,
        };
    },
    components: {
        alert: Alert,
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
        getNumCompleted() {
            const path = 'http://localhost:5000/completedGoals';
            axios.get(path)
                .then((res) => {
                    this.numCompleted = res.data.numCompleted;
                    console.log(this.numCompleted);
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
                    this.getNumCompleted();
                    this.message = 'Goal added!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals();
                    this.getNumCompleted();
                });
        },
        completeGoal(goalNum) {
            const path = `http://localhost:5000/completeGoal/${goalNum}`;
            axios.put(path)
                .then(() => {
                    this.getGoals();
                    this.getNumCompleted();
                    this.message = 'Goal completed!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals();
                    this.getNumCompleted();
                });
        },
        deleteGoal(goalNum) {
            const path = `http://localhost:5000/modGoals/${goalNum}`;
            axios.delete(path)
                .then(() => {
                    this.getGoals();
                    this.getNumCompleted();
                    this.message = 'Goal deleted!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals();
                    this.getNumCompleted();
                });
        },
        updateGoal(payload, goalNum) {
            const path = `http://localhost:5000/modGoals/${goalNum}`;
            axios.put(path, payload)
                .then(() => {
                    this.getGoals();
                    this.getNumCompleted();
                    this.message = 'Goal updated!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals();
                    this.getNumCompleted();
                });
        },
        editGoal(goal) {
            this.updateGoalForm = goal;
            this.updateGoalForm.rowNum = goal.goalNum;
            this.updateGoalForm.completed = goal.completed;
        },
        initForm() {
            this.addGoalForm.goalNum = 0;
            this.addGoalForm.goalTitle = '';
            this.addGoalForm.completed = false;
            this.updateGoalForm.rowNum = 0;
            this.updateGoalForm.goalNum = 0;
            this.updateGoalForm.goalTitle = '';
            this.updateGoalForm.completed = false;
        },
        onCompleteGoal(goal) {
            this.completeGoal(goal.goalNum);
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
                completed: this.updateGoalForm.completed,
            };
            this.updateGoal(payload, this.updateGoalForm.rowNum);
        },
        onResetUpdate(evt) {
            evt.preventDefault();
            this.$refs.updateGoalModal.hide();
            this.initForm();
            this.getGoals();
            this.getNumCompleted();
        },
        onSubmit(evt) {
            evt.preventDefault();
            this.$refs.addGoalModal.hide();
            const payload = {
                goalNum: this.addGoalForm.goalNum,
                goalTitle: this.addGoalForm.goalTitle,
                completed: this.addGoalForm.completed,
            };
            this.addGoal(payload);
            this.initForm();
        },
        onReset(evt) {
            evt.preventDefault();
            this.initForm();
        },
    },
    onReset(evt) {
        evt.preventDefault();
        this.initForm();
    },
    beforeMount() {
        this.getLoginNetID();
        this.getGoals();
        this.getNumCompleted();
    },
};
</script>