import asyncio
from Tepthon import zedub
from telethon import events, TelegramClient
from telethon.tl.custom import Button
from ..Config import Config

plugin_category = "البـوتات"

async def interact_with_botfather(client, command, wait_for=None):
    async with client.conversation('BotFather') as conv:
        await conv.send_message(command)
        if wait_for:
            response = await conv.get_response()
            return response.text
        return None

@zedub.on(events.NewMessage(pattern=r'\.صـنع بـوت (.*)'))
async def create_bot(event):
    try:
        input_str = event.pattern_match.group(1)
        if ' ' not in input_str:
            await event.respond("⎉╎يـجب كتـابة اسـم البـوت ويـوزره مـع المسـافة بيـنهم!\nمثـال: `.صـنع بـوت MyBot mybot`")
            return
            
        name, username = input_str.split(' ', 1)
        if not username.startswith('@'):
            username = f"@{username}"
        
        async with TelegramClient('bot_session', Config.APP_ID, Config.API_HASH) as client:
            # إنـشـاء الـبـوت
            result = await interact_with_botfather(
                client,
                f"/newbot\n{name}\n{username}",
                wait_for=True
            )
            
            if "Done!" in result or "تم!" in result:
                # الحـصـول عـلى الـتـوكـن
                await asyncio.sleep(2)
                token_msg = await interact_with_botfather(
                    client,
                    f"/token {username}",
                    wait_for=True
                )
                
                if "Use this token" in token_msg or "استخدم هذا الرمز" in token_msg:
                    token = token_msg.split('\n')[-1]
                    await event.respond(
                        f"⎉╎✅ تـم إنـشـاء الـبـوت بـنـجـاح!\n\n"
                        f"⎉╎الـيـوزر: {username}\n"
                        f"⎉╎الـتـوكـن: `{token}`\n\n"
                        f"⎉╎يـمـكـنـك الـتـحـكـم فـيه بـاسـتـخـدام الأمـر:\n`.تـحـكـم {username}`",
                        parse_mode='md'
                    )
                else:
                    await event.respond(f"⎉╎✅ تـم إنـشـاء الـبـوت: {username} ولـكـن لـم يـتـم الـحـصـول عـلى الـتـوكـن.")
            else:
                await event.respond(f"⎉╎❌ فـشـل فـي إنـشـاء الـبـوت. قـد يـكـون الـيـوزر مـحـجـوزاً.\n\nالـرد مـن بـوت فـاذر:\n{result}")
                
    except Exception as e:
        await event.respond(f"⎉╎❌ حـدث خـطـأ: {str(e)}")

@zedub.on(events.NewMessage(pattern=r'\.تـحـكـم (.*)'))
async def manage_bot(event):
    username = event.pattern_match.group(1)
    if not username.startswith('@'):
        username = f"@{username}"
    
    buttons = [
        [Button.inline("تـغـيـيـر اسـم الـبـوت", b"change_name")],
        [Button.inline("تـغـيـيـر وصـف الـبـوت", b"change_desc")],
        [Button.inline("تـغـيـيـر صـورة الـبـوت", b"change_pic")],
        [Button.inline("حـذف الـبـوت", b"delete_bot")],
        [Button.inline("الـحـصـول عـلى الـتـوكـن", b"get_token")],
    ]
    
    await event.respond(
        f"⎉╎اخـتـر مـا تـريـد فـعـلـه مـع الـبـوت {username}:",
        buttons=buttons
    )

@zedub.on(events.CallbackQuery(data=b"change_name"))
async def change_name_handler(event):
    async with event.client.conversation(event.sender_id) as conv:
        await conv.send_message("⎉╎ارسـل لـي الاسـم الـجـديـد لـلـبـوت:")
        name_response = await conv.get_response()
        new_name = name_response.text
        
        # الـحـصـول عـلى يـوزر الـبـوت مـن الـرسـالـة الأصـلـيـة
        original_msg = await event.get_message()
        username = original_msg.text.split()[-1]
        
        async with TelegramClient('bot_session', Config.APP_ID, Config.API_HASH) as client:
            result = await interact_with_botfather(
                client,
                f"/setname {username}\n{new_name}",
                wait_for=True
            )
            
            if "Done!" in result or "تم!" in result:
                await event.respond(f"⎉╎✅ تـم تـغـيـيـر اسـم الـبـوت {username} إلـى: {new_name}")
            else:
                await event.respond(f"⎉╎❌ فـشـل فـي تـغـيـيـر الاسـم. الـرد مـن بـوت فـاذر:\n{result}")

@zedub.on(events.CallbackQuery(data=b"change_desc"))
async def change_desc_handler(event):
    async with event.client.conversation(event.sender_id) as conv:
        await conv.send_message("⎉╎ارسـل لـي الـوصـف الـجـديـد لـلـبـوت:")
        desc_response = await conv.get_response()
        new_desc = desc_response.text
        
        original_msg = await event.get_message()
        username = original_msg.text.split()[-1]
        
        async with TelegramClient('bot_session', Config.APP_ID, Config.API_HASH) as client:
            result = await interact_with_botfather(
                client,
                f"/setdescription {username}\n{new_desc}",
                wait_for=True
            )
            
            if "Done!" in result or "تم!" in result:
                await event.respond(f"⎉╎✅ تـم تـغـيـيـر وصـف الـبـوت {username}")
            else:
                await event.respond(f"⎉╎❌ فـشـل فـي تـغـيـيـر الـوصـف. الـرد مـن بـوت فـاذر:\n{result}")

@zedub.on(events.CallbackQuery(data=b"change_pic"))
async def change_pic_handler(event):
    async with event.client.conversation(event.sender_id) as conv:
        await conv.send_message("⎉╎ارسـل لـي الـصـورة الـجـديـدة لـلـبـوت:")
        pic_response = await conv.get_response()
        
        original_msg = await event.get_message()
        username = original_msg.text.split()[-1]
        
        if pic_response.media:
            async with TelegramClient('bot_session', Config.APP_ID, Config.API_HASH) as client:
                await client.send_message(
                    'BotFather',
                    f"/setuserpic {username}",
                    file=pic_response.media
                )
                await asyncio.sleep(3)
                await event.respond(f"⎉╎✅ تـم تـغـيـيـر صـورة الـبـوت {username}")
        else:
            await event.respond("⎉╎❌ لـم يـتـم إرسـال صـورة!")

@zedub.on(events.CallbackQuery(data=b"delete_bot"))
async def delete_bot_handler(event):
    original_msg = await event.get_message()
    username = original_msg.text.split()[-1]
    
    confirm_buttons = [
        [Button.inline("✅ نـعـم، احـذف الـبـوت", b"confirm_delete")],
        [Button.inline("❌ إلـغـاء", b"cancel_delete")]
    ]
    
    await event.respond(
        f"⎉╎هـل أنـت مـتـأكـد مـن حـذف الـبـوت {username}؟ لا يـمـكـن الـتـراجـع عـن هـذا الإجـراء!",
        buttons=confirm_buttons
    )

@zedub.on(events.CallbackQuery(data=b"confirm_delete"))
async def confirm_delete_handler(event):
    original_msg = await event.get_message()
    username = original_msg.text.split()[-2]  # لأن النص تغير
    
    async with TelegramClient('bot_session', Config.APP_ID, Config.API_HASH) as client:
        result = await interact_with_botfather(
            client,
            f"/deletebot {username}",
            wait_for=True
        )
        
        if "Done!" in result or "تم!" in result:
            await event.respond(f"⎉╎✅ تـم حـذف الـبـوت {username} بـنـجـاح")
        else:
            await event.respond(f"⎉╎❌ فـشـل فـي حـذف الـبـوت. الـرد مـن بـوت فـاذر:\n{result}")

@zedub.on(events.CallbackQuery(data=b"cancel_delete"))
async def cancel_delete_handler(event):
    await event.respond("⎉╎تـم إلـغـاء عـمـلـيـة الـحـذف")

@zedub.on(events.CallbackQuery(data=b"get_token"))
async def get_token_handler(event):
    original_msg = await event.get_message()
    username = original_msg.text.split()[-1]
    
    async with TelegramClient('bot_session', Config.APP_ID, Config.API_HASH) as client:
        token_msg = await interact_with_botfather(
            client,
            f"/token {username}",
            wait_for=True
        )
        
        if "Use this token" in token_msg or "استخدم هذا الرمز" in token_msg:
            token = token_msg.split('\n')[-1]
            await event.respond(
                f"⎉╎✅ تـوكـن الـبـوت {username}:\n\n`{token}`",
                parse_mode='md'
            )
        else:
            await event.respond(f"⎉╎❌ لـم يـتـم الـعـثـور عـلى تـوكـن. الـرد مـن بـوت فـاذر:\n{token_msg}")
