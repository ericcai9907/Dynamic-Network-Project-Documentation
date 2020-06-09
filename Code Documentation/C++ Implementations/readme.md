This folder holds the code and files that are useful for implementing a C++ software for data transfer. 

There is a C++ implementation for RUDP mirrors the Python version; doesn't work very well and isnt the best approach. 
"sendrecv.cpp" 

queue.cpp  -> This is an implementation of a circular queue that is used for RUDP.

udpserver.cpp & udpclient.cpp -> These are sample codes for an UDP file transfer. 


One interesting implementation that warrants further research is UFTP; http://uftp-multicast.sourceforge.net/ 
licensed under GNU General Public Use license
This protocol uses UDP to handle FTP and manages data to ensure reliable transfer. 

Documentation:
Server: http://uftp-multicast.sourceforge.net/server_usage.txt
Client: http://uftp-multicast.sourceforge.net/client_usage.txt


