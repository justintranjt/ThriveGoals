webpackJsonp([1],{"1/oy":function(t,e){},"Ffg/":function(t,e,a){"use strict";var o={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("span",{attrs:{id:"time"},domProps:{innerHTML:t._s(t.time)}}),t._v(" "),a("br"),t._v(" "),a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-success btn-sm",attrs:{type:"b-button",title:"Play"},on:{click:t.resume}},[a("v-icon",{attrs:{small:""}},[t._v("play_circle_filled")])],1),t._v(" "),a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-warning btn-sm",attrs:{type:"b-button",title:"Pause"},on:{click:t.pause}},[a("v-icon",{attrs:{small:""}},[t._v("pause_circle_outline")])],1),t._v(" "),a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-sm",attrs:{type:"b-button",title:"Reset"},on:{click:t.reset}},[a("v-icon",{attrs:{small:""}},[t._v("replay")])],1)],1)},staticRenderFns:[]};e.a=o},GfHa:function(t,e){},"Gp+1":function(t,e){t.exports={data:function(){return{state:"paused",startTime:1e5,currentTime:1e5,interval:null,pauseTime:1e5,internalCounter:1e5}},props:["loaded","index"],mounted:function(){this.interval=setInterval(this.updateCurrentTime,1e3)},destroyed:function(){clearInterval(this.interval)},computed:{time:function(){return this.hours+":"+this.minutes+":"+this.seconds},milliseconds:function(){return this.currentTime==this.startTime?(this.currentTime=this.currentTime+this.loaded,this.currentTime-this.startTime):this.currentTime-this.startTime},hours:function(){var t=this.milliseconds,e=Math.floor(t/1e3/60/60);return e>=10?e:"0"+e},minutes:function(){var t=this.milliseconds,e=Math.floor(t/1e3/60%60);return e>=10?e:"0"+e},seconds:function(){var t=this.milliseconds,e=Math.ceil(t/1e3%60);return e>=10?e:"0"+e}},methods:{reset:function(){this.state="paused",this.startTime=1e5,this.currentTime=1e5,this.interval=null,this.pauseTime=1e5,this.loaded=0,this.internalCounter=1e5,this.$parent.getTime(this.index)},pause:function(){this.state="paused",this.pauseTime=this.internalCounter,this.$parent.getTime(this.index)},resume:function(){this.currentTime==this.startTime&&(this.curentTime=this.internalCounter+this.loaded),this.state="started"},updateCurrentTime:function(){"started"==this.state&&(this.currentTime=this.currentTime+1e3),this.internalCounter=this.internalCounter+1e3}}}},Id91:function(t,e){},Jmt5:function(t,e){},NHnr:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});a("Jmt5"),a("gJtD");var o=a("e6fC"),l=a("7+uW"),i=a("3EgV"),s=a.n(i),r={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"app"}},[e("router-view")],1)},staticRenderFns:[]};var n=a("VU/8")({name:"App"},r,!1,function(t){a("WBfT")},null,null).exports,d=a("/ocq"),c={data:()=>({clientURI:"https://thrive-goals.herokuapp.com"})},u={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{attrs:{fluid:"",id:"aboutUsContainer"}},[a("b-navbar",{attrs:{toggleable:"",fixed:"top",variant:"light",type:"light"}},[a("b-navbar-toggle",{attrs:{target:"nav_text_collapse"}}),t._v(" "),a("b-collapse",{attrs:{"is-nav":"",id:"nav_collapse"}},[a("b-navbar-brand",[t._v("Thrive")]),t._v(" "),a("b-navbar-nav",{staticClass:"ml-auto"},[a("b-nav-item",{attrs:{href:t.clientURI}},[t._v("Home")])],1)],1)],1),t._v(" "),a("b-container",{staticClass:"mt-4 pt-5 pb-2 text-center",attrs:{id:"bv-r2c2"}},[a("h1",{attrs:{id:"aboutUsText"}},[t._v("About Thrive")]),t._v(" "),a("p",{attrs:{id:"aboutUsText"}},[t._v("Thrive is a COS 333 project advised by Mohamed El-Dirany and Robert Dondero. The creation of Thrive was motivated by assisting first generation college students in the Office of Access and Inclusion’s FSI Summer program. Our system provides users with modifiable templates created by learning specialists and other students to help them structure their work processes for major assignments like papers and coding projects.")])]),t._v(" "),a("b-container",{staticClass:"mt-4 text-center",attrs:{id:"bv-r2c2"}},[a("h1",{attrs:{id:"aboutUsText"}},[t._v("Team")]),t._v(" "),a("b-card-group",{attrs:{deck:""}},[a("b-card",{staticClass:"border-0",attrs:{"img-src":"/static/JGardner.jpg","img-top":""}},[a("h5",{staticClass:"card-title"},[t._v("Josh Gardner")]),t._v(" "),a("p",{staticClass:"card-text"},[t._v("\n                    COS '20\n                ")]),t._v(" "),a("a",{staticClass:"card-link",attrs:{href:"https://www.linkedin.com/in/josh-gardner-957903134/"}},[t._v("LinkedIn")])]),t._v(" "),a("b-card",{staticClass:"border-0",attrs:{"img-src":"/static/blank.png","img-top":""}},[a("h5",{staticClass:"card-title"},[t._v("Sonia Joseph")]),t._v(" "),a("p",{staticClass:"card-text"},[t._v("\n                    NEU '19\n                ")])]),t._v(" "),a("b-card",{staticClass:"border-0",attrs:{"img-src":"/static/HMahmood.jpg","img-top":""}},[a("h5",{staticClass:"card-title"},[t._v("Hamza Mahmood")]),t._v(" "),a("p",{staticClass:"card-text"},[t._v("\n                    COS '20\n                ")])]),t._v(" "),a("b-card",{staticClass:"border-0",attrs:{"img-src":"/static/JTran.jpg","img-top":""}},[a("h5",{staticClass:"card-title"},[t._v("Justin Tran")]),t._v(" "),a("p",{staticClass:"card-text"},[t._v("\n                    COS '20\n                ")]),t._v(" "),a("a",{staticClass:"card-link",attrs:{href:"https://github.com/justintranjt"}},[t._v("GitHub")]),t._v(" "),a("a",{staticClass:"card-link",attrs:{href:"https://justintranjt.me/"}},[t._v("Website")])]),t._v(" "),a("b-card",{staticClass:"border-0",attrs:{"img-src":"/static/ZVlatinova.png","img-top":""}},[a("h5",{staticClass:"card-title"},[t._v("Viktoria Zlatinova")]),t._v(" "),a("p",{staticClass:"card-text"},[t._v("\n                    COS '19\n                ")])])],1)],1)],1)},staticRenderFns:[]},m=a("VU/8")(c,u,!1,null,null,null).exports,p=a("mtWM"),v=a.n(p),h={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",["Duplicate template names not allowed."==t.message?a("b-alert",{attrs:{dismissible:"",variant:"danger",show:""}},[t._v(t._s(t.message))]):a("b-alert",{attrs:{dismissible:"",variant:"success",show:""}},[t._v(t._s(t.message))]),t._v(" "),a("br")],1)},staticRenderFns:[]},g={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",[e("b-progress",{staticClass:"mb-3",attrs:{value:this.value,max:1,precision:2,"show-progress":"",variant:"success"}})],1)},staticRenderFns:[]},b={data:()=>({netID:null,goalTemplateIDs:[],currGoalTemplateID:null,currGoalClicked:null,currGoalClickedNum:0,goals:[],addGoalForm:{goalNum:0,goalTitle:"",completed:!1},addSubgoalForm:{nestLevel:0,goalTitle:"",completed:!1,goalNum:0},message:null,showMessage:!1,numCompleted:0,clientURI:"https://thrive-goals.herokuapp.com",updatedGoalTitle:null,updatedGoalTime:0,updatedTemplate:null,newGoalTitle:null,newTemplateID:null,startTime:Date.now(),currentTime:Date.now()}),components:{alert:a("VU/8")({props:["message"]},h,!1,null,null,null).exports,prog:a("VU/8")({props:["value"]},g,!1,null,null,null).exports,timer:a("ZqlF").default},methods:{async getLoginNetID(){v.a.defaults.withCredentials=!0;await v.a.get("https://thrive-goals.herokuapp.com/loginNetID",{withCredentials:!0,credentials:"same-origin"}).then(t=>{this.netID=t.data.netID}).catch(t=>{console.error(t)})},getGoals(t){v.a.defaults.withCredentials=!0;const e="https://thrive-goals.herokuapp.com/modGoals/"+t;v.a.get(e,{withCredentials:!0,credentials:"same-origin"}).then(t=>{this.goals=t.data.goals}).catch(t=>{console.error(t)})},getNumCompleted(t){v.a.defaults.withCredentials=!0;const e="https://thrive-goals.herokuapp.com/completedGoals/"+t;v.a.get(e,{withCredentials:!0,credentials:"same-origin"}).then(t=>{this.numCompleted=t.data.numCompleted}).catch(t=>{console.error(t)})},async getTemplates(){v.a.defaults.withCredentials=!0;await v.a.get("https://thrive-goals.herokuapp.com/getTemplates",{withCredentials:!0,credentials:"same-origin"}).then(t=>{this.goalTemplateIDs=t.data.goalTemplateIDs}).catch(t=>{console.error(t)})},update(t){v.a.defaults.withCredentials=!0;const e="https://thrive-goals.herokuapp.com/completedGoals/"+t;v.a.get(e,{withCredentials:!0,credentials:"same-origin"}).then(t=>{this.numCompleted=t.data.numCompleted}).catch(t=>{console.error(t)})},addGoal(t,e){v.a.defaults.withCredentials=!0;const a="https://thrive-goals.herokuapp.com/modGoals/"+e;v.a.post(a,t,{withCredentials:!0,credentials:"same-origin"}).then(()=>{this.getGoals(e),this.getNumCompleted(e),this.message="Goal added!",this.showMessage=!0}).catch(t=>{console.log(t)})},addTemplate(){v.a.defaults.withCredentials=!0;v.a.post("https://thrive-goals.herokuapp.com/modTemplates/Enter Your Template Title Here",{withCredentials:!0,credentials:"same-origin"}).then(()=>{this.getGoals("Enter Your Template Title Here"),this.currGoalTemplateID="Enter Your Template Title Here",this.numCompleted=0,this.message="Template created. Please title your template.",this.showMessage=!0}).catch(t=>{console.log(t)})},completeGoal(t,e){v.a.defaults.withCredentials=!0;const a="https://thrive-goals.herokuapp.com/completeGoal/"+t+"/"+e;v.a.put(a,{withCredentials:!0,credentials:"same-origin"}).then(t=>{this.getGoals(e),this.getNumCompleted(e),this.message=t.data.message,this.showMessage=!0}).catch(t=>{console.log(t)})},deleteGoal(t,e,a){v.a.defaults.withCredentials=!0;const o="https://thrive-goals.herokuapp.com/modGoals/"+t+"/"+e+"/"+a;v.a.delete(o,{withCredentials:!0,credentials:"same-origin"}).then(()=>{this.getGoals(e),this.getNumCompleted(e),this.message="Goal deleted!",this.showMessage=!0}).catch(t=>{console.log(t)})},deleteTemplate(){v.a.defaults.withCredentials=!0;const t="https://thrive-goals.herokuapp.com/modTemplates/"+this.currGoalTemplateID;v.a.delete(t,{withCredentials:!0,credentials:"same-origin"}).then(async()=>{await this.getTemplates(),0===this.goalTemplateIDs.length?(this.goals=[],this.currGoalTemplateID=null):(this.getGoals(this.goalTemplateIDs[0]),this.getNumCompleted(this.goalTemplateIDs[0]),this.currGoalTemplateID=this.goalTemplateIDs[0]),this.message="Template deleted!",this.showMessage=!0}).catch(t=>{console.log(t)})},inProgGoal(t,e){v.a.defaults.withCredentials=!0;const a="https://thrive-goals.herokuapp.com/inProgGoal/"+t+"/"+e;v.a.put(a,{withCredentials:!0,credentials:"same-origin"}).then(t=>{this.getGoals(e),this.getNumCompleted(e),this.message=t.data.message,this.showMessage=!0}).catch(t=>{console.log(t)})},swapGoal(t,e,a){v.a.defaults.withCredentials=!0;const o="https://thrive-goals.herokuapp.com/swapGoal/"+t+"/"+e+"/"+a;v.a.put(o,{withCredentials:!0,credentials:"same-origin"}).then(t=>{this.getGoals(a)}).catch(t=>{console.log(t)})},updateGoalTitle(t){v.a.defaults.withCredentials=!0,this.updatedGoalTitle="";const e={goalNum:t.goalNum,goalTitle:this.newGoalTitle,completed:t.completed,inProgress:t.inProgress,goalID:t.goalID},a="https://thrive-goals.herokuapp.com/modGoals/"+t.goalNum+"/"+this.currGoalTemplateID+"/"+t.goalID;v.a.put(a,e,{withCredentials:!0,credentials:"same-origin"}).then(()=>{this.getGoals(this.currGoalTemplateID),this.getNumCompleted(this.currGoalTemplateID),this.message="Goal updated!",this.showMessage=!0}).catch(t=>{console.log(t)})},updateGoalTime(t,e){v.a.defaults.withCredentials=!0,this.updatedGoalTime=0;const a={goalNum:t.goalNum,goalTitle:t.goalTitle,completed:t.completed,inProgress:t.inProgress,goalID:t.goalID},o="https://thrive-goals.herokuapp.com/updateTimer/"+this.currGoalTemplateID+"/"+t.goalID+"/"+e;v.a.put(o,a,{withCredentials:!0,credentials:"same-origin"}).then(()=>{this.getGoals(this.currGoalTemplateID),this.getNumCompleted(this.currGoalTemplateID)}).catch(t=>{console.log(t)})},updateTemplate(t){if(v.a.defaults.withCredentials=!0,this.newTemplateID=this.newTemplateID.trim(),this.goalTemplateIDs.includes(this.newTemplateID))return this.message="Duplicate template names not allowed.",void(this.showMessage=!0);const e={newTemplateID:this.newTemplateID};this.updatedTemplate="";const a="https://thrive-goals.herokuapp.com/modTemplates/"+this.currGoalTemplateID;v.a.put(a,e,{withCredentials:!0,credentials:"same-origin"}).then(()=>{this.getTemplates(),this.currGoalTemplateID=this.newTemplateID,this.getGoals(this.newTemplateID),this.getNumCompleted(this.newTemplateID),this.message="Template updated!",this.showMessage=!0}).catch(t=>{console.log(t)})},dialog(){Vue.dialog.confirm("Please confirm to continue")},initForm(){this.addGoalForm.goalNum=0,this.addGoalForm.goalTitle="",this.addGoalForm.completed=!1},initSubgoalForm(){this.addSubgoalForm.goalTitle="",this.addSubgoalForm.completed=0},onCompleteGoal(t){this.completeGoal(t.goalID,this.currGoalTemplateID)},onDeleteGoal(t){this.deleteGoal(t.goalNum,this.currGoalTemplateID,t.goalID)},onSwapGoal(t,e){this.swapGoal(t.goalID,e.goalID,this.currGoalTemplateID)},onInProgGoal(t){this.inProgGoal(t.goalID,this.currGoalTemplateID)},onSubmit(t){t.preventDefault(),this.$refs.addGoalModal.hide();const e={goalID:"",goalNum:0==this.goals.length?0:this.goals[this.goals.length-1].goalNum+1,goalTitle:this.addGoalForm.goalTitle,completed:this.addGoalForm.completed,isSubgoal:!1,nestLevel:0,parentID:""};this.addGoal(e,this.currGoalTemplateID),this.initForm()},setCurrGoalClicked(t){this.currGoalClicked=t.goalID,this.currGoalClickedNum=t.goalNum},onSubmitSubgoal(t){t.preventDefault(),this.$refs.addSubGoalModal.hide();for(var e=this.currGoalClicked,a=this.currGoalClickedNum,o=null,l=a;l>1;)l--;var i=(o=1==l?.1+Math.floor(a):l+.1+Math.floor(a))-10*Math.floor(a);const s={goalID:"",goalNum:o,goalTitle:this.addSubgoalForm.goalTitle,completed:this.addSubgoalForm.completed,isSubgoal:!0,nestLevel:i,parentID:e};this.addGoal(s,this.currGoalTemplateID),this.initSubgoalForm()},onReset(t){t.preventDefault(),this.initForm()},onSetTemplate(t){this.currGoalTemplateID=t,this.getGoals(t),this.getNumCompleted(t)},getTime(t){var e=this.goals[t],a=this.$refs.timercomponent[t].milliseconds;this.updateGoalTime(e,a)},getTimeAllGoals(){var t;for(t=0;t<this.goals.length;t++)this.getTime(t)},updateCurrentTime:function(){this.currentTime=Date.now(),this.currentTime-this.startTime>=3e3&&(this.startTime=this.currentTime,this.getTimeAllGoals())}},async created(){await this.getLoginNetID(),await this.getTemplates(),this.currGoalTemplateID=this.goalTemplateIDs[0],this.getGoals(this.currGoalTemplateID),this.getNumCompleted(this.currGoalTemplateID)}},T={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("b-navbar",{attrs:{toggleable:"",fixed:"top",variant:"light",type:"light"}},[a("b-navbar-toggle",{attrs:{target:"nav_collapse"}}),t._v(" "),a("b-collapse",{attrs:{"is-nav":"",id:"nav_collapse"}},[a("b-navbar-brand",[t._v("Thrive")]),t._v(" "),a("b-nav-text",[t._v("Logged in as "+t._s(t.netID))]),t._v(" "),a("b-navbar-nav",{staticClass:"ml-auto"},[a("b-nav-item",{attrs:{href:t.clientURI}},[t._v("Home")]),t._v(" "),a("b-nav-item",{attrs:{href:t.clientURI+"/AboutUs"}},[t._v("About Us")]),t._v(" "),a("b-nav-item",{on:{click:function(e){t.addTemplate()}}},[a("em",[t._v("Create Template")])]),t._v(" "),a("b-nav-item",{on:{click:function(e){t.deleteTemplate()}}},[a("em",[t._v("Delete Current Template")])]),t._v(" "),a("b-nav-item-dropdown",{attrs:{right:""}},[a("template",{slot:"button-content"},[a("em",[t._v("Templates")])]),t._v(" "),t._l(t.goalTemplateIDs,function(e,o){return a("b-dropdown-item",{key:o,on:{click:function(a){t.onSetTemplate(e)}}},[t._v("\n                        "+t._s(e)+"\n                    ")])})],2),t._v(" "),a("b-nav-item",{attrs:{href:"https://fed.princeton.edu/cas/logout"}},[t._v("Logout")])],1)],1)],1),t._v(" "),a("b-container",{attrs:{fluid:"",id:"goalsContainerBackground"}},[a("div",{staticClass:"container mt-4 pt-5 pb-2"},[a("div",{staticClass:"shadow-lg col-lg-12 bg-white",attrs:{id:"goalTable"}},[a("br"),t._v(" "),t.showMessage?a("alert",{attrs:{message:t.message}}):t._e(),t._v(" "),a("h1",{on:{touchstart:function(e){t.updatedTemplate=t.currGoalTemplateID,t.newTemplateID=t.currGoalTemplateID},dblclick:function(e){t.updatedTemplate=t.currGoalTemplateID,t.newTemplateID=t.currGoalTemplateID}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedTemplate!=t.currGoalTemplateID,expression:"updatedTemplate!=(currGoalTemplateID)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(t.currGoalTemplateID)+" ")]),t._v(" "),t.updatedTemplate!=t.currGoalTemplateID||0===t.goalTemplateIDs.length&&"Enter Your Template Title Here"!==this.currGoalTemplateID?t._e():a("input",{directives:[{name:"model",rawName:"v-model",value:t.newTemplateID,expression:"newTemplateID"}],domProps:{value:t.newTemplateID},on:{keyup:function(e){if(!("button"in e)&&t._k(e.keyCode,"enter",13,e.key,"Enter"))return null;t.updateTemplate(t.currGoalTemplateID)},input:function(e){e.target.composing||(t.newTemplateID=e.target.value)}}})]),t._v(" "),a("h5",[t._v("Overall Goal Progress")]),t._v(" "),0===t.goalTemplateIDs.length?a("prog",{attrs:{value:0}}):a("prog",{attrs:{value:t.numCompleted/t.goals.length}}),t._v(" "),"Enter Your Template Title Here"===this.currGoalTemplateID||0===t.goalTemplateIDs.length?a("b-button",{directives:[{name:"b-modal",rawName:"v-b-modal.goal-modal",modifiers:{"goal-modal":!0}}],staticClass:"btn btn-success btn-med",attrs:{type:"b-button",disabled:""}},[t._v("Add Goal")]):a("b-button",{directives:[{name:"b-modal",rawName:"v-b-modal.goal-modal",modifiers:{"goal-modal":!0}}],staticClass:"btn btn-success btn-med",attrs:{type:"b-button"}},[t._v("Add Goal")]),t._v(" "),a("br"),a("br"),t._v(" "),a("table",{staticClass:"table table-bordered table-hover"},[a("thead",[a("tr",{staticClass:"text-center"},[a("th",{attrs:{scope:"col"}},[t._v("Priority")]),t._v(" "),a("th",{attrs:{scope:"col"}},[t._v("Goal")]),t._v(" "),a("th",{attrs:{colspan:"2"}},[t._v("Subgoals")]),t._v(" "),a("th",{attrs:{scope:"col"}},[t._v("Time Spent")]),t._v(" "),a("th",{attrs:{scope:"col"}},[t._v("Actions")])])]),t._v(" "),t._l(t.goals,function(e,o){return a("tr",{key:o},[e.completed?a("td",{style:{backgroundColor:"#28a745c4"}},[a("div",{staticClass:"btn-toolbar justify-content-center"},[0!=o?a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"mr-1",attrs:{type:"b-button",title:"Move Up"},on:{click:function(a){t.onSwapGoal(e,t.goals[o-1])}}},[a("v-icon",{attrs:{small:""}},[t._v("keyboard_arrow_up")])],1):t._e(),t._v(" "),o!=t.goals.length-1?a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"mr-1",attrs:{type:"b-button",title:"Move Down"},on:{click:function(a){t.onSwapGoal(e,t.goals[o+1])}}},[a("v-icon",{attrs:{small:""}},[t._v("keyboard_arrow_down")])],1):t._e()],1)]):e.inProgress?a("td",{staticClass:"align-middle",style:{backgroundColor:"#e0a800"}},[a("div",{staticClass:"btn-toolbar justify-content-center"},[0!=o?a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"mr-1",attrs:{type:"b-button",title:"Move Up"},on:{click:function(a){t.onSwapGoal(e,t.goals[o-1])}}},[a("v-icon",{attrs:{small:""}},[t._v("keyboard_arrow_up")])],1):t._e(),t._v(" "),o!=t.goals.length-1?a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"mr-1",attrs:{type:"b-button",title:"Move Down"},on:{click:function(a){t.onSwapGoal(e,t.goals[o+1])}}},[a("v-icon",{attrs:{small:""}},[t._v("keyboard_arrow_down")])],1):t._e()],1)]):a("td",{staticClass:"align-middle"},[a("div",{staticClass:"btn-toolbar justify-content-center"},[0!=o?a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"mr-1",attrs:{type:"b-button",title:"Move Up"},on:{click:function(a){t.onSwapGoal(e,t.goals[o-1])}}},[a("v-icon",{attrs:{small:""}},[t._v("keyboard_arrow_up")])],1):t._e(),t._v(" "),o!=t.goals.length-1?a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"mr-1",attrs:{type:"b-button",title:"Move Down"},on:{click:function(a){t.onSwapGoal(e,t.goals[o+1])}}},[a("v-icon",{attrs:{small:""}},[t._v("keyboard_arrow_down")])],1):t._e()],1)]),t._v(" "),e.completed&&""==e.parentID?a("td",{style:{backgroundColor:"#28a745c4"},on:{touchstart:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle},dblclick:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedGoalTitle!=e,expression:"updatedGoalTitle!=(goal)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(e.goalTitle)+" ")]),t._v(" "),t.updatedGoalTitle==e?a("input",{directives:[{name:"model",rawName:"v-model",value:t.newGoalTitle,expression:"newGoalTitle"}],domProps:{value:t.newGoalTitle},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key,"Enter"))return null;t.updateGoalTitle(e)},input:function(e){e.target.composing||(t.newGoalTitle=e.target.value)}}}):t._e()]):e.completed?a("td",{style:{backgroundColor:"#28a745c4"}}):e.inProgress&&""==e.parentID?a("td",{style:{backgroundColor:"#e0a800"},on:{touchstart:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle},dblclick:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedGoalTitle!=e,expression:"updatedGoalTitle!=(goal)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(e.goalTitle)+" ")]),t._v(" "),t.updatedGoalTitle==e?a("input",{directives:[{name:"model",rawName:"v-model",value:t.newGoalTitle,expression:"newGoalTitle"}],domProps:{value:t.newGoalTitle},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key,"Enter"))return null;t.updateGoalTitle(e)},input:function(e){e.target.composing||(t.newGoalTitle=e.target.value)}}}):t._e()]):e.inProgress?a("td",{style:{backgroundColor:"#e0a800"}}):""!=e.parentID&&2!=t.nestLevel?a("td"):a("td",{on:{touchstart:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle},dblclick:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedGoalTitle!=e,expression:"updatedGoalTitle!=(goal)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(e.goalTitle)+" ")]),t._v(" "),t.updatedGoalTitle==e?a("input",{directives:[{name:"model",rawName:"v-model",value:t.newGoalTitle,expression:"newGoalTitle"}],domProps:{value:t.newGoalTitle},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key,"Enter"))return null;t.updateGoalTitle(e)},input:function(e){e.target.composing||(t.newGoalTitle=e.target.value)}}}):t._e()]),t._v(" "),e.completed&&""==e.parentID?a("td",{style:{backgroundColor:"#28a745c4"}}):e.completed&&2==e.nestLevel?a("td",{style:{backgroundColor:"#28a745c4"},on:{touchstart:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle},dblclick:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedGoalTitle!=e,expression:"updatedGoalTitle!=(goal)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(e.goalTitle)+" ")]),t._v(" "),t.updatedGoalTitle==e?a("input",{directives:[{name:"model",rawName:"v-model",value:t.newGoalTitle,expression:"newGoalTitle"}],domProps:{value:t.newGoalTitle},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key,"Enter"))return null;t.updateGoalTitle(e)},input:function(e){e.target.composing||(t.newGoalTitle=e.target.value)}}}):t._e()]):e.completed&&3==e.nestLevel?a("td",{style:{backgroundColor:"#28a745c4"}}):e.completed&&4==e.nestLevel?a("td",{style:{backgroundColor:"#28a745c4"}}):e.inProgress&&3==e.nestLevel?a("td",{style:{backgroundColor:"#e0a800"}}):e.inProgress&&2==e.nestLevel?a("td",{style:{backgroundColor:"#e0a800"},on:{touchstart:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle},dblclick:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedGoalTitle!=e,expression:"updatedGoalTitle!=(goal)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(e.goalTitle)+" ")]),t._v(" "),t.updatedGoalTitle==e?a("input",{directives:[{name:"model",rawName:"v-model",value:t.newGoalTitle,expression:"newGoalTitle"}],domProps:{value:t.newGoalTitle},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key,"Enter"))return null;t.updateGoalTitle(e)},input:function(e){e.target.composing||(t.newGoalTitle=e.target.value)}}}):t._e()]):e.inProgress&&2!=e.nestLevel&&3!=e.nestLevel?a("td",{style:{backgroundColor:"#e0a800"}}):2==e.nestLevel&&""!=e.parentID?a("td",{on:{touchstart:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle},dblclick:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedGoalTitle!=e,expression:"updatedGoalTitle!=(goal)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(e.goalTitle)+" ")]),t._v(" "),t.updatedGoalTitle==e?a("input",{directives:[{name:"model",rawName:"v-model",value:t.newGoalTitle,expression:"newGoalTitle"}],domProps:{value:t.newGoalTitle},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key,"Enter"))return null;t.updateGoalTitle(e)},input:function(e){e.target.composing||(t.newGoalTitle=e.target.value)}}}):t._e()]):(3==e.nestLevel&&e.parentID,a("td")),t._v(" "),e.completed&&4!=e.nestLevel&&3!=e.nestLevel?a("td",{style:{backgroundColor:"#28a745c4"}}):e.completed&&4==e.nestLevel?a("td",{style:{backgroundColor:"#28a745c4"}}):e.completed&&3==e.nestLevel?a("td",{style:{backgroundColor:"#28a745c4"},on:{touchstart:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle},dblclick:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedGoalTitle!=e,expression:"updatedGoalTitle!=(goal)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(e.goalTitle)+" ")]),t._v(" "),t.updatedGoalTitle==e?a("input",{directives:[{name:"model",rawName:"v-model",value:t.newGoalTitle,expression:"newGoalTitle"}],domProps:{value:t.newGoalTitle},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key,"Enter"))return null;t.updateGoalTitle(e)},input:function(e){e.target.composing||(t.newGoalTitle=e.target.value)}}}):t._e()]):e.inProgress&&3!=e.nestLevel&&4!=e.nestLevel?a("td",{style:{backgroundColor:"#e0a800"}}):e.inProgress&&3==e.nestLevel?a("td",{style:{backgroundColor:"#e0a800"},on:{touchstart:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle},dblclick:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedGoalTitle!=e,expression:"updatedGoalTitle!=(goal)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(e.goalTitle)+" ")]),t._v(" "),t.updatedGoalTitle==e?a("input",{directives:[{name:"model",rawName:"v-model",value:t.newGoalTitle,expression:"newGoalTitle"}],domProps:{value:t.newGoalTitle},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key,"Enter"))return null;t.updateGoalTitle(e)},input:function(e){e.target.composing||(t.newGoalTitle=e.target.value)}}}):t._e()]):e.inProgress&&4==e.nestLevel?a("td",{style:{backgroundColor:"#e0a800"}}):""!=e.parentID&&3==e.nestLevel?a("td",{on:{touchstart:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle},dblclick:function(a){t.updatedGoalTitle=e,t.newGoalTitle=e.goalTitle}}},[a("label",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"show",rawName:"v-show",value:t.updatedGoalTitle!=e,expression:"updatedGoalTitle!=(goal)"}],attrs:{title:"Double-click to edit"}},[t._v(" "+t._s(e.goalTitle)+" ")]),t._v(" "),t.updatedGoalTitle==e?a("input",{directives:[{name:"model",rawName:"v-model",value:t.newGoalTitle,expression:"newGoalTitle"}],domProps:{value:t.newGoalTitle},on:{keyup:function(a){if(!("button"in a)&&t._k(a.keyCode,"enter",13,a.key,"Enter"))return null;t.updateGoalTitle(e)},input:function(e){e.target.composing||(t.newGoalTitle=e.target.value)}}}):t._e()]):(""!=e.parentID&&e.nestLevel,a("td")),t._v(" "),e.completed?a("td",{style:{backgroundColor:"#28a745c4"}},[a("div",{staticClass:"text-center"},[a("timer",{ref:"timercomponent",refInFor:!0,attrs:{loaded:Number(e.goalTime),index:o}})],1)]):e.inProgress?a("td",{style:{backgroundColor:"#e0a800"}},[a("div",{staticClass:"text-center"},[a("timer",{ref:"timercomponent",refInFor:!0,attrs:{loaded:Number(e.goalTime),index:o}})],1)]):a("td",[a("div",{staticClass:"text-center"},[a("timer",{ref:"timercomponent",refInFor:!0,attrs:{loaded:Number(e.goalTime),index:o}})],1)]),t._v(" "),e.completed?a("td",{staticClass:"align-middle",style:{backgroundColor:"#28a745c4"}},[a("div",{staticClass:"btn-toolbar justify-content-center"},[a("v-hover",{scopedSlots:t._u([{key:"default",fn:function(o){return o.hover,a("div",{staticClass:"mr-1"},[a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-secondary btn-sm",attrs:{type:"b-button",title:"Not Complete"},on:{click:function(a){t.onCompleteGoal(e)}}},[a("v-icon",{attrs:{small:""}},[t._v("undo")])],1)],1)}}])}),t._v(" "),a("v-hover",{scopedSlots:t._u([{key:"default",fn:function(o){return o.hover,a("div",{},[a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-danger btn-sm",attrs:{type:"b-button",title:"Delete"},on:{click:function(a){t.onDeleteGoal(e)}}},[a("v-icon",{attrs:{small:""}},[t._v("delete_forever")])],1)],1)}}])})],1)]):e.inProgress?a("td",{staticClass:"align-middle",style:{backgroundColor:"#e0a800"}},[a("div",{staticClass:"btn-toolbar justify-content-center"},[a("v-hover",{scopedSlots:t._u([{key:"default",fn:function(o){return o.hover,a("div",{staticClass:"mr-1"},[a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-secondary btn-sm",attrs:{type:"b-button",title:"Not In Progress"},on:{click:function(a){t.onInProgGoal(e)}}},[a("v-icon",{attrs:{small:""}},[t._v("undo")])],1)],1)}}])}),t._v(" "),a("v-hover",{scopedSlots:t._u([{key:"default",fn:function(o){return o.hover,a("div",{staticClass:"mr-1"},[a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-danger btn-sm",attrs:{type:"b-button",title:"Delete"},on:{click:function(a){t.onDeleteGoal(e)}}},[a("v-icon",{attrs:{small:""}},[t._v("delete_forever")])],1)],1)}}])})],1)]):a("td",{staticClass:"align-middle"},[a("div",{staticClass:"btn-toolbar justify-content-center"},[a("v-hover",{scopedSlots:t._u([{key:"default",fn:function(o){return o.hover,a("div",{staticClass:"mr-1"},[a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-success btn-sm",attrs:{type:"b-button",title:"Complete"},on:{click:function(a){t.onCompleteGoal(e)}}},[a("v-icon",{attrs:{small:""}},[t._v("done")])],1)],1)}}])}),t._v(" "),a("v-hover",{scopedSlots:t._u([{key:"default",fn:function(o){return o.hover,a("div",{staticClass:"mr-1"},[a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-warning btn-sm",attrs:{type:"b-button",title:"In Progress"},on:{click:function(a){t.onInProgGoal(e)}}},[a("v-icon",{attrs:{small:""}},[t._v("schedule")])],1)],1)}}])}),t._v(" "),a("v-hover",{scopedSlots:t._u([{key:"default",fn:function(o){return o.hover,a("div",{staticClass:"mr-1"},[a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}}],staticClass:"btn btn-danger btn-sm",attrs:{type:"b-button",title:"Delete"},on:{click:function(a){t.onDeleteGoal(e)}}},[a("v-icon",{attrs:{small:""}},[t._v("delete_forever")])],1)],1)}}])}),t._v(" "),e.nestLevel<3?a("v-hover",{scopedSlots:t._u([{key:"default",fn:function(o){return o.hover,a("div",{staticClass:"mr-1"},[a("b-button",{directives:[{name:"b-tooltip",rawName:"v-b-tooltip.hover",modifiers:{hover:!0}},{name:"b-modal",rawName:"v-b-modal.subgoal-modal",modifiers:{"subgoal-modal":!0}}],attrs:{type:"b-button",variant:"primary",size:"sm",title:"Add Subgoal"},on:{click:function(a){t.setCurrGoalClicked(e)}}},[a("v-icon",{attrs:{small:""}},[t._v("add")])],1)],1)}}])}):t._e()],1)]),t._v(" "),a("br")])})],2)],1)])]),t._v(" "),a("b-modal",{ref:"addGoalModal",attrs:{id:"goal-modal",title:"Add a new goal","hide-footer":""}},[a("b-form",{staticClass:"w-100",on:{submit:t.onSubmit,reset:t.onReset}},[a("b-form-group",{attrs:{label:"Goal Title:","label-for":"form-goalTitle-input"}},[a("b-form-input",{attrs:{id:"form-goalTitle-input",type:"text",required:"",placeholder:"Enter goal title"},model:{value:t.addGoalForm.goalTitle,callback:function(e){t.$set(t.addGoalForm,"goalTitle",e)},expression:"addGoalForm.goalTitle"}})],1),t._v(" "),a("b-form-checkbox",{staticClass:"mb-3",attrs:{label:"Completed?"},model:{value:t.addGoalForm.completed,callback:function(e){t.$set(t.addGoalForm,"completed",e)},expression:"addGoalForm.completed"}},[t._v("\n                Completed?\n            ")]),t._v(" "),a("br"),t._v(" "),a("b-button",{attrs:{type:"submit",variant:"primary"}},[t._v("Submit")]),t._v(" "),a("b-button",{attrs:{type:"reset",variant:"danger"}},[t._v("Reset")])],1)],1),t._v(" "),a("b-modal",{ref:"addSubGoalModal",attrs:{id:"subgoal-modal",title:"Add a new subgoal","hide-footer":""}},[a("b-form",{staticClass:"w-100",on:{submit:t.onSubmitSubgoal,reset:t.onReset}},[a("b-form-group",{attrs:{label:"Subgoal Title:","label-for":"form-goalTitle-input"}},[a("b-form-input",{attrs:{id:"form-goalTitle-input",type:"text",required:"",placeholder:"Enter subgoal title"},model:{value:t.addSubgoalForm.goalTitle,callback:function(e){t.$set(t.addSubgoalForm,"goalTitle",e)},expression:"addSubgoalForm.goalTitle"}})],1),t._v(" "),a("b-form-checkbox",{staticClass:"mb-3",attrs:{label:"Completed?"},model:{value:t.addSubgoalForm.completed,callback:function(e){t.$set(t.addSubgoalForm,"completed",e)},expression:"addSubgoalForm.completed"}},[t._v("\n                Completed?\n            ")]),t._v(" "),a("br"),t._v(" "),a("b-button",{attrs:{type:"submit",variant:"primary"}},[t._v("Submit")]),t._v(" "),a("b-button",{attrs:{type:"reset",variant:"danger"}},[t._v("Reset")])],1)],1)],1)},staticRenderFns:[]},f=a("VU/8")(b,T,!1,null,null,null).exports,_={data:()=>({clientURI:"https://thrive-goals.herokuapp.com",serverURI:"https://thrive-goals.herokuapp.com"})},w={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("b-container",{attrs:{fluid:"",id:"splashContainer"}},[a("b-navbar",{attrs:{toggleable:"",fixed:"top",variant:"light",type:"light"}},[a("b-navbar-toggle",{attrs:{target:"nav_text_collapse"}}),t._v(" "),a("b-collapse",{attrs:{"is-nav":"",id:"nav_collapse"}},[a("b-navbar-brand",[t._v("Thrive")]),t._v(" "),a("b-navbar-nav",{staticClass:"ml-auto"},[a("b-nav-item",{attrs:{href:t.clientURI+"/AboutUs"}},[t._v("About Us")])],1)],1)],1),t._v(" "),a("b-row",{attrs:{id:"intro"}},[a("b-col",[a("h3",{attrs:{id:"hometitle"}},[t._v("THRIVE")]),t._v(" "),a("h2",{attrs:{id:"row1-1"}},[t._v("Set goals and track "),a("br"),t._v(" your progress every "),a("br"),t._v(" step of the way.")]),t._v(" "),a("b-form",{attrs:{id:"loginButton"}},[a("b-button",{attrs:{variant:"secondary lg",size:"lg",href:t.serverURI+"/loginPage"}},[t._v("Login via CAS")])],1)],1)],1),t._v(" "),a("b-row",{attrs:{id:"aboutText"}},[a("b-col",{attrs:{id:"bv-r2c2"}},[a("h1",[t._v("About Thrive")]),t._v(" "),t._v("\n            Our software helps you break down large projects into manageable subgoals in a goal hierarchy, reducing procrastination and making work more enjoyable and intrinsically motivating. Our modifiable templates are created by learning specialists and other students with the purpose of guiding you through major assignments.\n        ")])],1)],1)},staticRenderFns:[]},G=a("VU/8")(_,w,!1,null,null,null).exports,C={render:function(){var t=this.$createElement,e=this._self._c||t;return e("b-container",{staticClass:"mt-5 text-center text-white shadow-lg col-lg-12",attrs:{id:"notFoundContainer"}},[e("h1",[this._v("404")]),this._v(" "),e("h2",[this._v("Oops! Nothing was found")]),this._v(" "),e("p",[this._v("The page you are looking for might have been removed had its name changed or is temporarily unavailable.")])])},staticRenderFns:[]},k=a("VU/8")(null,C,!1,null,null,null).exports;l.default.use(d.a);var y=new d.a({routes:[{path:"/",name:"Splash",component:G},{path:"/AboutUs",name:"AboutUs",component:m},{path:"/goals",name:"Goals",component:f},{path:"/404",component:k},{path:"*",component:k}],mode:"history"});l.default.config.productionTip=!1,l.default.use(o.a),l.default.use(s.a,{iconfont:"mdi"}),l.default.directive("tooltip",function(t,e){$(t).tooltip({title:e.value,placement:e.arg,trigger:"hover"})}),new l.default({el:"#app",router:y,components:{App:n},template:"<App/>"})},WBfT:function(t,e){},ZqlF:function(t,e,a){"use strict";var o=a("Gp+1"),l=a.n(o),i=a("Ffg/"),s=a("VU/8")(l.a,i.a,!1,null,null,null);e.default=s.exports},gJtD:function(t,e){},zj2Q:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.c82512d3b023e4eb6dcd.js.map