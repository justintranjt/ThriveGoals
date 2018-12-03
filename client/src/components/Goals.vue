<template>
    <div>
        <b-navbar toggleable fixed="top" variant="light" type="light">
            <b-navbar-toggle target="nav_text_collapse"></b-navbar-toggle>
            <b-navbar-brand>Thrive</b-navbar-brand>
            <b-nav-text>Logged in as {{ netID }}</b-nav-text>
            <b-navbar-nav class="ml-auto">
                <b-nav-item v-bind:href="clientURI">Home</b-nav-item>
                <!-- Allow this template creation to change the template name -->
                <b-nav-item @click="addTemplate()"><em>Create Template</em></b-nav-item>
                <b-nav-item @click="deleteTemplate()"><em>Delete Current Template</em></b-nav-item>
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
        <div id="goalsContainerBackground">
            <div class="container mt-4 pt-5 pb-2">
                <div class="shadow-lg col-lg-12 bg-white">
                    <br>
                    <alert :message="message" v-if="showMessage"></alert>
                    <!-- Editable template name -->
                    <h1 @dblclick="updatedTemplate=(currGoalTemplateID); newTemplateID=currGoalTemplateID">
                            <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedTemplate!=(currGoalTemplateID)"> {{ currGoalTemplateID }} </label>
                            <!-- Disable template input if no templates exist -->
                            <input v-if="updatedTemplate==(currGoalTemplateID) && (goalTemplateIDs.length!==0 || this.currGoalTemplateID==='Enter Your Template Title Here')" v-model="newTemplateID" @keyup.enter="updateTemplate(currGoalTemplateID);">
                        </h1>
                    <h5>Overall Goal Progress</h5>
                    <prog v-if="goalTemplateIDs.length===0" :value="0"></prog>
                    <prog v-else :value="numCompleted/goals.length"></prog>
                    <!-- Disable "add goal" button if template is untitled -->
                    <b-button v-if="this.currGoalTemplateID==='Enter Your Template Title Here' || goalTemplateIDs.length===0" type="b-button" class="btn btn-success btn-med" v-b-modal.goal-modal disabled>Add Goal</b-button>
                    <b-button v-else type="b-button" class="btn btn-success btn-med" v-b-modal.goal-modal>Add Goal</b-button>
                    <br><br>
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th scope="col">Goal #</th>
                                <th scope="col">Goal</th>
                                <th>3</th>
                                <th>4</th>
                                <th>5</th>
                                <th scope="col" class="text-right">Actions</th>
                            </tr>
                        </thead>
                        <draggable v-model="list" :element="'tbody'">
                            <tr v-for="(goal, index) in goals" :key="index">
                                <!-- Every cell has a bg color if goal.completed=True or goal.inProgress=True. No bg color if False -->
                                <!-- Goal Number/ Col 1 -->
                                <!-- completed color with goal # -->
                                <td v-if="goal.completed && !goal.isSubgoal" v-bind:style="{backgroundColor: '#28a745c4'}">
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <!-- just completed color -->
                                <td v-else-if="goal.completed && goal.isSubgoal" v-bind:style="{backgroundColor: '#28a745c4'}">
                                </td>
                                <!-- progress color with # -->
                                <td v-else-if="goal.inProgress && !goal.isSubgoal" v-bind:style="{backgroundColor: '#e0a800'}">
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <!-- just progress color-->
                                <td v-else-if="goal.inProgress && goal.isSubgoal" v-bind:style="{backgroundColor: '#e0a800'}">
                                </td>
                                <!-- if subgoal, empty cell 1-->
                                <td v-else-if="goal.isSubgoal">
                                </td>
                                <!-- default: goal #-->
                                <td v-else>
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <!-- Goal title/ Col 2 -->
                                <!-- completed color with title -->
                                <td v-if="goal.completed && !goal.isSubgoal" v-bind:style="{backgroundColor: '#28a745c4'}" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <!-- completed color with # -->
                                <td v-else-if="goal.completed && goal.nestLevel==1" v-bind:style="{backgroundColor: '#28a745c4'}">
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <!-- just completed color -->
                                <td v-else-if="goal.completed && goal.nestLevel != 1" v-bind:style="{backgroundColor: '#28a745c4'}">
                                </td>
                                <!-- progress color w title -->
                                <td v-else-if="goal.inProgress && !goal.isSubgoal" v-bind:style="{backgroundColor: '#e0a800'}" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <!-- progress color w # -->
                                <td v-else-if="goal.inProgress && goal.nestLevel==1" v-bind:style="{backgroundColor: '#e0a800'}">
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <!-- progress color -->
                                <td v-else-if="goal.inProgress && goal.nestLevel != 1" v-bind:style="{backgroundColor: '#e0a800'}">
                                </td>
                                <!-- subgoal -->
                                <td v-else-if="goal.isSubgoal && goal.nestLevel == 1">
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <td v-else-if="goal.isSubgoal && nestLevel != 1">
                                </td>
                                <!-- default title -->
                                <td v-else @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <!-- Added Col 3-->
                                <td v-if="goal.completed && !goal.isSubgoal" v-bind:style="{backgroundColor: '#28a745c4'}">
                                </td>
                                <td v-else-if="goal.completed && goal.nestLevel == 1" v-bind:style="{backgroundColor: '#28a745c4'}" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <td v-else-if="goal.completed && goal.nestLevel == 2" v-bind:style="{backgroundColor: '#28a745c4'}">
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <td v-else-if="goal.completed && goal.nestLevel == 3" v-bind:style="{backgroundColor: '#28a745c4'}">
                                </td>
                                <td v-else-if="goal.inProgress && goal.nestLevel == 2" v-bind:style="{backgroundColor: '#e0a800'}">
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <!-- TODO: POSSIBLE BUG HERE WITH GOAL TITLE DISPLAY -->
                                <td v-else-if="goal.inProgress && goal.nestLevel == 1" v-bind:style="{backgroundColor: '#e0a800'}" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <td v-else-if="goal.inProgress && goal.nestLevel != 1 && goal.nestLevel != 2" v-bind:style="{backgroundColor: '#e0a800'}"></td>
                                <td v-else-if="goal.nestLevel == 1 && goal.isSubgoal" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <td v-else-if="goal.nestLevel == 2 && goal.isSubgoal">
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <td v-else></td>
                                <!-- Added Col 4-->
                                <td v-if="goal.completed && goal.nestLevel != 3 && goal.nestLevel != 2" v-bind:style="{backgroundColor: '#28a745c4'}">
                                </td>
                                <td v-else-if="goal.completed && goal.nestLevel == 3" v-bind:style="{backgroundColor: '#28a745c4'}">
                                    <label> {{ goal.goalNum }} </label>
                                </td>
                                <td v-else-if="goal.completed && goal.nestLevel == 2" v-bind:style="{backgroundColor: '#28a745c4'}" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                <td v-else-if="goal.inProgress && goal.nestLevel != 2 && goal.nestLevel != 3" v-bind:style="{backgroundColor: '#e0a800'}">
                                </td>
                                <td v-else-if="goal.inProgress && goal.nestLevel == 2" v-bind:style="{backgroundColor: '#e0a800'}" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <td v-else-if="goal.inProgress && goal.nestLevel==3" v-bind:style="{backgroundColor: '#e0a800'}">
                                    <label> {{ goal.goalNum }} </label>>
                                <td v-else-if="goal.isSubgoal && goal.nestLevel == 2" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <td v-else-if="goal.isSubgoal && goal.nestLevel == 3">
                                    <label> {{ goal.goalNum }} </label>>
                                </td>
                                </td>
                                <td v-else></td>
                                <!-- Added Col 5-->
                                <td v-if="goal.completed && !goal.isSubgoal" v-bind:style="{backgroundColor: '#28a745c4'}">
                                </td>
                                <td v-else-if="goal.completed && goal.nestLevel != 3" v-bind:style="{backgroundColor: '#28a745c4'}">
                                </td>
                                <td v-else-if="goal.completed && goal.nestLevel == 3" v-bind:style="{backgroundColor: '#28a745c4'}" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <td v-else-if="goal.inProgress && goal.nestLevel == 3" v-bind:style="{backgroundColor: '#e0a800'}">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <td v-else-if="goal.inProgress && !goal.isSubgoal" v-bind:style="{backgroundColor: '#e0a800'}">
                                </td>
                                <td v-else-if="goal.inProgress && goal.nestLevel != 3" v-bind:style="{backgroundColor: '#e0a800'}">
                                </td>
                                <td v-else-if="goal.isSubgoal && goal.nestLevel==3" @dblclick="updatedGoalTitle=(goal); newGoalTitle=goal.goalTitle">
                                    <label v-b-tooltip.hover title="Double-click to edit" v-show="updatedGoalTitle!=(goal)"> {{ goal.goalTitle }} </label>
                                    <input v-if="updatedGoalTitle==(goal)" v-model="newGoalTitle" @keyup.enter="updateGoalTitle(goal);">
                                </td>
                                <td v-else></td>
                                <!-- Buttons/ Col 6 -->
                                <td v-if=goal.completed v-bind:style="{backgroundColor: '#28a745c4'}">
                                    <div class="btn-toolbar float-right" role="toolbar">
                                        <v-hover>
                                            <div slot-scope="{hover}" class="btn-group mr-2" role="group">
                                                <b-button type="b-button" class="btn btn-secondary btn-sm" v-b-tooltip.hover title="Not Complete" @click="onCompleteGoal(goal)">
                                                    <v-icon>undo</v-icon>
                                                </b-button>
                                            </div>
                                        </v-hover>
                                        <v-hover>
                                            <div slot-scope="{hover}" class="btn-group" role="group">
                                                <b-button type="b-button" class="btn btn-danger btn-sm" v-b-tooltip.hover title="Delete" @click="onDeleteGoal(goal)">
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
                                                <b-button type="b-button" class="btn btn-secondary btn-sm" v-b-tooltip.hover title="Not In Progress" @click="onInProgGoal(goal)">
                                                    <v-icon>undo</v-icon>
                                                </b-button>
                                            </div>
                                        </v-hover>
                                        <v-hover>
                                            <div slot-scope="{hover}" class="btn-group mr-2" role="group">
                                                <b-button type="b-button" class="btn btn-danger btn-sm" v-b-tooltip.hover title="Delete" @click="onDeleteGoal(goal)">
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
                                                <b-button type="b-button" class="btn btn-success btn-sm" v-b-tooltip.hover title="Complete" @click="onCompleteGoal(goal)">
                                                    <v-icon>done</v-icon>
                                                </b-button>
                                            </div>
                                        </v-hover>
                                        <v-hover>
                                            <div slot-scope="{hover}" class="btn-group mr-2" role="group">
                                                <b-button type="b-button" class="btn btn-warning btn-sm" v-b-tooltip.hover title="In Progress" @click="onInProgGoal(goal)">
                                                    <v-icon>schedule</v-icon>
                                                </b-button>
                                            </div>
                                        </v-hover>
                                        <!-- mr-2 for spacing -->
                                        <v-hover>
                                            <div slot-scope="{hover}" class="btn-group mr-2" role="group">
                                                <b-button type="b-button" v-b-tooltip.hover title="Delete" class="btn btn-danger btn-sm" @click="onDeleteGoal(goal)">
                                                    <v-icon>delete_forever</v-icon>
                                                </b-button>
                                            </div>
                                        </v-hover>
                                        <!-- added subgoal form -->
                                        <v-hover>
                                            <div slot-scope="{hover}" class="btn-group mr-2" role="group">
                                                <b-button type="b-button" variant="primary" size="sm" v-b-tooltip.hover title="Add Subgoal" v-b-modal.subgoal-modal>
                                                    <v-icon>add</v-icon>
                                                </b-button>
                                                </b-button>
                                            </div>
                                        </v-hover>
                                    </div>
                                </td>
                                <br>
                            </tr>
                        </draggable>
                    </table>
                </div>
            </div>
        </div>
        <!-- Pop-up modals -->
        <b-modal ref="addGoalModal" id="goal-modal" title="Add a new goal" hide-footer>
            <b-form @submit="onSubmit" @reset="onReset" class="w-100">
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
        <b-modal ref="addSubGoalModal" id="subgoal-modal" title="Add a new subgoal" hide-footer>
            <b-form @submit="onSubmitSubgoal" @reset="onReset" class="w-100">
                <b-form-group label="Goal Number:" label-for="form-goalNumber-input">
                    <b-form-input id="form-goalNumber-input" type="number" v-model.number="addSubgoalForm.goalNum" required placeholder="Enter goal number">
                    </b-form-input>
                </b-form-group>
                <b-form-group label="Level of Nesting:" label-for="form-goalNumber-input">
                    <b-form-input id="form-goalNumber-input" type="number" v-model.number="addSubgoalForm.nestLevel" required placeholder="Enter nesting level" :min=1 :max=3 value=1>
                    </b-form-input>
                </b-form-group>
                <b-form-group label="Subgoal Title:" label-for="form-goalTitle-input">
                    <b-form-input id="form-goalTitle-input" type="text" v-model="addSubgoalForm.goalTitle" required placeholder="Enter subgoal title">
                    </b-form-input>
                </b-form-group>
                <b-form-checkbox class="mb-3" label="Completed?" v-model="addSubgoalForm.completed">
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
            netID: null,
            goalTemplateIDs: [],
            currGoalTemplateID: null, // Default template ID
            goals: [],
            addGoalForm: {
                goalNum: 0,
                goalTitle: '',
                completed: false,
            },
            addSubgoalForm: {
                nestLevel: 0,
                goalTitle: '',
                completed: false,
                goalNum: 0,
            },
            message: null,
            showMessage: false,
            numCompleted: 0,
            clientURI: process.env.URI_CLIENT_ROOT,
            // Double click to edit boolean and new entry fields
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
        async getLoginNetID() {
            const path = process.env.URI_SERVER_ROOT + '/loginNetID';
            await axios.get(path)
                .then((res) => {
                    this.netID = res.data.netID;
                })
                .catch((error) => {
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
        update(goalTemplateID) {
            const path = process.env.URI_SERVER_ROOT + '/completedGoals/' + goalTemplateID;
            axios.get(path)
                .then((res) => {
                    this.numCompleted = res.data.numCompleted;
                })
                .catch((error) => {
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
                    console.log(error);
                });
        },
        addTemplate() {
            const path = process.env.URI_SERVER_ROOT + '/modTemplates/' + 'Enter Your Template Title Here';
            axios.post(path)
                .then(() => {
                    this.getGoals('Enter Your Template Title Here');
                    this.currGoalTemplateID = 'Enter Your Template Title Here';
                    this.numCompleted = 0;
                    this.message = 'Template created. Please title your template.';
                    this.showMessage = true;
                })
                .catch((error) => {
                    console.log(error);
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
                    console.log(error);
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
                    console.log(error);
                });
        },
        deleteTemplate() {
            const path = process.env.URI_SERVER_ROOT + '/modTemplates/' + this.currGoalTemplateID;
            axios.delete(path)
                .then(async () => {
                    // Wait to get the new template list before setting fields
                    await this.getTemplates();

                    // Display template at top of list, if no templates, show blank screen
                    if (this.goalTemplateIDs.length === 0) {
                        this.goals = [];
                        this.currGoalTemplateID = null;
                    } else {
                        this.getGoals(this.goalTemplateIDs[0]);
                        this.getNumCompleted(this.goalTemplateIDs[0]);
                        this.currGoalTemplateID = this.goalTemplateIDs[0];
                    }
                    this.message = 'Template deleted!';
                    this.showMessage = true;
                })
                .catch((error) => {
                    console.log(error);
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
                    console.log(error);
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
                    console.log(error);
                });
        },
        updateTemplate(goalTemplateID) {
            // Strip spaces from ends of changed template name
            this.newTemplateID = this.newTemplateID.trim();

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
                    console.log(error);
                });
        },
        initForm() {
            this.addGoalForm.goalNum = 0;
            this.addGoalForm.goalTitle = '';
            this.addGoalForm.completed = false;
        },
        initSubgoalForm() {
            this.addSubgoalForm.goalNum = 0;
            this.addSubgoalForm.goalTitle = '';
            this.addSubgoalForm.completed = false;
            this.addSubgoalForm.isSubgoal = true;
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
                goalID: '',
                goalNum: this.addGoalForm.goalNum,
                goalTitle: this.addGoalForm.goalTitle,
                completed: this.addGoalForm.completed,
                isSubgoal: false,
                nestLevel: 0,
                parentID: '',
            };
            this.addGoal(payload, this.currGoalTemplateID);
            this.initForm();
        },
        onSubmitSubgoal(evt) {
            evt.preventDefault();
            this.$refs.addSubGoalModal.hide();
            const payload = {
                goalID: '',
                goalNum: this.addSubgoalForm.goalNum,
                goalTitle: this.addSubgoalForm.goalTitle,
                completed: this.addSubgoalForm.completed,
                isSubgoal: true,
                nestLevel: this.addSubgoalForm.nestLevel,
                parentID: '',
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
        await this.getLoginNetID();
        await this.getTemplates();
        // Update current goal template if user reloads page
        this.currGoalTemplateID = this.goalTemplateIDs[0];
        this.getGoals(this.currGoalTemplateID);
        this.getNumCompleted(this.currGoalTemplateID);
    },
};
</script>