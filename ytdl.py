#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import expanduser
import os, sys, subprocess, textwrap
import urllib.request, urllib.error, urllib.parse

#-------------------------------------
# Criado por: Wolfterro
# Modificado por Rafael Fernandes
# Versão: 2.0.1 - Python 3.x
# Data: 26/06/2021
#-------------------------------------

version = "2.0.4"
is_termux = "true"

ajuda = f"""\
==================================================
Youtube-DL Script - Versão {version} - Python 3.x
==================================================

 * Este script requer o youtube-dl instalado e reconhecido como comando do shell
 * O pacote 'libav' ou 'ffmpeg' deverá estar instalado para converter os vídeos baixados
 * Caso não tenha o youtube-dl instalado, utilize a opção 'Instalar/Atualizar youtube-dl'
 * É necessário privilégios de root para instalar e atualizar o youtube-dl"
 * Utilize os formatos de conversão caso o formato escolhido não esteja disponível
 
Uso: ./ytdl.py [Argumento]

Argumentos:
-----------

 -h || --help			Mostra este menu de ajuda
 
"""

main_menu = f"""\
	====================================================
	Youtube-DL Script - Versão {version} - Python 3.x"
	====================================================

	Escolha uma das opções abaixo (qualquer outra tecla para sair):
	---------------------------------------------------------------
 
	Áudio (Conversão):
	------------------
 
	(1) Formato MP3
	(2) Formato WAV
	
	Vídeo (Nativo):
	---------------
 
	(3) Formato MP4
	(4) Formato WEBM
	(5) Formato 3GP
	(6) Formato MKV
	
	Vídeo (Conversão):
	------------------
 
	(7) Formato MP4
	(8) Formato WEBM
	(9) Formato MKV

	Opções:
	-------
 
	(0) Instalar/Atualizar youtube-dl
 
"""

def help():
	print(ajuda)

def get_home_dir():
	get_home = os.path.expanduser("/sdcard/Download/")
	return get_home

def check_download_dir(get_home, video):
	if video == True:
		if os.path.exists(get_home + "/Vídeos"):
			os.chdir(get_home + "/Vídeos")
		else:
			print("Criando pasta 'Vídeos' em '" + get_home + "' ...")
			os.makedirs(get_home + "/Vídeos")
			os.chdir(get_home + "/Vídeos")
	else:
		if os.path.exists(get_home + "/Música"):
			os.chdir(get_home + "/Música")
		else:
			print("Criando pasta 'Música' em '" + get_home + "' ...")
			os.makedirs(get_home + "/Música")
			os.chdir(get_home + "/Música")

def install_youtube_dl(home_dir):
	print("Baixando youtube-dl ...")
	latest = "https://yt-dl.org/downloads/latest/youtube-dl"

	try:
		response = urllib.request.urlopen(latest)
		data = response.read()
	except Exception:
		print("Erro! Não foi possível baixar o youtube-dl! Saindo ...")
		sys.exit(1)
	
	try:
		file = open("youtube-dl", "wb")
		file.write(data)
		file.close()
	except Exception:
		print("Erro! Não foi possível criar o arquivo 'youtube-dl' em '" + home_dir + "'! Saindo ...")
		sys.exit(1)

	print("Aplicando permissões ...")
	os.chmod("youtube-dl", 0o755)

	print("Movendo para a pasta '/usr/local/bin' ...")
	subprocess.Popen("mv youtube-dl /usr/local/bin", shell=True)

	print("Finalizado! Execute o script novamente para utilizá-lo corretamente.")

def youtube_dl_options(home_dir):
	os.chdir(home_dir)

	print("\n(A) Atualizar youtube-dl")
	print("(I) Instalar youtube-dl\n")

	user_input = input("Escolha uma das opções acima: ")
	if user_input.upper() == "A":
		if os.geteuid() != 0:
			print("Erro! É necessário privilégios de root para atualizar! Saindo ...")
			sys.exit(1)
		else:
			subprocess.call("youtube-dl -U", shell=True)
	elif user_input.upper() == "I":
		if os.geteuid() != 0:
			print("Erro! É necessário privilégios de root para instalar! Saindo ...")
			sys.exit(1)
		else:
			install_youtube_dl(home_dir)
	else:
		print("Saindo ...")

def main_menu():
	print(main_menu)

	user_input = input("Escolha uma das opções acima: ")
	return user_input

def text_id(obj, substring = None, start = 0, qtd = None):

	qtd = len(obj) if qtd is None else qtd

	if substring:
		inicio = obj.find(substring)
		return obj[inicio:inicio+qtd]
	elif not substring:
		return obj[start:start+qtd]

def get_video_id():
	os.system('clear')
	video_id = input("Insira a url do Vídeo ou da Playlist: ")

	ytmc=text_id(video_id, qtd=26)
	if(ytmc == "https://music.youtube.com/"):
		video_id=text_id(video_id, start=34, qtd=11)
	else:

		video_id=text_id(video_id, start=17)

	if len(video_id) > 11:
		is_playlist = True
	else:
		is_playlist = False
	
	return [video_id, is_playlist]

def prepare_command(video, conversion, video_format):
	if video == True:
		if conversion == True:
			command = "youtube-dl --recode-video " + video_format
		else:
			command = "youtube-dl --format " + video_format
	else:
		command = "youtube-dl --extract-audio --audio-format " + video_format

	return command

def check_video_id(video_id, is_playlist):
	if is_playlist == True:
		url = " https://www.youtube.com/playlist?list=" + video_id
	else:
		url = " https://www.youtube.com/watch?v=" + video_id

	return url

def download_video(command, url):
	print(" ")
	subprocess.call(command + url, shell=True)

def main():
	home_dir = get_home_dir()
	user_input = main_menu()
	
	if user_input == "1":
		video = False
		conversion = True
		video_format = "mp3"
	elif user_input == "2":
		video = False
		conversion = True
		video_format = "wav"
	elif user_input == "3":
		video = True
		conversion = False
		video_format = "mp4"
	elif user_input == "4":
		video = True
		conversion = False
		video_format = "webm"
	elif user_input == "5":
		video = True
		conversion = False
		video_format = "3gp"
	elif user_input == "6":
		video = True
		conversion = False
		video_format = "mkv"
	elif user_input == "7":
		video = True
		conversion = True
		video_format = "mp4"
	elif user_input == "8":
		video = True
		conversion = True
		video_format = "webm"
	elif user_input == "9":
		video = True
		conversion = True
		video_format = "mkv"
	elif user_input == "0":
		youtube_dl_options(home_dir)
		sys.exit(0)
	else:
		print("Saindo ...")
		sys.exit(0)

	video_id, is_playlist = get_video_id()

	check_download_dir(home_dir, video)
	command = prepare_command(video, conversion, video_format)
	url = check_video_id(video_id, is_playlist)
	download_video(command, url)

if __name__ == "__main__":
	argc = len(sys.argv)
	
	if argc > 1:
		if str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "--help":
			help()
		else:
			print("Erro! Argumento desconhecido! Use '-h' ou '--help' para ajuda.")
			print("Uso: ./Youtube-DL-Script.py [Argumento]")
	else:
		main()
		while True:

			if(is_termux == "true"):
				os.system('termux-vibrate -d 50')

			os.system('clear')
			print(" ")
			one_more_time = input("Deseja executar o script mais uma vez? [s/N]: ")
			if one_more_time.upper() == "S":
				main()
			else:
				break
