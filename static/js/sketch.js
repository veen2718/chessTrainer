console.log("sketch.js")

let i;
let text0;
let col;
let images = {};

let colors = ["w","b"]
let pieces = ["b","k","n","p","q","r"]

col = c1;
text0 = "0"

let click = 0; //If click is 0 => clicking a square will trigger possible moves if a piece is there, if click is 1 => clicking a square will try to move a piece if possible

let board = new Array(8);
for (let i = 0; i < board.length; i++) {
    board[i] = new Array(8).fill(null);
}

let legalMoves = []

function preload(){
  
  for(i = 0; i < 2;i++){
    for(j = 0; j < 6;j++){
      var c = colors[i]
      var p = pieces[j]
      images[`${c}${p}`] = loadImage(`/static/assets/${c}${p}.png`)
    }
  }
  console.log(images,'images')
}




function setup() {
  
  createCanvas(windowWidth,windowHeight);
  i = 0
  console.log(i, "i")
  post('/setup',[squareSize])
  getReq('/setupMoves').then(data => {
    board=data
    console.table(board)
    console.log(board[0],"board[0]")
  })

  let quitButton = createButton('Quit')
  quitButton.position(squareSize * 9, squareSize * 8)
  quitButton.mousePressed(function(){
    post('/shutdown')
  })
  

  let backButton = createButton('Back')
  backButton.position(squareSize * 9.5, squareSize * 8)
  backButton.mousePressed(function(){
    getReq('/back').then(data =>{
      board=data
      redraw()
      console.log("\n\n\n\n")
      console.table(board)
      console.table(data)
    })
  })

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
  for(let i = 0; i < 8; i++){
    for(let j = 0; j < 8; j++){
      if(board){
        var piece = board[i][j]
        //console.log(piece)
        if(piece != null){
          //console.log(piece,"piece")
          image(images[piece.id], piece.x,piece.y, squareSize, squareSize)
          //console.log(piece.id,piece.x,piece.y,squareSize, squareSize)
        }else{
          //console.log(piece,"piece is null")
        }
        //
      }
    }
  }
  fill(...c3)
  for(let i = 0; i < legalMoves.length; i++){
    cxy = legalMoves[i]
      ellipse(cxy[0],cxy[1],circleSize,circleSize)
      //console.log('drawing Ellipse',cxy[0],cxy[1])

  }
 
}


async function post(path, data,wait = true){
  const response = await fetch(path, {
    method:'POST',
    headers: {'Content-Type': 'application/json',},
    body: JSON.stringify(data)
  })
  if(wait){
  const result = await response.json();
  console.log(result,"0")
  return result
}
}

async function getReq(path){
  const response = await fetch(path)
  const data = await response.json();
  console.log(data)
  return data
}

function mouseClicked(){
  if(mouseX <= 8*squareSize && mouseY <= 8*squareSize){
    post('/click_at',[mouseX,mouseY],true).then(data =>{
      allData = data
      legalMoves = allData[0]
      board = allData[1]
      console.log("legalMoves:",legalMoves)
      console.table(legalMoves)
      console.log("board")
      console.table(board)
    })
  }
  
  
}

