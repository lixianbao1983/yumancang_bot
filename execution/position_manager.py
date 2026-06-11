from state_manager import StateManager

state = StateManager()


def can_open_position():

    return state.get("position") is None


