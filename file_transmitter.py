import base64, os, socket, shutil, time

class ClientListener():
    """
    Instantiate by declaring receive port, send port and an authorisation code that the client
    must send to egress data.
    
    Activate by calling listen_for_client, with no arguments.
    """
    
    def __init__(self, recv_port=5010, send_port=5011, auth_code="go"):
        self.recv_port = recv_port
        self.send_port = send_port
        self.auth_code = auth_code
        
        self.SEPARATOR = "<SEP>"
        self.BUFFER_SIZE = 1024

    def listen_for_client(self):
        """
        Listens for connection from a client (guy with device that will receive images/data)
        Once detected, with correct auth code, send data
        """    
        
        client_found = False
        client_authorised = False
        
        while True:
            if not client_found:
                connection = socket.socket()
                connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                connection.bind(('0.0.0.0', self.recv_port))
                print("listening")
                connection.listen(5)
                
                client_socket, client_address = connection.accept()
                
                client_found = True
            print(f"{client_address[0]} connected")
            
            if not client_authorised:
                raw_message = client_socket.recv(self.BUFFER_SIZE).decode()
                print(f"{client_address[0]}: {raw_message}")
                
                # to be used later if we are splitting messages up into packets
                cleaned_message = raw_message.split(self.SEPARATOR)
                
                if raw_message == self.auth_code:
                    print("Auth code accepted - begin data transfer")
                    client_authorised = True
                    
                else:
                    client_found = False
                    print("Incorrect auth code - waiting for new client")
                    
            else:
                # wait to receive message to hang the while loop
                raw_message = client_socket.recv(self.BUFFER_SIZE).decode()
                print(f"{client_address[0]}: {raw_message}")
                
                if raw_message == "send":
                    time.sleep(1)
                    self.send_data(client_socket)
                else:
                    msg = input("Message: ")
                    self.send_msg(client_socket, msg)
                
                time.sleep(1)
                
    def send_data(self, client_connection):
        """
        Once a client device is detected and approved, begin sending files
        Once files are sent, move them to the sent folder
        """
        files_to_send = ["not_sent/" + file for file in os.listdir("not_sent")]
        
        # ===send files as one zipped file===
        zipped_folder = self.zip_files(files_to_send)
        self.send_file(zipped_folder, client_connection)
        for file in files_to_send:
            shutil.move(file, "sent/")
        
        # ===send files separately===
        # print(f"Sending {len(files_to_send)} files to client.")
        # self.send_msg(client_connection, f"{len(files_to_send)}")
        # time.sleep(0.25)
        # for file in files_to_send:
        #     print(f"Next file to send is: {file}")
        #     self.send_file(file, client_connection)
        #     shutil.move(file, "sent/")
            
    

            
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
            
        self.send_msg(client_connection, "data")
        time.sleep(0.5)
        
        pos = 0
        for _ in range(len(file_string)):
            bytes_read = file_string[pos:pos+self.BUFFER_SIZE]
            if not bytes_read:
                break

            self.send_msg(client_connection, bytes_read, file=True)
            packets += 1
            print(f"Send image: sent packet {packets}")
            pos += self.BUFFER_SIZE

        self.send_msg(client_connection, "end")

        time.sleep(0.5)

    def get_files(self):
        """
        Gets a list of all the files to be sent based on whether client activates
        heavy mode or light mode (heavy true/false)
        """
        
        files = []
        
        for file in os.listdir("not_sent"):
            print(file)
            files.append("not_sent/" + file)
            
        print(files)
        return files
    
    def zip_files(self, files):
        return shutil.make_archive("egressdata", "zip", "not_sent")
        
         
            
if __name__ == '__main__':
    listener = ClientListener()
    listener.listen_for_client()