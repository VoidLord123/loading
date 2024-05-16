from system.config import dialogs_tg, tg_channel, test, results, dialogs_vk, time_constants
from system.tg_keyboards import markup_nums, markup_to_user, markup_start
from aiogram import types, F, Router, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command
from system.lib import Database

router = Router()
database = Database("system/db/database.sqlite")


async def check_sub(chat_id, user_id, bot: Bot):
    chat_member = await bot.get_chat_member(chat_id, user_id)
    status = chat_member.status
    if status not in ['left', 'kicked']:
        return True
    else:
        return False


async def get_user_id(chat_id, user_id, bot: Bot):
    chat_member = await bot.get_chat_member(chat_id, user_id)
    status = chat_member.user.username
    return status


async def check_admin(chat_id, user_id, bot: Bot):
    chat_member = await bot.get_chat_member(chat_id, user_id)
    status = chat_member.status
    if status in ['administrator', 'creator']:
        return True
    else:
        return False


async def check_sub_by_name(chat_names, user_id, bot):
    chat_ids = [await get_channel_id(i, bot) for i in chat_names]
    for i in chat_ids:
        if not await check_sub(i, user_id, bot):
            return False
    return True


async def get_channel_id(channel_name, bot: Bot):
    chat = await bot.get_chat(channel_name)
    return chat.id


async def send_with_reply(text: str, kb: ReplyKeyboardMarkup, chat_id, bot: Bot):
    await bot.send_message(chat_id, text, reply_markup=kb)


async def send_with_inline(text: str, kb: InlineKeyboardMarkup, chat_id, bot: Bot):
    await bot.send_message(chat_id, text, reply_markup=kb)


async def send_without_dialog(text: str, chat_id, bot: Bot):
    await bot.send_message(chat_id, text)


@router.message(Command("start"))
async def start(msg: Message, bot: Bot):
    message = dialogs_tg["start"]
    await send_with_inline(message["text"], message["kb"], msg.chat.id, bot)


@router.message(Command("statistic"))
async def statistic_handler(msg: Message, bot: Bot):
    if not await check_admin(await get_channel_id(tg_channel, bot), msg.from_user.id, bot):
        await send_without_dialog("У вас недостаточно прав", msg.from_user.id, bot)
        return
    st = database.get_statistics()
    t = dialogs_vk["statistic"]
    t = t.replace("{vk_m}", str(st["month"]["vk"]))
    t = t.replace("{tg_m}", str(st["month"]["tg"]))
    t = t.replace("{all_m}", str(st["month"]["all"]))
    t = t.replace("{vk_a}", str(st["all_time"]["vk"]))
    t = t.replace("{tg_a}", str(st["all_time"]["tg"]))
    t = t.replace("{all_a}", str(st["all_time"]["all"]))
    await send_without_dialog(t, msg.from_user.id, bot)


async def sending(n: int, d: str, msg: str, bot: Bot):
    if d != "all":
        d2 = time_constants[d] * n
        for i in database.get_active_users(d2, "tg"):
            await send_without_dialog(msg, i.user_id, bot)
    else:
        for i in database.get_all_users("tg"):
            await send_without_dialog(msg, i.user_id, bot)


@router.message(Command("sending"))
async def handle_sending(msg: Message, bot: Bot):
    user_id = msg.from_user.id
    if not await check_admin(await get_channel_id(tg_channel, bot), msg.from_user.id, bot):
        await send_without_dialog("У вас недостаточно прав", msg.from_user.id, bot)
        return
    try:
        k = msg.text.split("~")
        n = k[0].split(' ')
        if len(n) == 3:
            await sending(1, "all", k[1], bot)
        else:
            await sending(int(n[2]), n[1], k[1], bot)
        await send_without_dialog("Успешно", user_id, bot)
    except Exception:
        await send_without_dialog("Что то пошло не так. Попробуйте снова или проверьте правильность команды.",
                                  user_id, bot)


@router.message(Command("to_bot"))
async def to_bot_msg(msg: Message, bot: Bot):
    if not await check_admin(await get_channel_id(tg_channel, bot), msg.from_user.id, bot):
        await send_without_dialog("У вас недостаточно прав", msg.from_user.id, bot)
        return
    await send_with_inline(dialogs_tg["to_bot"]["text"], dialogs_tg["to_bot"]["kb"], msg.from_user.id, bot)


@router.callback_query(lambda c: c.data == 'start_test')
async def start_button(callback_query: types.CallbackQuery, bot: Bot):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    string_id = str(user_id)
    is_sub = await check_sub_by_name([tg_channel], user_id, bot)
    in_db = database.check_user(string_id, "tg")
    if in_db:
        in_test = database.get_user_status(string_id, "tg")
        passed = database.get_user_passed(string_id, "tg")
    else:
        in_test = False
        passed = False
    if not is_sub and not in_test:
        await send_with_inline(dialogs_tg["not_subscribed"]["text"], dialogs_tg["not_subscribed"]["kb"], user_id, bot)
    elif is_sub and not in_db:
        database.add_user(string_id, user_type="tg")
        database.set_user_status(string_id, True, "tg")
        await send_without_dialog(dialogs_tg["start_test"]["text"], user_id, bot)
        await send_with_reply(test[database.get_user_index(string_id, "tg")], markup_nums, user_id, bot)
    elif is_sub and not in_test and not passed:
        database.set_user_status(string_id, True, "tg")
        await send_without_dialog(dialogs_tg["start_test"]["text"], user_id, bot)
        await send_with_reply(test[database.get_user_index(string_id, "tg")], markup_nums, user_id, bot)


@router.message()
async def msg_handler(msg: Message, bot: Bot):
    text = msg.text
    user_id = msg.from_user.id
    string_id = str(user_id)
    in_db = database.check_user(string_id, "tg")
    if in_db:
        in_test = database.get_user_status(string_id, "tg")
        passed = database.get_user_passed(string_id, "tg")
    else:
        in_test = False
        passed = False
    if text in [str(i) for i in range(1, 11)] and in_test and not passed:
        fin, scr = database.answer(string_id, int(text), "tg")
        if fin:
            i = 0
            while not scr < results[i][0]:
                i += 1
            database.set_user_passed(string_id, True, "tg")
            await send_with_reply(results[i][-1], ReplyKeyboardRemove(), user_id, bot)
            await send_with_inline(dialogs_tg["finish_test"]["text"], dialogs_tg["finish_test"]["kb"], user_id, bot)

        else:
            await send_with_reply(test[database.get_user_index(string_id, "tg")], markup_nums, user_id, bot)
