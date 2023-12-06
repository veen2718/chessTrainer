colors = ["w","b"]
pieces = ["b","k","n","p","q","r"]

for col in colors:
    for piece in pieces:
        print(f"{col}{piece} = loadImage(/static/assets/{col}{piece}.png)")