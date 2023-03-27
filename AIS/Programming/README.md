# Programming
### 15pts: [Brutal Force]
Submit the correct PIN to proceed (3 - 4 digits long).

1. Open DevTools, Submit an invalid PIN, Note the `pin_hash` value returned in the JSON Response
2. Determine the hash type: https://www.tunnelsup.com/hash-analyzer/ `SHA2-256`
3. Using a simple shell script and `openssl`, iterate and hash all 3-4 digits looking for a match. See `brutal-force.sh`

### 150pts: [Code Breaker]
*Break the alpha-numeric code like in spy movies. Each guess returns a score. The higher the score the more characters you have correct and in the correct position*.

Submit your guesses (code is 7 alpha-numeric characters long).

1. Discover valid characters. This can be done by submitting the same character and observe the returned score. Valid characters will have a non-zero score, for example:
   ```sh
   0000000 = score: 0.0
   AAAAAAA = score: 28.571....
   BBBBBBB = score: 0.0
   ccccccc = score: 0.0
   ...
   ```
2. Discover valid character positions. Since `0000000` returns a zero value, we can use this as a mask to determine valid character positions, for example:
   ```sh
   A000000 = score: 0.0
   0A00000 = score: 14.285...
   00A0000 = score: 0.0
   000A000 = score: 14.285...
   0000A00 = score: 0.0
   00000A0 = score: 0.0
   000000A = score: 0.0
   ...
   ```
3. See `code-breaker.sh`

### 250pts: [Tiles]
Slide fast...There's not much time. (The puzzle will reset/change when the timer runs out)

1. There is a NodeJS package available to solve this. (Work smarter not harder?)
2. Visit: https://www.npmjs.com/package/slide-puzzle-solver/v/1.0.2
3. Click on Run (RunKit): https://npm.runkit.com/slide-puzzle-solver
4. Copy the tiles matrix into a text file for parsing. This will be used to convert the tiles matrix into a usable array: <br>
   `cat tiles.txt | sed -e 's/|/,/g' -e 's/^,/[/g' -e 's/,$/],/g' | sed -s "s/X/'X'/g"`
5. Copy the output into the following RunKit code template:
   ```sh
   const { solve } = require("slide-puzzle-solver")
   const steps = []
   const puzzle = [
        <... parsed tiles matrix here ...>
   ]
   const solvedPuzzle = solve(puzzle, steps)
   console.log(steps)
   ```
6. Click run
7. Click to expand the array, copy/paste into an new file and parse: <br>
   `cat steps.txt | awk '{print $2}' | sed -e 's/^"//g' | sed -e 's/"$/,/g' | tr -d '\n'`
8. Paste result to solve the puzzle.

