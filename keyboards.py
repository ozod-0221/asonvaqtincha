
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import INSTAGRAM_URL, TG_CHANNEL_URL
from aiogram.utils.keyboard import InlineKeyboardBuilder
from json_utils import delete_event,pin_event,search_active_event   ,is_event_active
def contact_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="☎️Kontaktni ulashish", request_contact=True))
    
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
def  subs_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="↗️Instagram",url=INSTAGRAM_URL),
        InlineKeyboardButton(text="↗️Telegram",url=TG_CHANNEL_URL),

        InlineKeyboardButton(text="✅Tekshirish",callback_data="check"),
    )
    builder.adjust(1)
    return builder.as_markup()
def admin_key():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="💬 Xabar yuborish"))
    builder.add(KeyboardButton(text="📊 Statistika"))
    builder.add(KeyboardButton(text="🎁Event qo'shish"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
async def stats_key(event_name: str) -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()
    if is_event_active(event_name):
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text="👤 Qatnashuvchilar",callback_data=f"participants_{event_name}"),
            InlineKeyboardButton(text="🗑️O'chirish",callback_data=f"delete_{event_name}"),
            InlineKeyboardButton(text="📍Mahkamlangan",callback_data=f"pin_{event_name}"),
        )
    else:
        
        builder.add(
            InlineKeyboardButton(text="👤 Qatnashuvchilar",callback_data=f"participants_{event_name}"),
            InlineKeyboardButton(text="🗑️O'chirish",callback_data=f"delete_{event_name}"),
            InlineKeyboardButton(text="🔁Faollashtirish",callback_data=f"pin_{event_name}"),
        )
    builder.adjust(1)
    return builder.as_markup()