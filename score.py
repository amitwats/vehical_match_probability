from match_score import MatchScore


class Score:
    def __init__(self, main_str, word):
        self.main_str=main_str
        self.word=word
        self.match_scores=[]

    def add_match_score(self, token_str, similarity_score, dependency_type):
        ms=MatchScore(self.main_str,self.word,token_str=token_str,similarity_score=similarity_score, dependency_type=dependency_type)
        self.match_scores.append(ms)

    def get_match_score_filtered(self,threshold=.75, dependency_exclude=None):

        if dependency_exclude and threshold:
            filter_function=lambda x:x.compare_similarity_score(threshold)==1 and x.dependency_type not in dependency_exclude
        elif dependency_exclude and not threshold:
            filter_function=lambda x: x.dependency_type not in dependency_exclude
        elif not dependency_exclude and threshold:
            filter_function=lambda x:x.compare_similarity_score(threshold)==1
        else:
            filter_function=lambda x: True

        # return list(filter(lambda x:x.compare_similarity_score(threshold)==1 ,self.match_scores))
        return list(filter(filter_function ,self.match_scores))


    def __repr__(self):
        match_scores_string='\n'.join([str(ms) for ms in self.match_scores])
        return f"Score(main_str='{self.main_str}', word='{self.word}', match_scores=\n{match_scores_string})"