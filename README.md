# Simple Web Server

A simple TCP web server supporting both persistent and non-persistent HTTP connections serving concurrent clients.

This simple wb server uses the STREAM socket (i.e., supported by TCP) in Python to support both persistent and non-persistent HTTP connections.  

The SWS details: 
Only supports “GET /filename HTTP/1.0” command, and “Connection: keep-alive” and “Connection: close” request and response header when supporting persistent HTTP connection. The request header is terminated by an empty line. If unsupported commands received or in unrecognized format, SWS will respond “HTTP/1.0 400 Bad Request”. If the file indicated by filename is inaccessible, SWS will return “HTTP/1.0 404 Not Found”. For successful requests, SWS will respond “HTTP/1.0 200 OK”, followed by response header if any, an empty line indicating the end of the response header, and the content of the file.

How to run SWS: 
On server side, “python3 sws.py ip_address port_number”, where ip_address and port_number indicate where SWS binds its socket for incoming requests. 
On client side, “telnet sws_ip_address sws_port_number” to connect to SWS, and type “GET /sws.py HTTP/1.0” followed by “Connection: keep-alive” and an empty line to request the file sws.py from SWS.

For each served request, even if unsuccessfully, SWS will output a log line “time: client_ip:client_port request; response”, e.g., “Wed Sep 16 21:44:35 PDT 2020: 192.168.1.100:54321 GET /sws.py HTTP/1.0; HTTP/1.0 200 OK”. Please note that SWS will keep waiting to serve more clients and can serve multiple concurrent clients, until interrupted by Ctrl-C.
