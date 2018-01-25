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
    HTTPversion = ''

    #Get input options
    try:
        opts, args = getopt.getopt(argv,"v")
    except getopt.GetoptError:
        print ('Error with input options.\n Try in the form SmartClient.py %targetip%\n Use -h for help.\n')
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

    if (verbose): print ('Initiating main...')

    #Check input format
    if (verbose): print ('Checking input address...')


    #Create socket
    if (verbose): print ('Creating socket...')
    
    
    #Attempt to connect socket
    if (verbose): print ('Attempting to connect to target...')
    
    
    #Check if HTTPS
    if (verbose): print ('Checking for HTTPS...')
    
    
    #Check HTTP version
    if (verbose): print ('Checking HTTP version...')
    
    
    #Print Result
    if (verbose): print ('Printing results...')
    
    
    
    if (verbose): print ("Job's Done!")
    sys.exit
    
    
    
if __name__ == "__main__":
    main(sys.argv[1:])