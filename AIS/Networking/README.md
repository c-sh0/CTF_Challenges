# Networking
### 15pts: [HTTP Basic]
Find the username and password in the PCAP

1. Download the packet capture:
     ```wget https://hack.ainfosec.com/static/hackerchallenge/bin/http_auth/http-auth.cap```

2. Run tcpdump, port 80, ascii output, grep for "pass":
     ```tcpdump -r ./http-auth.cap -s 0 -A tcp port 80  | grep pass```
    
### 30pts: [WPA2 Deauth]
Crack the WPA2 password using the PCAP

1. Download the packet capture:
     ```wget https://hack.ainfosec.com/static/hackerchallenge/bin/wpa_deauth/de-auth.cap```

2. Find the BSSID:
    ```tcpdump -e -r ./de-auth.cap | grep BSSID | head -1```
    
3. Download wordlist for cracking:
     ```sh
     wget http://downloads.skullsecurity.org/passwords/rockyou.txt.bz2
     bzip2 -d rockyou.txt.bz2
     ```
4. Using aircrack-ng:
    ```sh
    git clone https://github.com/aircrack-ng/aircrack-ng
    cd aircrack-ng
    autoreconf -i
    ./configure
    make 
    ./aircrack-ng -w rockyou.txt -b 7c:8b:ca:cb:d7:82 de-auth.cap
    ```

