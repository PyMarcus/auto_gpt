import requests

# URL do arquivo no GitHub
github_url = "https://github.com/apache/syncope/blob/114c412afbfba24ffb4fbc804e5308a823a16a78/client/idrepo/ui/src/main/java/org/apache/syncope/client/ui/commons/ConnIdSpecialName.java"

# Números da linha que você quer extrair
linha_inicial = 35
linha_final = 37
import json

# Fazendo a requisição HTTP ao GitHub
response = requests.get(github_url)
conteudo = json.loads(response.text)["payload"]["blob"]["rawLines"]
# Extraindo as linhas específicas de código
linhas_de_codigo = conteudo[linha_inicial - 1:linha_final]
# Imprimindo as linhas de código
for linha in linhas_de_codigo:
    print(linha)