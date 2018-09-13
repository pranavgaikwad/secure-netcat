# Secure Net Cat

Netcat application with AES & HMAC  <br/>

## Installation & Usage

### Requirements

- Python 2.7

- python-argparse 

### Usage

Start **snc server** using following command

```sh
python snc.py --key <encryption_key> -l <port>  
```

Start **snc client** using following command

```sh
python snc.py --key <encryption_key> <server> <port>
```

stdout / stdin can be redirected to file using 

```sh
python snc.py --key <encryption_key> -l <port> < input_file > output_file
```

similarly, for client, 

```sh
python snc.py --key <encryption_key> <server> <port> < input_file > output_file
```

### Options

See following definitions for command line options available

```
usage: snc.py [-h] [-l] --key KEY server port

positional arguments:
  connection  Connection string in format [server] [port]

optional arguments:
  -h, --help  show this help message and exit
  -l          listen mode / start as client
  --key KEY   encryption key

```