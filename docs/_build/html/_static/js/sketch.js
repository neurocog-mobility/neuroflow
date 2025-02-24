// Adapted from: https://ronikaufman.github.io

let margin = 0;
let n, s, u;
let dMin, dMax, dDiff;
let eps = 1e-4;

const N_FRAMES = 720;

function setup() {
  createCanvas(windowWidth * 0.45, 240);
  n = 6; // number of tiles
  s = (width-2*margin)/n; // size of 1 tile
  u = s / 4; // how each tile is divided
  dMin = 4;
  dMax = 6;
  dDiff = dMax-dMin;
  strokeWeight(s/10);
  strokeCap(ROUND);
}

function draw() {
  //background(255);
	
	//fill(255);
  clear();
	noStroke();
	rect(0, 0, width, height);
	noFill();
  
  let t = (frameCount%N_FRAMES)/N_FRAMES;
  
  let tCol = (constrain(fract(t*dDiff*2), 0, 1/2) + floor(t*dDiff*2)/2)/dDiff;
  let palette = ["#23354b", rainbow(tCol)];
  
  for (let i = 0; i < n; i++) {
    let x = i*s+margin;
    for (let j = 0; j < n; j++) {
      let y = j*s+margin;
      let tij = (t+floor(noise(x, y)*dDiff)/dDiff)%1;
      makeTile(x, y, tij, palette);
    }
  }
}

function makeTile(x, y, t, palette) {
  let dt = d(t);
  
  let d1 = dMin + floor(dt); // amount of arcs on top-left and bottom-right corners
  let d2 = 7 - d1; // amount of arcs on top-right and bottom-left corners
  
  let f = fract(dt);
  let f1 = constrain(f, eps, 1-eps), f2 = constrain(1-f, eps, 1-eps);
  
	// top-left and bottom-right corners
  let k = 0;
  for (let i = 1; i < d1; i++) {
    stroke(palette[k%palette.length]);
    arc(x, y, i * u, i * u, 0, PI / 2);
    arc(x + s, y + s, i * u, i * u, PI, (3 * PI) / 2);
    k++;
  }
  stroke(palette[k%palette.length]);
  arc(x, y, d1 * u, d1 * u, 0, f1*PI/2);
  arc(x, y, d1 * u, d1 * u, PI/2 - f1*PI/2, PI/2);
  arc(x + s, y + s, d1 * u, d1 * u, PI, PI + f1*PI/2);
  //arc(x + s, y + s, d1 * u, d1 * u, 3*PI/2 - f1*PI/2, 3*PI/2);
  //k++;
  
	// top-right and bottom-left corners
  stroke(palette[k%palette.length]);
  arc(x + s, y, (d2+1) * u, (d2+1) * u, PI/2, PI/2 + f2*PI/2);
  //arc(x + s, y, (d2+1) * u, (d2+1) * u, PI - f2*PI/2, PI);
  arc(x, y + s, (d2+1) * u, (d2+1) * u, 3*PI/2, 3*PI/2 + f2*PI/2);
  //arc(x, y + s, (d2+1) * u, (d2+1) * u, TAU - f2*PI/2, TAU);
  k++;
  for (let i = d2; i > 0; i--) {
    stroke(palette[k%palette.length]);
    arc(x + s, y, i * u, i * u, PI / 2, PI);
    arc(x, y + s, i * u, i * u, (3 * PI) / 2, 2 * PI);
    k++;
  }
}

function d(x) {
  let dx = constrain(fract(x*dDiff*2), 0, 1/2) + floor(2*x*dDiff)/2;
  if (dx > dDiff/2) dx = dDiff-dx;
  return 2*dx;
}

function rainbow(t) {
  let palette = ["#0249da", "#0369d4", "#0095f9"];
  let i = floor(palette.length*t);
  let amt = fract(palette.length*t);
  return lerpColor(color(palette[i%palette.length]), color(palette[(i+1)%palette.length]), amt);
}
