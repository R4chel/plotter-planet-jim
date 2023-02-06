let canvasWidth = 500;
let canvasHeight = 500;

let download = false;
let canvasName = "hue-green-2500-day4";
let downloadAfter = 2500;
let downloaded = false;

let numSteps = 1000;

let circles = [];
let colors = [];

let backgroundColor;
let maxPossibleRadius = canvasWidth / 5;
let maxInnerCircles = 10;

function setup() {
    createCanvas(canvasWidth, canvasHeight);
    colorMode(RGB, 255);
    angleMode(DEGREES);

    // colors = [rgb(30, 81, 40), rgb(78, 159, 61), rgb(216, 233, 168)];
    backgroundColor = color(25, 26, 25);

    /*
  backgroundColor = rgb(85, 80, 92);
  colors = [
    rgb(250, 243, 62),
    rgb(0, 174, 173),
    rgb(171, 146, 191, 1),
    rgb(229, 116, 188),
  ];
*/

    let oranges = [
        color(255, 72, 0),
        rgba(255, 84, 0, 1),
        rgba(255, 96, 0, 1),
        rgba(255, 109, 0, 1),
        rgba(255, 121, 0, 1),
        rgba(255, 133, 0, 1),
        rgba(255, 145, 0, 1),
        rgba(255, 158, 0, 1),
        rgba(255, 170, 0, 1),
        rgba(255, 182, 0, 1),
    ];
    colors = oranges;
    noStroke();

    let bigCircle = {
        x: canvasWidth / 2,
        y: canvasWidth / 2,
        d: min(canvasWidth, canvasHeight),
        color: random(colors),
        inner: [],
    };

    for (let i = 0; i < numSteps; i++) {
        spawnInnerCircle(bigCircle);
    }
    circles = [bigCircle];
}

function rgba(r, g, b, a) {
    return color(r, g, b);
}

function spawnCircle() {
    let x = random(canvasWidth);
    let y = random(canvasHeight);
    let r = maxRadius(circles, maxPossibleRadius, x, y);
    r *= random(0.25, 0.95)
    if (r > minCircleRadius) {
        let newCircle = {
            x: x,
            y: y,
            d: r * 2,
            color: random(colors),
            inner: []
        };
        let maxInnerCircles = r;
        for (let j = 0; j < maxInnerCircles; j++) {
            spawnInnerCircle(newCircle);
        }

        circles.push(newCircle);
    }
}
let minCircleRadius = 1;

function spawnInnerCircle(c) {
    let theta = random(360);
    let offset = random(c.d / 2 - 1);
    let cx = offset * cos(theta) + c.x;
    let cy = offset * sin(theta) + c.y;
    let upperBound = c.d / 2 - offset;
    let r = maxRadius(c.inner, upperBound, cx, cy);
    r *= random(0.25, 0.95);
    if (r > minCircleRadius) {
        //let innerColor = lerpColor(c.color, color(256), random(0.1, 0.3));
        let innerColor = random(colors);
        while (innerColor == c.color) {
            innerColor = random(colors);
        }
        let newCircle = {
            x: cx,
            y: cy,
            d: r * 2,
            color: innerColor,
            inner: []
        };
        let maxInnerCircles = r * 2;
        for (let j = 0; j < maxInnerCircles; j++) {
            spawnInnerCircle(newCircle);
        }
        c.inner.push(newCircle);
    }
}

function maxRadius(circles, maxPossibleRadius, x, y) {
    let m = maxPossibleRadius;
    for (let i = 0; i < circles.length && m > 1; i++) {
        let c = circles[i];
        let distance = dist(x, y, c.x, c.y);
        if (distance < c.d / 2) {
            return -1;
        }
        m = min([distance - c.d / 2, m]);
    }
    return m;
}

function drawCircles(circles) {
    for (let i = 0; i < circles.length; i++) {
        let c = circles[i];
        fill(c.color);
        circle(c.x, c.y, c.d);
        drawCircles(c.inner);
    }
}

let t = 0;

function draw() {
    background(backgroundColor);

    drawCircles(circles);

    spawnInnerCircle(circles[0]);

    if (download && !downloaded && circles.length > downloadAfter) {
        saveCanvas(canvas, canvasName, "png");
        console.log("saved");
        downloaded = true;
    }

    if (t % 1000 == 0) {
        console.log(t, circles.length);
    }
    t++;
}