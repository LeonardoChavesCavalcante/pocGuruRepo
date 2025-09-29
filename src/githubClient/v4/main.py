# Linux/git bash Exemplo de como executar o script 
# GITHUB_TOKEN="??" python src/githubClient/v4/main.py

#Windows Exemplo de como executar o script
# set GITLAB_TOKEN=
# python src/githubClient/v4/main.py

import os

#Utilizar o token desta forma
PRIVATE_TOKEN = os.getenv("GIT_API_TOKEN") 

# Endpoint
url = "https://api.github.com/graphql"
headers = {"Authorization": f"bearer {GITHUB_TOKEN}"}

# Repositório alvo
owner = "JabRef"
repo = "jabref"


def fetch_paginated(query_template, root_field, sub_field=None, limit=500):
    """
    Busca dados paginados da API GraphQL do GitHub.
    query_template -> query GraphQL com placeholder {AFTER}
    root_field -> ex: "issues", "pullRequests", "defaultBranchRef"
    sub_field -> ex: "history", ou None se já tiver nodes direto
    limit -> número de registros desejados
    """
    results = []
    has_next_page = True
    after = "null"

    while has_next_page and len(results) < limit:
        query = query_template.replace("{AFTER}", after)
        response = requests.post(url, json={"query": query}, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Erro {response.status_code}: {response.text}")

        data = response.json()
        repo_data = data["data"]["repository"]

        # Navega até o campo root
        parts = root_field.split(".")
        field_data = repo_data
        for part in parts:
            if field_data is None:
                return []  # sem acesso
            field_data = field_data.get(part)

        if field_data is None:
            return []  # sem acesso ou sem dados

        # Se sub_field existir, desce mais um nível
        if sub_field:
            field_data = field_data[sub_field]

        if not field_data or "nodes" not in field_data:
            return []

        nodes = field_data["nodes"]
        page_info = field_data["pageInfo"]

        results.extend(nodes)
        has_next_page = page_info["hasNextPage"]
        after = f"\"{page_info['endCursor']}\""

    return results[:limit]


# Queries com paginação
issues_query = f"""
{{
  repository(owner: "{owner}", name: "{repo}") {{
    issues(first: 100, after: {{AFTER}}, orderBy: {{field: CREATED_AT, direction: DESC}}) {{
      nodes {{
        title
        number
        createdAt
        author {{ login }}
      }}
      pageInfo {{
        endCursor
        hasNextPage
      }}
    }}
  }}
}}
"""

pulls_query = f"""
{{
  repository(owner: "{owner}", name: "{repo}") {{
    pullRequests(first: 100, after: {{AFTER}}, orderBy: {{field: CREATED_AT, direction: DESC}}) {{
      nodes {{
        title
        number
        createdAt
        author {{ login }}
        merged
      }}
      pageInfo {{
        endCursor
        hasNextPage
      }}
    }}
  }}
}}
"""

commits_query = f"""
{{
  repository(owner: "{owner}", name: "{repo}") {{
    defaultBranchRef {{
      target {{
        ... on Commit {{
          history(first: 100, after: {{AFTER}}) {{
            nodes {{
              messageHeadline
              committedDate
              author {{ name email }}
            }}
            pageInfo {{
              endCursor
              hasNextPage
            }}
          }}
        }}
      }}
    }}
  }}
}}
"""

collaborators_query = f"""
{{
  repository(owner: "{owner}", name: "{repo}") {{
    collaborators(first: 100, after: {{AFTER}}) {{
      nodes {{
        login
        name
      }}
      pageInfo {{
        endCursor
        hasNextPage
      }}
    }}
  }}
}}
"""


MAX_RECORDS = 500
print("🔄 Buscando issues...")
issues = fetch_paginated(issues_query, "issues", limit=MAX_RECORDS)

print("🔄 Buscando pull requests...")
pulls = fetch_paginated(pulls_query, "pullRequests", limit=MAX_RECORDS)

print("🔄 Buscando commits...")
commits = fetch_paginated(commits_query, "defaultBranchRef.target", sub_field="history", limit=MAX_RECORDS)

print("🔄 Buscando colaboradores...")
collaborators = fetch_paginated(collaborators_query, "collaborators", limit=MAX_RECORDS)

# Monta resultado final
result = {
    "issues": issues,
    "pullRequests": pulls,
    "commits": commits,
    "collaborators": collaborators,
}

# Salva em JSON
with open("jabref_github_data.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✅ Dados do repositório JabRef/jabref salvos em jabref_github_data.json (até 500 registros por categoria)")
