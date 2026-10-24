# bldchecker
A tool for practicing checking blindfolded Rubik's Cube solutions. Uses the Speffz lettering notation.
## Install
Download and run the exe.
## How to use
You can provide a scramble into the scramble text box. Pressing the "scramble" button will then scramble the cube on screen to match.  
Scrambles must adhere to the following format:
- Only single-layer moves are allowed (R,L,U,D,F,B). Only the move suffixes `2` and `'` are allowed (ex: `R2` and `R'` are legal moves).
- Rotation notation is not recognized.
- Individual moves must be separated by a space (Ex: `R U R'` is valid, but `RUR'` is not).
- Any scramble that is pasted from the default 3x3 category of csTimer will be a valid scramble.
  
Solutions must adhere to the following format:
- Pieces are notated using the Speffz lettering notation.
  - For edges, B is the buffer piece.
  - For corners, A is the buffer piece.
- Edges are entered first, followed by corners. A new line denotes the change from edges to corners.
- Whitespace is allowed (besides `\n`)
    
The following shows an example of a valid solution input:
```
NOWIGLUPHAEA
PSMBFLKV
```
The "Reset Cube" button resets the cube to a solved state.
## Hotkeys
`W`/`S`: Rotate around the X axis  
`A`/`D`: Rotate around the Y axis  
`Q`/`E`: Rotate around the Z axis  
`R`: Reset camera  
`Esc`: Quit  
