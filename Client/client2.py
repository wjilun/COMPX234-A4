import UDPclient

#check for "multiple clients can download files at the same time ",when you run client1,please run this too in 15 second
def main():
    host="localhost"
    port=50000
    client2=UDPclient.UDPclient(host, port)
    filename = "t1.jpg"
    client2.download_file(filename)

if __name__ == "__main__":
    main()