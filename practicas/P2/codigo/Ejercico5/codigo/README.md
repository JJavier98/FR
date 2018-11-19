# simple-ftp
Simple FTP emulation based on TCP Sockets

## Usage
```
python3 client.py/server.py [args]
```

### Client
```
usage: client.py [-h] [--port PORT] remote

Simple FTP client

positional arguments:
  remote       remote ftp server to establish a connection

optional arguments:
  -h, --help   show this help message and exit
  --port PORT  default=21

Command list: get, put, pwd, ls, cd, cdup, delete, mkdir, rmdir
```

### Server
```
usage: server.py [-h] [--port PORT]

Simple FTP server

optional arguments:
  -h, --help   show this help message and exit
  --port PORT  default=21
```
