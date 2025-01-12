import logging

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, ContentType, Message, PreCheckoutQuery
from keyboards.subscription import extend_subscription_kb, get_subscription_option_kb, payload2days, subscribe_kb
from services.essence_backend import EssenceBackendAPI

subscription_router = Router(name="subscription_router")


# TODO: вынести все тексты в message SubscriptionMessages
@subscription_router.message(F.text == ("Подписка"))
async def subscription_handler(message: Message, essence_api: EssenceBackendAPI, logger: logging):
    user_id = str(message.from_user.id)

    try:
        user = await essence_api.get_user(user_id)
    except Exception:
        await message.answer("Произошла ошибка при получении данных пользователя.")
        return

    remaining_days = user.remaining_days

    if remaining_days is not None:
        response_text = f"У вас осталось {remaining_days} дней подписки."
        await message.answer(response_text, reply_markup=extend_subscription_kb)
    else:
        response_text = "У вас нет активной подписки."
        await message.answer(response_text, reply_markup=subscribe_kb)


@subscription_router.callback_query(F.data.in_(["extend_subscription", "subscribe"]))
async def subscription_callback(callback_query: CallbackQuery, bot: Bot):
    sub_kb = await get_subscription_option_kb(bot)
    print(sub_kb)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=("Выберите подходящий вариант подписки \nТестовые данные карты `1111 1111 1111 1026`, `12/22`, CVC `000`"),
        reply_markup=sub_kb,
    )


# Обработчик предчекового запроса
@subscription_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, logger: logging.Logger):
    payload = pre_checkout_query.invoice_payload
    logger.info(f"Received pre-checkout query with payload: {payload} from user {pre_checkout_query.from_user.id}")

    if not payload.startswith("subscription_payment_"):
        await pre_checkout_query.answer(ok=False, error_message="Некорректный платежный запрос.")
        logger.warning(f"Invalid payload in pre-checkout: {payload}")
        return

    subscription_payload = payload.replace("subscription_payment_", "")
    duration = payload2days.get(subscription_payload, None)

    if not duration:
        await pre_checkout_query.answer(ok=False, error_message="Некорректный тип подписки.")
        logger.warning(f"Unknown subscription in pre-checkout: {subscription_payload}")
        return

    # Здесь можно добавить дополнительные проверки, например, проверку пользователя или доступности подписки
    await pre_checkout_query.answer(ok=True)
    logger.info(f"Pre-checkout query approved for payload: {payload}")


@subscription_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message, essence_api: EssenceBackendAPI, logger: logging.Logger):
    successful_payment = message.successful_payment
    user_id = str(message.from_user.id)
    payload = successful_payment.invoice_payload
    logger.info(f"Received successful payment from user {user_id} with payload: {payload}")

    if not payload.startswith("subscription_payment_"):
        await message.answer("Неизвестный тип подписки. Пожалуйста, обратитесь в поддержку.")
        logger.error(f"Invalid payload in successful payment: {payload}")
        return

    subscription_payload = payload.replace("subscription_payment_", "")
    duration = payload2days.get(subscription_payload, None)

    if not duration:
        await message.answer("Неизвестный тип подписки. Пожалуйста, обратитесь в поддержку.")
        logger.error(f"Unknown subscription in successful payment: {subscription_payload}")
        return

    try:
        await essence_api.subscribe_user(
            payment_id=successful_payment.provider_payment_charge_id,
            user_id=user_id,
            days_cnt=duration,
        )
        logger.info(f"Updated subscription for user {user_id} for {duration} days.")
    except Exception as e:
        logger.error(f"Error updating subscription for user {user_id}: {e}")
        await message.answer("Произошла ошибка при обновлении подписки. Пожалуйста, обратитесь в поддержку.")
        return

    await message.answer(f"Спасибо за оплату! Ваша подписка продлена на {duration} дней.")


async def notify_expiring_subscriptions(bot: Bot, essence_api: EssenceBackendAPI, logger: logging.Logger) -> None:
    logger.info("Checking for expiring subscriptions.")
    user_ids = await essence_api.get_expiring_subscriptions(shift_days=2)
    logger.info(f"Found {len(user_ids)} expiring subscriptions.")
    for user_id in user_ids:
        try:
            await bot.send_message(
                user_id,
                "Ваша подписка истекает через 2 дня. Пожалуйста, обновите её, чтобы продолжить пользоваться сервисом.",
            )
            logger.info(f"Sent expiring subscription warning to user {user_id}.")
        except Exception as e:
            logger.error(f"Failed to send expiring subscription warning to user {user_id}: {e}")
    logger.info("Expiring subscriptions check completed.")


async def notify_canceled_subscriptions(bot: Bot, essence_api: EssenceBackendAPI, logger: logging.Logger) -> None:
    logger.info("Checking for canceled subscriptions.")
    user_ids = await essence_api.get_expiring_subscriptions(shift_days=0)
    logger.info(f"Found {len(user_ids)} canceled subscriptions.")
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, "Ваша подписка отменена. Если это была ошибка, свяжитесь с поддержкой.")
            logger.info(f"Notified user {user_id} about subscription cancellation.")
            await essence_api.deactivate_subscription(user_id)
            logger.info(f"Deactivated subscription for user {user_id}.")
        except Exception as e:
            logger.error(f"Failed to notify or deactivate subscription for user {user_id}: {e}")
    logger.info("Canceled subscriptions check completed.")
