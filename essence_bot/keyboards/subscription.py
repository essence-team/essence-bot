from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from core.config import load_config

cfg = load_config()
subs_config = cfg.subscriptions
provider_token = cfg.provider_token

payload2days = {sub.payload: sub.duration_days for sub in subs_config}


extend_subscription_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Продлить подписку",
                callback_data="extend_subscription",
            )
        ]
    ]
)


subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Оформить подписку",
                callback_data="subscribe",
            )
        ]
    ]
)


async def get_subscription_option_kb(bot: Bot):
    subscription_options_kb = InlineKeyboardMarkup(inline_keyboard=[])
    for sub in subs_config:
        subscription_options_kb.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=sub.title,
                    callback_data=f"subscribe_{sub.payload}",
                    pay=True,
                    url=await bot.create_invoice_link(
                        title=sub.title,
                        description=sub.description,
                        payload="subscription_payment_" + sub.payload,
                        provider_token=provider_token,
                        currency="RUB",
                        prices=[LabeledPrice(label=sub.title, amount=sub.price)],
                        # start_parameter=sub.start_parameter,
                    ),
                )
            ]
        )

    return subscription_options_kb
