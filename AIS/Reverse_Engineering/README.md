# Reverse Engineering
Anytime you run across these types of challenges
* Disable Address Space Layout Randomization (ASLR)
* Set ulimit to `unlimited` for core file generation
* Disable SELinux
   ```sh
    sysctl kernel.randomize_va_space=0
    ulimit -S -c unlimited > /dev/null 2>&1
    setenforce 0
   ```

## 100pts: [Sentence Bot]
It's not very good at sentences.
* Using `strings` shows nothing obvious
* Debugger: https://github.com/radareorg/radare2

1. Run program under a debugger (using `radare2`):
   ```sh
     r2 -d ./sentencebot
     [0x00400a70]> aaaaa
   ```
2. Go into visual mode looking for clues:
   ```sh
     [0x000001e8]> v

     [X] Disassembly
      ...
     int main()
        - argument "--set-seed"
        - argument "--debug"
        - "Searching..."
        - sym.generateSentence()
        - "Seed:"

     sym.generateSentence();
        - sym.getFlag();
            - de:ad:be:ef:fa:ce
            - Mac Address: %s\n"
      ...
   ```
   * Note the `--set-seed` and `--debug` arguments
   * `de:ad:be:ef:fa:ce` looks like a MAC address?

3. Run with `--debug` argument gives:
   ```sh
    ./sentencebot --debug
    Searching...
    Mac Address: 00:00:00:00:00:00
    Seed: 19016
   ```
4. Running the program through `strace`, we can it's it's looking at the MAC address on the loopback interface:
   ```sh
     strace -f -s4028 ./sentencebot --debug
     ...
     openat(AT_FDCWD, "/sys/class/net/lo/address", O_RDONLY) = 3
     fstat(3, {st_mode=S_IFREG|0444, st_size=4096, ...}) = 0
     read(3, "00:00:00:00:00:00\n", 4096)    = 18
     ...
   ```
5. What happens if we change the MAC address on lo interface to `de:ad:be:ef:fa:ce` and re-run program?:
   ```sh
     ip link set dev lo address de:ad:be:ef:fa:ce

     ./sentencebot --debug
     Searching...
     Mac Address: de:ad:be:ef:fa:ce
     Seed: 19016
   ```
6. What happens if we run the program again with `--set-seed` argument using the above seed value?:
   ```sh
     ./sentencebot --set-seed 19016
     You win!
     Mac Address: de:ad:be:ef:fa:ce
     The flag is ...flag{}....
   ```
   Win!

## 250pts: [License Key]
Reverse the license key validation binary

1. DevTools Console, Hint: <br> `Don't try to reverse the key generation function and most definitely don't try to bypass it.`
2. Running `strings` on the binary doesn't reveal anything interesting.
3. Key appears to have a max length of 16 characters? (indicated by error messages):
   ```sh
      ./license_key_easy
      License key: 12345678901234567
      Checking key: 12345678901234567
      invalid key

      ./license_key_easy
      License key: 1234567890123456
      Checking key: 1234567890123456
      incorrect key
   ```
3. Run program under a debugger looking for clues (using `radare2`):
    - Is bypassing the key checking function *REALLY* cheating if you learn something new? I say No! ;-P
4. Run through `radare2` debugger (write mode) and view execution flow:
   ```sh
     r2 -Aw ./license_key_easy
     [0x00400a50]> s main
     [0x00400a50]> pdf
   ```
5. Just before `"invalid key"` is printed, there is a jump instruction:
   ```sh
     ...
      ┌─< 0x00400cca      7f16           jg 0x400ce2  <----- HERE (jg: jump if value is greater)

      │   0x00400ccc      488d3d7ab30a.  lea rdi, str.invalid_key    ; 0x4ac04d ; "invalid key"
      │   0x00400cd3      e828fa0000     call sym.puts               ; int puts(const char *s)
      │   0x00400cd8      b8ffffffff     mov eax, 0xffffffff         ; -1
     ┌──< 0x00400cdd      e9ba000000     jmp 0x400d9c

     ...
   ```
6. We want to jump into "you got a flag!" function:
   ```sh
    │││   ; CODE XREF from main @ 0x400d23(x)
    ││└─> 0x00400d38      488d85e0fbff.  lea rax, [var_420h] <-------- HERE
    ││    0x00400d3f      beefbeadde     mov esi, 0xdeadbeef
    ││    0x00400d44      4889c7         mov rdi, rax
    ││    0x00400d47      e821feffff     call sym.generate_table
    ││    0x00400d4c      488d85e0fbff.  lea rax, [var_420h]
    ││    0x00400d53      b924000000     mov ecx, 0x24               ; '$' ; 36
    ││    0x00400d58      488d1509b30a.  lea rdx, str.AIS_Basic_Keygen_Flag__No_Cheating__ ; 0x4ac068 ; "AIS Basic Keygen Flag (No Cheating!)"
   ```
7. Verify address of the conditional jump:
   ```sh
     [0x00400c56]> ao @ 0x00400cca
     address: 0x400cca
     opcode: jg 0x400ce2
   ```
8. Modify the instruction: <br>
https://research.checkpoint.com/2019/deobfuscating-apt32-flow-graphs-with-cutter-and-radare2/<br>
*"Unlike the `wa <instruction> @ <addr>` command to overwrite an instruction with another instruction, the `wai` command will fill the remaining bytes with NOP instructions. Thus, in a case where the JMP <addr> instruction we want to use is shorter than the current conditional-jump instruction, the remaining bytes will be replaced with NOPs."*
   ```sh
     [0x00400c56]> wai jmp 0x400d38 @ 0x00400cca
     INFO: Written 2 byte(s) ( jmp 0x400d38) = wx eb6c @ 0x00400cca
   ```
9. Double check the modified execution flow:
   ```sh
    [0x00400c56]> pdf
    ...
    │  ┌─< 0x00400cca      eb6c           jmp 0x400d38
    │  │   0x00400ccc      488d3d7ab30a.  lea rdi, str.invalid_key    ; 0x4ac04d ; "invalid key"
    │  │   0x00400cd3      e828fa0000     call sym.puts               ; int puts(const char *s)
    │  │   0x00400cd8      b8ffffffff     mov eax, 0xffffffff         ; -1
    ...
   ```
10. Run the modified program:
    ```sh
     [0x00400c56]> q

     ./license_key_easy
     License key: AAAAAAAAAAAAAAAAAAAAAAAAAAAAA
     Checking key: AAAAAAAAAAAAAAAA
     Congratulations, you got a flag!
     ...flag...
    ```

## 400pts: [Challenge Response]
Provide the correct response based on a challenge
* I haven't solved this one yet. The following are just some notes.

1. DevTools Console, Hint: <br> `When you run my software, you'll be given a challenge key that is only valid for 30 seconds.`
2. Resetting the local system date/time backwards in time (while loop, freeze the date/time), will prevent the program from issuing a new challenge key.

## 500pts: [Debug Me]
If you can.
* I haven't solved this one yet. The following are just some notes.
* Recommended reading: https://research.checkpoint.com/2019/deobfuscating-apt32-flow-graphs-with-cutter-and-radare2/

1. Download: `wget https://hack.ainfosec.com/static/hackerchallenge/bin/debugme/debugme`
2. Running the program:
   ```sh
     ./debugme
     I'm thinking of a number between 1 and 3000000.
     Guess it and I'll give up my secrets.
     12345
     Nope! Next time, try concentrating harder.
   ```
3. File is packed, looks like UPX?:
   ```sh
      strings debugme | grep -i 'packed\|Team'
      $Info: This file is packed with the     executable packer http://   .sf.net $
      $Id:     3.94 Copyright (C) 1996-2017 the     Team. All Rights Reserved. $

      yum install upx
      upx -f -d debugme
      ...
      upx: debugme: NotPackedException: not packed by UPX
   ```
4. What do other tools report:
   ```sh
     https://github.com/lcashdol/UPX
     ./upx_dec ../debugme
      ...
      Reading File :../debugme
      Missing required UPX Headers. Found 0


      https://github.com/horsicq/DIE-engine
      git clone --recursive https://github.com/horsicq/DIE-engine.git
      yum install qt5-qttools-devel qt5-qttools-common qt5-qttools qt5-qtscript qt5-qtscript-devel
      cd DIE-engine
      chmod 755 configure
      ./configure
      make
      make install

      diec -a ./debugme
      ELF64
      Operation system: Linux(-)[AMD64, 64-bit, EXEC]
   ```
5.  Unpack using `retdec` (It does not care about UPX magic strings):
   ```sh
      https://github.com/avast/retdec
      OS: CentOS 8
   
      dnf install graphviz zlib-devel pkg-config m4 libtool automake autoconf python3 openssl-devel openssl git make cmake gcc gcc-c++
      git clone https://github.com/avast/retdec.git
      cd retdec
      mkdir build && cd build
      cmake .. -DCMAKE_INSTALL_PREFIX=/opt/retdec
      make
      make install
      cd /opt/retdec

      retdec]# bin/retdec-unpacker -o debugme.out debugme
      [UPX] Detected NRV2E unpacking stub based on signature.
      [UPX] Started unpacking of file 'debugme'.
      [UPX] Unfiltering filter 0x0 with parameter 0.
      [UPX] Unpacking block at file offset 0x19c.
      [UPX] Unfiltering filter 0x49 with parameter 81.
      [UPX] Unpacking block at file offset 0x98611.
      [UPX] Unfiltering filter 0x0 with parameter 0.
      [UPX] Additional packed data detected at the end of the file.
      [UPX] Additional data are at file offset 0x9b0bc and have size of 0x744.
      [UPX] Unpacking block from additional data behind segment 0.
      [UPX] Unfiltering filter 0x0 with parameter 0.
      [UPX] Unpacking last block from additional data at the end of the file.
      [UPX] Unfiltering filter 0x0 with parameter 0.
      [UPX] Successfully unpacked 'debugme'!
   ```
6. What does `checksec` show?:
```sh
checksec --file=debugme.unpacked
RELRO          STACK CANARY     NX          PIE     RPATH     RUNPATH    Symbols    FORTIFY Fortified Fortifiable     FILE
Partial RELRO  No canary found  NX enabled  No PIE  No RPATH  No RUNPATH No Symbols No      0         0      debugme.unpacked
```
7. Running the unpacked binary through `radare2` and viewing the execution flow, there is a lot of junk/obfuscated `jump` instructions.

