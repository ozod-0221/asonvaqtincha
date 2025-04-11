import json
from aiogram.types import Message
from config import *
from datetime import datetime
from aiogram import  Bot
import os
import pandas as pd

def save_user_data(user_id, first_name, last_name=None, username=None, phone_number=None):
    try:
        # Avvalgi foydalanuvchilarni o'qish
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    # Yangi foydalanuvchining id sini avtomatik inkrement qilish
    new_id = len(users) + 1  # id avtomatik ravishda inkrementlanadi
    if  not is_user_exist(user_id):
    # Foydalanuvchi ma'lumotlarini qo'shish
        users.append({
        "id": new_id,
        "user_id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "phone_number": phone_number
        })

    # Ma'lumotlarni JSON faylga yozish
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(users, file, indent=4)

# JSON fayldan foydalanuvchi ma'lumotlarini olish
def update_user_data(user_id: int, first_name: str, last_name: str, username: str, phone_number: str):
    # Fayl mavjudligini tekshirish va o'qish
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                users = json.load(file)
        except json.JSONDecodeError:
            users = []
    else:
        users = []

    # Foydalanuvchi mavjudligini tekshirish
    user_found = False
    for user in users:
        if user['user_id'] == user_id:
            user['first_name'] = first_name or None
            user['last_name'] = last_name or None
            user['username'] = username or None
            user['phone_number'] = phone_number or None
            user_found = True
            break

    # Agar topilmasa, yangi foydalanuvchi qo'shish
    if not user_found:
        new_id = (max([u["id"] for u in users]) + 1) if users else 1
        users.append({
            "id": new_id,
            "user_id": user_id,
            "first_name": first_name or None,
            "last_name": last_name or None,
            "username": username or None,
            "phone_number": phone_number or None
        })

    # Yangilangan ro'yxatni saqlash
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)
def get_all_user_ids():
    try:
        # user_data.json faylini o'qish
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)
        
        # Foydalanuvchilarning user_id'larini ro'yxat sifatida qaytarish
        user_ids = [user['user_id'] for user in users]
        return user_ids
    except (FileNotFoundError, json.JSONDecodeError):
        # Agar fayl topilmasa yoki xato bo'lsa, bo'sh ro'yxat qaytaradi
        return []
   
def is_user_exist(user_id: int) -> bool:
    try:
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)
        # user_id bor-yo'qligini tekshirish
        return any(user['user_id'] == user_id for user in users)
    except (FileNotFoundError, json.JSONDecodeError):
        # Agar fayl mavjud bo'lmasa yoki bo'sh bo'lsa
        return False
def get_user_data(user_id):
    try:
        with open(USER_DATA_FILE, 'r') as file:
            users = json.load(file)
        for user in users:
            if user["user_id"] == user_id:
                return user
    except (FileNotFoundError, json.JSONDecodeError):
        return None  # Agar fayl topilmasa yoki xato bo'lsa

    return None  # Foydalanuvchi topilmasa
def save_event(event_name, event_description, event_link_end,is_active):
    try:
        # Avvalgi events'ni o'qish
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []

    # Yangi event'ning id sini avtomatik inkrement qilish
    new_id = len(events) + 1  # id avtomatik ravishda inkrementlanadi

    # Event ma'lumotlarini qo'shish
    events.append({
        "id": new_id,
        "event_name": event_name,
        "event_description": event_description,
        "event_link_end": event_link_end,
        "is_active": is_active # Default qiymat False
    })

    # Ma'lumotlarni JSON faylga yozish
    with open(EVENT_DATA_FILE, 'w') as file:
        json.dump(events, file, indent=4)
def is_event_exist(event_name: str) -> bool:
    if not os.path.exists(EVENT_DATA_FILE):
        return False

    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except json.JSONDecodeError:
        return False

    # event_name mavjudligini tekshirish (katta-kichik harflarni hisobga olmasdan)
    return any(event.get('event_name', '').lower() == event_name.lower() for event in events)
# JSON fayldan barcha event ma'lumotlarini olish
def get_all_events():
    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
        return events
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Agar fayl topilmasa yoki xato bo'ls
def pin_event(event_name: str) -> bool:
    if not os.path.exists(EVENT_DATA_FILE):
        return False

    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except json.JSONDecodeError:
        return False

    found = False
    for event in events:
        if event.get('event_name', '').lower() == event_name.lower():
            event['is_active'] = True
            found = True
        else:
            event['is_active'] = False

    if found:
        with open(EVENT_DATA_FILE, 'w') as file:
            json.dump(events, file, indent=4)

    return found
def search_active_event():
    if not os.path.exists(EVENT_DATA_FILE):
        return None

    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except json.JSONDecodeError:
        return None

    for event in events:
        if event.get('is_active') == True:
            return event

    return None
def is_event_active(event_name: str) -> bool:
    if not os.path.exists(EVENT_DATA_FILE):
        return False

    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except json.JSONDecodeError:
        return False

    for event in events:
        if event.get('event_name', '').lower() == event_name.lower():
            return event.get('is_active', False)
    
    return False
def delete_event(event_name: str) -> bool:
    if not os.path.exists(EVENT_DATA_FILE):
        return False

    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except json.JSONDecodeError:
        return False

    # Eski ro'yxatdan eventni olib tashlaymiz
    new_events = [event for event in events if event.get('event_name', '').lower() != event_name.lower()]

    if len(new_events) == len(events):
        # Hech nima o‘chmadi — demak topilmadi
        return False

    # Yangilangan ro'yxatni yozamiz
    with open(EVENT_DATA_FILE, 'w') as file:
        json.dump(new_events, file, indent=4)

    return True

# JSON faylga event participants ma'lumotlarini saqlash
def save_event_participant(event_name, user_id):
    try:
        # Avvalgi participants'ni o'qish
        with open(EVENT_PARTICIPANTS_FILE, 'r') as file:
            participants = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        participants = []

    # Yangi participant'ning id sini avtomatik inkrement qilish
    new_id = len(participants) + 1  # id avtomatik ravishda inkrementlanadi

    # Qo'shilgan vaqtni olish
    joined_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Event participant'ini qo'shish
    participants.append({
        "id": new_id,
        "event_name": event_name,
        "user_id": user_id,
        "joined_at": joined_at
    })

    # Ma'lumotlarni JSON faylga yozish
    with open(EVENT_PARTICIPANTS_FILE, 'w') as file:
        json.dump(participants, file, indent=4)


# JSON fayldan barcha event participants ma'lumotlarini olish
def get_all_event_participants():
    try:
        with open(EVENT_PARTICIPANTS_FILE, 'r') as file:
            participants = json.load(file)
        return participants
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    # Agar fayl topilmasa yoki xato bo'lsa, bo'sh ro'yxat qaytaradi
def get_event_id_by_event_name(event_name: str) -> int:
    if not os.path.exists(EVENT_DATA_FILE):
        return -1  # Fayl mavjud emas

    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except json.JSONDecodeError:
        return -1  # Faylda xatolik

    # Event nomi bo‘yicha qidiramiz
    for event in events:
        if event.get('event_name', '').lower() == event_name.lower():
            return event.get('id', -1)

    return -1  # Event topilmasa
def get_count_of_participants(event_name):
    participants = get_all_event_participants()
    count = sum(1 for participant in participants if participant['event_name'] == event_name)
    return count




EVENTS_FILE = 'events.json'
PARTICIPANTS_FILE = 'event_participants.json'
USERS_FILE = 'user_data.json'

def get_event_participants_data(event_name: str):
    if not all(os.path.exists(f) for f in [EVENTS_FILE, PARTICIPANTS_FILE, USERS_FILE]):
        return []

    # Fayllarni ochamiz
    try:
        with open(EVENTS_FILE, 'r') as f:
            events = json.load(f)
        with open(PARTICIPANTS_FILE, 'r') as f:
            participants = json.load(f)
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    except json.JSONDecodeError:
        return []

    # Eventni topamiz
    event = next((e for e in events if e.get("event_name", "").lower() == event_name.lower()), None)
    
    if not event:
        return []

    

    # Shu eventga tegishli qatnashchilarni filtrlaymiz
    event_participants = [p for p in participants if p["event_name"] == event_name]
    

    # Har bir qatnashchi uchun to‘liq user ma'lumotlarini qo‘shamiz
    result = []
    for p in event_participants:
        user = next((u for u in users if u["user_id"] == p["user_id"]), {})
        result.append({
            "event_name": event["event_name"],
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "username": user.get("username"),
            "phone_number": user.get("phone_number"),
            "joined_at": p["joined_at"],
        })

    return result

def get_last_participant_event_link(user_id: int) -> str:
    if not os.path.exists(EVENT_DATA_FILE) or not os.path.exists(EVENT_PARTICIPANTS_FILE):
        return None
    
    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
        
        with open(EVENT_PARTICIPANTS_FILE, 'r') as file:
            participants = json.load(file)
        
    except json.JSONDecodeError:
        return None

    # Foydalanuvchi bo'yicha barcha qatnashchilarni topamiz
    user_participants = [
        p for p in participants if p['user_id'] == user_id
    ]

    if not user_participants:
        return None  # Agar foydalanuvchi qatnashmagan bo'lsa

    # Eng oxirgi qatnashgan eventni topamiz (datetime bo'yicha)
    last_participant = max(user_participants, key=lambda p: p['joined_at'])

    # Eventni topamiz
    event = next((e for e in events if e['id'] == last_participant['event_id']), None)
    
    if event:
        return event.get('event_link_end')  # Eventning linkini qaytaramiz
    
    return None
import pandas as pd

def export_participants_to_excel(event_name: str, filename: str = None):
    data = get_event_participants_data(event_name)

    if not data:
        print(f"Event '{event_name}' uchun hech qanday qatnashchi topilmadi.")
        return None

    df = pd.DataFrame(data)
    df['joined_at'] = pd.to_datetime(df['joined_at']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Fayl nomini avtomatik hosil qilamiz
    if not filename:
        safe_event_name = event_name.replace(" ", "_").lower()
        filename = f"{safe_event_name}_participants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"{event_name} qatnashchilari '{filename}' fayliga eksport qilindi.")
    return filename 

def get_active_event_link() -> str:
    if not os.path.exists(EVENT_DATA_FILE):
        return None

    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except json.JSONDecodeError:
        return None

    # Aktiv eventni qidiramiz
    active_event = next((e for e in events if e.get('is_active') == True), None)

    if active_event:
        return active_event.get('event_link_end')  # Aktiv eventning linkini qaytaramiz

    return None

def get_event_link_by_event_name(event_name: str) -> str:
    if not os.path.exists(EVENT_DATA_FILE):
        return None

    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except json.JSONDecodeError:
        return None

    # Event nomi bo'yicha qidiramiz
    event = next((e for e in events if e.get('event_name', '').lower() == event_name.lower()), None)

    if event:
        return event.get('event_link_end')  # Eventning linkini qaytaramiz

    return None
def get_last_participiant_event_name_by_user_id(user_id: int) -> str:
    if not os.path.exists(EVENT_PARTICIPANTS_FILE) or not os.path.exists(EVENT_DATA_FILE):
        return None

    try:
        with open(EVENT_PARTICIPANTS_FILE, 'r') as p_file:
            participants = json.load(p_file)
        with open(EVENT_DATA_FILE, 'r') as e_file:
            events = json.load(e_file)
    except json.JSONDecodeError:
        return None

    # Foydalanuvchining barcha qatnashgan eventlarini topamiz
    user_events = [
        p for p in participants if p['user_id'] == user_id
    ]

    if not user_events:
        return None  # Foydalanuvchi hech qayerda qatnashmagan

    # Eng oxirgi qatnashgan eventni aniqlaymiz
    last_participant = max(
        user_events,
        key=lambda p: datetime.fromisoformat(p['joined_at'])
    )

    # Eventni olaylik
    event = next((e for e in events if e['id'] == last_participant['event_id']), None)

    return event.get('event_name') if event else None
def get_event_name_by_event_link(event_link: str) -> str:
    if not os.path.exists(EVENT_DATA_FILE):
        return None

    try:
        with open(EVENT_DATA_FILE, 'r') as file:
            events = json.load(file)
    except json.JSONDecodeError:
        return None

    # event_link_end bo‘yicha qidiramiz
    event = next((e for e in events if e.get('event_link_end') == event_link), None)

    return event.get('event_name') if event else None