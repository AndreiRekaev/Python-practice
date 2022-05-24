from aiogram import types
from dispatcher import dp
import config
import re
from bot import BotDB


@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Welcome, friend!")

@dp.message_handler(commands = ("spent", "earned", "s", "e"), commands_prefix = "/!")
async def start(message: types.Message):
    cmd_variants = (('/spent', '/s', '!spent', '!s'), ('/earned', '/e', '!earned', '!e'))
    operation = '-' if message.text.startswith(cmd_variants[0]) else '+'

    value = message.text
    for i in cmd_variants:
        for j in i:
            value = value.replace(j, '').strip()

    if (len(value)):
        x = re.findall(r"\d+(?:.\d+)?", value)
        if (len(x)):
            value = float(x[0].replace(',', '.'))

            BotDB.add_record(message.from_user.id, operation, value)

            if (operation == '-'):
                await message.reply("✅ Record about <u><b>spent</b></u> sucessfully is created!")
            else:
                await message.reply("✅ Record about <u><b>earn</b></u> succesfully is created!")
        else:
            await message.reply("Couldn't determine the amount!")
    else:
        await message.reply("No amount entered!")


@dp.message_handler(commands = ("history", "h"), commands_prefix = "/!")
async def start(message: types.Message):
    cmd_variants = ('/history', '/h', '!history', '!h')
    within_als = {
        "day": ('today', 'day'),
        "month": ('month'),
        "year": ('year'),
    }

    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, '').strip()

    within = 'day'
    if(len(cmd)):
        for k in within_als:
            for als in within_als[k]:
                if(als == cmd):
                    within = k

    records = BotDB.get_records(message.from_user.id, within)

    if (len(records)):
        answer = f"🕘 History of operations from {within_als[within][-1]}\n\n"

        for r in records:
            answer += "<b>" + ("➖ Spent" if not r[2] else "➕ Earn") + "</b>"
            answer += f" - {r[3]}"
            answer += f" <i>({r[4]})</i>\n"

        await message.reply(answer)
    else:
        await message.reply("No records found!")