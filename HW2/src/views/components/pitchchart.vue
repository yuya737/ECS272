<template>
    <div id="chart"></div>
</template>


<script>
import * as d3 from "d3";

const pitch_result = {
    'S': '#e41a1c',
    'B': '#4daf4a',
    'X': '#377eb8',
};

const pitch_label = {
    'Strike': '#e41a1c',
    'Ball': '#4daf4a',
    'In Play': '#377eb8',
};


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

            let containerWidth = Math.min(container.clientWidth, container.clientHeight);
            let containerHeight = containerWidth;

            const x = d3.scaleLinear()
                .domain([-3, 3])
                .range([margin.left, containerWidth - margin.right]);

            const y = d3.scaleLinear()
                .domain([-2, 4])
                .range([containerHeight - margin.bottom, margin.top]);

            let svg = d3.select(id)
                .append("svg")
                .attr("viewBox", [0, 0, containerWidth, containerHeight])
                .attr("width", containerWidth )
                .attr("height", containerHeight)
                .style("margin", "auto")
                .style("height", "100%");

            // Strike zone 
            let top = [], bot = [];

            data.forEach(x => top.push(x['sz_top']));
            data.forEach(x => bot.push(x['sz_bot']));

            top = top.reduce((a,b) => parseFloat(a) + parseFloat(b)) / top.length;
            bot = bot.reduce((a,b) => parseFloat(a) + parseFloat(b)) / bot.length;

            // bottom of strike zone is at -2
            let points = [
                {x: x(-17/24),y: y(bot) },
                {x: x(17/24),y: y(bot) },
                {x: x(17/24),y: y(top) },
                {x: x(-17/24),y:  y(top) },
            ];
            // let strikeZonePath = d3.line(points);
            let strikeZonePath = d3.line()
                .x(d => d.x)
                .y(d => d.y);

            svg.selectAll("rect")
                .data([0])
                .join("rect")
                .attr('x', x(-17/24))
                .attr('y', y(top))
                .attr('width', x(17/24)-x(-17/24))
                .attr('height', y(bot)-y(top))
                .style('fill', '#69b3a2')
                .style("opacity", 0.3);

            svg.selectAll("dot")
                .data(data)
                .join("circle")
                .attr("cx", d => x(d.px))
                .attr("cy", d => y(d.pz))
                .attr("r", 8)
                .style("fill", d => pitch_result[d['type']]) ;

            svg.selectAll("text")
                .data(data)
                .join("text")
                .attr("x", d => x(d.px)+10)
                .attr("y", d => y(d.pz)+15)
                //.text(d=>{parseInt(d['pitch_num'])})
                .text(d=>parseInt(d['pitch_num']))
                //.text(parseInt(d['pitch_num']) - 1)


            // Add one dot in the legend for each name.
            let size = 20;
            let keys = ['Strike', 'Ball', 'In Play']

            svg.selectAll("mydots")
                .data(keys)
                .enter()
                .append("rect")
                .attr("x", 10)
                .attr("y", function(d,i){ return 10 + i*(size+5) }) // 100 is where the first dot appears. 25 is the distance between dots
                .attr("width", size)
                .attr("height", size)
                .style("fill", d => pitch_label[d]);

            // Add one dot in the legend for each name.
            svg.selectAll("mylabels")
                .data(keys)
                .enter()
                .append("text")
                .attr("x", 10 + size*1.2)
                .attr("y", function(d,i){ return 10 + i*(size+5) + (size/2) }) // 100 is where the first dot appears. 25 is the distance between dots
                .style("fill", function(d){ return pitch_label[d] })
                .text(function(d){ return d })
                .attr("text-anchor", "left")
                .style("alignment-baseline", "middle")


        }
    }
}
</script>
