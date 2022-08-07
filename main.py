from genericpath import exists
from time import sleep
from Cbot import bot
import re
import json
import os
import pandas as pd



def fazerDownload(usuarioNovo,usuarioAnterior,bot):
    try:   
        if ((usuarioAnterior["usuario"] != usuarioNovo["usuario"] or usuarioAnterior["senha"]!= usuarioNovo["senha"]) and bot.logado):
            print("trocando usuario e senha")
            bot.sairLogin()
        if not(bot.logado):
            print("logando...")
            bot.fazerLogin(usuarioNovo["usuario"],usuarioNovo["senha"])
        if not(bot.logado):
            print("não conseguiu logar com usuario e senha")
            return
        if (usuarioAnterior["uc"] != usuarioNovo["uc"]):
            if bot.selecionarUc(usuarioNovo["uc"]) == 0:
                return
        bot.fazerDownload("Downloads/" + re.sub("[^0-9]", "", usuarioNovo["usuario"]) + "/UC_" + re.sub("[^0-9]", "", usuarioNovo["uc"]) + " " + bot.getMes(usuarioNovo["mes"]) +"_"+ usuarioNovo["mes"].split("/")[1] ,usuarioNovo["mes"])
    except Exception as e:
        print("não conseguiu fazer o download " + str(e))
    finally:
            usuarioAnterior["usuario"] = usuarioNovo["usuario"]
            usuarioAnterior["senha"] = usuarioNovo["senha"]
            usuarioAnterior["uc"] = usuarioNovo["uc"]
            usuarioAnterior["mes"] = usuarioNovo["mes"]
            



usuarioAnterior={"usuario":"","senha":"","uc":"","mes":""}
usuario = {"usuario":"","senha":"","uc":"","mes":""}

#pegar configurações
if exists("configs.json"):
    arquivo = open('configs.json',encoding='utf-8')
    config = json.load(arquivo)
    arquivo.close()
else:
    print("Arquivo configs.json Não encontrado na pasta")
    quit()



print(config["campos"]["mes"])

#for filename in os.listdir(pathlib.Path().resolve()):

#vasculha somente a pasta
if config["EntrarPastas"] == True:
    listaArquivos = []
    for diretorio, subpastas, arquivos in os.walk("./"):
        for arquivo in arquivos:
            if arquivo.endswith(".xlsx"):
                listaArquivos.append(os.path.join(diretorio, arquivo))
else:
    listaArquivos = []
    for diretorio, subpastas, arquivos in os.walk("."):
        for arquivo in arquivos:
            if arquivo.endswith(".xlsx"):
                listaArquivos.append(os.path.join(diretorio, arquivo))
        break



#para testar o IP ou header 
#botEnergisa = bot("https://www.myip.com/")
#botEnergisa = bot("https://httpbin.org/headers")
#botEnergisa.abrirPagina()
#botEnergisa.entrarSite()
#sleep(10)
#quit()

botEnergisa = bot(config["url"],config["tempoEspera"])
botEnergisa.abrirPagina()
botEnergisa.entrarSite()
botEnergisa.selecionarUfCidade()
for arquivo in listaArquivos:
    try:
        print("********************************************")
        print(arquivo)
        planilha = pd.read_excel(arquivo)
        for index, row in planilha.iterrows():
            print("--------------------------------------")
            usuario["usuario"] = row[config["campos"]["usuario"]]
            usuario["senha"] = row[config["campos"]["senha"]]
            usuario["uc"] = row[config["campos"]["uc"]]
            usuario["mes"] = row[config["campos"]["mes"]]
            print(usuario["usuario"],"  ",usuario["uc"],"  ",usuario["mes"])
            if (usuario["usuario"] == "" or usuario["senha"]== "" or usuario["uc"]== ""  or usuario["mes"]== "" ):
                continue
            fazerDownload(usuario,usuarioAnterior,botEnergisa)
            print("--------------------------------------")
    except Exception as e:
        print("erro ao ler a planilhia " + arquivo + ", ERRO: " + str(e))
    finally:
        print("********************************************")
print("tempo total: " + str(botEnergisa.tempoTotal()))
botEnergisa.sairLogin()
botEnergisa.fecharPagina()
botEnergisa.fecharBrowser()
botEnergisa.fecharAsyncPlay()

    







"""
teste = bot("http://teste.com")
teste.abrirPagina()
teste.entrarSite()
teste.selecionarUfCidade()
usuario = ""
senha = ""
UC_ = ""
mesAno = ""

for i in lista:
    try:
        print("ROW - " + i[1] + " " + i[2]+ " " + i[0]+ " " + i[3])
        usuarioNovo = i[1]
        senhaNova = i[3]
        UCNova = i[2]
        mesAno = i[0]     
        if ((usuario != usuarioNovo or senha != senhaNova) and teste.logado):
            teste.sairLogin()
        if not(teste.logado):
            usuario = usuarioNovo
            senha= senhaNova
            teste.fazerLogin(usuarioNovo,senhaNova)
        if (UC_ != UCNova):
            UC_ = UCNova
            teste.selecionarUc(UCNova)
        teste.fazerDownload("Downloads/" + re.sub("[^0-9]", "", usuarioNovo) + "/UC_" + re.sub("[^0-9]", "", UCNova) + " " + teste.getMes(mesAno) +"_"+ mesAno.split("/")[1] ,mesAno)
    except Exception as e:
        print(e)
teste.sairLogin()
teste.fecharPagina()
teste.fecharBrowser()
teste.fecharAsyncPlay()
"""
#
# 
# 
# print("Tempo total Downloads: " + str(teste.tempoTotal()))

#print("Downloads/" + re.sub("[^0-9]", "", "12345/1231-"))
