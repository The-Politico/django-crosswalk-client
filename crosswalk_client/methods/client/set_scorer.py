from crosswalk_client.validators.client import validate_required_scorer


class SetScorer(object):
    @validate_required_scorer
    def set_scorer(self, scorer):
        self.scorer = scorer
