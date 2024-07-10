from typing import Protocol


class RigModule(Protocol):

    def base_skeleton(self) -> None:
        pass

    def forward_kinematic(self) -> None:
        pass

    def inverse_kinematic(self) -> None:
        pass

    def switch_kinematic(self) -> None:
        pass

    def twist_mechanism(self) -> None:
        pass

    def stretch_mechanism(self) -> None:
        pass

    def generate_module(self) -> None:
        pass
