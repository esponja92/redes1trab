CONTADOR=0
echo "################ 8 CONEXÕES EM PARALELO" >> resultados.txt
echo "" >> resultados.txt
echo "" >> resultados.txt

while [  $CONTADOR -lt 30 ]; do
	
	date >> resultados.txt
	echo "-= 8 CNX" >> resultados.txt
	python grupo2.py -c 2000 -h 54.85.161.250 -p 3421 -b 1024 -t 0.0001 -th 8 >> resultados.txt
	echo "" >> resultados.txt
	echo "8 CONEXÕES EM PARALELO valor $CONTADOR"
    let CONTADOR=CONTADOR+1; 

done

