from aiogram.fsm.state import State, StatesGroup


class ChannelStates(StatesGroup):
    waiting_for_channels = State()


class DigestParamsStates(StatesGroup):
    waiting_for_freq = State()
    waiting_for_hour = State()


class DigestQuestionsStates(StatesGroup):
    waiting_for_questions = State()
