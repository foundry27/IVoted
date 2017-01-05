import time

import grequests
import numpy

from humanizing import Humanizer
from voting.requestcreation import VotingRequestCreationService
from voting.requestcontroller import TargetRequestController
from voting.voteridentity import VoterIdentity
from voting.voterprovider import VoterProvider
from voting.resulthandling import VotingResultProcessor


class BotConfiguration:

    def __init__(self, voter_provider: VoterProvider,
                 request_generator: VotingRequestCreationService,
                 request_controller: TargetRequestController,
                 result_processor: VotingResultProcessor,
                 humanizer: Humanizer):
        self.voter_provider = voter_provider
        self.request_generator = request_generator
        self.request_controller = request_controller
        self.result_processor = result_processor
        self.humanizer = humanizer

    def get_voter_provider(self) -> VoterProvider:
        return self.voter_provider

    def get_request_creation_strategy(self) -> VotingRequestCreationService:
        return self.request_generator

    def get_request_controller(self) -> TargetRequestController:
        return self.request_controller

    def get_result_processor(self) -> VotingResultProcessor:
        return self.result_processor

    def get_humanizer(self) -> Humanizer:
        return self.humanizer


class VotingBot:

    def __init__(self, configuration: BotConfiguration):
        self.voter_provider = configuration.get_voter_provider()
        self.request_creator = configuration.get_request_creation_strategy()
        self.request_controller = configuration.get_request_controller()
        self.result_processor = configuration.get_result_processor()
        self.humanizer = configuration.get_humanizer()

    def do_voting(self):

        def submit_votes(voter: VoterIdentity):
            voting_results = grequests.map(self.request_controller.generate_target_requests(voter, self.request_creator))

            self.result_processor.parse_voting_results(voting_results)

        while self.voter_provider.has_voters_remaining():
            self.humanizer.perform_pre_voting_actions()
            self.voter_provider.use_current_voter(submit_votes)
            self.humanizer.perform_post_voting_actions()
