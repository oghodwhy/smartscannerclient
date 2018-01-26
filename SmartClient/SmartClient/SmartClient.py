#
#       CSC361  Assignment 1
#   Written by Aaron Moen - V00786805
#           January 2018
#

#Imports
import sys
import getopt
import socket
import ssl

#Globals
global verbose = False

# recvLine
#
# Recieves data line by line from a socket. Generates a string for each line.
#
#Input is a socket item to recieve from, the size of a recieve buffer to recieve to, and the line delimiter to be searched for through the recieved text.
def recvLine(sock, recvBuff=4096, delim='\n'):

    if(verbose): print('Attempting to recieve lines of text...\n')
    buffer = ''
    data = True
    
    #Recieve while data is inccoming
    while data:
        data = sock.recv(recvBuff)
        buffer += str(data)
        if(verbose): print('Recieved buffer: ' + buffer)

        #Split buffer into lines at delim
        while buffer.find(delim) != -1:
            line, buffer = buffer.split('\n', 1)
            
            yield line

    if(verbose): print('Finished recieving text.\n')
    return


# parseToGet
#
# Generates a HTTP GET returned as a string.
#
# All inputs should be strings, protocol specifies http/https, version specifies http version, 
# hostname is the hostname, and headers a list of all the headers as full lines of text.
def parseToGet(protocol, version, hostname, headers):
    
    if(verbose): print('parsing request with attributes\nProtocol: ' + protocol + '\nVersion: ' + str(version) + '\nHostname: ' + hostname + '\nHeaders: ' + headers)

    #create GET request and absolute URL
    text = 'GET / ' + protocol.upper() + '/' + str(version) +'\r\nHost: ' + protocol.lower() + '://' + hostname + '/\r\n'
    
    #append headers
    if headers is list:
        for line in headers:
            text += str(line) + '/\r\n'
    else:
        text += headers

    #append final newline
    text += '\r\n'

    if(verbose): print('request parsed as follows:\n' + text)

    return text
    

# Main   
# 
# Main function of Smart Client. Takes input of command line arguments.   
#
def main(argv):

    #starting params
    verbose = False
    connects = False
    hasSSL = False
    targetAddr = ''
    currentAddr = '' 
    fqTarget = ''
    HTTPversion = ''
    toSend = ''
    newMessage = ''
    cookies = []
    cookieDomains = []

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
        fqTarget = socket.gethostbyname(targetAddr)
    except socket.gaierror:
        print ('Input host address cannot be resolved. Please check formatting.')
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
        toSend = parseToGet('https','1.1',targetAddr,'Connection: close')

        #Attempt HTTPS connection
        try:
            secureSocket.connect((targetAddr, 443))
            secureSocket = ssl.wrap_socket(secureSocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
            if (verbose): print("Sending: " + toSend)
            secureSocket.sendall(str.encode(toSend))

        #HTTPS connection failure
        except socket.error:
            if (verbose): print ('Failed to create HTTPS connection')
            break

        #Check for HTTPS response
        if (verbose): print ('Recieving incoming lines...')

        for line in recvLine(secureSocket):
            newMessage += line
            if (verbose): print (line)
            

        #No HTTPS response
        if not newMessage:
            if (verbose): print ('No message recieved from HTTPS connection')
            connects = False
            hasSSL = False
            break
    
        #HTTPS response
        else: 
            if (verbose): print ('Recieved message over HTTPS')
            connects = True
            hasSSL = True
            break
        
    #Attempt HTTP connection
    while(true):

        if (verbose): print ('Attempting to connect to target...')

        #Still needs to connect via HTTP
        if not (connected):

            toSend = parseToGet('http','1.1',targetAddr,'Connection: close')

            #Try initiating connection
            try:
                regularSocket.connect((targetAddr, 80))
                if (verbose): print("Sending: " + toSend)
                regularSocket.sendall(str.encode(toSend))

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
        i = 0
        for name in cookies:
            print('name: ' + name + ' Domain: ' + cookieDomains[i])
            i +=1

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