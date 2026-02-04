# -*- coding: utf-8 -*-
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = ""

# --- MA'LUMOTLAR OMBORI ---
MAFIA_GAMES = {}
QUIZ_DATA = {
    "tarix": [
  # Oson
        {"q": "Amir Temur qayerda tug'ilgan?", "o": ["Xo'ja Ilg'or", "Samarqand", "Buxoro"], "a": "Xo'ja Ilg'or"},
        {"q": "O'zbekiston mustaqilligi qachon?", "o": ["1991", "1990", "1992"], "a": "1991"},
        {"q": "Sohibqiron unvoni kimniki?", "o": ["Amir Temur", "Bobur", "Ulug'bek"], "a": "Amir Temur"},
        {"q": "Bobur qayerda tug'ilgan?", "o": ["Andijon", "Farg'ona", "Namangan"], "a": "Andijon"},
        {"q": "Eng qadimgi yozma yodgorlik?", "o": ["Avesto", "Qutadg'u bilig", "DLT"], "a": "Avesto"},
        {"q": "Konstitutsiya kuni?", "o": ["8-dekabr", "1-sentyabr", "21-mart"], "a": "8-dekabr"},
        {"q": "Nil daryosi qayerda?", "o": ["Misr", "Sudan", "Efiopiya"], "a": "Misr"},
        {"q": "Urush qachon tugagan?", "o": ["1945", "1941", "1946"], "a": "1945"},
        {"q": "Temurning onasi?", "o": ["Takina xotin", "Nodira", "Uvaysiy"], "a": "Takina xotin"},
        {"q": "Alisher Navoiy asri?", "o": ["XV asr", "XIV asr", "XVI asr"], "a": "XV asr"},
        # O'rta va Qiyin (qisqartirilgan namunalar, kodingizda hammasi bo'ladi)
        {"q": "Jaloliddin Manguberdi sulolasi?", "o": ["Xorazmshohlar", "Somoniylar", "Qoraxoniylar"], "a": "Xorazmshohlar"},
        {"q": "Samarqand necha yillik?", "o": ["2750", "2500", "3000"], "a": "2750"},
        {"q": "BMT tashkil topgan yil?", "o": ["1945", "1944", "1946"], "a": "1945"},
        {"q": "Temur tuzuklari necha qism?", "o": ["2", "3", "1"], "a": "2"},
        {"q": "Napoleon qayerda vafot etgan?", "o": ["Muqaddas Yelena", "Elba", "Korsika"], "a": "Muqaddas Yelena"}
    ],
    "matem": [
        # Oson
        {"q": "25 * 4 = ?", "o": ["100", "80", "125"], "a": "100"},
        {"q": "81 ning ildizi?", "o": ["9", "7", "8"], "a": "9"},
        {"q": "Eng kichik tub son?", "o": ["2", "1", "3"], "a": "2"},
        {"q": "15 ning kvadrati?", "o": ["225", "215", "195"], "a": "225"},
        {"q": "7 * 8 = ?", "o": ["56", "54", "64"], "a": "56"},
        {"q": "1 km necha metr?", "o": ["1000", "100", "500"], "a": "1000"},
        {"q": "3 ning kubi?", "o": ["27", "9", "18"], "a": "27"},
        {"q": "180 gradus qaysi burchak?", "o": ["Yoyiq", "O'tmas", "To'g'ri"], "a": "Yoyiq"},
        {"q": "Doira yuzi?", "o": ["πr²", "2πr", "ab"], "a": "πr²"},
        {"q": "20 ning 10% i?", "o": ["2", "4", "1"], "a": "2"},
        # O'rta va Qiyin
        {"q": "X² - 9 = 0 bo'lsa X?", "o": ["±3", "3", "9"], "a": "±3"},
        {"q": "Log₂(8) = ?", "o": ["3", "4", "2"], "a": "3"},
        {"q": "Sin(90°) = ?", "o": ["1", "0", "-1"], "a": "1"},
        {"q": "5! (faktorial)?", "o": ["120", "100", "60"], "a": "120"},
        {"q": "Diskriminant formulasi?", "o": ["b²-4ac", "b²+4ac", "2ab"], "a": "b²-4ac"}
    ],
    "python": [
 # Oson
        {"q": "Python yaratuvchisi?", "o": ["Gvido van Rossum", "Bill Geyts", "Jobs"], "a": "Gvido van Rossum"},
        {"q": "Turini aniqlash?", "o": ["type()", "id()", "len()"], "a": "type()"},
        {"q": "Ro'yxat qavsi?", "o": ["[]", "()", "{}"], "a": "[]"},
        {"q": "Fayl kengaytmasi?", "o": [".py", ".txt", ".exe"], "a": ".py"},
        {"q": "Chiqarish operatori?", "o": ["print", "echo", "out"], "a": "print"},
        {"q": "Komentariya belgisi?", "o": ["#", "//", "/*"], "a": "#"},
        {"q": "Kirish operatori?", "o": ["input()", "get()", "read()"], "a": "input()"},
        {"q": "Mantiqiy tur?", "o": ["bool", "int", "str"], "a": "bool"},
        {"q": "Math modulini chaqirish?", "o": ["import math", "include math", "use math"], "a": "import math"},
        {"q": "Oxiridan qo'shish?", "o": ["append()", "add()", "push()"], "a": "append()"},
        {"q": "O'zgarmas ro'yxat?", "o": ["tuple", "list", "set"], "a": "tuple"},
        {"q": "Funksiya kalit so'zi?", "o": ["def", "func", "start"], "a": "def"},
        {"q": "Lambda nima?", "o": ["Nomsiz funksiya", "Klass", "Modul"], "a": "Nomsiz funksiya"},
        {"q": "PIP nima?", "o": ["Paket menejeri", "Xato", "Sikl"], "a": "Paket menejeri"},
        {"q": "Generator so'zi?", "o": ["yield", "return", "give"], "a": "yield"}
    ]
}

# --- YORDAMCHI FUNKSIYALAR (XO va Minalar uchun) ---
def check_xo_winner(b):
    win_coords = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a, b_idx, c in win_coords:
        if b[a] == b[b_idx] == b[c] and b[a] != " ": return b[a]
    return "Durang" if " " not in b else None

def get_xo_kb(b):
    kb = [[InlineKeyboardButton(b[i*3+j], callback_data=f"xo_{i*3+j}") for j in range(3)] for i in range(3)]
    kb.append([InlineKeyboardButton("◀️ Chiqish", callback_data="mode_offline")])
    return InlineKeyboardMarkup(kb)

def get_mines_kb(ud, show_all=False):
    size = ud["m_size"]
    kb = []
    for r in range(size):
        row = []
        for c in range(size):
            idx = r * size + c
            if idx in ud["m_open"]: txt = "✅"
            elif show_all and idx in ud["m_bombs"]: txt = "💣"
            else: txt = "❓"
            row.append(InlineKeyboardButton(txt, callback_data=f"mplay_{idx}"))
        kb.append(row)
    kb.append([InlineKeyboardButton("◀️ Chiqish", callback_data="mode_offline")])
    return InlineKeyboardMarkup(kb)

async def send_quiz_q(q, ud):
    item = ud["q_list"][ud["q_cur"]]
    ud["q_ans"] = item["a"]
    options = item["o"].copy()
    random.shuffle(options)
    kb = [[InlineKeyboardButton(o, callback_data=f"qa_{o}")] for o in options]
    await q.edit_message_text(f"Savol {ud['q_cur']+1}/{ud['q_limit']}:\n\n{item['q']}", reply_markup=InlineKeyboardMarkup(kb))

# --- ASOSIY MENYULAR ---
def main_menu_kb(score=0):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🏆 Jami Ball: {score}", callback_data="score")],
        [InlineKeyboardButton("🌐 Online (Mafia)", callback_data="mode_online")],
        [InlineKeyboardButton("🤖 Offline O'yinlar", callback_data="mode_offline")]
    ])

def offline_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌⭕️ XO", callback_data="off_xo"), InlineKeyboardButton("🧠 Quiz", callback_data="off_quiz")],
        [InlineKeyboardButton("✂️ Tosh-Qog'oz", callback_data="off_rps"), InlineKeyboardButton("💣 Minalar", callback_data="off_mines")],
        [InlineKeyboardButton("◀️ Orqaga", callback_data="back_menu")]
    ])

# =====================================================================
# 🎭 ONLINE MAFIA QISMI
# =====================================================================


# --- MAFIA UCHUN YANGILANGAN START (ESKISINI O'RNIGA) ---
async def start_mafia_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Faqat guruhda ishlashi uchun cheklov
    if update.effective_chat.type == "private":
        await update.message.reply_text("🎭 Mafia o'yini faqat guruhlarda ishlaydi! Botni guruhga qo'shing.")
        return
    
    # O'yin xotirasini yangilash
    MAFIA_GAMES[chat_id] = {
        'players': [], 
        'state': 'reg',  # Ro'yxatga olish holati
        'roles': {},
        'alive': []
    }
    
    kb = [[InlineKeyboardButton("✅ Qo'shilish", callback_data="join_mafia")],
          [InlineKeyboardButton("🏁 O'yinni boshlash (Min. 4 kishi)", callback_data="start_mafia_game")]]
    
    await update.message.reply_text(
        "🎭 **Mafia o'yini boshlandi!**\n\n"
        "Bot moderatorlik qiladi. O'yinchilar pastdagi tugmani bosing.",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )

# =====================================================================
# ⚙️ CALLBACK HANDLER (Barcha o'yinlar mantiqi shu yerda)
# =====================================================================

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    ud = context.user_data
    data = q.data
    chat_id = q.message.chat_id
    if "total_score" not in ud: ud["total_score"] = 0
    await q.answer()

    # --- NAVIGATSIYA ---
    if data == "back_menu":
        await q.edit_message_text("Asosiy menyu:", reply_markup=main_menu_kb(ud["total_score"]))
    elif data == "mode_offline":
        await q.edit_message_text("ofline--\n\nO'yinni tanlang:\n\n--ofline", reply_markup=offline_menu_kb())
    elif data == "mode_online":
        kb = [[InlineKeyboardButton("➕ Guruhga qo'shish", url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true")],
              [InlineKeyboardButton("◀️ Orqaga", callback_data="back_menu")]]
        await q.edit_message_text("🎭 Mafia o'yini uchun botni guruhga qo'shing va /start_mafia yozing.", reply_markup=InlineKeyboardMarkup(kb))

    # --- QUIZ MANTIQI ---
    elif data == "off_quiz":
        kb = [[InlineKeyboardButton("📜 Tarix", callback_data="qc_tarix")], [InlineKeyboardButton("🔢 Matematika", callback_data="qc_matem")],
              [InlineKeyboardButton("🐍 Python", callback_data="qc_python")], [InlineKeyboardButton("◀️ Orqaga", callback_data="mode_offline")]]
        await q.edit_message_text("Mavzuni tanlang:", reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("qc_"):
        ud["q_cat"] = data.split("_")[1]
        kb = [[InlineKeyboardButton("5 ta", callback_data="qn_5"), InlineKeyboardButton("10 ta", callback_data="qn_10")]]
        await q.edit_message_text("Nechta savol?", reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("qn_"):
        limit = int(data.split("_")[1])
        ud["q_limit"], ud["q_cur"], ud["q_corr"] = limit, 0, 0
        all_q = QUIZ_DATA[ud["q_cat"]]
        ud["q_list"] = random.sample(all_q, min(len(all_q), limit))
        await send_quiz_q(q, ud)
    elif data.startswith("qa_"):
        if data.split("_")[1] == ud["q_ans"]:
            ud["q_corr"] += 1
            ud["total_score"] += 10
        ud["q_cur"] += 1
        if ud["q_cur"] < ud["q_limit"]: await send_quiz_q(q, ud)
        else: await q.edit_message_text(f"🏁 Quiz tugadi!\n✅ To'g'ri: {ud['q_corr']}\n🏆 Jami ball: {ud['total_score']}", reply_markup=offline_menu_kb())

    # --- MINALAR MANTIQI ---
    elif data == "off_mines":
        kb = [[InlineKeyboardButton("3x3", callback_data="msize_3"), InlineKeyboardButton("4x4", callback_data="msize_4"), InlineKeyboardButton("5x5", callback_data="msize_5")]]
        await q.edit_message_text("O'lchamni tanlang:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("msize_"):
        ud["m_size"] = int(data.split("_")[1])
        kb = [[InlineKeyboardButton("1 Bomba", callback_data="mcount_1")], [InlineKeyboardButton("2 Bomba", callback_data="mcount_2")], [InlineKeyboardButton("3 Bomba", callback_data="mcount_3")]]
        await q.edit_message_text("Bombalar soni:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("mcount_"):
        ud["m_count"] = int(data.split("_")[1])
        ud["m_bombs"] = random.sample(range(ud["m_size"]**2), ud["m_count"])
        ud["m_open"] = []
        await q.edit_message_text("Minalarni topmang!", reply_markup=get_mines_kb(ud))

    elif data.startswith("mplay_"):
        idx = int(data.split("_")[1])
        if idx in ud["m_bombs"]:
            await q.edit_message_text("💥 PORTLADINGIZ!", reply_markup=get_mines_kb(ud, True))
        else:
            if idx not in ud["m_open"]:
                ud["m_open"].append(idx)
                ud["total_score"] += 5
                if len(ud["m_open"]) == (ud["m_size"]**2 - ud["m_count"]):
                    await q.edit_message_text(f"🎉 G'ALABA! +20 ball", reply_markup=offline_menu_kb())
                    ud["total_score"] += 20
                else:
                    await q.edit_message_text(f"✅ Ball: {ud['total_score']}", reply_markup=get_mines_kb(ud))

            elif data == "mode_online":
             kb = [[InlineKeyboardButton("➕ Guruhga qo'shish", url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true")],
              [InlineKeyboardButton("◀️ Orqaga", callback_data="back_menu")]]
        await q.edit_message_text("🎭 Mafia faqat guruhlarda ishlaydi!", reply_markup=InlineKeyboardMarkup(kb))
        

    # --- TOSH-QOG'OZ-QAYCHI ---
# --- TOSH-QOG'OZ-QAYCHI (5 BALLGACHA) ---
# --- TOSH-QOG'OZ-QAYCHI (5 BALLGACHA + 20 BALL MUKOFOT) ---
    elif data == "off_rps":
        # Yangi o'yin boshlanganda joriy hisobni nollaymiz
        ud["rps_user_score"] = 0
        ud["rps_bot_score"] = 0
        kb = [[InlineKeyboardButton("🪨 Tosh", callback_data="rps_tosh")],
              [InlineKeyboardButton("📄 Qog'oz", callback_data="rps_qogoz")],
              [InlineKeyboardButton("✂️ Qaychi", callback_data="rps_qaychi")],
              [InlineKeyboardButton("◀️ Orqaga", callback_data="mode_offline")]]
        await q.edit_message_text("ofline--\n\n🎮 Tosh-Qog'oz-Qaychi: 5 ballgacha!\nKim birinchi 5 ball to'plasa, 20 ochko oladi.\n\nTanlang:\n--ofline", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("rps_"):
        u = data.split("_")[1]
        b = random.choice(["tosh", "qogoz", "qaychi"])
        em = {"tosh": "🪨", "qogoz": "📄", "qaychi": "✂️"}
        
        # Hisobni tekshirish (agar o'zgaruvchi yo'q bo'lsa yaratish)
        if "rps_user_score" not in ud: ud["rps_user_score"] = 0
        if "rps_bot_score" not in ud: ud["rps_bot_score"] = 0

        # Raund natijasini aniqlash
        if u == b:
            res_text = f"Durang! ⚖️\nIkkalamiz ham {em[b]} tanladik."
        elif (u=="tosh" and b=="qaychi") or (u=="qogoz" and b=="tosh") or (u=="qaychi" and b=="qogoz"):
            ud["rps_user_score"] += 1
            res_text = f"Siz yutdingiz! ✅\nSiz: {em[u]} | Bot: {em[b]}"
        else:
            ud["rps_bot_score"] += 1
            res_text = f"Bot yutdi! 🤖\nSiz: {em[u]} | Bot: {em[b]}"

        status = f"\n\n📊 JORIY HISOB: Siz {ud['rps_user_score']} : {ud['rps_bot_score']} Bot"

        # G'olibni tekshirish
        if ud["rps_user_score"] >= 5:
            ud["total_score"] += 20  # 20 ball berish
            final_msg = f"ofline--\n\n🎉 G'ALABA! 5:{ud['rps_bot_score']} hisobida yutdingiz!\n💰 Sizga 20 ball berildi.\n\n--ofline"
            await q.edit_message_text(final_msg, reply_markup=offline_menu_kb())
        elif ud["rps_bot_score"] >= 5:
            final_msg = f"ofline--\n\n😞 MAG'LUBIYAT! Bot 5:{ud['rps_user_score']} hisobida yutdi.\nBall berilmadi.\n\n--ofline"
            await q.edit_message_text(final_msg, reply_markup=offline_menu_kb())
        else:
            # O'yin davom etmoqda
            kb = [[InlineKeyboardButton("🪨 Tosh", callback_data="rps_tosh")],
                  [InlineKeyboardButton("📄 Qog'oz", callback_data="rps_qogoz")],
                  [InlineKeyboardButton("✂️ Qaychi", callback_data="rps_qaychi")],
                  [InlineKeyboardButton("◀️ Orqaga", callback_data="mode_offline")]]
            await q.edit_message_text(f"ofline--\n\n{res_text}{status}\n\nTanlang:\n--ofline", reply_markup=InlineKeyboardMarkup(kb))
    # --- XO MANTIQI ---
    elif data == "off_xo":
        kb = [[InlineKeyboardButton("🤖 Bot", callback_data="xm_bot")], [InlineKeyboardButton("👥 PvP", callback_data="xm_pvp")]]
        await q.edit_message_text("Rejim:", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("xm_"):
        ud["xo_m"], ud["xo_b"], ud["xo_t"] = data.split("_")[1], [" "] * 9, "❌"
        await q.edit_message_text("❌ Navbat:", reply_markup=get_xo_kb(ud["xo_b"]))

    elif data.startswith("xo_"):
        i = int(data.split("_")[1])
        if ud.get("xo_b") and ud["xo_b"][i] == " ":
            ud["xo_b"][i] = ud["xo_t"]
            res = check_xo_winner(ud["xo_b"])
            if not res:
                if ud["xo_m"] == "bot":
                    empty = [k for k,v in enumerate(ud["xo_b"]) if v == " "]
                    if empty: ud["xo_b"][random.choice(empty)] = "⭕️"
                    res = check_xo_winner(ud["xo_b"])
                else: ud["xo_t"] = "⭕️" if ud["xo_t"] == "❌" else "❌"
            if res: await q.edit_message_text(f"Natija: {res}", reply_markup=offline_menu_kb())
            else: await q.edit_message_text(f"Navbat: {ud['xo_t']}", reply_markup=get_xo_kb(ud["xo_b"]))

    # --- ONLINE MAFIA CALLBACKS ---
# --- ONLINE MAFIA (BOT BOSHQARADIGAN) ---
    elif data == "mode_online":
        kb = [[InlineKeyboardButton("➕ Guruhga qo'shish", url=f"https://t.me/{(await context.bot.get_me()).username}?startgroup=true")],
              [InlineKeyboardButton("◀️ Orqaga", callback_data="back_menu")]]
        await q.edit_message_text("🎭 Mafia: Bot o'zi rollarni beradi va o'yinni boshqaradi.\n\nBotni guruhga qo'shing va /start_mafia buyrug'ini bering.", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "join_mafia":
        user = q.from_user
        if chat_id not in MAFIA_GAMES: MAFIA_GAMES[chat_id] = {'players': [], 'state': 'reg'}
        
        player_ids = [p.id for p in MAFIA_GAMES[chat_id]['players']]
        if user.id not in player_ids:
            MAFIA_GAMES[chat_id]['players'].append(user)
            p_list = "\n".join([f"- {p.first_name}" for p in MAFIA_GAMES[chat_id]['players']])
            kb = [[InlineKeyboardButton("✅ Qo'shilish", callback_data="join_mafia")],
                  [InlineKeyboardButton("🏁 O'yinni boshlash", callback_data="start_mafia_game")]]
            await q.edit_message_text(f"🎭 Ro'yxatdagilar:\n{p_list}\n\nO'yinchilar soni: {len(MAFIA_GAMES[chat_id]['players'])}", reply_markup=InlineKeyboardMarkup(kb))
        else:
            await q.answer("Siz allaqachon qo'shilgansiz!")

    elif data == "start_mafia_game":
        game = MAFIA_GAMES.get(chat_id)
        if not game or len(game['players']) < 4:
            await q.answer("O'yin uchun kamida 4 kishi kerak!", show_alert=True)
            return

        players = game['players']
        random.shuffle(players)
        
        # Rollarni taqsimlash
        roles = ["Mafia 🔪", "Komissar 👮‍♂️", "Shifokor 💊"] + ["Fuqaro 👨‍💼"] * (len(players) - 3)
        game['roles'] = {}
        game['alive'] = []

        for i, p in enumerate(players):
            role = roles[i]
            game['roles'][p.id] = role
            game['alive'].append(p.id)
            try:
                await context.bot.send_message(p.id, f"Sizning rolingiz: {role}\nO'yin boshlanmoqda, guruhga qayting!")
            except:
                await q.message.reply_text(f"⚠️ {p.first_name} botga /start bosmagan, rolni bilmay qolishi mumkin!")

        await q.edit_message_text("🎭 Rollar tarqatildi! \n🌃 Shahar uyquga ketmoqda... Tun boshlandi.\n\n(Mafia, Komissar va Shifokor o'z tanlovlarini botning shaxsiy xabarida amalga oshiradilar)")
        # Bu yerda bot avtomatik tun mantiqini boshlaydi (qisqartirilgan mantiq)    

# --- START VA MAIN ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.setdefault("total_score", 0)
    await update.message.reply_text("🎮 Game Hub!", reply_markup=main_menu_kb(context.user_data["total_score"]))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("start_mafia", start_mafia_cmd))
    app.add_handler(CallbackQueryHandler(handle_callbacks))
    print("🤖 BOT ISHGA TUSHDI!")
    app.run_polling()

if __name__ == "__main__":
    main()
