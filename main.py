import requests
from bs4 import BeautifulSoup
import pymysql as pmq
from datetime import datetime
import yagmail


conexao = pmq.connect(
    host = 'localhost',
    user = 'root',
    password = 'root'
)

cursor = conexao.cursor()

cursor.execute("DROP DATABASE IF EXISTS CHOCOLATERIA")

cursor.execute("CREATE DATABASE CHOCOLATERIA")
cursor.execute("USE CHOCOLATERIA")
cursor.execute("CREATE TABLE CHOCOLATES (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, NOME_PRODUTO VARCHAR(255) NOT NULL, PRECO DECIMAL(10,2) NOT NULL, DATA_COLETA DATETIME NOT NULL)""")


hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
hora_email = datetime.now().strftime('%d/%m/%Y %H:%M')

stut = 'https://www.stuttgart.com.br/bomboniere/barras-de-chocolate.html'

resposta = requests.get(stut)
if resposta.status_code != 200:
    raise SystemExit('Erro ao requisitar informações do site.')

stut_site = BeautifulSoup(resposta.text, features='html.parser')

ol_principal = stut_site.find('ol', class_='filterproducts products list items product-items')

nome_choc_tudo = ol_principal.find_all('strong', class_ = 'product name product-item-name')
nome_tabela_choc = [nome.text.strip() for nome in nome_choc_tudo]


preco_choc_tudo = ol_principal.find_all('div', class_ = 'price-box price-final_price')
preco_naoconvertido_choc = [preco.text.strip() for preco in preco_choc_tudo]
preco_tabela_choc = [
    float(preco_antes.replace('R$', '').replace(',', '.').strip())
    for preco_antes in preco_naoconvertido_choc
    if preco_antes.strip() != ''
]

query = '''
SELECT COUNT(*) FROM CHOCOLATES
'''
cursor.execute(query)
tem_dados = cursor.fetchone()
if tem_dados[0] > 0:
    query = '''DELETE FROM CHOCOLATES'''
    cursor.execute(query)
for nome,preco in zip(nome_tabela_choc,preco_tabela_choc):
    query = '''
    INSERT INTO CHOCOLATES(NOME_PRODUTO, PRECO, DATA_COLETA) VALUES
    (%s,%s,%s)'''
    valores = (nome,preco,hora_atual)
    cursor.execute(query,valores)

conexao.commit()

query = '''
SELECT NOME_PRODUTO, PRECO FROM CHOCOLATES
'''
cursor.execute(query)
resultados = cursor.fetchall()
cursor.close()
conexao.close()

corpo_html = '''
<p style="font-size: 1em;">🍫🥚Feliz Páscoa! Veja as ofertas de chocolates Stuttgart</p><table><thead><tr><th>Produtos</th><th>Preço</th></tr></thead><tbody style="font-size: 1em">
'''


for nome,preco in resultados:
    preco_formatado = f'R${preco:.2f}'
    corpo_html += f'''<tr><td>{nome}</td><td style="padding-left: 25px">{preco_formatado.replace(".",",")}</td></tr>'''

html = f'''{corpo_html}</tbody></table><p>⌚ Coleta realizada em: {hora_email}</p><p>Veja mais em: https://www.stuttgart.com.br/bomboniere/barras-de-chocolate.html</p>'''

yag = yagmail.SMTP('teste@gmail.com', 'abcd efgh ijkl mnop')

try:
    yag.send(to='teste@gmail.com', subject='🐰Ofertas de Páscoa - Chocolates Stuttgart', contents=html)
except Exception as erro:
    print(f'Erro ao enviar o email: {erro}')
