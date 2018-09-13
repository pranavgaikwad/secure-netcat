# Secure Net Cat

Netcat application with AES & HMAC  <br/>

## Installation & Usage

### Requirements

- Python 2.7

- python-argparse 

### Usage

Start **snc server** using following command

```sh
python snc.py --key ENCRYPTION_KEY -l PORT  
```

Start **snc client** using following command

```sh
python snc.py --key ENCRYPTION_KEY SERVER PORT
```

stdout / stdin can be redirected to file using 

```sh
python snc.py --key ENCRYPTION_KEY -l PORT < INPUT_FILE > OUTPUT_FILE
```

similarly, for client, 

```sh
python snc.py --key ENCRYPTION_KEY SERVER PORT < INPUT_FILE > OUTPUT_FILE
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