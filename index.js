// import {
// 	GestureRecognizer,
// 	FilesetResolver,
// 	DrawingUtils
//   } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.mjs";
let video = undefined;
let src =undefined;
let dst = undefined;
let cap = undefined;
let streaming = false;
let gestureRecognizer = undefined;
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
		setTimeout(processVideo, 0);

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
			//const gestureRecognitionResult = gestureRecognizer.recognize(src);
			//console.log(gestureRecognitionResult);
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
	const vision = await mp.FilesetResolver.forVisionTasks(
		// path/to/wasm/root
		"https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/wasm"
	);
	gestureRecognizer = await mp.GestureRecognizer.createFromOptions(vision, {
		baseOptions: {
			modelAssetPath: "mp_handpass/hand_pass.task"
		},
		numHands: 2
	});
	
	await gestureRecognizer.setOptions({ runningMode: "video" });
	renderLoop();
}

let lastVideoTime = -1;
function renderLoop() {
  const video = document.getElementById("capture");

  if (video.currentTime !== lastVideoTime) {
    const gestureRecognitionResult = gestureRecognizer.recognizeForVideo(video);
    console.log(gestureRecognitionResult);
    lastVideoTime = video.currentTime;
  }

  requestAnimationFrame(() => {
    renderLoop();
  });
}