console.log("sketch.js")

let i;
let text0;
let col;
col = c1;
text0 = "0"
function setup() {
  createCanvas(windowWidth,windowHeight);
  i = 0
  console.log(i, "i")
}

function draw() {
  background(220);
  for(let i = 0;i < 8; i++){
    if(col == c2){
      col = c1
    }else{
      col = c2
    }
    for(let j = 0;j < 8; j++){
      fill(...col)
      rect(squareSize *i, squareSize *j, squareSize, squareSize);
      if(col == c2){
        col = c1
      }else{
        col = c2
      }
    }
  }



  
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