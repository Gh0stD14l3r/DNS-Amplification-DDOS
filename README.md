This DDoS attack is a reflection-based volumetric distributed denial-of-service (DDoS) attack in
which an attacker leverages the functionality of open DNS resolvers in order to overwhelm a 
target server or network with an amplified amount of traffic, rendering the server and its 
surrounding infrastructure inaccessible.

## Basic Info
```
### DNS Servers List
You dont need your own list of spoofable DNS servers. This script will grab 
all public DNS servers and checks each one if its spoofable or not

### Multithreading
This script is multithreaded for the attack. Each request is sent with a 500ms
delay between them. Each DNS server is given to its own thread.
```


## Installation
```
- Download or Clone the repository
- Install requirements
-- pip install scapy
-- pip install wget
```


## Usage
```
python dns-ddos.py host_url -p port_number -t max_threads
```

![image](https://user-images.githubusercontent.com/38970826/227402397-f8a52c4c-26dd-45ee-9b59-d26147910f05.png)
