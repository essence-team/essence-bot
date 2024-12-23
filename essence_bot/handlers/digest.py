import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from services.essence_backend import EssenceBackendAPI
from states.states import DigestQuestionsStates

digest_router = Router(name="digest_router")


@digest_router.message(F.text == "Получить дайджест")
async def get_digest(message: Message, state: FSMContext, essence_api: EssenceBackendAPI, logger: logging.Logger):
    user_id = str(message.from_user.id)
    logger.info(f"User {user_id} requested a digest.")

    digest_date = (await state.get_data()).get("digest_date")
    if digest_date and digest_date.date() != message.date.date():
        await state.clear()

    if (await state.get_state()) == DigestQuestionsStates.waiting_for_questions:
        await message.answer(
            "Ты уже получил сегодня дайджест. Для нового нужно подождать, а по старому дайджесту можно задать вопросы."
        )
        return

    digest = await essence_api.get_digest(user_id)
    if not digest:
        await message.answer("У вас нет активной подписки. Пожалуйста, оформите подписку, чтобы получать дайджест.")
        return

    digest_message = build_digest_text(digest)
    await send_or_split_digest(digest_message, message)

    await state.set_state(DigestQuestionsStates.waiting_for_questions)
    await state.update_data(digest_date=message.date)
    await message.answer("Ты можешь задать любой вопрос появившийся по дайджесту. Я очень постараюсь на него ответить.")


def build_digest_text(digest):
    text = "Ваш дайджест:\n\n"
    for aggregated_post in digest:
        text += f"🔵 {aggregated_post.title}\n"
        for post in aggregated_post.posts:
            text += f"- {post.post_link}\n"
        text += "\n"
    return text


async def send_or_split_digest(digest_message: str, message: Message):
    if len(digest_message) > 4096:
        parts = digest_message.split("🔵")
        for p in parts:
            content = p.strip()
            if content:
                await message.answer(f"🔵 {content}", disable_web_page_preview=True)
    else:
        await message.answer(digest_message, disable_web_page_preview=True)


@digest_router.message(DigestQuestionsStates.waiting_for_questions)
def get_answer_for_question(message: Message, state: FSMContext, essence_api: EssenceBackendAPI):
    pass
