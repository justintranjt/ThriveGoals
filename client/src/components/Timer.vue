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
            state: "paused",
            startTime: Date.now(),
            currentTime: Date.now(),
            interval: null,
            netTimeDiff: 0,
            pauseTime: Date.now() ,
        }
    },

    props: {
        loaded: Number,
    },

    mounted: function() {
        this.interval = setInterval(this.updateCurrentTime, 1000);
    },
    destroyed: function() {
        clearInterval(this.interval)
    },
    computed: {
        time: function() {
            return this.hours + ':' + this.minutes + ':' + this.seconds;
        },
        milliseconds: function() {
            if (this.loaded == null) {
                this.loaded = 0;
            }
            return this.loaded + (this.currentTime - this.startTime) - this.netTimeDiff;
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
            this.loaded = 0;
        },
        pause: function() {
            this.state = "paused";
            this.pauseTime = Date.now();
        },
        resume: function() {
            
            if(this.state== "paused"){
                this.netTimeDiff = this.netTimeDiff + (Date.now() - this.pauseTime);
                this.currentTime = Date.now()
            }
            this.state = "started";
            this.currentTime = Date.now() 
        },
        updateCurrentTime: function() {
            if (this.state == "started") {
                this.currentTime = Date.now();
            }
        },
    },
};
</script>