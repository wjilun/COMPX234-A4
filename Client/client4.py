import UDPclientWithLoss

#check for "can correctly download 1 file despite losses"
def main():
    host = "localhost"
    port = 50000
    client3 = UDPclientWithLoss.UDPclientWithLoss(host, port, packet_loss_rate=0.2)
    filename_list = ["t1.jpg", "testfile.txt", "mm.mov"]
    
    for filename in filename_list:
        client3.download_file(filename)

if __name__ == "__main__":
    main()