import UDPclient

#check for "can download multiple file"
def main():
    host="localhost"
    port=50000
    client3=UDPclient.UDPclient(host, port)
    filename_list = ["t1.jpg","testfile.txt","mm.mov"]
    for filename in filename_list:
        client3.download_file(filename)

main()