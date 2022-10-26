<template>
    <info>Progression of all ball-strike counts and current at-bat result</info>
    <div id="chart3"></div>
</template>


<script>

const pitch_result_dict = {
    'Groundout': 'O',
    'Double': 'H',
    'Single': 'H',
    'Strikeout': 'O',
    'Walk': 'BB',
    'Runner Out': 'OT',
    'Flyout': 'O',
    'Forceout': 'O',
    'Pop Out': 'O',
    'Intent Walk': 'OT',
    'Lineout': 'O',
    'Home Run': 'H',
    'Triple': 'H',
    'Hit By Pitch': 'OT',
    'Grounded Into DP': 'O',
    'Sac Bunt': 'OT',
    'Fielders Choice': 'O',
    'Bunt Groundout': 'O',
    'Field Error': 'OT',
    'Double Play': 'O',
    'Sac Fly': 'OT',
    'Fielders Choice Out': 'O',
    'Bunt Pop Out': 'O',
    'Catcher Interference': 'OT',
    'Strikeout - DP': 'O',
    'Batter Interference': 'OT',
    'Sac Fly DP': 'O',
    'Bunt Lineout': 'O',
    'Sacrifice Bunt DP': 'O',
    'Triple Play': 'O'
}
import * as d3 from "d3";

export default {
    name: 'HeatChart',
    data() {
        return {
            ab_path: [],
            data: [],
            selectedPitchType: "FF"
        };
    },
    props: {
        myHeatData: Object,
        selectedPitchType_prop: String
    },
    mounted() {
        console.log("HeatChart: Data Passed down as a Prop  ", this.myHeatData);
        this.draw();
    },
    watch:{
        selectedPitchType_prop(newVal, oldVal){
            this.selectedPitchType = newVal;
            d3.select('#heat').remove();
            //x._groups[0].forEach( x => x.remove() );
            this.draw();
        }
    },
    methods: {
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

            this.data = this.myHeatData.filter(x => (x["pitch_type"] === this.selectedPitchType) && (x["code"] == 'C' || x["code"] == 'S'))
            // compute the density data

            let densityData = d3.contourDensity()
                .x(function(d) { return x(d['px']);  })
                .y(function(d) { return y(d['pz']);  })
                .weight((d) => (100 / this.data.length) )
                .size([containerWidth, containerHeight])
                .bandwidth(6)
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

            top = top.reduce((a,b) => parseFloat(a) + parseFloat(b)) / top.length;
            bot = bot.reduce((a,b) => parseFloat(a) + parseFloat(b)) / bot.length;
            console.log(top,bot)


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
