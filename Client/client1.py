import UDPclient 

#check for "can download 1 file"
def main():
    server_host = "localhost"
    server_port = 50000
    client1= UDPclient.UDPclient(server_host, server_port)
    filename = "testfile.txt"
    client1.download_file(filename)
    
if __name__ == "__main__":
    main()