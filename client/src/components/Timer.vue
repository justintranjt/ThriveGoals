<template>
    <div>
        <span id="time" v-html="time"></span>
        <br>
        <b-button type="b-button" class="btn btn-success btn-sm" v-b-tooltip.hover title="Play" @click="resume">
        <v-icon>play_circle_filled</v-icon> </b-button>

        <b-button type="b-button" class="btn btn-warning btn-sm" v-b-tooltip.hover title="Pause" @click="pause">
        <v-icon>pause_circle_outline</v-icon>
        </b-button>

        <b-button type="b-button" class="btn btn-sm" v-b-tooltip.hover title="Reset" @click="reset" >
        <v-icon>replay</v-icon>
        </b-button>
    </div>
</template>


<script>
module.exports = {
    data: function() {
        return {
            id: null,
            state: "paused",
            startTime: Date.now(),
            currentTime: Date.now(),
            interval: null,
            netTimeDiff: 0,
            pauseTime: Date.now() ,
        }
    },
    mounted: function() {
        this.id = this._uid;
        this.interval = setInterval(this.updateCurrentTime, 1000);
    },
    destroyed: function() {
        clearInterval(this.interval)
    },
    computed: {
        time: function() {
            time = this.hours + ':' + this.minutes + ':' + this.seconds;
            this.$emit('getTime', time);
            return time;
        },
        milliseconds: function() {
            console.log('current net diff in milliseconds: '+this.netTimeDiff);
            console.log('current - start in milliseconds: '+(this.currentTime - this.startTime));
            return (this.currentTime - this.startTime) - this.netTimeDiff;
        },
        hours: function() {
            var lapsed = this.milliseconds;
            var hrs = Math.floor((lapsed / 1000 / 60 / 60));
            return hrs >= 10 ? hrs : '0' + hrs;
        },
        minutes: function() {
            var lapsed = this.milliseconds;
            var min = Math.floor((lapsed / 1000 / 60) % 60);
            return min >= 10 ? min : '0' + min;
        },
        seconds: function() {
            var lapsed = this.milliseconds;
            var sec = Math.ceil((lapsed / 1000) % 60);
            return sec >= 10 ? sec : '0' + sec;
        }
    },
    methods: {
        reset: function() {
            this.state = "paused";
            this.startTime = Date.now();
            this.currentTime = Date.now();
            this.interval = null;
            this.netTimeDiff = 0; 
            this.pauseTime = Date.now();
            console.log('reset function called');
        },
        pause: function() {
            this.state = "paused";
            this.pauseTime = Date.now();
            console.log('pause function called');
        },
        resume: function() {
            console.log('resume function has been called');
            if(this.state== "paused"){
                console.log('apparently the prior state was pasued since we made it to the inside of the if');
                console.log('this.netTimeDiff prior to updating: '+this.netTimeDiff);
                console.log('(Date.now() - this.pauseTime): '+(Date.now() - this.pauseTime));
                this.netTimeDiff = this.netTimeDiff + (Date.now() - this.pauseTime);
                console.log('this.netTimeDiff prior to updating: '+this.netTimeDiff);
            }
            this.state = "started";
            console.log("Redfined STATE as", this.state);
            console.log('current value of pauseTime in resume: '+this.pauseTime);
            console.log('current net diff in resume:'+this.netTimeDiff);
            
        },
        updateCurrentTime: function() {
            if (this.state == "started") {
                this.currentTime = Date.now();
            }
        },
    },
};
</script>