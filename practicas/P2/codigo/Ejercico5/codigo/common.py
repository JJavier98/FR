from os.path import basename, getsize, join
from pathlib import Path
import math
from tqdm import tqdm
import socket

BUFFER_SIZE = 1024


def fill_bytearray(b_array):
    """Fills bytearray with 0 until having BUFFER_SIZE length"""
    length = len(b_array)
    if length < BUFFER_SIZE:
        return b_array + bytearray(BUFFER_SIZE - length)
    else:
        return b_array


def strip_trailing(b_array):
    """Remove trailing zeros"""
    return b_array.rstrip(b'\x00')


def encode_data(data):
    """Encode String into Bytestring representation"""
    return str(data).encode('utf_8')


def decode_data(encoded_data):
    """Extracts a String from encoded Bytestring"""
    return encoded_data.decode('utf_8')


def chunkstring(string, length):
    """Splits a string into chunks of given length"""
    return (string[0 + i:length + i] for i in range(0, len(string), length))


def wrap_message(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = 'FATAL. The following exception was thrown \n{}'.format(e)
        finally:
            if result:
                chunks = chunkstring(result, BUFFER_SIZE)
            else:
                chunks = ['']
            return (chunks, len(result))

    return wrapper


class SocketWrapper(object):
    """Docstring for SocketWrapper. """

    def __init__(self, _socket=None):
        if not _socket:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = _socket

    def connect(self, host, port):
        """Connects to a remote socket"""
        self.socket.connect((host, port))

    def close(self):
        self.socket.close()

    def send(self, data, encode=True):
        """Sends a message securely.
        Add trailing zeros to the msg to fill the buffer"""
        msg = encode_data(data) if encode else data
        msg = fill_bytearray(msg)
        totalsent = 0
        while totalsent < BUFFER_SIZE:
            sent = self.socket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive(self, decode=True):
        """Receives a message securely.
        Receives a message of BUFFER_SIZE and remove trailing zeros to
        save space"""
        chunks = []
        bytes_received = 0
        while bytes_received < BUFFER_SIZE:
            chunk = self.socket.recv(BUFFER_SIZE - bytes_received)
            if chunk == b'':
                break
            chunks.append(chunk)
            bytes_received = bytes_received + len(chunk)
        data = strip_trailing(b''.join(chunks))
        return decode_data(data) if decode else data

    def _receive_file(self, file_size, file, progress_bar):
        bytes_received = 0
        while bytes_received < file_size:
            data = self.socket.recv(file_size - bytes_received)
            data_length = len(data)
            bytes_received = bytes_received + data_length
            if data_length == 0:
                raise RuntimeError("socket connection broken")
            else:
                file.write(data)
                if progress_bar:
                    progress_bar.update(data_length)

    def receive_file(self, base_dir, verbose=True):
        file_size = int(self.receive())
        if file_size > 0:
            filename = self.receive()
            f = open(join(base_dir, filename), 'wb')
            progress_bar = None
            if verbose:
                progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)
            try:
                self._receive_file(file_size, f, progress_bar)
            finally:
                f.close()
            return True
        else:
            return False

    def _send_file(self, file_size, file, progress_bar):
        totalsent = 0
        while totalsent < file_size:
            data = file.read(BUFFER_SIZE)
            sent = self.socket.send(data)
            totalsent = totalsent + sent
            if sent == 0:
                raise RuntimeError("socket connection broken")
            else:
                if progress_bar:
                    progress_bar.update(sent)

    def send_file(self, filepath, new_name=None, verbose=True):
        file = basename(filepath)
        if not new_name:
            new_name = file
        if Path(filepath).exists():
            file_size = getsize(filepath)
            self.send(file_size)
            self.send(new_name)
            f = open(filepath, 'rb')
            progress_bar = None
            if verbose:
                progress_bar = tqdm(total=file_size, unit='B', unit_scale=True)
            try:
                self._send_file(file_size, f, progress_bar)
            finally:
                f.close()
            return True
        else:
            return False
