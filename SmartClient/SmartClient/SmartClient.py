import sys
import getopt
import socket
import ssl
import http

def main(argv):

    #starting params
    verbose = False
    connects = False
    hasSSL = False
    targetAddr = '' 
    fqTarget = ''
    HTTPversion = ''
    cookies = []

    #Get input options
    try:
        opts, args = getopt.getopt(argv,"v")
    except getopt.GetoptError:
        print ('Error with input options.\n Try in the form SmartClient.py %targetaddress%\n Use -h for help.\n')
        sys.exit(2)

    #Check input options
    for param in opts:

        #help option
        if param == '-h':
            print ('basic use with SmartClient.py %targetip%')
            print ('Use -v for verbose mode.\n')
            sys.exit()
        
        #verbose option
        if param == '-v':
            verbose = True
            print ('Starting client in verbose mode.\n')

    #if no entered args
    if not (args):
        print ('No input address!\n Try in the form SmartClient.py %targetaddress%\n Use -h for help.\n')
        sys.exit(2)

    if (verbose): print ('Initiating main...')

    #Check input format
    if (verbose): print ('Checking input address...')

    targetAddr = args[0]
   
    try:
        socket.inet_aton(targetAddr)
    except socket.error:
        print ('input address cannot be used. Please check formatting.')
        sys.exit(2)

    if (verbose): print ('Passed address validation.')

    #Create socket
    if (verbose): print ('Creating socket...')
    
    try:
        secureSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        regularSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print ('failed to create socket.')
        sys.exit(2)

    if (verbose): print ('Socket created successfully.')
    
    #Attempt HTTPS connection
    while(true):    

        if (verbose): print ('Attempting to connect to https...')

        #Attempt HTTPS connection
        try:
            secureSocket.connect((targetAddr, 443))
            secureSocket = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
            if (verbose): print("Sending: 'GET / HTTP/1.1\r\nHost: " + targetAddr +  "\r\nConnection: close\r\n\r\n'")
            secureSocket.sendall("GET / HTTP/1.1\r\nHost: " + targetAddr +  "\r\nConnection: close\r\n\r\n")

        #HTTPS connection failure
        except socket.error:
            if (verbose): print ('Failed to create HTTPS connection')
            break

        #Check for HTTPS response
        recieved = secureSocket.recv(4096)

        #No HTTPS response
        if not recieved:
            if (verbose): print ('No message recieved from HTTPS connection')
            connects = False
            hasSSL = False
            break
    
        #HTTPS response
        else: 
            if (verbose): print ('Recieved message over HTTPS')
            if (verbose): print ('Recieved:' + recieved)
            connects = True
            hasSSL = True
            break
        
    #Attempt HTTP connection
    while(true):

        if (verbose): print ('Attempting to connect to target...')

        #Still needs to connect via HTTP
        if not (connected):

            #Try initiating connection
            try:
                regularSocket.connect((targetAddr, 80))
                if (verbose): print("Sending: 'GET / HTTP/1.1\r\nHost: " + targetAddr +  "\r\nConnection: close\r\n\r\n'")
                regularSocket.sendall("GET / HTTP/1.1\r\nHost: " + targetAddr +  "\r\nConnection: close\r\n\r\n")

            #HTTP connection error
            except socket.error:
                if (verbose): print("Failed to initiate HTTP connection.")
                break
            
            #Check for response
            recieved = ''
            recieved = regularSocket.recv(4096)
            
            #No HTTP response
            if not recieved:
                if (verbose): print ('No message recieved from HTTP connection')
                connects = False
                break
    
            #HTTPS response
            else: 
                if (verbose): print ('Recieved message over HTTP')
                if (verbose): print ('Recieved:' + recieved)
                connects = True
                break
        
        #Already connected with HTTPS
        else:
            if (verbose): print ('already connected via HTTPS')
            break
    

    #Check HTTP version
    while(true):
        if (verbose): print ('Checking HTTP version...')
        
        #On our existing connection
        if(connects):
            
            #Existing connection is HTTPS
            if (hasSSL):
                if (verbose): print ('Checking version over HTTPS...')
                
                
                
                if (verbose): print ('Finished version check.')
                break
            
            #Existing connection is HTTP
            else:
                if (verbose): print ('Checking version over HTTP...')
                
                
                
                if (verbose): print ('Finished version check.')
                break

        #No connection exists to check
        else:
            if (verbose): print ('No existing connection to check.')
            break

    #Check cookies
    while(true):
        if (verbose): print ('Checking for cookies...')
        
        #On our existing connection
        if(connects):
            
            #Existing connection is HTTPS
            if (hasSSL):
                if (verbose): print ('Checking cookies over HTTPS...')
                
                
                
                if (verbose): print ('Finished cookie check.')
                break
            
            #Existing connection is HTTP
            else:
                if (verbose): print ('Checking cookies over HTTP...')
                
                
                
                if (verbose): print ('Finished cookie check.')
                break

        #No connection exists to check
        else:
            if (verbose): print ('No existing connection to check.')
            break
    
    #Print Result
    while (true):
        if (verbose): print ('Printing results...')
        
        #Report website
        Print('Website: ' + targetAddr)
        
        #Report if no HTTP
        if not (connects):
            Print('No HTTP or HTTPS connections could be made.')
            break

        #Report HTTPS support
        if(hasSSL):
            print('1. Support of HTTPS: Yes')
        else:
            print('1. Support of HTTPS: No')
        
        #Report HTTP version
        print('2. Newest version of HTTP supported: '+ HTTPversion)

        #Report Cookies
        print('3. List of cookies:')
        for name in cookies:
            print('name: ' + name)
        
        #Finish Report
        break
    
    #Close sockets
    if (verbose): print ("Closing Sockets.")
    secureSocket.close()
    regularSocket.close()
    
    #Close app
    if (verbose): print ("Job's Done!")
    sys.exit
    
    
    
if __name__ == "__main__":
    main(sys.argv[1:])