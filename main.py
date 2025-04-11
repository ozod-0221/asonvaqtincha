from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message,CallbackQuery
import asyncio
import logging
from config import *
from keyboards import *
from helpers import *
from json_utils import *
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import FSInputFile
admin_filter = F.from_user.id.in_(ADMIN_IDS)
bot=Bot(token=TOKEN)
dp=Dispatcher()

class Form(StatesGroup):
    
    phone = State()
    check = State()
class SendMessage(StatesGroup):

    waiting_for_message= State()
class Event(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_link = State()
    waiting_for_activation=State()
    
    
@dp.message(F.text.startswith("/start"))
async def start(message: Message,state:FSMContext):
    
    user_id = message.from_user.id
    first_name = message.from_user.first_name if message.from_user.first_name else "None"
    last_name = message.from_user.last_name if message.from_user.last_name else "None"
    username = message.from_user.username if message.from_user.username else "None"
    phone_number = "None"
    if user_id in ADMIN_IDS:
        await message.answer("Admin panelga xush kelibsiz!",reply_markup=admin_key())
        return
    else:
        await message.answer(f"Assalomu alekum {first_name}, Xush kelibsiz!", reply_markup=contact_keyboard())
        try:
            if is_user_exist(user_id):
                save_user_data(user_id, first_name, last_name, username, phone_number)
        except Exception as e:
            logging.error(f"Error: {e}")
    
        await message.answer("Iltimos, kontaktni ulashing")
    
    
        await state.set_state(Form.phone)
        data = message.text.split()
        event_name = data[1] if len(data) > 1 else None
        if event_name:
            if is_event_exist(event_name):
                
                try:
                    save_event_participant(event_name,user_id)
                    link=get_event_link_by_event_name(event_name)
                    print(link)
                    await state.update_data(link=link)
                except Exception as e:
                    logging.error(f"Error: {e}")
            else:
                await message.answer("Bunday event mavjud emas!")
        else:
            print("oddiy start")
            
            link=get_active_event_link()
            if link:
                await state.update_data(link=link)
    
            
    
    
    
    
    
    
    
    
   
@dp.message(admin_filter, Command("add_event"))
@dp.message(admin_filter, F.text == "🎁Event qo'shish")
async def add_event(message: Message, state: FSMContext):
    await message.answer("Event nomini kiriting:(space ishlatmang, pastgi chiziqichadan foydalaning)")
    await state.set_state(Event.waiting_for_name)
@dp.message(Event.waiting_for_name)
async def process_event_name(message: Message, state: FSMContext):
    event_name = message.text
    data= event_name.split()
    
    if len(data)>1:
        await message.answer("Iltimos, event nomini faqat bitta so'zda kiriting!")
        return
        await state.set_state(Event.waiting_for_name)
    else:
        await state.update_data(event_name=event_name)
        await message.answer("Event haqida ma'lumot kiriting:")
        await state.set_state(Event.waiting_for_description)
    
@dp.message(Event.waiting_for_description)
async def process_event_description(message: Message, state: FSMContext):
    event_description = message.text
    await state.update_data(event_description=event_description)
    await message.answer("Event linkini kiriting:")
    await state.set_state(Event.waiting_for_link)
@dp.message(Event.waiting_for_link)
async def process_event_link(message: Message, state: FSMContext):
    event_link = message.text
   
    await state.update_data(event_link=event_link)
    await message.answer("Event aktivligini belgilang (True yoki False):")
    await state.set_state(Event.waiting_for_activation)

@dp.message(Event.waiting_for_activation)
async def process_event_activation(message: Message, state: FSMContext):
    event_activation = message.text.lower() == "true"
    await state.update_data(event_activation=event_activation)
    data = await state.get_data()
    event_name = data.get("event_name")
    event_description = data.get("event_description")
    event_link = data.get("event_link")
    event_activation = data.get("event_activation")
    save_event(event_name, event_description, event_link, event_activation)
    await message.answer("Event muvaffaqiyatli qo'shildi!")
    await state.clear()
@dp.message(Form.phone, F.contact)
async def process_contact(message: Message, state: FSMContext,bot:Bot):
    message_id = message.message_id
    contact = message.contact
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username if message.from_user.username else "Aniqlanmadi"
    
    if not is_true_contact(contact,message):
        await message.answer("Iltimos, to'g'ri kontaktni ulang")
        return
    phone_number = contact.phone_number
    
    if not str(phone_number).startswith("+"):
        phone_number = f"+{phone_number}"
    await state.update_data(phonenumber=phone_number,message_id=message_id,user_id=user_id,full_name=full_name,username=username)
    await state.set_state(Form.check)
    
    await message.answer(f"Translyatsiyaga qo'shilishuchun  uchun bizning Telegram va Instagram sahifalarimizga  a`zo bo`ling",reply_markup=subs_key())
async def check_subscription(user_id:int,bot:Bot) -> bool:
    try:
        user = await bot.get_chat_member(CHANNEL_ID, user_id)
        if user.status in ["member", "administrator", "creator"]:
            return True
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
    return False 
@dp.message(admin_filter,F.text == "💬 Xabar yuborish")
async def send_message(message: Message,state: FSMContext):
    await message.answer("Kanaldagi postning URL manzilini kiriting:")
    await state.set_state(SendMessage.waiting_for_message)
@dp.message(SendMessage.waiting_for_message)
async def forward_message(message: Message, state: FSMContext,bot:Bot):
    post_link = message.text
    message_id = post_link.split("/")[-1]

    # Kanaldagi postni olish
    for user_id in get_all_user_ids() :
        try:
            await bot.forward_message(user_id,CHANNEL_ID,  message_id)
            await asyncio.sleep(0.3)
        except Exception as e:
            logging.error(f"Xatolik sodir bo'ldi: {e}")
    await message.answer("Xabar yuborildi!")
    
    await state.clear()
@dp.message(admin_filter,F.text == "📊 Statistika")
async def send_statistics(message: Message):
   events=get_all_events()
   for event in events:
    event_name = event["event_name"]
    referal_link = f"https://t.me/{BOT_USERNAME}?start={event_name}"
    count = get_count_of_participants(event_name)

    await message.answer(
        f"📕Event nomi: {event_name}\n"
        f"ℹ️Event haqida ma'lumot: {event['event_description']}\n"
        f"🔗Event linki: {event['event_link_end']}\n"
        f"➕Qatnashuchilar soni: {count}\n"
        f"🔗Referal link: {referal_link}\n",
        reply_markup=await stats_key(event_name)
    )

@dp.callback_query(F.data.startswith("pin_"))
async def handle_pin_event(callback: CallbackQuery, bot: Bot):
    event_id = str(callback.data.split("_")[1])
    await callback.answer("bajarildi", show_alert=True)
    try:
        pin_event(event_id)
        
        await callback.message.answer("Event faollashtirildi")
    except Exception as e:
        await callback.message.answer(f"Xatolik yuz berdi: {str(e)}")
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
@dp.callback_query(F.data.startswith("delete_"))
async def delete_events(callback: CallbackQuery):
    event_id = str(callback.data.split("_")[1])
   
    try:
        delete_event(event_id)
        await callback.answer("Event o'chirildi", show_alert=True)
        await callback.message.answer("Event o'chirildi")
        
    except Exception as e:
        await callback.message.answer(f"Xatolik yuz berdi: {str(e)}")
        print(f"Xatolik yuz berdi: {str(e)}")
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
@dp.callback_query(F.data.startswith("participants_")) 
async def handle_export_participants(callback: CallbackQuery, bot: Bot):
    try:
        event_name = str(callback.data.split("_")[1])
        
        await callback.answer("Excel fayl tayyorlanmoqda...", show_alert=False)
        
        filename = export_participants_to_excel(event_name)
        print(f"Fayl nomi: {filename}")
        
        if not filename:
            await callback.message.answer("Bu eventda hali qatnashchilar yo'q")
            return

        # Faylni to'g'ri formatda yuborish
        document = FSInputFile(filename)
        
        await callback.message.answer_document(
            document=document,
            caption=f"Event {event_name} qatnashchilari ro'yxati"
        )
        
        # Faylni o'chirish
        os.remove(filename)
            
    except Exception as e:
        await callback.message.answer(f"Xatolik yuz berdi: {str(e)}")
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
    
@dp.callback_query(Form.check,F.data=="check")
async def get_callback(callback:CallbackQuery,state:FSMContext,bot:Bot):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name if callback.from_user.first_name else "None"
    last_name = callback.from_user.last_name if callback.from_user.last_name else "None"
    username = callback.from_user.username if callback.from_user.username else "None"
    phone_number = "None"
    
    
    user_data = await state.get_data()
    phone_number = user_data.get('phonenumber')
    link=user_data.get('link')
    event_name= get_event_name_by_event_link(link)
    # Check if the user is subscribed to the channel
    if not await check_subscription(user_id,bot):
        await callback.answer("Iltimos, avval kanalga a'zo bo'ling", show_alert=True)
        return
    if await check_subscription(user_id,bot):
        
        #send file to user by id file
        order_text = (
        f"🚨Yangi buyurtma!\n"
        f"📛Ism: {user_data.get('full_name', 'Aniqlanmadi')}\n"
        f"🆔Foydalanuvchi ID: {user_data.get('user_id', 'Aniqlanmadi')}\n"
        f"☎️Telefon: {phone_number}\n"
        f"👤Username: @{callback.from_user.username if callback.from_user.username else ' Aniqlanmadi'}\n"
        f"🎁Event nomi:{event_name if event_name else 'Active event orqali orqali'}\n"
    )
        for admin_id in ADMIN_IDS:
            try:
                if not callback.from_user.username:
                    await bot.forward_message(
                    chat_id=admin_id,
                    from_chat_id=callback.from_user.id,
                #any_message_id_from_user
                    message_id=user_data.get('message_id')
             )
                await bot.send_message(admin_id, order_text)
            
                

            except Exception as e:
                logging.error(f"Adminga yuborishda xatolik: {e}")
                await callback.answer(
                "Xatolik yuz berdi, yana bir bor urinib ko`ring:\n/start",
                reply_markup=ReplyKeyboardRemove()
                )
        
        
        
        await bot.send_message(
                user_id,
                f"!Translyatsiyaga shu yerda bo`ladi : \n{link}\n\n",
                reply_markup=ReplyKeyboardRemove()
                )
        await callback.answer("Tabriklaymiz , siz ro`yhatdan o`tdingiz 🚨\n Jonli efir havolasi jo`natildi 🎁🎁",show_alert=True)
    update_user_data(user_id,first_name,last_name,username,phone_number)     
            
       
    await state.clear()    
       



async def main():
   
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    try: 
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
