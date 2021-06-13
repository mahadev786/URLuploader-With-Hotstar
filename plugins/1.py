import logging
logger = logging.getLogger(__name__)

import datetime
from sample_config import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied


@Client.on_message(filters.private & filters.incoming)
async def force_sub(bot, update):
    if Config.FORCE_SUB:
        try:
            chat = await bot.get_chat_member(Config.FORCE_SUB, update.from_user.id)
            if chat.status=='kicked':
                return await update.reply_text('Hai you are kicked from my updates channel. So, you are not able to use me',  quote=True)

        except UserNotParticipant:
            button = [[InlineKeyboardButton('Join Our Updates Channel', url=f'https://t.me/Deva_TG_UPDATE')]]
            markup = InlineKeyboardMarkup(button)
            return await update.reply_text(text="Hey join in my updates channel to use me.", parse_mode='markdown', reply_markup=markup, quote=True)

        except ChatAdminRequired:
            logger.warning(f"Make me admin in @{Config.FORCE_SUB}")
            if update.from_user.id in Config.AUTH_USERS:
                return await update.reply_text(f"Make me admin in @{Config.FORCE_SUB}")

        except UsernameNotOccupied:
            logger.warning("The forcesub username was Incorrect. Please give the correct username.")
            if update.from_user.id in Config.AUTH_USERS:
                return await update.reply_text("The forcesub username was Incorrect. Please give the correct username.")

        except Exception as e:
            if "belongs to a user" in str(e):
                logger.warning("Forcesub username must be a channel username Not yours or any other users username")
                if update.from_user.id in Config.AUTH_USERS:
                    return await update.reply_text("Forcesub username must be a channel username Not yours or any other users username")
            logger.error(e)
            return await update.reply_text("Some thing went wrong. Try again and if same issue occur contact [our group](https://t.me/MeGBotsChat)", disable_web_page_preview=True, quote=True)

    await update.continue_propagation()
