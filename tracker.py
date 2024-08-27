import requests
import logging.config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
import schedule
import time
import datetime
import pandas as pd

def extrai_preco_do_bitcoin():
    # Consome a API do CoinGecko para obter o preço atual do Bitcoin em Real 
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl"
    response = requests.get(url)
    data = response.json()
    preco = data['bitcoin']['brl']
    return preco

def cria_planilha(preco, csvPath):
    dados = {
        'Data e Hora': [datetime.datetime.now()],
        'Cotação': [preco]
    }
    
    # Adiciona os dados ao CSV
    df = pd.DataFrame(dados)
    df.to_csv('preco_produto.csv', mode='a', header=not pd.io.common.file_exists(csvPath), index=False)

# enviar_email('./preco_bitcoin.csv', preco)
def enviar_email(csvPath, preco):
    com_anexo = csvPath
    email_de = "andrepinto.cg@gmail.com"
    email_destino = "andrepinto.cg@gmail.com"
    senha = 'jkru nswj iqbu uwsm'
    assunto = "Alerta: Preço do Bitcoin Abaixo do Limite"
    corpo = f"O preço atual do Bitcoin é: ${preco:.2f}"

    # Configurar a mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = email_de
    mensagem['To'] = email_destino
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(corpo, 'plain'))
    
    # Anexo
    anexo = open(com_anexo, "rb")
    
    # Configurar o anexo
    parte = MIMEBase('application', 'octet-stream')
    parte.set_payload(anexo.read())
    encoders.encode_base64(parte)
    parte.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(com_anexo)}')

    mensagem.attach(parte)
    
    # Configuração do servidor
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()

    # Login no servidor
    servidor.login(email_de, senha)
    
    # Envia o e-mail
    texto = mensagem.as_string()
    servidor.sendmail(email_de, email_destino, texto)

    # Encerrar a sessão
    servidor.quit()

def monitor_de_preco_bitcoin(limite, csvPath):
    preco_atual = extrai_preco_do_bitcoin()
    cria_planilha(preco_atual, csvPath)
    if preco_atual < limite:
        enviar_email(csvPath, preco_atual)
    
def main():
    csvPath = './planilha_preco_bitcoin.csv'
    limite = 300000 # Definir o limite aqui
    monitor_de_preco_bitcoin(limite, csvPath)

schedule.every(30).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)