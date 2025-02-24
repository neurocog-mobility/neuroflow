let truchet = [];
let columns = 12;
let rows = 3;
let TILE_SIZE = 0;

function setup() {
    TILE_SIZE = (windowWidth * 0.42) / columns;
	createCanvas(TILE_SIZE*(columns+1), TILE_SIZE*(rows+1));
	//background('#f9f0de');

	let palette = ["#23354b"]

	primaryColor = color(random(palette));
	secondaryColor = "#0249da";

	for (let column = 0; column < columns; ++column) {
		truchet[column] = []; // create nested array
		for (let row = 0; row < rows; ++row) {
			truchet[column][row] = new Tile(TILE_SIZE, primaryColor, secondaryColor);
		}
	}
}

function draw() {
	//noLoop();

    if (frameCount % 60 == 1) {
        //clear();
        if (frameCount == 1) {
            for (let column = 0; column < columns; ++column) {
                for (let row = 0; row < rows; ++row) {
                    let rotateShape = round(random());
                    // print(rotateShape);
                    truchet[column][row].draw((column + 1) * TILE_SIZE, (row + 1) * TILE_SIZE, rotateShape);
                }
            }
        } else {
            for (let column = 0; column < columns; ++column) {
                for (let row = 0; row < rows; ++row) {
                    let rotateShape = round(random());
                    if (random() < 0.25) {
                        truchet[column][row].draw((column + 1) * TILE_SIZE, (row + 1) * TILE_SIZE, rotateShape);
                    }
                }
            }
        }
        
    }
}

class Tile {
	constructor(size, primaryColor, secondaryColor) {
		this.size = size;
		this.primaryColor = primaryColor;
		this.secondaryColor = secondaryColor;
	}

	// TODO: refactor
	/*
	// x 				=> x position of the tile
	// y 				=> y position of the tile
	// rotated 	=> bool, true rotates the inside arcs 180°
	*/
	draw(x, y, rotated) {
		// create a new drawing state
		push();

		noStroke();
		translate(x - (this.size / 2), y - (this.size / 2));

		fill(this.secondaryColor);
		square(0, 0, this.size);

		if (rotated) {
			rotate(HALF_PI);
			translate(0, -this.size);
		}
		fill(this.primaryColor);
		// top left arc
        fill("#ffffff");
		arc(0, 0, this.size * 4 / 3, this.size * 4 / 3, 0, HALF_PI);
		//circle(this.size / 2, 0, this.size / 3);
		//circle(0, this.size / 2, this.size / 3);

		// bottom right arc
        fill(this.primaryColor);
        stroke("#ffffff")
        strokeWeight(1)
		arc(this.size, this.size, this.size * 4 / 3, this.size * 4 / 3, PI, 3 * HALF_PI);
        noStroke()
		//circle(this.size, this.size / 2, this.size / 3);
		//circle(this.size / 2, this.size, this.size / 3);

		// white circles in 4 corners
		fill(this.secondaryColor);
		circle(0, 0, this.size * 2 / 3);
		circle(this.size, 0, this.size * 2 / 3);
		circle(0, this.size, this.size * 2 / 3);
		circle(this.size, this.size, this.size * 2 / 3);
        
		// restore original draw settings
		pop();
	}
}