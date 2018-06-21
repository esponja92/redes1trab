#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Testa a vazão da rede
#
# Usage:
# 1) on host_A: python grupo2.py -s [port]                                                  # start a server
# 2) on host_B: python grupo2.py -c  count -h host_A -p [port] [-b bufsize] [-t tempo]      # start a client
#
# O servidor irá servir múltiplos clientes até ser desligado
#
# O cliente realiza uma transferência de count*BUFSIZE bytes e
# mede o tempo que demora (roundtrip!)
#
# Tempo em segundos!!!!!!

'''
cenário 1:

python grupo2.py -c 2 -h 54.85.161.250 -p 3421 -b 1024 -t 1

'''


import sys, time
from socket import *
from math import sqrt

MY_PORT = 50000 + 42

BUFSIZE = 1024


def main():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-s':
        server()
    elif sys.argv[1] == '-c':
        client()
    else:
        usage()


def usage():
    sys.stdout = sys.stderr
    print 'Usage:    (on host_A) python grupo2.py -s [port]'
    print 'and then: (on host_B) python grupo2.py -c  count -h host_A -p [port] [-b bufsize] [-t seconds]'
    sys.exit(2)


def server():
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
    else:
        port = MY_PORT

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port))
    s.listen(1)
    print 'Server ready...'

    while 1:
        conn, (host, remoteport) = s.accept()
        while 1:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            del data
        conn.send('OK\n')
        conn.close()
        print 'Done with', host, 'port', remoteport

def media(dataset): #calcula media dos dados
	soma=0.0
	for i in range(0, len(dataset)):
		soma=soma+dataset[i]
	
	return soma/len(dataset)

def desvioPadrao(dataset): #desvio padrao 
	media_local=0.0
	media_local=media(dataset)
	soma=0

	for i in range(0, len(dataset)):
		soma=(soma + ( (dataset[i] - media_local) * (dataset[i] - media_local) ) )

	variance=(soma/( len(dataset) - 1.0) )
	
	return sqrt(variance)

def client():

    global BUFSIZE

    tempo = 0

    vazoes = []

    if ('-c' not in sys.argv) or ('-h' not in sys.argv) or ('-p' not in sys.argv):
        usage()

    if '-c' in sys.argv:
        pos = sys.argv.index('-c') + 1 
        count = int(sys.argv[pos])

    if '-h' in sys.argv:
        pos = sys.argv.index('-h') + 1 
        host = sys.argv[pos]
    
    if '-p' in sys.argv:
        pos = sys.argv.index('-p') + 1 
        port = eval(sys.argv[pos])
    else:
        port = MY_PORT

    if '-b' in sys.argv:
        pos = sys.argv.index('-b') + 1 
        BUFSIZE = int(sys.argv[pos])

    if '-t' in sys.argv:
        pos = sys.argv.index('-t') + 1
        tempo = float(sys.argv[pos])

    testdata = 'x' * (BUFSIZE-1) + '\n'
    t1 = time.time()
    s = socket(AF_INET, SOCK_STREAM)
    #t2 = time.time()
    s.connect((host, port))
    #t3 = time.time()

    for i in range(count):
        i = i+1
        s.send(testdata)
        time.sleep(tempo)

    s.shutdown(1) # Send EOF
    #t4 = time.time()
    data = s.recv(BUFSIZE)
    t5 = time.time()

    vazao = round((BUFSIZE*count*0.001) / (t5-t1), 3)

    print '\nTamanho do pacote: ', BUFSIZE,' bytes'
    print 'Vazão: ', vazao,' KB/s'
    print 'Tempo entre geração de pacotes (segundos): ', tempo,' segundos'

'''
        print data
        print 'Tamanho do pacote:', BUFSIZE
        print '\nTempo entre geração de pacotes (segundos):', tempo
        print '\nRaw timers:', t1, t2, t3, t4, t5
        print '\nIntervalos:', t2-t1, t3-t2, t4-t3, t5-t4
        print '\nTotal:', t5-t1
        print '\nThroughput:', round((BUFSIZE*count*0.001) / (t5-t1), 3), #POR QUE ESSE 0.001???
        print 'KB/s.'
'''

main()
