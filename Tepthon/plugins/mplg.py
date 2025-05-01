import asyncio
import os
import logging
from pathlib import Path

from telethon import functions
from telethon.tl.types import InputPeerChannel, InputMessagesFilterDocument

from . import zedub
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.utils import install_pip
from ..utils import lload_module, inst_done

LOGS = logging.getLogger(__name__)
h_type = True

if Config.ZELZAL_A and Config.ZELZAL_HASH:

    async def install():
        if gvarstatus("PMLOG") and gvarstatus("PMLOG") != "false":
            delgvar("PMLOG")
        if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") != "false":
            delgvar("GRPLOG")
        try:
            entity = InputPeerChannel(channel_id=int(Config.ZELZAL_A), access_hash=int(Config.ZELZAL_HASH))
            full_info = await zedub(functions.channels.GetFullChannelRequest(channel=entity))
            zilzal = full_info.full_chat.id
        except Exception as e:
            LOGS.error(f"خطأ أثناء جلب القناة: {e}")
            return

        documentss = await zedub.get_messages(zilzal, None, filter=InputMessagesFilterDocument)
        total = int(documentss.total)
        plgnm = 0
        for module in range(total):
            if plgnm == 21:
                break
            plugin = documentss[module]
            if not plugin or not plugin.file:
                continue
            plugin_name = plugin.file.name
            if plugin_name.endswith(".py"):
                if os.path.exists(f"Tepthon/plugins/{plugin_name}"):
                    continue
                downloaded_file_name = await zedub.download_media(plugin, "Tepthon/plugins/")
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                flag = True
                check = 0
                while flag:
                    try:
                        lload_module(shortname.replace(".py", ""))
                        plgnm += 1
                        break
                    except ModuleNotFoundError as e:
                        install_pip(e.name)
                        check += 1
                        if check > 5:
                            break
        print(inst_done)
        addgvar("PMLOG", h_type)
        if gvarstatus("GRPLOOG") is not None:
            addgvar("GRPLOG", h_type)

    zedub.loop.create_task(install())
