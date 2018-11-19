from os import listdir, getcwd, remove
from os import mkdir as _mkdir
from os.path import isfile, join, isdir
from pathlib import Path
import socket
import argparse
from collections import defaultdict
import shutil
from typing import MutableMapping
from common import wrap_message, SocketWrapper

pwds: MutableMapping[str, str] = defaultdict(getcwd)
current_client_address: str
receiving_file: bool = False
sending_filepath: str = ''
sending_file_newname: str


def get_pwd() -> str:
    return pwds[current_client_address]


def cdup() -> str:
    pwds[current_client_address] = str(Path(get_pwd()).parent)
    return ''


def cd(new_dir) -> str:
    if new_dir == '.':
        return ''
    if new_dir == '..':
        return cdup()
    path = join(get_pwd(), new_dir)
    if isdir(path):
        pwds[current_client_address] = path
        return ''
    return 'Directory not found'


def ls(dir=None) -> str:
    response = ''
    if dir:
        path = join(get_pwd(), dir)
        if isdir(path):
            response = '\n'.join(listdir(path))
        else:
            response = '{} is not a directory'.format(dir)
    else:
        response = '\n'.join(listdir(get_pwd()))
    return response


def pwd() -> str:
    return get_pwd()


def mkdir(new_dir) -> str:
    dirpath = join(get_pwd(), new_dir)
    if isdir(dirpath):
        return 'There is already a directory or file with the same name.'
    _mkdir(dirpath)
    return ''


def delete(file) -> str:
    path = join(get_pwd(), file)
    if isdir(path):
        return 'Directories cannot be deleted. Use rmdir instead.'
    if not isfile(path):
        return 'File not found'
    remove(path)
    return ''


def get(file, new_name=None) -> str:
    global sending_filepath, sending_file_newname
    filepath = join(get_pwd(), file)
    if isfile(filepath):
        sending_filepath = filepath
        sending_file_newname = new_name
        return ''
    return 'File not found'


def rmdir(dir) -> str:
    dirpath = join(get_pwd(), dir)
    if isdir(dirpath):
        shutil.rmtree(dirpath)
        return ''
    return '{} is not a directory'.format(dir)


def put(file) -> str:
    global receiving_file
    filepath = join(get_pwd(), file)
    if isdir(filepath):
        return 'A directory with the same name already exists. It cannot be overriden'
    receiving_file = True
    return ''


COMMANDS = {
    'get': get,
    'put': put,
    'pwd': pwd,
    'ls': ls,
    'cd': cd,
    'cdup': cdup,
    'delete': delete,
    'mkdir': mkdir,
    'rmdir': rmdir,
}


def process_command(cmd, args):
    result = None
    if cmd in COMMANDS.keys():
        result = wrap_message(COMMANDS[cmd])(*args)
    return result


def connection_loop(client_socket):
    global sending_filepath, receiving_file
    while True:
        # Receive client request
        msg = client_socket.receive()
        if msg:
            msg_list = msg.split(' ')
            response = process_command(msg_list[0], msg_list[1:])
            if response:
                response_generator = response[0]
                # Send response size to client
                client_socket.send(response[1])
                # Send actual response
                for data in response_generator:
                    client_socket.send(data)
            else:
                client_socket.send(-1)
            if receiving_file:
                client_socket.receive_file(base_dir=get_pwd(), verbose=False)
                receiving_file = False
            if sending_filepath != '':
                client_socket.send_file(
                    sending_filepath, sending_file_newname, verbose=False)
                sending_filepath = ''
        else:
            break


def listening_loop(server_socket):
    global current_client_address, receiving_file, sending_filepath
    while True:
        (client_socket, address) = server_socket.accept()
        client_socket = SocketWrapper(client_socket)
        print("New connection {}".format(address))
        pwds[address] = getcwd()
        current_client_address = address[0]
        try:
            connection_loop(client_socket)
        finally:
            receiving_file = False
            sending_filepath = ''
            client_socket.close()


def main(args):
    """Program entry point"""
    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Force OS to reuse socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind the socket to a public host, and a well-known port
    server_socket.bind(('', int(args.port)))
    # become a server socket
    server_socket.listen(1)
    print('Running on 127.0.0.1 : {}'.format(args.port))
    # Run loop to listen iteratively to clients
    listening_loop(server_socket)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Simple FTP server')
    PARSER.add_argument('--port', help='default=2121', default='2121')
    main(PARSER.parse_args())
