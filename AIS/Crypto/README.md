# Crypto
## 15pts: [ROT]
Rotation cipher challenge.

1. Copy the text and use https://rot13.com/
2. Cycle through the drop down options

## 25pts: [Encoded]
Encoding is not cryptography!

1. Base64 encoded string.
2. Decode: `echo -n 'base64_string_here' | base64 -d > out.file`
3. Find the file format:
   ```sh
   file out.tmp
   out.file: bzip2 compressed data, block size = 900k
   ```
4. Decompress:
   ```sh
   mv out.file out.file.bz2
   bzip2 -vd out.file.bz2
     out.file.bz2: done

   file out.file
   out.file: ASCII text, with no line terminators
   ```
5. View contents: `cat out.file` (Output is a binary string)
6. Convert the string to ASCII. Output is in Hex, See: `convert.sh` (There are plenty of online converters)
7. Convert Hex to ASCII: `echo HexStringHere | perl -ne 's/([0-9a-f]{2})/print chr hex $1/gie'`

## 75pts: [Base64]
Can you even base64?

1. Copy the base64 text into a file and decode. `cat b64.txt | base64 -d | strings` You will get a Hint.
2. Create the docx file: `cat b64.txt | base64 -d > out-file.docx`
3. Unzip the file: `unzip out-file.docx` (Note the extracted files: `flag.txt` and `xor_key.txt`)
4. Using an online XOR tool: https://www.dcode.fr/xor-cipher (Work smarter, Not harder?)
    - Text to be XORed: `flag.txt`
    - Use the ascii key: `xor_key.txt`

## 100pts: [ENIGMA]
Decrypt an Enigma I encrypted message.
* I haven't solved this one yet. The following are just some notes.

1. Challenge Hints can be found by opening the DevTools Console.
2. While plugboard, rotor positions, and reflector information is there in the Hints
    - https://pypi.org/project/py-enigma/
    - https://www.dcode.fr/enigma-machine-cipher
    - https://www.cachesleuth.com/enigma.html
    - https://cryptii.com/pipes/enigma-machine

## 300pts: [XOR]
XOR crypto challenge. Hint: Key Length: 6

1. Copy text, go to https://www.dcode.fr/xor-cipher
2. Brute, Key size 6
3. May have to Run it a few times, The key will be a hex encoded string
4. Convert hex to Ascii: `echo HexStringHere | perl -ne 's/([0-9a-f]{2})/print chr hex $1/gie'`

