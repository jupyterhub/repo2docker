"""
Test Port mappings work on running non-jupyter workflows
"""
import subprocess
import requests
import time
import os
import tempfile
import signal
import random


def read_port_mapping_response(host, port, protocol = None):
    """
    Deploy container and test if port mappings work as expected

    Args:
        host: the host interface to bind to.
        port: the random host port to bind to
        protocol: the protocol to use valid values /tcp or /udp
    """
    builddir = os.path.dirname(__file__)
    port_protocol = '8000'
    if protocol:
        port_protocol += protocol
    host_port = port
    if host:
        host_port = host + ':' + port
    else:
        host = 'localhost'
    with tempfile.TemporaryDirectory() as tmpdir:
        username = os.getlogin()

        # Deploy a test container using r2d in a subprocess
        # Added the -v volumes to be able to poll for changes within the container from the
        # host (In this case container starting up)
        proc = subprocess.Popen(['repo2docker',
                                 '-p',
                                 host_port + ':' + port_protocol,
                                 '-v', '{}:/home'.format(tmpdir),
                                 '--user-id', str(os.geteuid()),
                                 '--user-name', username,
                                 '.',
                                 '/bin/bash', '-c', 'echo \'hi\' > /home/ts && python -m http.server 8000'],
                                 cwd=builddir + "/../",
                                 stderr=subprocess.STDOUT)
        try:
            # Wait till docker builds image and starts up
            while not os.path.exists(os.path.join(tmpdir, 'ts')):
                if proc.poll() is not None:
                    # Break loop on errors from the subprocess
                    raise Exception("Process running r2d exited")

            # Sleep to wait for python http server to start
            time.sleep(20)
            resp = requests.request("GET", 'http://' + host + ':' + port)

            # Check if the response is correct
            assert b'Directory listing' in resp.content
        finally:
            if proc.poll() is None:
                # If the subprocess running the container is still running, interrupt it to close it
                os.kill(proc.pid, signal.SIGINT)
                time.sleep(10)


def test_all_port_mapping_response():
    """
    Deploy container and test if all port expose works as expected
    """
    builddir = os.path.dirname(__file__)
    with tempfile.TemporaryDirectory() as tmpdir:
        username = os.getlogin()

        # Deploy a test container using r2d in a subprocess
        # Added the -v volumes to be able to poll for changes within the container from the
        # host (In this case container starting up)
        proc = subprocess.Popen(['repo2docker',
                                 "--image-name",
                                 "testallport:0.1",
                                 '-P',
                                 '-v', '{}:/home'.format(tmpdir),
                                 '--user-id', str(os.geteuid()),
                                 '--user-name', username,
                                 '.',
                                 '/bin/bash', '-c', 'echo \'hi\' > /home/ts && python -m http.server 52000'],
                                 cwd=builddir + "/../",
                                 stderr=subprocess.STDOUT)

        try:
            # Wait till docker builds image and starts up
            while not os.path.exists(os.path.join(tmpdir, 'ts')):
                if proc.poll() is not None:
                    # Break loop on errors from the subprocess
                    raise Exception("Process running r2d exited")

            # Sleep to wait for python http server to start
            time.sleep(20)
            port = subprocess.check_output("docker ps -f ancestor=testallport:0.1 --format '{{.Ports}}' | cut -f 1 -d - | cut -d: -f 2",
                                            shell=True).decode("utf-8")
            port = port.strip("\n\t")
            resp = requests.request("GET", 'http://localhost' + ':' + port)

            # Check if the response is correct
            assert b'Directory listing' in resp.content
        finally:
            if proc.poll() is None:
                # If the subprocess running the container is still running, interrupt it to close it
                os.kill(proc.pid, signal.SIGINT)
                time.sleep(10)


def test_port_mapping_random_port():
    """
    Test a simple random port bind
    """
    port = str(random.randint(50000, 51000))
    host = None
    read_port_mapping_response(host, port)


def test_port_mapping_particular_interface():
    """
    Test if binding to a single interface is possible
    """
    port = str(random.randint(50000, 51000))
    host = '127.0.0.1'
    read_port_mapping_response(host, port)


def test_port_mapping_protocol():
    """
    Test if a particular protocol can be used
    """
    port = str(random.randint(50000, 51000))
    host = None
    read_port_mapping_response(host, port, '/tcp')
