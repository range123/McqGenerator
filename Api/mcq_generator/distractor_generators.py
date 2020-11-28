class DistractorGenerator:
    
    def __init__(self, model_path : str):
        pass
    def generate_distractors(self, question : str, answer : str):
        pass

class BertDistractorGenerator(DistractorGenerator):
    
    def __init__(self, BDG_model_path : str, BDG_ANPM_model_path : str, BDG_PM_model_path : str):
        pass
    def generate_distractors(self, question : str, answer : str):
        pass

class Sense2VecDistractorGenerator(DistractorGenerator):

    def __init__(self, model_path : str):
        pass
    def generate_distractors(self, question : str, answer : str):
        pass

class ConceptNetDistractorGenerator(DistractorGenerator):
    def __init__(self, BDG_model_path : str, BDG_ANPM_model_path : str, BDG_PM_model_path : str):
        pass
    def generate_distractors(self, question : str, answer : str):
        pass

if __name__ == "__main__":
    pass

