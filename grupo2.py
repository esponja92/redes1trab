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

python grupo2.py -c 10 -h 54.85.161.250 -p 3421 -b 1024 -t 1



cenário 2: (para rodar com 3 clientes)

python grupo2.py -c 30 -h 54.85.161.250 -p 3421 -b 4096 -t 3



cenário 3: (para rodar com 5 clientes)

python grupo2.py -c 15 -h 54.85.161.250 -p 3421 -b 2048 -r
'''


import sys, time, threading
from socket import *
from math import sqrt

MY_PORT = 50000 + 42

BUFSIZE = 1024

def main():

    threads = 1

    if len(sys.argv) < 2:
        usage()

    if sys.argv[1] == '-s':
        server()

    elif sys.argv[1] == '-servidor':
        parametros = sys.argv[0] + ' -s 3421'
        sys.argv = parametros.split()
        server()

    else:

        if sys.argv[1] == '-c':
            client()

        elif sys.argv[1] == '-cenario1':
            parametros = sys.argv[0] + ' -c 10 -h 54.85.161.250 -p 3421 -b 1024 -t 1'

        elif sys.argv[1] == '-cenario2':
            parametros = sys.argv[0] + ' -c 30 -h 54.85.161.250 -p 3421 -b 4096 -t 3 -r'
            threads = 3

        elif sys.argv[1] == '-cenario3':
            parametros = sys.argv[0] + ' -c 15 -h 54.85.161.250 -p 3421 -b 2048 -t 0.005 -r'
            threads = 4

        sys.argv = parametros.split()

        for i in range(threads):
            print i
            threading.Thread(target=client).start()


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

    rajada = False

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

    if '-r' in sys.argv:
        rajada = True

    testdata = 'x' * (BUFSIZE-1) + '\n'
    t1 = time.time()
    s = socket(AF_INET, SOCK_STREAM)
    #t2 = time.time()
    s.connect((host, port))
    #t3 = time.time()

    for i in range(count):
        
        s.send(testdata)

        if (i == 0) and (rajada):
            time.sleep(10)

        time.sleep(tempo)
        i = i+1

    s.shutdown(1) # Send EOF
    #t4 = time.time()
    data = s.recv(BUFSIZE)
    t5 = time.time()

    vazao = round((BUFSIZE*count*0.001) / (t5-t1), 3)

    print '\nTamanho do pacote: ', BUFSIZE,' bytes'
    print 'Vazão: ', vazao,' KB/s'
    print 'Tempo entre geração de pacotes (segundos): ', tempo,' segundos'


main()
