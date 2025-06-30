import sys
import socket
import time

HOST = 'localhost' 
PORT = 13666       
SCREEN_DURATION = 5

def send_command(sock, command):
    """Sends a command to LCDd and returns the response."""
    try:
        sock.sendall((command + '\n').encode('utf-8'))
        response = sock.recv(1024).decode('utf-8').strip()
        return response
    except socket.error as e:
        print(f"Socket error during send/receive: {e}")
        return None

def main():
    sock = None
    try:
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print(f"Connected to LCDd on {HOST}:{PORT}")
        
        send_command(sock, "hello")
        send_command(sock, "client_set name conky_lcd_client")

        screen_id = 'conky_info_screen'

        send_command(sock, f'screen_add {screen_id}')
        send_command(
            sock,
            f'screen_set {screen_id} -name "Conky Info" -priority 255 -duration {SCREEN_DURATION} -heartbeat off'
        )

        for i in range(1, 6):
            send_command(sock, f'widget_add {screen_id} line{i} string')

        print("Starting LCD client, waiting for Conky data via stdin...")

        line_buffer = []

        for raw_line in sys.stdin:
            processed_line = raw_line.strip()
            if processed_line:
                line_buffer.append(processed_line)
                
                if len(line_buffer) == 5:
                    for idx, text in enumerate(line_buffer):

                        if len(text) > 20:
                            text = text[:20]

                        send_command(
                            sock,
                            f'widget_set {screen_id} line{idx+1} 1 {idx+1} "{text}"'
                        )

                    line_buffer = []

    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    except ConnectionRefusedError:
        print(f"Error: Could not connect to LCDd on {HOST}:{PORT}. Make sure LCDd is running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if sock:
            print("Closing connection to LCDd.")
            sock.close()

if __name__ == '__main__':
    main()