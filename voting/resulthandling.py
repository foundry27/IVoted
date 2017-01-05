from typing import List
from abc import ABCMeta, abstractmethod
from requests import Response
from datetime import datetime


class VotingResultProcessor(metaclass=ABCMeta):

    @abstractmethod
    def parse_voting_results(self, responses: List[Response]) -> None:
        pass


class SuccessCheckingVotingResultProcessor(VotingResultProcessor):

    def parse_voting_results(self, responses: List[Response]) -> None:
        for response in responses:
            if response.status_code == 200:
                saving_confirmation_string = 'nggv_js.saved = '
                encoded_response_content = str(response.content, encoding=response.encoding)
                saving_status_index = encoded_response_content.index(saving_confirmation_string) + len(
                    saving_confirmation_string)
                saving_status = True if encoded_response_content[saving_status_index] == '1' else False
                print('Submitted vote to server at {}; performed in {}, vote received -{}-!'
                      .format(datetime.now(), response.elapsed, 'successfully' if saving_status else 'unsuccessfully'))
            else:
                print('Tried to submit vote to server, failed with status code {}'.format(response.status_code))
