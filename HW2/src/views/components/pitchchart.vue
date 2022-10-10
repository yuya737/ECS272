<template>
    <div id="chart"></div>
</template>


<script>
import * as d3 from "d3";



export default {
    name: 'PitchChart',
    data() {
        return {};
    },
    props: {
        myData: Object
    },
    mounted() {
        console.log("pitchart: Data Passed down as a Prop  ", this.myData);
        this.drawPitchChart(this.myData, "#chart");
    },
    methods: {
        drawPitchChart(data, id){
            const margin = {top: 20, right: 20, bottom: 20, left: 20};
        let container = document.getElementById('chart');

        let containerWidth = container.clientWidth;
        let containerHeight = container.clientHeight;

        const x = d3.scaleLinear()
                .domain([-7, 7])
                .range([margin.left, containerWidth - margin.right]);
            
        const y = d3.scaleLinear()
                .domain([-7, 7])
                .range([containerHeight - margin.bottom, margin.top]);

        let svg = d3.select(id)
                .append("svg")
                .attr("viewBox", [0, 0, containerWidth, containerHeight])
                .attr("width", containerWidth )
                .attr("height", containerHeight)

        svg.selectAll("dot")
            .data(data)
            .join("circle")
            .attr("cx", d => x(d.px))
            .attr("cy", d => y(d.pz))
            .attr("r", 5)
            .style("fill", "#69b3a2") 
                
                

        }
    }
}
</script>
