<template>
    <div>
        <span id="time" v-html="time"></span>
    </div>
</template>

<script>
module.exports = {
    data: function() {
        return {
            state: "paused",
            startTime: 100000,
            currentTime: 100000,
            interval: null,
            pauseTime: 100000,
            internalCounter:100000,
            timerID: null,
            saveCounter: 0,
        }
    },
    props: {
        loaded: Number,
        index: Number,
        keyValue: String
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
            if(this.currentTime == this.startTime) {
                this.currentTime = this.currentTime + this.loaded;
                return (this.currentTime - this.startTime);
         }
         return (this.currentTime - this.startTime);
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
        },
        getIndex: function(){
            return this.index;
        },
        getLoaded: function(){
            return this.loaded;
        },
        getKey: function(){
            return this.keyValue;
        },
    },
    methods: {
        reset: function() {
            this.state = "paused";
            this.startTime = 100000;
            this.currentTime = 100000;
            this.interval = null;
            this.pauseTime = 100000;
            this.loaded = 0;
            this.internalCounter = 100000;
            this.timerID = null;
            this.saveCounter= 0;
            this.$parent.getTime(this.index);
        },
        pause() {
            this.state = "paused";
            this.pauseTime = this.internalCounter;
            console.log('\nYEET! We paused! Pause time was:'+this.pauseTime);
            console.log('\nYEET! We paused! Pause yeet index was:');
            this.$parent.getTime(this.index);
        },
        resume(timerIndex) {
            console.log("\n\n\nresume function called!!!:\nyeet index was: ");
            if(this.currentTime == this.startTime) {
                this.currentTime += this.loaded;
            }
            this.state = "started";
            this.$parent.getTime(timerIndex);
           // this.$parent.startTimer(this.index);
        },
        updateCurrentTime() {
            if (this.state == "started") {
                this.currentTime = this.currentTime + 1000;
                this.saveCounter = this.saveCounter + 1000;
            }
            if(this.saveCounter = 30000){
                this.saveCounter = 0; 
                // this.$parent.getTime(this.index);
            }

            this.internalCounter = this.internalCounter + 1000;
            
        },
        // getIndexYeet(){
        //     return this.indexYeet;
        // }
    },
};
</script>