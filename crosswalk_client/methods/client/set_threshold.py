from crosswalk_client.validators.client import validate_required_threshold


class SetThreshold(object):
    @validate_required_threshold
    def set_threshold(self, threshold):
        self.threshold = threshold
