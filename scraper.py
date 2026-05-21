import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SITES = [
    {"nome": "FUNCEB", "url": "https://fundacaocultural.ba.gov.br/category/editais/", "selector": "article h2 a"},
    {"nome": "SecultBA", "url": "https://cultura.ba.gov.br/category/editais/", "selector": "h3 a"},
]

DADOS_MOCK = [
    {"id":1,"type":"edital","title":"Prêmio Jovem Criador Baiano","organization":"FUNCEB","region":"salvador","regionLabel":"Bahia (Todas as regiões)","category":"artes-visuais","categoryLabel":"Artes Visuais","deadline":"2026-06-15","value":"R$ 15.000,00","description":"Edital de fomento à produção de artes visuais para jovens de 18 a 29 anos.","tags":["Fomento","Jovens"],"proposal":"Financiar a criação de obras de arte inéditas.","requirements":["Ter entre 18 e 29 anos","Apresentar portfólio","Residir na Bahia"],"activities":["Desenvolvimento da obra","Exposição coletiva de encerramento"],"link":"https://fundacaocultural.ba.gov.br/"},
    {"id":300,"type":"recurso","title":"Ateliê Coletivo do Subúrbio (ACS)","organization":"Coletivo ACS","region":"salvador","regionLabel":"Plataforma, Salvador","category":"artes-visuais","categoryLabel":"Artes Visuais / Criação","deadline":"contínuo","value":"Contribuição simbólica (ou isento)","description":"Espaço compartilhado com cavaletes, tintas básicas e ferramentas.","tags":["Ateliê","Coletivo","Baixo Custo"],"proposal":"Rede de artistas periféricos que mantém um galpão com mesas, iluminação e alguns materiais.","requirements":["Residir na região metropolitana de Salvador","Disposição para ajudar na limpeza coletiva"],"activities":["Produção artística livre","Participação em mutirões","Possibilidade de expor no espaço"],"link":"https://www.instagram.com/explore/tags/atelieracoletivo/"}
]

def raspar_site(nome, url, selector):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        itens = soup.select(selector)
        oportunidades = []
        for item in itens[:10]:
            titulo = item.get_text(strip=True)
            link = item.get("href")
            if link and not link.startswith("http"):
                link = url.rstrip("/") + "/" + link.lstrip("/")
            oportunidades.append({
                "id": abs(hash(link or titulo)) % 100000,
                "type": "edital",
                "title": titulo,
                "organization": nome,
                "region": "salvador",
                "regionLabel": "Bahia",
                "category": "artes-visuais",
                "categoryLabel": "Artes Visuais",
                "deadline": "consulte o site",
                "value": "Consultar edital",
                "description": titulo,
                "tags": [nome],
                "proposal": titulo,
                "requirements": ["Consultar edital"],
                "activities": ["Consultar edital"],
                "link": link or url
            })
        return oportunidades
    except Exception as e:
        print(f"[ERRO] {nome}: {e}")
        return []

todas_oportunidades = []
for site in SITES:
    todas_oportunidades.extend(raspar_site(site["nome"], site["url"], site["selector"]))

if not todas_oportunidades:
    todas_oportunidades = DADOS_MOCK

with open("oportunidades.json", "w", encoding="utf-8") as f:
    json.dump(todas_oportunidades, f, ensure_ascii=False, indent=2)

print(f"[{datetime.now()}] {len(todas_oportunidades)} oportunidades salvas.")
