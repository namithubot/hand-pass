<script lang="ts">
	import { spring } from 'svelte/motion';
	import cv from "@techstark/opencv-js";
	import { browser } from '$app/environment';
	import { FilesetResolver, GestureRecognizer } from '@mediapipe/tasks-vision';

	let buildInfo: string = "";

	let video: any = undefined;
	let src: any =undefined;
	let dst: any = undefined;
	let cap: any = undefined;
	let streaming = false;
	let gestureRecognizer: any = undefined;
	function startCapturing(){
		video =  document.getElementById("capture"); // video is the id of video tag
		navigator.mediaDevices.getUserMedia({ video: true, audio: false })
		.then(function(stream) {
			video.srcObject = stream;
			video.play();
			setupRecognizer();
			video.width = 640;
			video.height = 480;
			src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
			dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
			cap = new cv.VideoCapture(video);

			streaming = true;
			// schedule the first one.
			// setTimeout(processVideo, 0);

		})
		.catch(function(err) {
			console.log("An error occurred! " + err);
		});
	}

		
	const FPS = 30;
	function processVideo() {
		try {
			if (!streaming) {
				// clean and stop.
				src.delete();
				dst.delete();
				return;
			}
			let begin = Date.now();
			// start processing.
			cap.read(src);
			if (gestureRecognizer) {
				const gestureRecognitionResult = gestureRecognizer.recognize(src);
				console.log(gestureRecognitionResult);
			}
			//cv.cvtColor(src, dst, cv.COLOR_) //, cv.COLOR_RGBA2GRAY);
			cv.imshow('canvasOutput', src);
			// schedule the next one.
			let delay = 1000/FPS - (Date.now() - begin);
			setTimeout(processVideo, delay);
		} catch (err) {
			console.error(err);
		}
	};

	async function setupRecognizer() {
		// Create task for image file processing:
		const vision = await FilesetResolver.forVisionTasks(
			// path/to/wasm/root
			"https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/wasm"
		);
		gestureRecognizer = await GestureRecognizer.createFromModelPath(vision, "mp-handpass/hand_pass.task"); 
		// createFromOptions(vision, {
		// 	baseOptions: {
		// 		modelAssetPath: "mp-handpass/hand_pass.task",
		// 	},
		// 	numHands: 2
		// });
		
		//await gestureRecognizer.setOptions({ runningMode: "video" });
		renderLoop();
	}

	let lastVideoTime = -1;
	function renderLoop() {
		const video: any = document.getElementById("capture");
		(new (window as any).ImageCapture(video.srcObject.getVideoTracks()[0])).grabFrame()
		.then((capture: any) => {

			if (video.currentTime !== lastVideoTime) {
				const gestureRecognitionResult = gestureRecognizer.recognize(capture);
				console.log(gestureRecognitionResult);
				lastVideoTime = video.currentTime;
			}

			requestAnimationFrame(() => {
				renderLoop();
			});

		});
	}

	if (browser) {
		window.setTimeout(() => {
			(window as any).cv = cv;
			buildInfo = cv.getBuildInformation();
		}, 1000);

	}
	

	let count = 0;

	const displayed_count = spring();
	$: displayed_count.set(count);
	$: offset = modulo($displayed_count, 1);

	function modulo(n: number, m: number) {
		// handle negative numbers
		return ((n % m) + m) % m;
	}
</script>

<div class="counter">
	<video id="capture">
		<track kind="captions" />
	</video>
	<canvas id="canvasOutput"></canvas>
	<div>
	</div>
	<button on:click={() => startCapturing()} aria-label="Decrease the counter by one">
		<svg aria-hidden="true" viewBox="0 0 1 1">
			<path d="M0,0.5 L1,0.5" />
		</svg>
	</button>

	<div class="counter-viewport">
		<div class="counter-digits" style="transform: translate(0, {100 * offset}%)">
			<strong class="hidden" aria-hidden="true">{Math.floor($displayed_count + 1)}</strong>
			<strong>{Math.floor($displayed_count)}</strong>
		</div>
	</div>

	<button on:click={() => (count += 1)} aria-label="Increase the counter by one">
		<svg aria-hidden="true" viewBox="0 0 1 1">
			<path d="M0,0.5 L1,0.5 M0.5,0 L0.5,1" />
		</svg>
	</button>
</div>

<style>
	.counter {
		display: flex;
		border-top: 1px solid rgba(0, 0, 0, 0.1);
		border-bottom: 1px solid rgba(0, 0, 0, 0.1);
		margin: 1rem 0;
	}

	.counter button {
		width: 2em;
		padding: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 0;
		background-color: transparent;
		touch-action: manipulation;
		font-size: 2rem;
	}

	.counter button:hover {
		background-color: var(--color-bg-1);
	}

	svg {
		width: 25%;
		height: 25%;
	}

	path {
		vector-effect: non-scaling-stroke;
		stroke-width: 2px;
		stroke: #444;
	}

	.counter-viewport {
		width: 8em;
		height: 4em;
		overflow: hidden;
		text-align: center;
		position: relative;
	}

	.counter-viewport strong {
		position: absolute;
		display: flex;
		width: 100%;
		height: 100%;
		font-weight: 400;
		color: var(--color-theme-1);
		font-size: 4rem;
		align-items: center;
		justify-content: center;
	}

	.counter-digits {
		position: absolute;
		width: 100%;
		height: 100%;
	}

	.hidden {
		top: -100%;
		user-select: none;
	}
</style>
