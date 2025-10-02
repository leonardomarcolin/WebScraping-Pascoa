PT-BR:
Projeto freelance de webscraping utilizando Python, BeatifulSoup, Yagmail e MySQL.
Ao executar o script, primeiramente é deletada a database "CHOCOLATERIA" caso exista para não haver interferências, e, após feito isso, é criada a database e a tabela "CHOCOLATES" para armazenar ID, nome, preço e a data da coleta.
Depois, no site da Stuttgart na aba de chocolates, o script procura o nome e o preço de cada um deles e retorna. Após o recebimento das informações do site, os dados são formatados para serem armazenados dentro da database.
Por fim, é resgatado o nome e o preço de dentro do banco de dados, formatado em HTML e enviado o relatório para o email desejado.
Requer email para realizar o envio, senha de app desse email e o email que deseja receber o relatório (pode ser o mesmo email para envio e recebimento).
Pode ser transformado em executavel baixando a biblioteca Pyinstaller e executando o seguinte comando no console: "pyinstaller --onefile --noconsole main.py" ("--noconsole" remove a janela do prompt de comando que apareceria caso contrário).

EN:
A webscraping freelance project made with Python, BeatifulSoup, Yagmail and MySQL.
After executing the script, it begins trying to delete the "CHOCOLATERIA" database to avoid interferences. After that, the "CHOCOLATERIA" database is created, with the "CHOCOLATES" table to store ID, name, price and collection date.
In the Stuttgart site, in the chocolates section, the script searches for the name and price of each item and returns them. After receiving information from the website, the data is formatted to be stored in the database.
Finally, the name and price are retrieved from the SQL, formatted in HTML and the report is sent to the wanted email.
It is required a email to send, the app password from that respective email and the email that wants to recieve the report (it can be the same email for both sending and receiving).
Can be transformed in executable by installing the Pyinstaller library and executing the following command on the console: "pyinstaller --onefile --noconsole main.py" ("--noconsole" removes the command prompt window that would popup otherwise).
