import asyncio
from Tepthon import zedub
from telethon import events, TelegramClient
from telethon.tl.types import Bot
from telethon.tl.functions.messages import EditBotGroup
from ..Config import Config

plugin_category = "بوتات"

@zedub.on(events.NewMessage(pattern='\.صنع بوت (.*)'))
async def create_bot(event):
    name, username = event.pattern_match.group(1).split()
    async with TelegramClient('bot_session', Config.APP_ID, Config.API_HASH) as client:
        await client.send_message('BotFather', f"/newbot\n{name}\n@{username}")
        await event.respond(f"**⎉╎✅ تـمّ صُنــع البوت: **@{username}**\n**يُمكنُـكَ التحكم فيه باستخدام الأمر .تحكم **@{username}**")


@zedub.on(events.NewMessage(pattern='\.تحكم (.*)'))
async def manage_bot(event):
    username = event.pattern_match.group(1)
    buttons = [
        ["تغييـر اسم البوت"],
        ["تغييـر وصف البوت"],
        ["تغييـر صورة البوت"],
        ["حـذف البوت"],
    ]
    
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=text) for text in buttons]])
    await event.respond("⎉╎ اختــر ما تريـد فعلـهُ:", reply_markup=reply_markup)


@zedub.on(events.CallbackQuery())
async def callback_query_handler(event):
    # معالجة الأزرار
    if event.data.decode() == "تغييـر اسم البوت":
        await event.respond("أرسل لي الاسم الجديد للبوت.")
    elif event.data.decode() == "تغييـر وصف البوت":
        await event.respond("أرسل لي الوصف الجديد للبوت.")
    elif event.data.decode() == "تغييـر صورة البوت":
        await event.respond("أرسل لي الصورة الجديدة للبوت.")
    elif event.data.decode() == "حـذف البوت":
        await delete_bot(event)


async def delete_bot(event):
    username = event.message.reply_to_msg_id
    async with TelegramClient('bot_session', Config.API_ID, Config.API_HASH) as client:
        await client.send_message('BotFather', f"/deletebot\n@{username}")
        await event.respond(f"⎉╎ تـمّ حَــذف البوت: @{username}")


@zedub.on(events.NewMessage(pattern='\.تغيير اسم البوت (.*)'))
async def change_bot_name(event):
    username, new_name = event.pattern_match.group(1).split()
    async with TelegramClient('bot_session', Config.API_ID, Config.API_HASH) as client:
        await client.send_message('BotFather', f"/setname\n@{username}\n{new_name}")
        await event.respond(f"⎉╎ تمّ تغييـر اسم البـوت إلى: {new_name}")


@zedub.on(events.NewMessage(pattern='\.تغيير وصف البوت (.*)'))
async def change_bot_description(event):
    username, new_description = event.pattern_match.group(1).split()
    async with TelegramClient('bot_session', Config.API_ID, Config.API_HASH) as client:
        await client.send_message('BotFather', f"/setabout\n@{username}\n{new_description}")
        await event.respond(f"⎉╎ تمّ تغييـر وصف البوت.")


@zedub.on(events.NewMessage(pattern='\.تغيير صورة البوت'))
async def change_bot_photo(event):
    username = event.message.reply_to_msg_id
    if event.message.media:
        async with TelegramClient('bot_session', Config.API_ID, Config.API_HASH) as client:
            await client.send_message('BotFather', f"/setphoto\n@{username}", file=event.message.media)
            await event.respond("⎉╎ تمّ تغييـر صورة البوت.")
    else:
        await event.respond("⎉╎ تفضل بإرسال صورة.")
