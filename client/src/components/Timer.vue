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
            internalCounter: 100000,
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
            if (this.currentTime == this.startTime) {
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
    },
    methods: {
        pause(nugget) {
            this.state = "paused";
            this.pauseTime = this.internalCounter;
            this.$parent.getTime(nugget);
        },
        resume(nugget) {
            if (this.currentTime == this.startTime) {
                this.currentTime += this.loaded;
            }
            this.state = "started";
            this.$parent.getTime(nugget);
            // this.$parent.startTimer(this.index);
        },
        updateCurrentTime() {
            if (this.state == "started") {
                this.currentTime = this.currentTime + 1000;
            }

            this.internalCounter = this.internalCounter + 1000;
        },
    },
};
</script>