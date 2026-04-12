import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    PreCheckoutQueryHandler,
    filters
)

TOKEN = "8541678914:AAFux-COt-fm2IZPRHO-MQu_TgSDDh9M5l8"

logging.basicConfig(level=logging.INFO)

NAME, AGE, STATE, CITY, Q1, Q2, Q3, Q4, Q5, GENDER, IDEAL = range(11)

PAGE_SIZE = 5

# ------------------ YOUR PROFILE PHOTOS ------------------
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

# ------------------ START ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter your name:")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Enter your age:")
    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter your state:")
    return STATE

async def state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = update.message.text
    await update.message.reply_text("Enter your city:")
    return CITY

async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text

    keyboard=[["Yes","No"]]
    await update.message.reply_text("Are you interested in having s*x with strangers?", reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return Q1

async def q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[["Yes","No"]]
    await update.message.reply_text("Are you interested in having s*x with multiple partners?", reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return Q2

async def q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[["Yes","No"]]
    await update.message.reply_text("Are you interested in nude video calls?", reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return Q3

async def q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[["Yes","No"]]
    await update.message.reply_text("Are you interested in having s*x outdoors?", reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return Q4

async def q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[["Yes","No"]]
    await update.message.reply_text("Are you interested in sharing nude photos?", reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return Q5

async def q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[["Male","Female"]]
    await update.message.reply_text("Select gender preference", reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gender"] = update.message.text

    keyboard=[["Younger","Older","Does not matter"]]
    await update.message.reply_text("Ideal type?", reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return IDEAL

# ------------------ PROFILE DISPLAY ------------------

async def ideal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ideal_type"] = update.message.text
    context.user_data["index"] = 0
    await send_profiles(update, context)
    return ConversationHandler.END


async def send_profiles(update, context):

    chat_id = update.effective_chat.id

    gender = context.user_data.get("gender")
    ideal = context.user_data.get("ideal_type")

    user_city = context.user_data.get("city")
    user_state = context.user_data.get("state")

    profiles = PROFILES_DB.get((gender, ideal), [])
    index = context.user_data.get("index", 0)

    page = profiles[index:index + PAGE_SIZE]

    if not page:
        await context.bot.send_message(chat_id=chat_id, text="No more profiles")
        return

    for p in page:

        caption = f"{p['name']}, {p['age']}\n📍 {user_city}, {user_state}"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"💬 Chat with {p['name']}", callback_data=f"chat_{p['name']}")]
        ])

        await context.bot.send_photo(
            chat_id=chat_id,
            photo=p["photo"],
            caption=caption,
            reply_markup=keyboard
        )

    context.user_data["index"] = index + PAGE_SIZE

    load_more = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Load More", callback_data="load_more")]
    ])

    await context.bot.send_message(chat_id=chat_id, text="👇 Load more profiles", reply_markup=load_more)

# ------------------ BUTTON HANDLER ------------------

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "load_more":
        await send_profiles(update, context)

    elif data.startswith("chat_"):

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 Unlock Premium (500 ⭐)", callback_data="pay")]
        ])

        await query.message.reply_text(
            "🔒 Premium Access Required\n\n"
            "This fee helps us ensure that all members of the community are genuine and that everyone’s identity and privacy remain protected.\n\n"
            "It also helps maintain a safe and trusted environment for meaningful connections.\n\n"
            "💎 Unlock premium access to continue and chat with your matches.",
            reply_markup=keyboard
        )

    elif data == "pay":

        prices = [LabeledPrice("Premium Access", 500)]

        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title="Premium Community Access",
            description="Unlock chat and premium features",
            payload="premium_access",
            provider_token="",
            currency="XTR",
            prices=prices
        )

# ------------------ PAYMENT ------------------

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Thank you for joining the premium community!\n\n"
        "Your profile upgrade is currently in process.\n\n"
        "⏳ Please wait while we verify and activate your access. "
        "You will be able to chat with your matches shortly."
    )

# ------------------ MAIN ------------------

def main():

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
        NAME:[MessageHandler(filters.TEXT,name)],
        AGE:[MessageHandler(filters.TEXT,age)],
        STATE:[MessageHandler(filters.TEXT,state)],
        CITY:[MessageHandler(filters.TEXT,city)],
        Q1:[MessageHandler(filters.TEXT,q1)],
        Q2:[MessageHandler(filters.TEXT,q2)],
        Q3:[MessageHandler(filters.TEXT,q3)],
        Q4:[MessageHandler(filters.TEXT,q4)],
        Q5:[MessageHandler(filters.TEXT,q5)],
        GENDER:[MessageHandler(filters.TEXT,gender)],
        IDEAL:[MessageHandler(filters.TEXT,ideal)]
        },
        fallbacks=[]
    )

    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
