<template>
    <div>
        <h1>Welcome Home</h1>
        <BarChart v-if="dataExists" :myData="myData" />
    </div>
</template>

<script>
import BarChart from "../components/barchart.vue"
import * as d3 from "d3";
/* import csvPath from '../../assets/data/SF_Historical_Ballot_Measures.csv'; */
import csvPath from './test.csv';

export default {
    data(){
        return {
            dataExists: false,
            myData: [],
        }
    },
    components: {
        BarChart
    },
    created(){
        /* Fetch via CSV */
        this.drawBarFromCsv()
    },
    mounted(){
        d3.csv(csvPath, e => this.myData = e);
    },
    methods: {
        drawBarFromCsv(){
            
            /* let csvPath = '../../assets/data/test.csv'; */
            
            //async method
            d3.csv(csvPath).then((data) => {
                // array of objects
                console.log(data.length);
                console.log(data);
                this.dataExists = true; // updates the v-if to conditionally show the barchart only if our data is here.
                this.myData = data; // updates the prop value to be the recieved data, which we hand in to our bar-chart

            });
        }
    }
}

</script>
