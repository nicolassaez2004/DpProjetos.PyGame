import json
from datetime import datetime
from pathlib import Path


class LeaderboardRepository:
    def __init__(self, caminho_arquivo='dados/leaderboard.json', limite=10):
        self.caminho_arquivo = Path(caminho_arquivo)
        self.limite = limite

    def carregar(self):
        if not self.caminho_arquivo.exists():
            return []

        try:
            with self.caminho_arquivo.open('r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, list):
                return dados
        except (json.JSONDecodeError, OSError):
            pass

        return []

    def salvar(self, ranking):
        self.caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho_arquivo.open('w', encoding='utf-8') as arquivo:
            json.dump(ranking, arquivo, ensure_ascii=False, indent=2)

    def adicionar_pontuacao(self, nome, score):
        ranking = self.carregar()

        nova_entrada = {
            'nome': nome,
            'score': int(score),
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        ranking.append(nova_entrada)

        ranking_ordenado = sorted(ranking, key=lambda item: item.get('score', 0), reverse=True)
        ranking_ordenado = ranking_ordenado[:self.limite]

        self.salvar(ranking_ordenado)
        return ranking_ordenado
