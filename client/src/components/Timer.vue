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
            startTime: 100000,
            currentTime: 100000,
            interval: null,
            netTimeDiff: 0,
            pauseTime: 100000,
            internalCounter:100000, 
        }
    },

    props: ['loaded', 'index'],

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
            console.log('\n\nloaded in milliseconds: '+this.loaded);
            console.log('other terms: '+((this.currentTime - this.startTime) - this.netTimeDiff))
            console.log('At call time, pauseTime is: '+ this.pauseTime); 
            console.log('At call time, startTime is: '+ this.startTime); 
            console.log('At call time, netTimeDiff is: '+ this.netTimeDiff); 
            console.log('At call time, currentTime is: '+ this.currentTime); 
            if(this.currentTime == this.startTime) {
                console.log("yeet, we in the if block");
                this.currentTime = this.currentTime + this.loaded;
                console.log('After update, currentTime is: '+ this.currentTime); 
                return ((this.currentTime - this.startTime) - this.netTimeDiff);
         }
         console.log('After load, currentTime is: '+ this.currentTime); 
         console.log('computed milliseconds: '+ ((this.currentTime - this.startTime) - this.netTimeDiff)); 
           return ((this.currentTime - this.startTime) - this.netTimeDiff);

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

        getPauseTime: function(){
            // console.log('\n\nYEET INDEED getPause Time returns: '+ this.loaded + ((this.pauseTime - this.startTime) - this.netTimeDiff));
            // console.log('At call time, milliseconds is: '+ this.milliseconds); 
            // console.log('At call time, pauseTime is: '+ this.pauseTime); 
            // console.log('At call time, startTime is: '+ this.startTime); 
            // console.log('At call time, netTimeDiff is: '+ this.netTimeDiff); 
             return this.loaded + ((this.pauseTime - this.startTime) - this.netTimeDiff);
        } , 
        
        seconds: function() {
            var lapsed = this.milliseconds;
            var sec = Math.ceil((lapsed / 1000) % 60);
            return sec >= 10 ? sec : '0' + sec;
        }
    },
    methods: {
        reset: function() {
            this.state = "paused";
            this.startTime = 100000;
            this.currentTime = 100000;
            this.interval = null;
            this.netTimeDiff = 0;
            this.pauseTime = 100000;
            this.loaded = 100000;
            this.internalCounter = 100000;
        },
        pause: function() {
            this.state = "paused";
            this.pauseTime = this.internalCounter;
            console.log('\n\n\nYEET!! Pause time was:'+this.pauseTime);
            this.$parent.getTime(this.index);
        },



        resume: function() {
            console.log("\n\n\nresume function called!!!:"); 
            if(this.currentTime == this.startTime) {
                this.curentTime = this.internalCounter + this.loaded
            }
            else{
                        if(this.state == "paused"){
                        console.log("internal counter: "+ this.internalCounter);
                        console.log("pauseTime: "+ this.pauseTime);
                        console.log("netDiff updated: "+ this.netTimeDiff);
                        this.netTimeDiff = this.netTimeDiff + (this.internalCounter - this.pauseTime);  
                        console.log("netDiff updated: "+ this.netTimeDiff);
                    }

            }


            this.state = "started";
            
        },
        updateCurrentTime: function() {
            if (this.state == "started") {
                this.currentTime = this.currentTime + 1000;
            }
            this.internalCounter = this.internalCounter + 1000;
        },
    },
};
</script>