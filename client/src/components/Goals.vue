<template>
    <div>
        <b-navbar toggleable fixed="top" variant="light" type="light">
            <b-navbar-toggle target="nav_text_collapse"></b-navbar-toggle>
            <b-navbar-brand>Thrive</b-navbar-brand>
            <b-nav-text>Logged in as {{ netID }}</b-nav-text>
            <b-navbar-nav class="ml-auto">
                <b-nav-item v-bind:href="clientURI">Home</b-nav-item>
                <!-- Allow this template creation to change the template name -->
                <b-nav-item><em>Create Template</em></b-nav-item>
                <b-nav-item-dropdown right>
                    <!-- Using button-content slot -->
                    <template slot="button-content">
                        <em>Templates</em>
                    </template>
                    <b-dropdown-item v-for="(template, index) in goalTemplateIDs" :key="index" @click="onSetTemplate(template)">
                        {{ template }}
                    </b-dropdown-item>
                </b-nav-item-dropdown>
                <b-nav-item href="https://fed.princeton.edu/cas/logout">Logout</b-nav-item>
            </b-navbar-nav>
        </b-navbar>
        <div class="container">
            <div class="col-md-12">
                <h1>Goals</h1>
                <hr>
                <alert :message="message" v-if="showMessage"></alert>
                <!-- Editable template name -->
                <h1 @dblclick="updatedTemplate=(currGoalTemplateID); newTemplateID=currGoalTemplateID">
                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedTemplate!=(currGoalTemplateID)"> {{ currGoalTemplateID }} </label>
                    <input v-if="updatedTemplate==(currGoalTemplateID)" v-model="newTemplateID" @keyup.enter="updateTemplate(currGoalTemplateID);">
                </h1>
                <h5>Overall Goal Progress</h5>
                <prog :value="numCompleted/goals.length"></prog>
                <b-button type="b-button" class="btn btn-success btn-med" v-b-modal.goal-modal>Add Goal</b-button>
                <br><br>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th scope="col">Goal #</th>
                            <th scope="col">Goal</th>
                            <th scope="col" class="text-right">Actions</th>
                        </tr>
                    </thead>
                    <draggable v-model="list" :element="'tbody'">
                        <tr v-for="(goal, index) in goals" :key="index">
                            <!-- Every cell has a bg color if goal.completed=True or goal.inProgress=True. No bg color if False -->
                            <!-- Goal Number -->
                            <td v-if=goal.completed v-bind:style="{backgroundColor: '#28a745c4'}" @dblclick="updatedGoalNum=(goal); newGoalNum=goal.goalNum">
                                <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalNum!=(goal)"> {{ goal.goalNum }} </label>
                                <input v-if="updatedGoalNum==(goal)" v-model="newGoalNum" @keyup.enter="updateGoalNum(goal);">
                            </td>
                            <td v-else-if=goal.inProgress v-bind:style="{backgroundColor: '#e0a800'}" @dblclick="updatedGoalNum=(goal); newGoalNum=goal.goalNum">
                                <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalNum!=(goal)"> {{ goal.goalNum }} </label>
                                <input v-if="updatedGoalNum==(goal)" v-model="newGoalNum" @keyup.enter="updateGoalNum(goal);">
                            </td>
                            <td v-else @dblclick="updatedGoalNum=(goal); newGoalNum=goal.goalNum">
                                <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalNum!=(goal)"> {{ goal.goalNum }} </label>
                                <input v-if="updatedGoalNum==(goal)" v-model="newGoalNum" @keyup.enter="updateGoalNum(goal);">
                            </td>
                            <!-- Goal title -->
                            <td v-if=goal.completed v-bind:style="{backgroundColor: '#28a745c4'}" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                            </td>
                            <td v-else-if=goal.inProgress v-bind:style="{backgroundColor: '#e0a800'}" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                            </td>
                            <td v-else @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                            </td>
                            <!-- Buttons -->
                            <td v-if=goal.completed v-bind:style="{backgroundColor: '#28a745c4'}">
                                <div class="btn-toolbar float-right" role="toolbar">
                                    <v-hover>
                                        <div slot-scope="{hover}" class="btn-group mr-2" role="group">
                                            <b-button v-if="hover" type="b-button" class="btn btn-secondary btn-sm" @click="onCompleteGoal(goal)">
                                                Not Complete
                                            </b-button>
                                            <b-button v-else type="b-button" class="btn btn-secondary btn-sm" @click="onCompleteGoal(goal)">
                                                <v-icon>undo</v-icon>
                                            </b-button>
                                        </div>
                                    </v-hover>
                                    <v-hover>
                                        <div slot-scope="{hover}" class="btn-group" role="group">
                                            <b-button v-if="hover" type="b-button" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">
                                                Delete
                                            </b-button>
                                            <b-button v-else="hover" type="b-button" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">
                                                <v-icon>delete_forever</v-icon>
                                            </b-button>
                                        </div>
                                    </v-hover>
                                </div>
                            </td>
                            <td v-else-if=goal.inProgress v-bind:style="{backgroundColor: '#e0a800'}">
                                <div class="btn-toolbar float-right" role="toolbar">
                                    <v-hover>
                                        <div slot-scope="{hover}" class="btn-group mr-2" role="group">
                                            <b-button v-if="hover" type="b-button" class="btn btn-secondary btn-sm" @click="onInProgGoal(goal)">
                                                Not In Progress
                                            </b-button>
                                            <b-button v-else type="b-button" class="btn btn-secondary btn-sm" @click="onInProgGoal(goal)">
                                                <v-icon>undo</v-icon>
                                            </b-button>
                                        </div>
                                    </v-hover>
                                    <v-hover>
                                        <div slot-scope="{hover}" class="btn-group" role="group">
                                            <b-button v-if="hover" type="b-button" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">
                                                Delete
                                            </b-button>
                                            <b-button v-else="hover" type="b-button" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">
                                                <v-icon>delete_forever</v-icon>
                                            </b-button>
                                        </div>
                                    </v-hover>
                                </div>
                            </td>
                            <td v-else>
                                <div class="btn-toolbar float-right" role="toolbar">
                                    <v-hover>
                                        <div slot-scope="{hover}" class="btn-group mr-2" role="group">
                                            <b-button v-if="hover" type="b-button" class="btn btn-success btn-sm" @click="onCompleteGoal(goal)">Complete</b-button>
                                            <b-button v-else type="b-button" class="btn btn-success btn-sm" @click="onCompleteGoal(goal)">
                                                <v-icon>done</v-icon>
                                            </b-button>
                                        </div>
                                    </v-hover>
                                    <v-hover>
                                        <div slot-scope="{hover}" class="btn-group mr-2" role="group">
                                            <b-button v-if="hover" type="b-button" class="btn btn-warning btn-sm" @click="onInProgGoal(goal)">
                                                In Progress
                                            </b-button>
                                            <b-button v-else type="b-button" class="btn btn-warning btn-sm" @click="onInProgGoal(goal)">
                                                <v-icon>schedule</v-icon>
                                            </b-button>
                                        </div>
                                    </v-hover>
                                    <v-hover>
                                        <div slot-scope="{hover}" class="btn-group" role="group">
                                            <b-button v-if="hover" type="b-button" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">
                                                Delete
                                            </b-button>
                                            <b-button v-else="hover" type="b-button" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">
                                                <v-icon>delete_forever</v-icon>
                                            </b-button>
                                        </div>
                                    </v-hover>
                                </div>
                            </td>
                        </tr>
                    </draggable>
                </table>
            </div>
        </div>
        <!-- Pop-up modals -->
        <b-modal ref="addGoalModal" id="goal-modal" title="Add a new goal" hide-footer>
            <b-form @submit="onSubmit" @reset="onReset" class="w-100">
                <b-form-group label="Goal Number:" label-for="form-goalNumber-input">
                    <b-form-input id="form-goalNumber-input" type="number" v-model.number="addGoalForm.goalNum" required placeholder="Enter goal number">
                    </b-form-input>
                </b-form-group>
                <b-form-group label="Goal Title:" label-for="form-goalTitle-input">
                    <b-form-input id="form-goalTitle-input" type="text" v-model="addGoalForm.goalTitle" required placeholder="Enter goal title">
                    </b-form-input>
                </b-form-group>
                <b-form-checkbox class="mb-3" label="Completed?" v-model="addGoalForm.completed">
                    Completed?
                </b-form-checkbox>
                <br>
                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>
    </div>
</template>
<script>
import axios from 'axios';
import draggable from 'vuedraggable';
import alert from './Alert';
import prog from './Progress';

export default {
    data() {
        return {
            netID: '',
            goalTemplateIDs: [],
            currGoalTemplateID: 'Template 1', // Default template ID
            goals: [],
            addGoalForm: {
                goalNum: 0,
                goalTitle: '',
                completed: false,
            },
            message: '',
            showMessage: false,
            numCompleted: 0,
            clientURI: process.env.URI_CLIENT_ROOT,
            // Double click to edit boolean and new entry fields
            updatedGoalNum: null,
            updatedGoalTitle: null,
            updatedTemplate: null,
            newGoalNum: null,
            newGoalTitle: null,
            newTemplateID: null,
        };
    },
    components: {
        alert,
        draggable,
        prog,
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
        getGoals(goalTemplateID) {
            const path = process.env.URI_SERVER_ROOT + '/modGoals/' + goalTemplateID;
            axios.get(path)
                .then((res) => {
                    this.goals = res.data.goals;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        getNumCompleted(goalTemplateID) {
            const path = process.env.URI_SERVER_ROOT + '/completedGoals/' + goalTemplateID;
            axios.get(path)
                .then((res) => {
                    this.numCompleted = res.data.numCompleted;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        async getTemplates() {
            const path = process.env.URI_SERVER_ROOT + '/getTemplates';
            await axios.get(path)
                .then((res) => {
                    this.goalTemplateIDs = res.data.goalTemplateIDs;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
        },
        addGoal(payload, goalTemplateID) {
            const path = process.env.URI_SERVER_ROOT + '/modGoals/' + goalTemplateID;
            axios.post(path, payload)
                .then(() => {
                    this.getGoals(goalTemplateID);
                    this.getNumCompleted(goalTemplateID);
                    this.message = 'Goal added!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals(goalTemplateID);
                    this.getNumCompleted(goalTemplateID);
                });
        },
        completeGoal(goalNum, goalTemplateID) {
            const path = process.env.URI_SERVER_ROOT + '/completeGoal/' + goalNum + '/' + goalTemplateID;
            axios.put(path)
                .then((res) => {
                    this.getGoals(goalTemplateID);
                    this.getNumCompleted(goalTemplateID);
                    this.message = res.data.message;
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals(goalTemplateID);
                    this.getNumCompleted(goalTemplateID);
                    this.showMessage = true;
                });
        },
        deleteGoal(goalNum, goalTemplateID) {
            const path = process.env.URI_SERVER_ROOT + '/modGoals/' + goalNum + '/' + goalTemplateID;
            axios.delete(path)
                .then(() => {
                    this.getGoals(goalTemplateID);
                    this.getNumCompleted(goalTemplateID);
                    this.message = 'Goal deleted!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals(goalTemplateID);
                    this.getNumCompleted(goalTemplateID);
                });
        },
        inProgGoal(goalNum, goalTemplateID) {
            const path = process.env.URI_SERVER_ROOT + '/inProgGoal/' + goalNum + '/' + goalTemplateID;
            axios.put(path)
                .then((res) => {
                    this.getGoals(goalTemplateID);
                    this.getNumCompleted(goalTemplateID);
                    this.message = res.data.message;
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals(goalTemplateID);
                    this.getNumCompleted(goalTemplateID);
                    this.showMessage = true;
                });
        },
        updateGoalNum(goal) {
            this.updatedGoalNum = '';
            const payload = {
                goalNum: parseInt(this.newGoalNum),
                goalTitle: goal.goalTitle,
                completed: goal.completed,
                inProgress: goal.inProgress,
            };
            const path = process.env.URI_SERVER_ROOT + '/modGoals/' + goal.goalNum + '/' + this.currGoalTemplateID;
            axios.put(path, payload)
                .then(() => {
                    this.getGoals(this.currGoalTemplateID);
                    this.getNumCompleted(this.currGoalTemplateID);
                    this.message = 'Goal updated!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals(this.currGoalTemplateID);
                    this.getNumCompleted(this.currGoalTemplateID);
                });
        },
        updateGoalTitle(goal) {
            this.updatedGoalTitle = '';
            const payload = {
                goalNum: goal.goalNum,
                goalTitle: this.newGoalTitle,
                completed: goal.completed,
                inProgress: goal.inProgress,
            };
            const path = process.env.URI_SERVER_ROOT + '/modGoals/' + goal.goalNum + '/' + this.currGoalTemplateID;
            axios.put(path, payload)
                .then(() => {
                    this.getGoals(this.currGoalTemplateID);
                    this.getNumCompleted(this.currGoalTemplateID);
                    this.message = 'Goal updated!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.getGoals(this.currGoalTemplateID);
                    this.getNumCompleted(this.currGoalTemplateID);
                });
        },
        updateTemplate(goalTemplateID) {
            const payload = {
                newTemplateID: this.newTemplateID,
            };

            this.updatedTemplate = '';

            const path = process.env.URI_SERVER_ROOT + '/modTemplates/' + this.currGoalTemplateID;
            axios.put(path, payload)
                .then(() => {
                    this.getTemplates();
                    this.currGoalTemplateID = this.newTemplateID;
                    this.getGoals(this.newTemplateID);
                    this.getNumCompleted(this.newTemplateID);
                    this.message = 'Template updated!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error);
                    this.currGoalTemplateID = this.newTemplateID;
                    this.getGoals(this.newTemplateID);
                    this.getNumCompleted(this.newTemplateID);
                });
        },
        initForm() {
            this.addGoalForm.goalNum = 0;
            this.addGoalForm.goalTitle = '';
            this.addGoalForm.completed = false;
        },
        onCompleteGoal(goal) {
            this.completeGoal(goal.goalNum, this.currGoalTemplateID);
        },
        onDeleteGoal(goal) {
            this.deleteGoal(goal.goalNum, this.currGoalTemplateID);
        },
        onInProgGoal(goal) {
            this.inProgGoal(goal.goalNum, this.currGoalTemplateID);
        },
        onSubmit(evt) {
            evt.preventDefault();
            this.$refs.addGoalModal.hide();
            const payload = {
                goalNum: this.addGoalForm.goalNum,
                goalTitle: this.addGoalForm.goalTitle,
                completed: this.addGoalForm.completed,
            };
            this.addGoal(payload, this.currGoalTemplateID);
            this.initForm();
        },
        onReset(evt) {
            evt.preventDefault();
            this.initForm();
        },
        onSetTemplate(goalTemplateID) {
            this.currGoalTemplateID = goalTemplateID;
            this.getGoals(goalTemplateID);
            this.getNumCompleted(goalTemplateID);
        },
    },
    async created() {
        this.getLoginNetID();
        await this.getTemplates();
        this.getGoals(this.currGoalTemplateID);
        this.getNumCompleted(this.currGoalTemplateID);
    },
};
</script>