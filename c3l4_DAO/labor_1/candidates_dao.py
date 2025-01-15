import json, os

from candidate import Candidate
from config import Config

class CandidatesDAO:

    # def __init__(self):
    #     # Определяем абсолютный путь к JSON-файлу
    #     self.file_path = os.path.join(
    #         os.path.dirname(__file__), 
    #         "static", 
    #         "candidates.json"
    #     )

    # def __init__(self):
    #     self.file_path = '/home/v/Python/c3l4_DAO/labor_1/static/candidates.json'

    def load_data(self):

        config_info = Config ()

        with open(config_info.file_path, "r", encoding="utf-8") as file:
            candidates_data = json.load(file)
            candidates = []
						# Создаем список объектов класса Candidate
            for candidate in candidates_data:
                candidates.append(Candidate(
                    candidate["id"],
                    candidate["name"],
                    candidate["position"],
                    candidate["skills"]
                ))
        return candidates

    def get_all(self):
        return self.load_data()

    def get_by_skill(self, skill):
        candidates = self.load_data()
        skilled_candidates = []
        skill_lower = skill.lower()

        for candidate in candidates:
            candidate_skills = candidate.skills.lower().split(", ")
            if skill_lower in candidate_skills:
                skilled_candidates.append(candidate)

        return skilled_candidates


    def get_by_id(self, candidate_id):
        candidates = self.load_data()
        for candidate in candidates:
            if candidate.id == candidate_id:
                return candidate
