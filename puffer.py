#/usr/bin/python3
import requests
import signal
import argparse
import os
import time
import threading
import sys
def main():
    #CTRL + C
    def def_handler(signal,frame):
        print(f"\n[!]Saliendo.....")
        os._exit(1)
    signal.signal(signal.SIGINT, def_handler)
    #Definimos los parametros
    parser = argparse.ArgumentParser("Fuzzer para descubrir directorios de un servidor")
    parser.add_argument("-u","--url",type=str,required=True,help="Url a fuzzear")
    parser.add_argument("-f","--file",required=True,help="Diccionario que se va a utilizar")
    parser.add_argument("-t","--threads",type=int, default=10, help="Numero de hilos (por defecto 10)")
    args = parser.parse_args()
    #Petición para realizar el fuzzing
    def fuzzing(ruta):
        ruta = ruta.strip()
        urlCompleta = f"{args.url}/{ruta}"
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            time.sleep(5)
            response = requests.get(urlCompleta, headers=headers)
            if response.status_code in [200,301,302]:
                print(f"\n[+] Ruta Encontrada: {urlCompleta} ({response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error en la solicitud: {e}")
    #Indicamos la funcion del diccionario
    try:
        with open (args.file, 'r') as file:
            rutas = file.readlines()
    except FileNotFoundError:
        print(f"\n[-] El archivo {args.file} no se encuentra")
        sys.exit(1)


    def thread_manager():
        while rutas:
            ruta = rutas.pop(0)
            fuzzing(ruta)

    #Definimos los hilos
    threads = []
    for _ in range(args.threads):
        thread = threading.Thread(target=thread_manager)
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()
if __name__ == '__main__':
    main()
