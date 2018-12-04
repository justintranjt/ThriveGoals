<script>
    module.exports = {
        data: function() {
            return {
                state: "started",
                startTime: Date.now(),
                currentTime: Date.now(),
                interval: null
            }
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
                return this.currentTime - this.$data.startTime;
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
                this.state = "started";
                this.startTime = Date.now();
                this.currentTime = Date.now();
            },
            pause: function() {
                this.state = "paused";
            },
            resume: function() {
                this.state = "started";
            },
            updateCurrentTime: function() {
                if (this.state == "started") {
                    this.currentTime = Date.now();
                }
            }        
        },

    } 
</script>
