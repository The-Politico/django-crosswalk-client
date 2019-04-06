from crosswalk_client.exceptions import MalformedThreshold


class SetThreshold(object):
    def set_threshold(self, threshold):
        if not isinstance(threshold, int):
            raise MalformedThreshold("Threshold should be an integer")
        if threshold < 0 or threshold > 100:
            raise MalformedThreshold("Threshold should be between 0 and 100")
        self.threshold = threshold
