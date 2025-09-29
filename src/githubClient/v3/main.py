# Linux/git bash Exemplo de como executar o script 
# GITLAB_TOKEN="seu_token" python src/githubClient/v3/main.py

#Windows Exemplo de como executar o script
# set GITLAB_TOKEN=seu_token
# python src/githubClient/v3/main.py

import os

#Utilizar o token desta forma
PRIVATE_TOKEN = os.getenv("GIT_API_TOKEN") 

print("Hello, GuroRepo! Github API V3 "  )
