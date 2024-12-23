import logging

from aiogram import Bot, Router

# from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

# from messages import PARSE_MODE_MARKDOWN, AdminMessages

admin_router = Router()


@admin_router.message(Command("admin_msg"))
async def admin_message_handler(
    message: Message,
    command: CommandObject,
    bot: Bot,
    logger: logging.Logger,
):
    #     if not is_user_admin(message.from_user.id, user_groups.admins, logger):
    #         await message.answer(AdminMessages.NOT_ADMIN_ERROR)
    #         return

    #     try:
    #         user_group_name, send_type, msg_to_send = parse_command_args(command.args, user_groups.valid_names)
    #     except ValueError:
    #         logger.info(f"User {message.from_user.id} typed wrong format for admin message")
    #         await message.reply(
    #             AdminMessages.WRONG_FORMAT.format(groups=list(user_groups.valid_names)),
    #             parse_mode=PARSE_MODE_MARKDOWN,
    #         )
    #         return

    #     user_group = await user_groups(session=session, user_group_name=user_group_name)

    #     stats = await send_messages_to_group(bot, user_group, send_type, msg_to_send, logger)

    #     await message.answer(
    #         AdminMessages.SUCCESS.format(
    #             group_name=user_group_name,
    #             group_cnt=len(user_group),
    #             sent_cnt=stats["sent_cnt"],
    #             blocked_cnt=stats["blocked_cnt"],
    #             chat_not_found=stats["chat_not_found"],
    #             other_err=stats["other_err"],
    #         ),
    #         parse_mode=PARSE_MODE_MARKDOWN,
    #     )

    #     logger.info(
    #         f"Number of users to whom the message was sent: {stats['sent_cnt']}",
    #         extra={
    #             "user_id": message.from_user.id,
    #             "command": "admin_msg",
    #             "user_group": user_group_name,
    #             "stats": stats,
    #         },
    #     )

    # def is_user_admin(user_id, admins, logger):
    #     if user_id not in admins:
    #         logger.info(f"User {user_id} is not in admins group")
    #         return False
    #     return True

    # def parse_command_args(command_args, valid_group_names):
    #     try:
    #         user_group_name, send_type, msg_to_send = command_args.split(" ", maxsplit=2)
    #         if user_group_name not in valid_group_names:
    #             raise ValueError("Invalid user group name")
    #         if send_type not in ["check", "send"]:
    #             raise ValueError("Invalid send type")
    #         return user_group_name, send_type, msg_to_send
    #     except ValueError:
    #         raise ValueError("Invalid command format")

    # async def send_messages_to_group(bot, user_group, send_type, msg_to_send, logger):
    #     stats = {
    #         "sent_cnt": 0,
    #         "blocked_cnt": 0,
    #         "chat_not_found": 0,
    #         "other_err": 0,
    #     }
    #     for user in user_group:
    #         try:
    #             if send_type == "send":
    #                 await bot.send_message(chat_id=user, text=msg_to_send)
    #             else:
    #                 await bot.get_chat(chat_id=user)
    #             stats["sent_cnt"] += 1
    #         except TelegramForbiddenError as e:
    #             if "bot was blocked by the user" in str(e):
    #                 stats["blocked_cnt"] += 1
    #             else:
    #                 stats["other_err"] += 1
    #         except TelegramBadRequest as e:
    #             if "chat not found" in str(e):
    #                 stats["chat_not_found"] += 1
    #             else:
    #                 stats["other_err"] += 1
    #         except Exception:
    #             stats["other_err"] += 1
    #             logger.error(
    #                 "Some problem with admin message.",
    #                 exc_info=True,
    #             )
    #     return stats
    pass
