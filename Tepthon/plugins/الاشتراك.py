#زدثون
import asyncio
import requests
import logging

from telethon import events, Button
from telethon.tl.functions.messages import ExportChatInviteRequest

from Tepthon import zedub
from Tepthon import BOTLOG_CHATID
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

@zedub.zed_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def supc(event):  # Zed-Thon - ZelZal
    chat = await event.get_chat()
    zed_dev = (1260465030, 925972505, 5176749470, 5280339206)
    zelzal = (await event.get_sender()).id
    if zelzal in zed_dev:
        return
    if chat.bot:
        return
    if gvarstatus("sub_private"):
        try:
            idd = event.peer_id.user_id
            tok = Config.TG_BOT_TOKEN
            ch = gvarstatus("Custom_Pm_Channel")
            try:
                ch = int(ch)
            except Exception as r:
                return await zedub.tgbot.send_message(BOTLOG_CHATID, f"**- خطأ في معرف القناة\n{r}**")

            url = f"https://api.telegram.org/bot{tok}/getChatMember?chat_id={ch}&user_id={idd}"
            req = requests.get(url)
            data = req.json()

            if not data.get("ok", False):
                desc = data.get("description", "")
                if desc == "Bad Request: PARTICIPANT_ID_INVALID":
                    # العضو ليس في القناة
                    c = await zedub.get_entity(ch)
                    chn = c.username
                    if c.username is None:
                        ra = await zedub.tgbot(ExportChatInviteRequest(ch))
                        chn = ra.link
                    if chn.startswith("https://"):
                        await event.reply(
                            f"**⎆╎يجب عليك الاشتراك بالقناة أولًا\n⎆╎قناة الاشتراك : {chn}**",
                            buttons=[[Button.url("اضغط للاشتراك 🤍", chn)]]
                        )
                        return await event.delete()
                    else:
                        await event.reply(
                            f"**⎆╎اشترك في قناة الاشتراك للتحدث معي رجاءً لا يمكنك التحدث إلا بعد الاشتراك ♡\n⎆╎قناة الاشتراك : @{chn}**",
                            buttons=[[Button.url("اضغط للاشتراك 🤍", f"https://t.me/{chn}")]]
                        )
                        return await event.delete()
                else:
                    await zedub.tgbot.send_message(BOTLOG_CHATID, f"**- خطأ من تيليجرام:\n{data}**")
                    return

            member_status = data.get("result", {}).get("status", "")
            if member_status in ("left", "kicked"):
                c = await zedub.get_entity(ch)
                chn = c.username
                if c.username is None:
                    ra = await zedub.tgbot(ExportChatInviteRequest(ch))
                    chn = ra.link
                if chn.startswith("https://"):
                    await event.reply(
                        f"**⎆╎يجب عليك الاشتراك بالقناة أولًا\n⎆╎قناة الاشتراك : {chn}**",
                        buttons=[[Button.url("اضغط للاشتراك 🤍", chn)]]
                    )
                    return await event.message.delete()
                else:
                    await event.reply(
                        f"**⎆╎اشترك في قناة الاشتراك للتحدث معي رجاءً لا يمكنك التحدث إلا بعد الاشتراك ♡\n⎆╎قناة الاشتراك : @{chn}**",
                        buttons=[[Button.url("اضغط للاشتراك 🤍", f"https://t.me/{chn}")]]
                    )
                    return await event.message.delete()

        except Exception as er:
            await zedub.tgbot.send_message(BOTLOG_CHATID, f"**- خطـأ\n{er}**")
