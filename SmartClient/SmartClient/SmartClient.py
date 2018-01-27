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
global verbose
verbose = False

# recvLine
#
# Recieves data line by line from a socket. Generates a string for each line.
#
# Input is a socket item to recieve from (required), the size of a recieve buffer to recieve to (defaults to 4096), 
# and the line delimiter to be searched for through the recieved text (defaults to '\n'). Generates strings.
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

# recvMessage
#
# Recieves data from a host as a list of lines.
#
# Input is a socket item to recieve from (required), a list to append the lines to (defaults to empty list), the size of a recieve buffer to recieve to (defaults to 4096), 
# and the line delimiter to be searched for through the recieved text (defaults to '\n'). Returns a list of strings.
def recvMessage(sock, newMessage = list(), recvBuff=4096, delim='\n'):
    if (verbose): print('Attempting to recieve message from host...')
    
    #read lines to line list.
    for line in recvLine(sock, recvBuff, delim):
                newMessage.append(line)
                if (verbose): print (line)
    
    #return list of lines.
    if (verbose): print('Finished receiving message from host.')
    return newMessage
    
# parseToGet
#
# Builds a HTTP GET request returned as a string.
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
    
# validHTTP
#
# Checks a message to see if it is a legitimate HTTP response.
#
# Takes a list of strings as input. Returns a bool.
def validHTTP(message = list(str())):
    if(verbose): print('Checking if reponse is valid HTTP response...')
    
    #If blank first line.
    if not message[0]:
        if(verbose): print('Blank message is not a valid HTTP response.')
        return False
    
    #split head into words
    head = message[0].split()  

    #Check if first word starts with HTTP and second is a status code.
    if head[0].startswith('HTTP') and head[1].isdigit():
        if(verbose): print('Found a valid HTTP response.')
        return True
    
    #Otherwise not HTTP we can use
    if(verbose): print('Not a valid HTTP response.')
    return False

# checkStatus
#
# Parses through a message to determine HTTP validity, and status code.
#
# Takes a message in the form of a list of strings. Returns a status code as a string.
def checkStatus(message = list(str())):
    if(verbose): print('Parsing Message for HTTP status code...')
    
    #if it's valid HTTP find and return status code.
    if validHTTP(message):
        head = message[0].split()
        status = head[1]
        if(verbose): print('Found a status code of: ' + str(status))
        return str(status)
    
    #if invalid message return none.
    else:
        if(verbose): print('No status code found in invalid message.')
        return ''
    
    return ''

# checkRedirect
#
# Checks a message to see if it redirects to an https site.
#
# Takes a list of strings as input. Returns a bool.
def checkRedirect(message = list(str())):
    if(verbose): print('Checking if redirect is to https site...')
    
    #if valid
    if validHTTP(message):
        
        #find location line
        locationLine = ''
        for line in message:
            if line.startswith('Location:'):
                locationLine = line.split()
        
        #if no location line
        if not locationLine:
            if(verbose): print('Not a https redirect.')
            return False

        #check if redirect is to https
        else:
            if(verbose): print('Found and checking location line...')

            #redirects to https
            if locationLine[1].startswith('https'):
                if(verbose): print('Redirect is to https!')
                return True
            
            #not an https redirect
            else:
                if(verbose): print('Not a https redirect.')
                return False
    
    #not a valid HTTP response    
    else:
        if(verbose): print('Not a valid HTTP response.')
        return False

# getHostVersion
#
# Repeatedly contacts host on set up socket verify HTTP versions.
#
# Takes name of host. Returns highest HTTP version. Probably.
def getHostVersion(hostname = str()):
    version = ''
    request10 = parseToGet('http','1.0',hostname,'Connection: close')
    request11 = parseToGet('http','1.1',hostname,'Connection: close')
    request20 = parseToGet('http','2.0',hostname,'Connection: close')
    
    try:    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error:
        print ('Client error. Failed to create socket.')
        sys.exit(2)
    
    #testing for 1.0   
    if (verbose): print ('Checking response to HTTP 1.0...')

    try:
        sock.connect((hostname, 80))
        sock.sendall(str.encode(request10))
        newMessage = recvMessage(sock)
        sock.close()

    except socket.error:
        if (verbose): print ('Connection with host failed.')

    code = checkStatus(newMessage)

    #check for failure
    if code.startswith('5') or code.startswith('4') or not code:
        if (verbose): print ('Failed HTTP 1.0 test.') 
        return version
    
    #update version
    if (verbose): print ('Passed 1.0 test.')
    version = '1.0'

    #testing for 1.1   
    if (verbose): print ('Checking response to HTTP 1.1...')

    try:
        sock.connect((hostname, 80))
        sock.sendall(str.encode(request11))
        newMessage = recvMessage(sock)
        sock.close()

    except socket.error:
        if (verbose): print ('Connection with host failed.')

    code = checkStatus(newMessage)

    #check for failure
    if code.startswith('5') or code.startswith('4') or not code:
        if (verbose): print ('Failed HTTP 1.1 test.') 
        return version
    
    #update version
    if (verbose): print ('Passed 1.1 test.')
    version = '1.1'

    #try 2.0   
    if (verbose): print ('Checking response to HTTP 2.0...')

    try:
        sock.connect((hostname, 80))
        sock.sendall(str.encode(request20))
        newMessage = recvMessage(sock)
        sock.close()

    except socket.error:
        if (verbose): print ('Connection with host failed.')

    code = checkStatus(newMessage)

    #check for failure
    if code.startswith('5') or code.startswith('4') or not code:
        if (verbose): print ('Failed HTTP 2.0 test.') 
        return version

    #update version and return
    if (verbose): print ('Passed 2.0 test.')
    version = '2.0'
    return version
    
# Main   
# 
# Main function of Smart Client. Takes input of command line arguments.   
#
def main(argv):

    #starting params
    verbose = False
    targetAddr = '' 
    toSend = ''
    newMessage = list()
    cookieList = list()
    cookieDomains = list()

    #hostinfo [domain, protocol, version, cookieList, cookieDomains]
    hostInfo = ['', '', '', cookieList, cookieDomains]

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
    hostInfo[0] = targetAddr

    #Create socket
    if (verbose): print ('Creating socket...')
    
    try:
        secureSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        regularSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print ('Internal error. Client failed to initialize sockets.')
        sys.exit(2)

    if (verbose): print ('Socket created successfully.')
    
    #Attempt HTTPS connection
    while(True):    

        if (verbose): print ('Attempting to connect to https...')
        toSend = parseToGet('http','1.0',targetAddr,'Connection: close')

        #Attempt HTTPS connection
        try:
            secureSocket.connect((targetAddr, 443))
            secureSocket = ssl.wrap_socket(secureSocket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
            if (verbose): print("Sending the following:\n" + toSend)
            secureSocket.sendall(str.encode(toSend))

        #HTTPS connection failure
        except socket.error:
            if (verbose): print ('Failed to create HTTPS connection with host.')
            hostInfo[1] = ''
            break

        #Check for HTTPS response
        if (verbose): print ('Recieving message from host...')

        try:
            newMessage = recvMessage(secureSocket, newMessage)
            secureSocket.close()

        #Recieving failure
        except socket.error:
            if verbose: print('Socket encountered error in connection with host.\n ')
            hostInfo[1] = ''
            break
            
        #No HTTPS response
        if not newMessage:
            if (verbose): print ('No message recieved from HTTPS connection')
            hostInfo[1] = ''
            break
    
        #HTTPS response
        else: 
            if (verbose): print ('Recieved message over HTTPS')
            
            #Find status of response
            code = checkStatus(newMessage)

            #if invalid response
            if not code:
                if (verbose): print ('Recieved invalid message over HTTPS. Proceeding with HTTP.')
                break
            
            #Handle codes
            if (verbose): print ('Checking status code...')

            #Accept or proceed status
            if code.startswith('2') or code.startswith('1'):
                if (verbose): print ('Recieved proper response over https!')
                hostInfo[1] = 'HTTPS'
                
                #
                # GET VERSION AND COOKIES
                #
            
            #Redirect status
            elif code.startswith('3'):
                if (verbose): print ('Recieved HTTP redirect. Checking...')
                
                secureRedirect = checkRedirect(newMessage)

                #redirect works
                if secureRedirect:
                    if (verbose): print ('Recieved proper response over https!')
                    hostInfo[1] = 'HTTPS'
                    
                    hostInfo[2] = getHostVersion(hostInfo[0])
                    #
                    # GET VERSION AND COOKIES
                    #
                
                #redirect does not work
                else:
                    if (verbose): print ('Redirect did not lead to secure connection. HTTPS not supported')
                    hostInfo[1] = ''
            
            #Client error status
            elif code.startswith('4'):
                if (verbose): print ('Recieved client error status. HTTPS not supported.')
                hostInfo[1] = ''
                break

            #Server error status
            elif code.startswith('5'):
                if (verbose): print ('Recieved server error status. HTTPS not supported.')
                hostInfo[1] = ''
                break

    #Attempt HTTP connection
    while(true):

        if (verbose): print ('Attempting HTTP connection to host...')

        #Still needs to connect via HTTP
        if not hostInfo[1]:

            toSend = parseToGet('http','1.0',targetAddr,'Connection: close')

            #Try initiating HTTP connection
            try:
                regularSocket.connect((targetAddr, 80))
                if (verbose): print("Sending: " + toSend)
                regularSocket.sendall(str.encode(toSend))

            #HTTP connection error
            except socket.error:
                if (verbose): print("Failed to initiate HTTP connection.")
                hostInfo[1] = ''
                break
            
            #Check for response
            newMessage = list()
            try:
                newMessage = recvMessage(regularSocket, newMessage)
            
            #HTTP Response Failure
            except socket.error:
                if verbose: print('Socket encountered error in connection with host.\n ')
                hostInfo[1] = ''
                break
            
            #No HTTP response
            if not newMessage:
                if (verbose): print ('No message recieved from HTTP connection')
                hostInfo[1]=''
                break
    
            #HTTP response
            else: 
                if (verbose): print ('Recieved message over HTTP')
                if (verbose): print ('Recieved the following:\n' + newMessage)
                
                code = checkStatus(newMessage)
 
                if code: 
                    if (verbose): print ('Recieved valid response on HTTP. Host supports HTTP.')
                    hostInfo[1] = 'HTTP'

                else:
                    if (verbose): print ('Recieved invalid response on HTTP. Host does not support HTTP.')
                    hostInfo[1] = ''
                break
        
        #Already connected with HTTPS
        else:
            if (verbose): print ('Host accepts HTTPS. No need to check with HTTP.')
            break

    #check HTTP version
    while(true):
        if (verbose): print ('Checking host HTTP version...')

        #if no HTTP
        if not hostInfo[1]:
            if (verbose): print ('Host supports no HTTP versions.')
            break

        #check version
        version = getHostVersion(hostInfo[0])
        if (verbose): print ('Host supports up to version ' + version)
        hostInfo[2] = version
            
    
    #Print Result
    while (true):
        if (verbose): print ('Printing results...')
        
        #Report website
        Print('Website: ' + hostInfo[0])
        
        #Report if no HTTP
        if not hostInfo[1]:
            Print('No HTTP or HTTPS connections could be made.')
            break

        #Report HTTPS support
        if(hostInfo[1] == 'HTTPS'):
            print('1. Support of HTTPS: Yes')
        else:
            print('1. Support of HTTPS: No')
        
        #Report HTTP version
        print('2. Newest version of HTTP supported: '+ hostInfo[2])

        #Report Cookies
        print('3. List of cookies:')

        if not hostInfo[3]:
            print('none found.\n')
            break

        i = 0
        for name in hostInfo[3]:
            print('name: ' + name + ' Domain: ' + hostInfo[4][i])
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