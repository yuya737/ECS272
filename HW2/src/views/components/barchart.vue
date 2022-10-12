<template>
    <div id="legend">
        <ul id="pitch_list">
        </ul>
    </div>
    <div id="scene"></div>
</template>

<script>

import * as THREE from 'three';
import { OrbitControls  } from 'three/addons/controls/OrbitControls.js';
import * as d3 from "d3";
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { LineMaterial  } from "three/examples/jsm/lines/LineMaterial";
import { LineGeometry  } from "three/examples/jsm/lines/LineGeometry";
import { Line2  } from "three/examples/jsm/lines/Line2";
import testData from "../../assets/data/test.json";
import homeplateData from "../../assets/data/Homeplate.obj"
import homeplateData2 from "../../assets/data/Homeplate.gltf"

const pitch_type = {
    'FF': 0x7fc97f,
    'CU': 0xbeaed4,
    'SI': 0xffff99,
    'CH': 0x386cb0,
    'SL': 0xfdc086,
    'FS': 0xf0027f
}

const pitch_type_name = {
    '4-Seam Fastball': '#7fc97f',
    'Curveball': '#beaed4',
    'Sinker': '#ffff99',
    'Changeup': '#386cb0',
    'Slider': '#fdc086',
    'Splitter': '#f0027f',
}

let curves_bool_array;

class bezierPath {

    constructor (config={}) {  

        let { parent, 
            name, 
            v1, 
            v2, 
            v3, 
            frequency = 1, 
            frameRate = 60, 
            height,
            pitch_speed,
            color = 0xffffff,
        } = config;

        //https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame
        this.frameRate = frameRate;       
        this.pitch_speed = pitch_speed;

        this.parent = parent;
        this.curveGroup = new THREE.Group();
        if (name) this.curveGroup.name = name;
        this.curveGroup.visible =  false;  
        this.currentSegment = -1;
        this.animationFrame = undefined; 

        const curve = new THREE.QuadraticBezierCurve3(
            v1.applyMatrix4(parent.matrixWorld),
            v2.applyMatrix4(parent.matrixWorld),
            v3.applyMatrix4(parent.matrixWorld)
        );

        const numPoints =  Math.max(Math.floor((frameRate / 2) * frequency),15);

        const points = curve.getPoints(numPoints);

        const material = new LineMaterial({
            color: color,
            linewidth: 0.006,
        });
        for (let i = 0; i < points.length - 1; i++) {
            const pts = []
            pts.push(points[i].x, points[i].y, points[i].z);
            pts.push(points[i+1].x, points[i+1].y, points[i+1].z);

            const clrs = []
            clrs.push(255, 0, 0);
            clrs.push(255, 0, 0);

            const geometry = new LineGeometry();
            geometry.setPositions(pts);
            geometry.setColors(clrs);

            const line = new Line2(geometry, material);
            line.computeLineDistances();

            this.curveGroup.add(line);

        }  // for

        parent.add(this.curveGroup);


    } // constructor


    animate(){

        let start, original_start;
        let currentSegment = this.currentSegment;
        let curveGroup = this.curveGroup;
        const framRate = this.frameRate;
        const pitch_speed = this.pitch_speed;
        const parent = this.parent;

        this.hide();
        curveGroup.visible = true;
        /* window.requestAnimationFrame(step); */ 
        this.animationFrame = window.requestAnimationFrame(step); 
        let animationFrame = this.animationFrame;

        function step(timestamp) {

            if (start === undefined) 
                start = timestamp;
            if (original_start === undefined)
                original_start = timestamp;

            const elapsed_from_original = timestamp - original_start;
            /* console.log(elapsed_from_original); */
            const elapsed = timestamp - start;

            let curveDone = true;
            curveGroup.traverse( curveSegment =>  {curveDone = curveDone && curveSegment.visible; })
            if (curveDone){
                if (elapsed_from_original >= 6000){
                    curveGroup.traverse( curveSegment => curveSegment.visible = false  );
                    original_start = timestamp;
                    currentSegment = -1; 
                    curveGroup.visible = true;
                }
                /* console.log(elapsed_from_original); */
            }

            const framHelper = 4500 - (1500/60)*(pitch_speed - 50);
            if (elapsed >= (framHelper / framRate) && curveGroup.visible ) {
                /* currentSegment = ++currentSegment; */

                /* if (currentSegment === curveGroup.children.length){ */
                /*     return; */
                /* } */
                currentSegment < curveGroup.children.length - 1  ? ++currentSegment : 0;

                curveGroup.children[currentSegment].visible = true;
                /* !curveGroup.children[currentSegment].visible; */
                start = timestamp; 
            }

            /* if (curveGroup.visible) */ 
            animationFrame = window.requestAnimationFrame(step);  
        }
    } //animate  

    destroy() {
        window.cancelAnimationFrame(this.animationFrame);
        this.parent.remove(this.curveGroup); 

    } // destroy

    display() {
        /* window.cancelAnimationFrame(this.animationFrame); */
        this.curveGroup.traverse( curveSegment => curveSegment.visible = true  );

    } // hide  

    hide() {
        window.cancelAnimationFrame(this.animationFrame);
        this.curveGroup.traverse( curveSegment => curveSegment.visible = false  );

    } // hide  

    setColor(color){
        this.curveGroup.traverse(curveSegment => curveSegment.material ? curveSegment.material.color.set(color) : null)  

    } // setColor 


}      

let scene, mesh;

export default {
    name: 'BarChart',
    data() {
        return {
            name: 'Hello',
            someLocalValues: [1, 2, 3, 4, 5],
            /* scene: null, */
            /* camera: null, */
            /* boundingbox: null, */
            /* renderer: null, */
            /* controls: null, */
            /* mesh: null, */
            height: 300,
            width: 300,
        }
    },
    props:{
        myData: Object,
    },
    mounted(){
        /* console.log(testData); */
        /* let localData = testData['data']; */
        /* this.drawBarChart(localData, "#bar"); */
        // this.drawBarChart(this.myBarchartData, "#bar")
        console.log("BarChart: Data Passed down as a Prop  ", this.myData);
        this.scene = this.setupScene();
        /* this.scene = new THREE.Scene(); */
        /* this.scene = new THREE.Scene(); */
        /* this.boundingBox = this.setupBoundingBox(); */
        this.camera = this.setupCamera();
        console.log(this);
        this.addHomePlate();
        this.temp();
        this.path = this.getPaths();
        this.addLegend();
        this.animate();
    },
    methods: {
        addHomePlate(){
            const loader = new OBJLoader();
            let homeplate = loader.parse(homeplateData);
            this.scene.add(homeplate);
            const light = new THREE.PointLight()
            light.position.set(2.5, 7.5, 15)
            this.scene.add(light)

            /* debugger; */
            // load a resource
            /* let obj = [] */
            /* loader.load( */
            /*     homeplateData, */
            /*     // resource URL */
            /*     /1* '../../assets/data/homeplate2.sv', *1/ */
            /*     // called when resource is loaded */
            /*     function ( object  ) { */
            /*         debugger; */
            /*         obj.push(object); */
            /*     }, */
            /*     // called when loading is in progresses */
            /*     function ( xhr  ) { */
            /*         console.log( ( xhr.loaded / xhr.total * 100  ) + '% loaded'  ); */
            /*     }, */
            /*     // called when loading has errors */
            /*     function ( error  ) { */
            /*         console.log( 'An error happened'  ); */
            /*     } */
            /* ) */
            /* debugger; */
        },

        makeStrikeZone(){
            // Strike zone 
            let top = [], bot = [];

            data.forEach(x => top.push(x['sz_top']));
            data.forEach(x => bot.push(x['sz_bot']));

            top = top.reduce((a,b) => parseFloat(a) + parseFloat(b)) / top.length;
            bot = bot.reduce((a,b) => parseFloat(a) + parseFloat(b)) / bot.length;

            /* const pts = [(-17/24),] */

            const clrs = []
            clrs.push(255, 0, 0);
            clrs.push(255, 0, 0);

            const geometry = new LineGeometry();
            geometry.setPositions(pts);
            geometry.setColors(clrs);

            const line = new Line2(geometry, material);
            line.computeLineDistances();

        },
        addLegend(){
            let container = document.getElementById('scene');

            let containerWidth = Math.min(container.clientWidth, container.clientHeight);
            let containerHeight = containerWidth;

            let svg = d3.select('#legend')
                .append("svg")
                .attr("viewBox", [0, 0, containerWidth, containerHeight])
                .attr("width", containerWidth )
                .attr("height", containerHeight)
                .style("margin", "auto")
                .style("height", "100%");

            let size = 20;
            let keys = [ '4-Seam Fastball', 'Curveball', 'Sinker', 'Changeup', 'Slider', 'Splitter'];

            svg.selectAll("mydots")
                .data(keys)
                .enter()
                .append("rect")
                .attr("x", 10)
                .attr("y", function(d,i){ return 10 + i*(size+5) }) // 100 is where the first dot appears. 25 is the distance between dots
                .attr("width", size)
                .attr("height", size)
                .style("fill", d => pitch_type_name[d]);

            // Add one dot in the legend for each name.
            svg.selectAll("mylabels")
                .data(keys)
                .enter()
                .append("text")
                .attr("x", 10 + size*1.2)
                .attr("y", function(d,i){ return 10 + i*(size+5) + (size/2) }) // 100 is where the first dot appears. 25 is the distance between dots
            /* .style("fill", function(d){ return pitch_type_name[d] }) */
                .text(function(d){ return d })
                .attr("text-anchor", "left")
                .style("alignment-baseline", "middle")

            /* let container = document.getElementById('pitch_list'); */
            /* let pitch_list = [] */
            /* this.myData.forEach(x => pitch_list.push(x['pitch_type'])) */
            /* pitch_list = [...new Set(pitch_list)] */

            /* for (const i of pitch_list){ */
            /*     let span = document.createElement('span'); */
            /*     let li = document.createElement('li'); */

            /*     span.style.backgroundColor="#"+pitch_type[i].toString(16); */
            /*     li.appendChild(document.createTextNode(pitch_type_name[i])); */

            /*     li.appendChild(span); */
            /*     container.appendChild(li); */
            /* } */

            /* let container = document.getElementById('legend'); */
            /* container.innerHTML += 'sdfsf<br>sdfsf' */
            /* let content = document.createTextNode('sdfsadfsasdf'); */
            /* let content2 = document.createTextNode('sdfsadfsasdf'); */
            /* container.appendChild(content); */
            /* container.appendChild(content2); */

        },
        temp(){
            let container = document.getElementById('scene');
            let renderer = new THREE.WebGLRenderer({antialias: true});

            const controls = new OrbitControls(this.camera, renderer.domElement);

            /* renderer.setSize(Math.min(container.clientWidth, container.clientHeight), Math.min(container.clientWidth, container.clientHeight)); */
            renderer.setSize(container.clientWidth, container.clientHeight);
            this.camera.aspect = container.clientWidth / container.clientHeight;
            this.camera.updateProjectionMatrix();
            renderer.setPixelRatio(window.devicePixelRatio);

            this.renderer = renderer;
            /* this.controls = controls; */

            /* let geometry = new THREE.BoxGeometry(1,1,1); */
            /* const material = new THREE.MeshNormalMaterial(); */

            /* this.mesh = new THREE.Mesh(geometry, material) */ 
            /* this.scene.add(this.mesh); */
            console.log(this.scene)
            container.appendChild(this.renderer.domElement);

            this.renderer.render(this.scene, this.camera);

        }, // while
        animate() {
            /* for (const p of this.path){ */
            /*     p['animate']() */
            /* } */

            requestAnimationFrame(this.animate);
            /* this.randomPath.animate(); */

            /* this.mesh.rotation.x += 0.01 */
            /* this.mesh.rotation.y += 0.01 */

            this.renderer.render(this.scene, this.camera);
        },


        getPaths(){
            let arr = []

            for (let path of this.myData){
                const p = new bezierPath({
                    parent: this.scene,
                    v1: new THREE.Vector3(
                        path['x0'],
                        path['z0'] - 5,
                        -25),
                    v2: new THREE.Vector3(
                        path['xmid'],
                        path['zmid'] - 5,
                        0),
                    v3: new THREE.Vector3(
                        path['px'],
                        path['pz'] - 5,
                        25),
                    height: 1,
                    color: pitch_type[path['pitch_type']],
                    pitch_speed: path['start_speed'],
                });
                arr.push(p);
                p['animate']();
            }
            return arr;
        },

        /* getRandomPath(){ */

        /*     const getRandom = () => d3.interpolate(-1*this.gridHelperSize/2, this.gridHelperSize/2)(Math.random()); */ 
        /*     const sceneHeight = 1; */

        /*     const path = new bezierPath({ parent: this.scene, */ 
        /*         v1: new THREE.Vector3(getRandom(), 0, getRandom() ), */ 
        /*         v2: new THREE.Vector3(getRandom(), 0, getRandom() ), */ 
        /*         v3: new THREE.Vector3(getRandom(), 0, getRandom() ), */ 
        /*         height: d3.interpolate(sceneHeight * 2, sceneHeight * 4)(Math.random()), */ 
        /*         color: d3.interpolateRainbow(Math.random()) */
        /*     }); */ 
        /*     const path2 = new bezierPath({ parent: this.scene, */ 
        /*         v1: new THREE.Vector3(getRandom(), 0, getRandom() ), */ 
        /*         v2: new THREE.Vector3(getRandom(), 0, getRandom() ), */ 
        /*         v3: new THREE.Vector3(getRandom(), 0, getRandom() ), */ 
        /*         height: d3.interpolate(sceneHeight * 2, sceneHeight * 4)(Math.random()), */ 
        /*         color: d3.interpolateRainbow(Math.random()) */
        /*     }); */ 
        /*     console.log(path); */

        /*     path['animate'](); */
        /*     path2['animate'](); */

        /*     return path; */

        /* }, // getRandomPath */

        setupScene() {
            /* const gridHelperSize = 10; */
            const gridHelperSize = 50;
            this.gridHelperSize = gridHelperSize;
            const scene = new THREE.Scene();

            scene.background = new THREE.Color(0xffffff);

            const sceneHeight = 1;
            //Cube is used temporarily to set size of boundingBox       
            /* const geometry = new THREE.BoxGeometry(1, sceneHeight, 1); */
            const geometry = new THREE.BoxGeometry(10, 10, 50);
            /* geometry.translate(0, sceneHeight / 2, 0); */
            const cube =  new THREE.Mesh(geometry, new THREE.MeshBasicMaterial()); 

            scene.add(cube);
            /* scene.add(cube); */

            const boundingBox = new THREE.BoxHelper(scene, 0x000000);
            boundingBox.geometry.computeBoundingBox();  
            boundingBox.geometry.computeBoundingSphere();
            /* debugger; */
            /* boundingBox.geometry.translate( 0, 0 ,0  ) */

            scene.add(boundingBox);
            this.boundingBox = boundingBox;
            /* scene.add(boundingBox); */

            scene.remove(cube);
            /* scene.remove(cube); */
            const helper = new THREE.GridHelper( this.gridHelperSize, 10 );
            /* helper.translate(0, -2, 0); */
            /* scene.add(helper); */
            /* helper.scale.addScaledVector(5,1); */

            const geometry_plane = new THREE.PlaneGeometry( 100, 100 );
            /* debugger; */
            /* debugger; */
            const material_plane = new THREE.MeshBasicMaterial( {color: 0xb38650, side: THREE.DoubleSide, transparent: true, opacity: 0.5}  );
            const plane = new THREE.Mesh( geometry_plane, material_plane  );
            /* const plane = new THREE.Plane( new THREE.Vector3( 0, 1, 0  ), 7  ); */
            /* const plane_helper = new THREE.PlaneHelper( plane, 1000, new THREE.Color( 0xb38650  )   ); */
            plane.rotation.x = Math.PI / 2;
            plane.position.y = -7;
            /* scene.add( plane_helper  ); */
            scene.add( plane  );

            /* const loader = new OBJLoader(); */

            /* loader.load(homeplateData, */ 
            /*     (o)=>scene.add(o), */
            /*     (xhr)=>console.log((xhr.loaded / xhr.total) * 100+'% loaded'), */
            /*     (e) => console.log(e)); */

            const loader2 = new GLTFLoader();

            loader2.load(homeplateData2, 
   (o)=>{let temp = o.scene.children[0]; temp.material = new THREE.MeshBasicMaterial ( {color: 0xFEEBC3} ); temp.rotation.x = -1 * Math.PI / 2; temp.position.y = -7; temp.position.z=25; temp.scale.set(1/9, 1/9, 1/9); scene.add(temp)},
                (xhr)=>console.log((xhr.loaded / xhr.total) * 100+'% loaded'),
                (e) => console.log(e));

            /* let homeplate = loader.parse(homeplateData); */
            

            return scene;  
        },

        setupCamera() {
            const fov = 45;
            /* const width = 500; */
            /* const height = 300; */
            const aspect = this.width / this.height;

            const near = 3;
            const sceneHeight = 1;
            const far = Math.max(10000,this.boundingBox.geometry.boundingSphere.radius * 2);
            const camera = new THREE.PerspectiveCamera(75, 1., near, far);

            // Position for a bird's eye view of the warehouse
            camera.position.set(-1 * this.boundingBox.geometry.boundingSphere.radius * 0.75, 
                0,0);
            /* this.boundingBox.geometry.boundingSphere.radius / 4 , */ 
            /* this.boundingBox.geometry.boundingSphere.radius * 1.5 ); */ 


            camera.lookAt(this.boundingBox.geometry.boundingSphere.center.x,
                this.boundingBox.geometry.boundingSphere.center.y,
                this.boundingBox.geometry.boundingSphere.center.z);    

            return camera;
        },
    }
}

</script>


<style>

</style>
