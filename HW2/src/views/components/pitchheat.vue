<template>
    <info>Effective pitch locations for {{ getPitchType() }}s against {{ getBatterSide() }}-handed batters</info>
    <div id="chart3"></div>
</template>


<script>

import { pitch_type_dict  } from './constants.js'
import * as d3 from "d3";

export default {
    name: 'HeatChart',
    data() {
        return {
            ab_path: [],
            data: [],
            selectedPitchType: null,
            batterSide: null
        };
    },
    props: {
        myHeatData: Object,
        selectedPitch: Object
    },
    mounted() {
        console.log("HeatChart: Data Passed down as a Prop  ", this.myHeatData);
        this.selectedPitchType = this.selectedPitch['pitch_type']
        this.batterSide = this.selectedPitch['stand']
        this.draw();
    },
    watch:{
        selectedPitch(newVal, oldVal){
            // Need to update
            if (this.selectedPitchType && (this.selectedPitchType !== newVal['pitch_type'])){
                this.selectedPitchType = newVal['pitch_type'];

                this.batterSide = newVal['stand']
                d3.select('#heat').remove();
                //x._groups[0].forEach( x => x.remove() );
                this.draw();
            }
        }
    },
    methods: {
        getBatterSide(){
            return this.batterSide == 'L' ? 'Left' : 'Right';
        },
        getPitchType(){
            return pitch_type_dict[this.selectedPitchType];
        },
        draw(){

            const margin = {top: 60, right: 60, bottom: 60, left: 60};
            let container = document.getElementById('chart3');

            let containerWidth = Math.min(container.clientWidth, container.clientHeight);
            let containerHeight = containerWidth;

            const x = d3.scaleLinear()
                .domain([-1.5, 1.5])
                .range([margin.left, containerWidth - margin.right]);

            const y = d3.scaleLinear()
                .domain([0.5, 3.5])
                .range([containerHeight - margin.bottom, margin.top]);

            let svg = d3.select('#chart3')
                .append("svg")
                .attr("id", "heat")
                .attr("viewBox", [0, 0, containerWidth, containerHeight])
                .attr("width", containerWidth )
                .attr("height", containerHeight)
                .style("margin", "auto")
                .style("height", "100%");

            //this.data = this.myHeatData.filter(x => (x['stand'] === this.batterSide) && (x["pitch_type"] === this.selectedPitchType) && (x["code"] == 'C' || x["code"] == 'S'))
            this.data = this.myHeatData.filter(x => (x['stand'] === this.batterSide) && (x["pitch_type"] === this.selectedPitchType) && (x["type"] == 'S'))
            // compute the density data

            let densityData = d3.contourDensity()
                .x(function(d) { return x(d['px']);  })
                .y(function(d) { return y(d['pz']);  })
                .weight((d) => (100 / this.data.length) )
                .size([containerWidth, containerHeight])
                .bandwidth(15)
                (this.data)

            // Prepare a color palette
            const color = d3.scaleLinear()
                .domain([
                    Math.min(...densityData.map( x=> x['value'] )),
                    Math.max(...densityData.map( x=> x['value'] ))
                ]) // Points per square pixel.
                .range(["white", "#eb4034"])

            // Strike zone 
            let top = [], bot = [];

            this.data.forEach(x => top.push(x['sz_top']));
            this.data.forEach(x => bot.push(x['sz_bot']));

            top = top.reduce((a,b) => parseFloat(a) + parseFloat(b), 0) / top.length;
            bot = bot.reduce((a,b) => parseFloat(a) + parseFloat(b), 0) / bot.length;


            svg.selectAll("rect")
                .data([0])
                .join("rect")
                .attr('x', x(-17/24))
                .attr('y', y(top))
                .attr('width', x(17/24)-x(-17/24))
                .attr('height', y(bot)-y(top))
                .style('fill', '#69b3a2')
                .style("opacity", 0.3);

            // show the shape!
            svg.insert("g", "g")
                .selectAll("path")
                .data(densityData)
                .enter().append("path")
                .attr("d", d3.geoPath())
                .attr("fill", function(d) { return color(d.value);  })
                .style("opacity", 0.1);


        },
    },
}

</script>
