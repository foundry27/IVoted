from abc import ABCMeta, abstractmethod
from numpy import random
from typing import List, Callable, Tuple

from grequests import AsyncRequest

from rating import StarRating
from targeting import VotingTarget
from voting.requestcreation import VotingRequestCreationService
from voting.voteridentity import VoterIdentity


class TargetRequestController(metaclass=ABCMeta):

    @abstractmethod
    def generate_target_requests(self, voter: VoterIdentity, requester: VotingRequestCreationService) -> List[AsyncRequest]:
        pass


class SpecializedTargetRequestController(TargetRequestController):

    def __init__(self, targets_and_creation_strategies: Callable[[], List[Tuple[VotingTarget, Callable[[VotingTarget, VoterIdentity, VotingRequestCreationService], AsyncRequest]]]]):
        self.targets_and_creation_strategies = targets_and_creation_strategies

    def generate_target_requests(self, voter: VoterIdentity, requester: VotingRequestCreationService) -> List[AsyncRequest]:
        return [creation_strategy(target, voter, requester) for target, creation_strategy in
                self.targets_and_creation_strategies()]


class PreferentialTargetRequestController(SpecializedTargetRequestController):

    def __init__(self, preferred_targets: Callable[[], List[VotingTarget]], other_targets: Callable[[], List[VotingTarget]]):
        def get_targets():
            preferred_targets_and_creation_strategies = [
                (target, lambda target, voter, req: req.create_request(target, random.choice([
                    StarRating.FOUR_STARS, StarRating.FIVE_STARS],
                    p=[0.1, 0.9]), voter)) for target in preferred_targets()
                ]  # type: List[Tuple[VotingTarget, Callable[[VotingTarget, VoterIdentity, VotingRequestCreationService], AsyncRequest]]

            other_targets_and_creation_strategies = [
                (target, lambda target, voter, req:
                    req.create_request(target, random.choice([
                        StarRating.THREE_STARS, StarRating.FOUR_STARS, StarRating.FIVE_STARS],
                        p=[0.6, 0.2, 0.2]), voter)) for target in other_targets()
                ]  # type: List[Tuple[VotingTarget, Callable[[VotingTarget, VoterIdentity, VotingRequestCreationService], AsyncRequest]]

            return preferred_targets_and_creation_strategies + other_targets_and_creation_strategies

        super().__init__(get_targets)
