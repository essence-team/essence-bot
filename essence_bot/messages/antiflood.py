from dataclasses import dataclass


@dataclass
class AntiFloodMessages:
    DAILY_LIMIT_EXCEEDED = "Вы достигли дневного лимита в {limit} сообщений.\nПожалуйста, попробуйте снова завтра."
    TOO_MANY_MESSAGES = "Превышен лимит отправки сообщений.\nПопробуйте снова через {seconds} секунд"
    MESSAGE_TOO_LONG = "Ваше сообщение слишком длинное. Максимальная длина - {max_message_len} символов."
