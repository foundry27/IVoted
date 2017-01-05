from proxy import ProxySpyRefreshableProxyProvider
from targeting import VotingTarget
from random import sample, choice
from nonce import PageViewNonceGenerator
from humanizing import Humanizer, voting_delay_action, create_view_manipulation_action
from voting.voteridentity import AutoUpdatingProxyVoterPool
from voting.voterprovider import BlockingDaytimeOnlyVoterProviderDecorator, EndlessPooledVoterProvider
from voting.requestcreation import ProxiedNextGENGalleryVotingRequestCreationService
from voting.requestcontroller import PreferentialTargetRequestController
from voting.votingbot import VotingBot, BotConfiguration
from voting.resulthandling import SuccessCheckingVotingResultProcessor

if __name__ == '__main__':
    main_target = VotingTarget('Delores	Reid', 0)

    other_targets = [VotingTarget(name, r_id) for name, r_id in
                     {'Pamela Rios': 1, 'Erick George': 2,
                      'Edgar Myers': 3, 'Beulah Mcgee': 4,
                      'Alvin Haynes': 5, 'Dave Duncan': 6,
                      'Gertrude	Burke': 7, 'Christie	Mccarthy': 8,
                      'Lance James': 9, 'Isabel	Rivera': 10}.items()]

    voting_page_link = 'http://main-website-address/gallery-voting-link'

    bot = VotingBot(
        BotConfiguration(
            BlockingDaytimeOnlyVoterProviderDecorator(
                EndlessPooledVoterProvider(
                    AutoUpdatingProxyVoterPool(
                        pool_size=15, proxy_provider=ProxySpyRefreshableProxyProvider()
                    )
                )
            ),
            ProxiedNextGENGalleryVotingRequestCreationService(
                voting_page_link=voting_page_link
            ),
            PreferentialTargetRequestController(
                preferred_targets=lambda: [main_target],
                other_targets=lambda: sample(other_targets, choice([2, 3]))
            ),
            SuccessCheckingVotingResultProcessor(),
            Humanizer(
                pre_voting_actions=[
                    create_view_manipulation_action(
                        request_link='http://main-website-address/wp-admin/admin-ajax.php',
                        nonce_generator=PageViewNonceGenerator(voting_page_link),
                        post_id=45927)],
                post_voting_actions=[voting_delay_action]
            )
        )
    )
    bot.do_voting()
