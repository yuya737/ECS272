<template>
    <body>
        <a-row :style="{ height: '100%' }">
                <a-col :span="10" :style="{ height: '100%' }" >
                            <PitchChart v-if="dataExists" :myData="myData" />
                </a-col>
                <a-col :span="14" :style="{ height: '100%' }">
                    <a-row :span="14" :style="{ height: '50%', width: '100%' }"> 
                        <a-col :style="{ width: '100%' }">
                            <BarChart v-if="dataExists" :myData="myData" />
                        </a-col>
                    </a-row>
                    <a-row :span="10" :style="{ height: '50%', width: '100%' }"/> 
                </a-col>
        </a-row>
    </body>
</template>

<script>
import BarChart from "../components/barchart.vue"
import PitchChart from "../components/pitchchart.vue"
import * as d3 from "d3";
/* import csvPath from '../../assets/data/SF_Historical_Ballot_Measures.csv'; */
import csvPath from '../../assets/data/test.csv';
/* import csvPath from './test.csv'; */

export default {
    data(){
        return {
            dataExists: false,
            myData: [],
        }
    },
    components: {
        BarChart,
        PitchChart
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
                /* this.myData = data; // updates the prop value to be the recieved data, which we hand in to our bar-chart */
                this.myData = data.slice(0, 50); // updates the prop value to be the recieved data, which we hand in to our bar-chart

            });
        }
    }
}

</script>
