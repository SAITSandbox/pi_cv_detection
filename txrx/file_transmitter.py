import base64, os, socket, shutil, time
from curses import raw
from datetime import datetime

class ClientListener():
    """
    Instantiate by declaring receive port, send port and an authorisation code that the client
    must send to egress data. Defaults to 5010, 5011 and 'go'.
    
    Activate by calling listen_for_client, with no arguments.
    """
    
    def __init__(self, recv_port=5010, send_port=5011, auth_code="go"):
        self.recv_port = recv_port
        self.send_port = send_port
        self.auth_code = auth_code
        
        self.all_files_sent = False
        self.client_found = False
        self.client_authorised = False
        self.files_to_send = []
        
        self.SEPARATOR = "<SEP>"
        self.BUFFER_SIZE = 1024

    def listen_for_client(self):
        """
        Listens for connection from a client (guy with device that will receive images/data)
        Once detected, with correct auth code, tells client how many files to expect.
        Client then requests files one by one.
        """    
        sending = False
        
        
        while True:
            print(f"client found: {self.client_found}")
            print(f"client authorised: {self.client_authorised}")
            
            if self.all_files_sent:
                break
            
            if sending:
                raw_message = client_socket.recv(self.BUFFER_SIZE).decode()
                if raw_message == "Bye":
                    self.all_files_sent = True
                else:
                    try:
                        print(f"send file {str(raw_message)}")
                        self.send_file(self.files_to_send[int(raw_message)])
                    except:
                        print(f"Unexpected message: {raw_message}")
            
            if not self.client_found:
                print("Wait for client")
                connection = socket.socket()
                connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                connection.bind(('0.0.0.0', self.recv_port))
                print("listening")
                connection.listen(5)
                
                client_socket, client_address = connection.accept()
                
                self.client_found = True
                print(f"{client_address[0]} connected")
            
            if not self.client_authorised:
                print("Wait for client auth...")
                raw_message = client_socket.recv(self.BUFFER_SIZE).decode()
                print(f"{client_address[0]}: {raw_message}")
                
                # to be used later if we are splitting messages up into packets
                # cleaned_message = raw_message.split(self.SEPARATOR)
                
                # if raw_message == self.auth_code:
                if raw_message == self.auth_code:
                    print("Auth code accepted - begin data transfer")
                    self.client_authorised = True
                    time.sleep(0.25)
                    self.send_msg(client_socket, "ready")
                    
                else:
                    print("Incorrect auth code - waiting for new client")
                    self.client_found = False
                    
            else:
                if not sending:
                    # wait to receive message to hang the while loop
                    print("Waiting for client ")
                    raw_message = client_socket.recv(self.BUFFER_SIZE).decode()
                    print(f"{client_address[0]}: {raw_message}")
                    
                    if raw_message == "Files":
                        self.files_to_send = ["not_sent/" + file for file in os.listdir("not_sent")]
                        self.send_msg(client_socket, f"{len(self.files_to_send)}")
                        time.sleep(1)
                        # self.send_data(client_socket)
                        sending = True                        
                    else:
                        print(raw_message)
                        # msg = input("Message: ")
                        # self.send_msg(client_socket, msg)
                
                    time.sleep(1)

    def send_msg(self, client_connection, msg, file=False):
        """
        For sending a short text message to the client
        Use to signal start/end of data streams or send commands
        Print to console if its not a filestring iot aid testing
        
        \r\n is the 'over' message to tell the java app the message is complete
        """
        
        if not file:
            print(f"sending: {msg}")
        client_connection.send(f"{msg}\r\n".encode())
        
    def send_file(self, filename, client_connection):
        """
        Sends an individual file in packets determined by buffer size, as a
        base64 encoded string
        """
        
        packets = 0
        
        with open(filename, "rb") as file:
            file_string = base64.b64encode(file.read())#.decode("utf-8")
            
        num_packets = len(file_string) / self.BUFFER_SIZE
        print(num_packets)
        time.sleep(2)
        with open("time.txt", "a") as f:
            f.write(f"\n{datetime.now().strftime('%H%M')}")
            
        self.send_msg(client_connection, "data")
        # time.sleep(0.5)
        
        pos = 0
        for _ in range(len(file_string)):
            bytes_read = file_string[pos:pos+self.BUFFER_SIZE]
            if not bytes_read:
                break

            self.send_msg(client_connection, bytes_read, file=True)
            packets += 1
            print(f"Send image: sent packet {packets}")
            pos += self.BUFFER_SIZE
        time.sleep(0.5)
        self.send_msg(client_connection, "'end'")
        with open("time.txt", "a") as f:
            f.write(f"\n{datetime.now().strftime('%H%M')}")

        time.sleep(0.5)
    
    def zip_files(self, files):
        return shutil.make_archive("egressdata", "zip", "not_sent")
        
         
            
if __name__ == '__main__':
    listener = ClientListener()
    listener.listen_for_client()