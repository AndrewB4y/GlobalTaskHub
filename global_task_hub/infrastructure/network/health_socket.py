import socket


def check_health(host: str = "google.com", port: int = 80) -> bool:
    """
    Perform a simple socket handshake to check connectivity.
    """
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)  # Set timeout to 2 seconds

        # Connection to hostname on the port.
        s.connect((host, port))

        # Receive no more than 1024 bytes
        # Just connecting is often enough for a handshake check in this context,
        # but we can try to send a simple HEAD request if strictly HTTP,
        # but the requirement is "native socket handshake".

        s.close()
        return True
    except (socket.timeout, socket.error):
        return False


if __name__ == "__main__":
    is_healthy = check_health()
    print(f"Network Health: {'Online' if is_healthy else 'Offline'}")
