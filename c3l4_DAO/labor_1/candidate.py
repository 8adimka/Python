class Candidate:
    def __init__(self, candidate_id, name, position, skills):
        self.id = candidate_id
        self.name = name
        self.position = position
        self.skills = skills

    def __repr__(self):
        return f"{self.name}"
