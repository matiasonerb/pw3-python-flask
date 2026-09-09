import requests

API_V1 = "https://digimon-api.vercel.app/api/digimon"
API_V2 = "https://digimon-api.com/api/v1/digimon"

class DigimonModel:

    @staticmethod
    def obter_todos():
        """Busca a lista completa de Digimons da API pública."""
        try:
            res = requests.get(API_V1, timeout=5)
            if res.status_code == 200:
                return res.json()
            return []
        except Exception as e:
            print(f"Erro ao buscar lista principal: {e}")
            return []

    @staticmethod
    def obter_detalhes_completos(nome):
        """Busca detalhes do Digimon em inglês garantindo exibição dos dados."""
        dados_basicos = {}
        
        # 1. Busca Principal na API V1 (Garante imagem, nome e nível)
        try:
            res_v1 = requests.get(f"{API_V1}/name/{nome}", timeout=5)
            if res_v1.status_code == 200 and res_v1.json():
                dados_basicos = res_v1.json()[0]
        except Exception as e:
            print(f"Erro na API V1: {e}")

        # Se não encontrou o Digimon na V1, encerra para evitar erros
        if not dados_basicos:
            return None

        # Valores padrão em inglês caso a V2 esteja off ou falhe
        description_en = "Information unavailable in the digital database."
        attributes = []
        types = []
        skills = []

        # 2. Busca Secundária na API V2 (Atributos, Tipos, Habilidades e História)
        try:
            res_v2 = requests.get(f"{API_V2}/{nome.lower()}", timeout=5)
            if res_v2.status_code == 200:
                dados_v2 = res_v2.json()

                # Extrai a descrição oficial em inglês
                descricoes = dados_v2.get("descriptions", [])
                for desc in descricoes:
                    if desc.get("language") == "en_us":
                        description_en = desc.get("description")
                        break

                # Atributos e Tipos em inglês
                attributes = [a.get("attribute") for a in dados_v2.get("attributes", []) if a.get("attribute")]
                types = [t.get("type") for t in dados_v2.get("types", []) if t.get("type")]
                skills = [s.get("skill") for s in dados_v2.get("skills", []) if s.get("skill")]
        except Exception as e:
            print(f"Aviso: Erro ao carregar dados complementares da V2: {e}")

        return {
            "name": dados_basicos.get("name", nome),
            "img": dados_basicos.get("img", ""),
            "level": dados_basicos.get("level", "Unknown"),
            "attribute": ", ".join(attributes) if attributes else "N/A",
            "type": ", ".join(types) if types else "Unknown",
            "skills": skills[:4],
            "description": description_en
        }