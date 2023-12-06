console.log("sketch.js")

let i;
let text0;
text0 = "0"
function setup() {
  createCanvas(windowWidth,windowHeight);
  i = 0
  console.log(i, "i")
}

function draw() {
  background(220);
  rect(i,0,50,50)
  text(text0,100,100)
}


async function post(path, data){
  const response = await fetch(path, {
    method:'POST',
    headers: {'Content-Type': 'application/json',},
    body: JSON.stringify(data)
  })
  const result = await response.json();
  console.log(result,"0")
  text0 = result
}


function mouseClicked(){
  post('/get_moves',[mouseX,mouseY])
}