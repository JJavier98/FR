import argparse
from os import getcwd
from os.path import isfile, isdir, join
from common import BUFFER_SIZE, SocketWrapper
from server import COMMANDS


def put_available(file, socket):
    """Checks if the file exists and sends a 'put' command to the server.
    If the response is empty everything is OK and returns (True, ''), if not,
    return (False, response)"""
    filepath = join(getcwd(), file)
    if not isfile(filepath):
        return (False, 'File not found')
    response = send_command_and_wait_response(socket, 'put ' + file)
    if response:
        return (False, response)
    return (True, '')


# get <archivo> <archivo1>
def get_available(msg, socket):
    """Checks if the file is not a directory and sends a 'get' command to the server.
    If the response is empty everything is OK and returns (True, ''), if not,
    return (False, response)"""
    file = msg.split(' ')[-1]
    filepath = join(getcwd(), file)
    if isdir(filepath):
        return (False, 'Error. A directory with the same name already exists')
    response = send_command_and_wait_response(socket, msg)
    if response:
        return (False, response)
    return (True, '')


def try_put(file, socket):
    """Checks if put command is available for the given file and in that case,
    sends the file to the server"""
    (available, error_msg) = put_available(file, socket)
    if available:
        socket.send_file(join(getcwd(), file))
    else:
        print(error_msg)


def try_get(msg, socket):
    """Checks if get command is available for the given file and in that case,
    retreive the file to the server"""
    (available, error_msg) = get_available(msg, socket)
    if available:
        socket.receive_file(base_dir=getcwd())
    else:
        print(error_msg)


def send_command_and_wait_response(socket, msg):
    """Sends a command to the server and wait for the response.
    Returns that response."""
    socket.send(msg)
    response_size = int(socket.receive())
    response = ''
    if response_size < 0:
        response = 'Command not valid'
    else:
        for _ in range(int(response_size / BUFFER_SIZE) + 1):
            response = response + socket.receive()
    return response


def is_put_valid_sintax(words):
    return words[0] == 'put' and len(words) == 2


def is_get_valid_sintax(words):
    length = len(words)
    return words[0] == 'get' and (length in (2, 3))


def process_command(msg, socket):
    """"Sends a command to the server making distinction.
    if command is put -> try put
    if command is get -> receive file
    otherwise -> send command"""
    msg = msg.strip()  # Cleaning message
    words = msg.split()  # Splitting into words to process it efficiently
    if is_put_valid_sintax(words):
        try_put(words[1].strip(' '), socket)
    elif is_get_valid_sintax(words):
        try_get(msg, socket)
    else:
        response = send_command_and_wait_response(socket, msg)
        if response:
            print(response)


def connection_loop(socket):
    """Infinite loop that process input and execute commands."""
    while True:
        msg = input('ftp> ')
        msg = msg.strip()
        if msg == 'exit':
            break
        if msg:
            process_command(msg, socket)


def main(args):
    client_socket = SocketWrapper()
    client_socket.connect(args.host[0], int(args.port))
    connection_loop(client_socket)
    client_socket.close()


if __name__ == '__main__':
    EPILOG = 'Command list:\n' + ',\t'.join(COMMANDS.keys())
    PARSER = argparse.ArgumentParser(
        description='Simple FTP client', epilog=EPILOG)
    PARSER.add_argument(
        'host', nargs=1, help='host ftp server to establish a connection')
    PARSER.add_argument('--port', help='default=2121', default='2121')
    main(PARSER.parse_args())
