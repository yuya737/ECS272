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
                    <a-row :span="10" :style="{ height: '50%', width: '100%' }">
                        <a-col :style="{ width: '100%' }">
                            <FlowChart v-if="flowDataExists" :myFlowData="myFlowData" />
                        </a-col>
                    </a-row>
                </a-col>
        </a-row>
    </body>
</template>

<script>
import BarChart from "../components/barchart.vue"
import PitchChart from "../components/pitchchart.vue"
import FlowChart from "../components/flow.vue"
import * as d3 from "d3";
/* import csvPath from '../../assets/data/SF_Historical_Ballot_Measures.csv'; */
import csvPath from '../../assets/data/test.csv';
/* import csvPath2 from '../../assets/data/pitch_flow.csv'; */
import csvPath2 from '../../assets/data/pitch_flow_2.csv';
/* import csvPath from './test.csv'; */

export default {
    data(){
        return {
            dataExists: false,
            flowDataExists: false,
            myData: [],
            myFlowData: [],
        }
    },
    components: {
        BarChart,
        PitchChart,
        FlowChart,
    },
    created(){
        /* Fetch via CSV */
        this.getDataFromCsv();
        this.getDataFromCsv2();
    },
    mounted(){
        /* d3.csv(csvPath, e => this.myData = e); */
        /* d3.csv(csvPath2, e => this.myFlowData = e); */
    },
    methods: {
        getDataFromCsv(){
            //async method
            d3.csv(csvPath).then((data) => {
                // array of objects
                this.dataExists = true; // updates the v-if to conditionally show the barchart only if our data is here.
                /* this.myData = data; // updates the prop value to be the recieved data, which we hand in to our bar-chart */
                this.myData = data.slice(0, 50); // updates the prop value to be the recieved data, which we hand in to our bar-chart

            });
        },
        getDataFromCsv2(){
            //async method
            console.log(csvPath2)
            d3.csv(csvPath2).then((data) => {
                // array of objects
                this.flowDataExists = true; // updates the v-if to conditionally show the barchart only if our data is here.
                /* this.myData = data; // updates the prop value to be the recieved data, which we hand in to our bar-chart */
                console.log('sdfsdf', data)
                this.myFlowData = data;

            });
        },
    }
}

</script>
