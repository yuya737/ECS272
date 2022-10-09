<template>
    <div id="bar"></div>
    <div id="scene"></div>
</template>

<script>

import * as THREE from 'three';
import { OrbitControls  } from 'three/addons/controls/OrbitControls.js';
import * as d3 from "d3";
import { LineMaterial  } from "three/examples/jsm/lines/LineMaterial";
import { LineGeometry  } from "three/examples/jsm/lines/LineGeometry";
import { Line2  } from "three/examples/jsm/lines/Line2";
import testData from "../../assets/data/test.json";

const pitch_type = {

    'FF': 0x7fc97f,
    'CU': 0xbeaed4,
    'FC': 0xfdc086,
    'SI': 0xffff99,
    'CH': 0x386cb0
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
            linewidth: 0.003,
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
                if (elapsed_from_original >= 2700){
                    curveGroup.traverse( curveSegment => curveSegment.visible = false  );
                    original_start = timestamp;
                    currentSegment = -1; 
                    curveGroup.visible = true;
                }
                console.log(elapsed_from_original);
            }

            const framHelper = 2500 - (1000/60)*(pitch_speed - 50);
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
        console.log("Data Passed down as a Prop  ", this.myData);
        this.scene = this.setupScene();
        /* this.scene = new THREE.Scene(); */
        /* this.scene = new THREE.Scene(); */
        /* this.boundingBox = this.setupBoundingBox(); */
        this.camera = this.setupCamera();
        console.log(this);
        this.temp();
        this.path = this.getPaths();
        this.animate();
    },
    methods: {
        temp(){
            let container = document.getElementById('scene');
            let renderer = new THREE.WebGLRenderer({antialias: true});

            const controls = new OrbitControls(this.camera, renderer.domElement);

            renderer.setSize(Math.min(window.innerWidth, window.innerHeight), Math.min(window.innerWidth, window.innerHeight));
            renderer.setPixelRatio(window.devicePixelRatio);

            this.renderer = renderer;
            /* this.controls = controls; */

            /* let geometry = new THREE.BoxGeometry(1,1,1); */
            /* const material = new THREE.MeshNormalMaterial(); */

            /* this.mesh = new THREE.Mesh(geometry, material) */ 
            this.scene.add(this.mesh);
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
            boundingBox.geometry.translate( 0, 0 ,0  )

            scene.add(boundingBox);
            this.boundingBox = boundingBox;
            /* scene.add(boundingBox); */

            scene.remove(cube);
            /* scene.remove(cube); */
            const helper = new THREE.GridHelper( this.gridHelperSize, 10 );
            scene.add(helper);
            /* helper.scale.addScaledVector(5,1); */

            return scene;  
        },

        setupCamera() {
            const fov = 45;
            /* const width = 500; */
            /* const height = 300; */
            const aspect = this.width / this.height;

            const near = 1;
            const sceneHeight = 1;
            const far = Math.max(10000,this.boundingBox.geometry.boundingSphere.radius * 2);
            const camera = new THREE.PerspectiveCamera(60, 1., near, far);

            // Position for a bird's eye view of the warehouse
            camera.position.set(this.boundingBox.geometry.boundingSphere.center.x, 
                this.boundingBox.geometry.boundingSphere.radius , 
                this.boundingBox.geometry.boundingSphere.radius * 1.5); 


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
