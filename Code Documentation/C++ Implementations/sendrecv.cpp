#include <queue.cpp>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <iostream>
#include <fstream>

using namespace std;

void send_datagram(int sock, int IP, int S_PORT, int D_PORT,
 int LEN, int CHECKSUM, int SEQ, String payload, String type)
{
	String IPstr = to_string(IP);
	String S_PORTstr = to_string(IP);
	String D_PORTstr = to_string(IP);
	String LENstr = to_string(IP);
	String CHECKSUMstr = to_string(IP);
	String SEQstr = to_string(IP);
	String hdrStart = '!HHHHQ';

	String header = hdrStart + S_PORTstr + D_PORTstr + LENstr + CHECKSUMstr + SEQstr;

	send(sock, header + payload, strlen(header+payload) , 0);

	String output = "Sending" + type + ":" + SEQstr;

	cout << output << "\n";
}

int sendFile(int S_IP, int D_IP)
{
	int S_PORT = 55000;
	int D_PORT = 55001;
	int payload_length = 256;
	int window_size = 10;
	int timeout = 3;

	int LEN = 0;
	int CHECKSUM = 0;
	int head_SEQ = 0;
	Queue window = queue.Queue(window_size);
	int unacked = 0;
	int num_iter = 1; 
	int last_SEQ = -1;
	int num_timeouts = 0;
	FILE *file;


	int sock = 0, valread;
	String bin_header; 
	struct sockaddr_in serv_addr;

	if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) 
	{ 
		printf("\n Socket creation error \n");
		return -1;  
	} 

	serv_addr.sin_family = AF_INET; 
	serv_addr.sin_port = htons(D_PORT); 
	
	// Convert IPv4 and IPv6 addresses from text to binary form 
	if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0) 
	{ 
		printf("\nInvalid address/ Address not supported \n");
		return -1; 
	} 

	if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) 
	{ 
		printf("\nConnection Failed \n");
		return -1; 
	} 

	
	String filename = cin >> "Enter file name: ";
	file = fopen(filename, 'rb');

	if (file == NULL) 
	{
		printf("Invalid file name. File could not be opened.")
		return -1;
	}

	printf("Sending...");
	while(1)
	{
		cout << "---------------- ITERATION " << num_iter << endl;

		while(!window.isFull())
		{
			payload = file.read(payload_length);
			if(!payload) break;
			window.enQueue(payload);
			SEQ = head_SEQ + unacked;
			unacked++;
			cout << "Buffered SEQ: " << SEQ << endl;
		}
		for ( i = 0; i < unacked; i++)
		{
			SEQ = head_SEQ + i;
			payload = window.deQueue();
			window.enQueue(payload);
			LEN = payload.length() + 16;
			send_datagram(sock, D_IP, S_PORT, D_PORT,
                          LEN, CHECKSUM, SEQ, payload, 'SEQ');
			if(LEN < payload_length + 16)
			{
				last_SEQ = SEQ + 1;
				LEN = 16;
				payload = "";
				send_datagram(sock, D_IP, S_PORT, D_PORT, LEN,
                              CHECKSUM, last_SEQ, payload, 'final SEQ');

			}
		}

		printf("Waiting for ACKs...");
		while(1)
		{
			sock.settimeout(timeout)
			resp = sock.recv(64);

			bin_header = resp[:16];
			if(bin_header[4] == head_SEQ)
			{
				cout << "Received ACK:" << bin_header[4] << endl;
				unacked--;
				head_SEQ++;
				window.deQueue();
				if(head_SEQ == last_SEQ)
				{
					printf("------------------- FILE SENT");
					cout << "Number of timeouts: " << num_timeouts<<endl;
					return 1;
				}
			}
			if (unacked == 0)
			{
				printf("All packets ACKed");
				break;
			}
		}

		num_iter++;
	}



}


int recvFile(int S_IP, int D_IP)
{
	int S_PORT = 55001;  //# Source port
    int D_PORT = 55000; // # Destination port
    int LEN = 16; // # Length of the header
    int CHECKSUM = 0; // # Checksum, dummy value
    int exp_SEQ = 0; // # Expected SEQ number
    int timeout = 60;  //# Timeout on receiver side
    int num_recvd = 0; // # Number of datagrams received
    int num_iter = 1;  //# Number of iterations
    int last_SEQ = -1;

	int server_fd, new_socket, valread; 
    struct sockaddr_in address; 
    int opt = 1; 
    int addrlen = sizeof(address); 
    char buffer[1024] = {0}; 
    char *hello = "Hello from server"; 
    FILE *file;

    int window_size = 10;//  # Size of the window
    Queue window = queue.Queue(window_size);//  # Initialize the queue

    String filename = input('Enter output file name: ')  # Get file name
    file = open(filename, 'wb') 
       
    // Creating socket file descriptor 
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
    { 
        perror("socket failed"); 
        exit(EXIT_FAILURE); 
    } 
       
    // Forcefully attaching socket to the port 8080 
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 
                                                  &opt, sizeof(opt))) 
    { 
        perror("setsockopt"); 
        exit(EXIT_FAILURE); 
    } 
    address.sin_family = AF_INET; 
    address.sin_addr.s_addr = INADDR_ANY; 
    address.sin_port = htons( S_PORT ); 
       
    // Forcefully attaching socket to the port 8080 
    if (bind(server_fd, (struct sockaddr *)&address,  
                                 sizeof(address))<0) 
    { 
        perror("bind failed"); 
        exit(EXIT_FAILURE); 
    } 
    if (listen(server_fd, 3) < 0) 
    { 
        perror("listen"); 
        exit(EXIT_FAILURE); 
    } 
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address,  
                       (socklen_t*)&addrlen))<0) 
    { 
        perror("accept"); 
        exit(EXIT_FAILURE); 
    }

    printf("Waiting...");

    bool done = false;
    while(!done)
    {
    	cout << "-------------- ITERATION " << num_iter << endl;
    	num_recvd = window.numElements();
    	for(i = 0; i< window_size - num_recvd; i++)
    	{
    		// timeout here
    		// receive stuff
    		datagram = sock.recv(1024);

    		bin_header = datagram[:16];
    		SEQ = bin_header[4];
    		LEN = bin_header[2];
    		cout << "Received SEQ" << SEQ << endl;
    		if (SEQ == exp_SEQ)
    		{
    			num_recvd++;
    			exp_SEQ++;

    			if(LEN == 16)
    			{
    				last_SEQ = SEQ;
    				break;
    			}
    			payload = "";
    			send_datagram(sock, D_IP, S_PORT, D_PORT,
                              LEN, CHECKSUM, SEQ, payload, 'ACK');
    			payload = datagram[16:];
    			window.enQueue(payload)
    		} 
    	}
    	cout << "Number of datagrams received: " << num_recvd << endl;
    	for (i = 0; i < num_recvd; i++)
    	{
    		SEQ = exp_SEQ - num_recvd + i;
    		if(SEQ == last_SEQ)
    		{
    			cout << "Final SEQ: " << SEQ << endl;
    			cout << "----------------- FILE RECEIVED" << endl;
    			return 1;
    		}
    		cout << "Writing SEQ: " << SEQ << endl;
    		payload = window.deQueue();
    		file.write(payload);
    	}

    	num_iter++;
    }
}
