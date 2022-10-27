<template>
    <body>
        <a-row :style="{ height: '100%' }">
                <a-col :span="10" :style="{ height: '100%' }" >
                            <button @click="getRandomAB(); ">Get New at-bat</button>
                            <button v-if="selectedPitch" @click="reset(); $refs.PC.resetOpacity();">Clear selection</button>
                            <PitchChart ref="PC" v-if="dataExists" :myData="myData" :key="componentKey_pitch" @selected="getSelected"/>
                </a-col>
                <a-col :span="14" :style="{ height: '100%' }">
                    <a-row :span="14" :style="{ height: '50%', width: '100%' }"> 
                        <a-col :style="{ width: '100%' }">
                            <BarChart v-if="dataExists" :myRenderData="myRenderData" :key="componentKey_render"/>
                        </a-col>
                    </a-row>
                    <a-row :span="10" :style="{ height: '50%', width: '100%' }">
                        <a-col :style="{ width: '100%' }">
                            <HeatChart v-if="heatDataExists && showHeat" :selectedPitch="selectedPitch" :myHeatData="myHeatData" :key="componentKey_heat"/>
                            <FlowChart v-if="flowDataExists && dataExists && !showHeat" :myFlowData="myFlowData"  :myData="myData" :key="componentKey_flow"/>
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
import HeatChart from "../components/pitchheat.vue"
import * as d3 from "d3";
import csvPath from '../../assets/data/ab150_subset.csv';
import csvPath2 from '../../assets/data/pitch_flow_2.csv';
import csvPath3 from '../../assets/data/ab50000_subset.csv';

//<FlowChart v-if="flowDataExists && dataExists" :myFlowData="myFlowData"  :myData="myData" :key="componentKey_flow"/>

export default {
    data(){
        return {
            at_bat_list: [],
            data: Object,
            cur_at_bat: null,
            dataExists: false,
            flowDataExists: false,
            heatDataExists: false,
            showHeat: false,
            selectedPitch: null,
            myData: [],
            myRenderData: [],
            myFlowData: [],
            myHeatData: [],
            componentKey_pitch: 0,
            componentKey_render: 0,
            componentKey_flow: 0,
            componentKey_heat: 0,
        }
    },
    components: {
        BarChart,
        PitchChart,
        FlowChart,
        HeatChart,
    },
    created(){
        /* Fetch via CSV */
        this.getDataFromCsv();
        this.getDataFromCsv2();
        this.getDataFromCsv3();
    },
    mounted(){
        /* d3.csv(csvPath, e => this.myData = e); */
        /* d3.csv(csvPath2, e => this.myFlowData = e); */

    },
    methods: {
        reset(){
            this.selectedPitch = null;
            this.myRenderData = this.myData;
            this.componentKey_render += 1;
            this.showHeat = false;
        },
        getSelected(selected){
            this.myData_backup = this.myData;
            this.myRenderData = this.myData.filter(x => x[""] == selected)
            this.selectedPitch = this.myRenderData[0]
            /* this.selectedPitchType_prop = this.myRenderData[0]['pitch_type'] */
            this.componentKey_render += 1;
            this.showHeat = true;
        },
        getRandomAB(){
            let newAB = this.at_bat_list[Math.floor(Math.random()*this.at_bat_list.length)];
            this.cur_at_bat = newAB;
            this.myData = this.data.filter(x => x['ab_id'] === this.cur_at_bat)
            this.myRenderData = this.myData
            this.componentKey_pitch += 1;
            this.componentKey_render += 1;
            this.componentKey_flow += 1;
            this.showHeat = false;
        },
        getDataFromCsv(){
            //async method
            d3.csv(csvPath).then((data) => {
                // array of objects
                this.dataExists = true; // updates the v-if to conditionally show the barchart only if our data is here.
                /* this.myData = data; // updates the prop value to be the recieved data, which we hand in to our bar-chart */
                /* this.myData = data.slice(0, 50); // updates the prop value to be the recieved data, which we hand in to our bar-chart */
                /* this.myData = data; // updates the prop value to be the recieved data, which we hand in to our bar-chart */
                data.forEach((item) => {
                        if (this.at_bat_list.indexOf(item['ab_id']) === -1){
                            this.at_bat_list.push(item['ab_id']);
                        }
                        });
                this.data = data
                // For now select the first
                this.cur_at_bat = this.at_bat_list[0];
                this.myData = data.filter(x => x['ab_id'] === this.cur_at_bat)
                this.myRenderData = this.myData
                /* data.forEach(function(x) {debugger; if (!this.at_bat_list.includes(x['ab_id'])) { at_bat_list.push(x['ab_id']); }}) */
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
        getDataFromCsv3(){
            //async method
            console.log(csvPath3)
            d3.csv(csvPath3).then((data) => {
                this.heatDataExists = true; // updates the v-if to conditionally show the barchart only if our data is here.
                this.myHeatData = data;
            });
        },
    }
}

</script>
