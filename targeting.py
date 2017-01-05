class VotingTarget:

    def __init__(self, target_name: str, target_id: int) -> None:
        self.target_name = target_name
        self.target_id = target_id

    def get_target_id(self) -> int:
        return self.target_id

    def get_target_name(self) -> str:
        return self.target_name
