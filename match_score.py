class MatchScore:
    def __init__(self, main_str, compare_str, token_str, similarity_score, dependency_type) -> None:
        self.main_str=main_str
        self.compare_str=compare_str
        self.token_str=token_str
        self.similarity_score=similarity_score
        self.dependency_type=dependency_type

    def __repr__(self):
        return (f"MatchScore("
                f"main_str='{self.main_str}', "
                f"compare_str='{self.compare_str}', "
                f"token_str='{self.token_str}', "
                f"similarity_score={self.similarity_score}, "
                f"dependency_type='{self.dependency_type}')")

    def compare_similarity_score(self,num):
        if self.similarity_score==num:
            return 0
        elif self.similarity_score>num:
            return 1
        else:
            return -1