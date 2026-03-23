from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes, CallbackQueryHandler

NAME, AGE, STATE, CITY, Q1, Q2, Q3, Q4, Q5, GENDER, IDEAL_TYPE = range(11)

YES_NO_KEYBOARD = ReplyKeyboardMarkup([["Yes", "No"]], resize_keyboard=True)
GENDER_KEYBOARD = ReplyKeyboardMarkup([["Male", "Female"]], resize_keyboard=True)
IDEAL_TYPE_KEYBOARD = ReplyKeyboardMarkup([["Younger", "Older", "Does not matter"]], resize_keyboard=True)

PAGE_SIZE = 5

# ================= DATABASE =================
PROFILES_DB = {

("Male","Younger"): [
{"name":"Aarti","age":23,"match":"99%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"},
{"name":"Priya","age":24,"match":"98%","photo":"AgACAgUAAxkBAAEcWLVpv2yItnoDClxvFugJyEh6xIWC4QACCA5rG1Mg8FUOOA7pf5d9OwEAAwIAA3gAAzoE"},
{"name":"Sneha","age":22,"match":"97%","photo":"AgACAgUAAxkBAAEcWLNpv2yB2jysTimWvX5qU1FRF8ojwgACBw5rG1Mg8FWdp9FjObBNXwEAAwIAA3gAAzoE"},
{"name":"Riya","age":25,"match":"96%","photo":"AgACAgUAAxkBAAEcWLFpv2x5O2nP49lbYBLe5cW7TMtjDAACBg5rG1Mg8FWwJBGq61wcyQEAAwIAA20AAzoE"},
{"name":"Ananya","age":24,"match":"94%","photo":"AgACAgUAAxkBAAEcWK9pv2xzsm141F062UTzRoFaX1z7dAACBQ5rG1Mg8FXNS_Fb0tOkTQEAAwIAA20AAzoE"},
{"name":"Kavya","age":23,"match":"93%","photo":"AgACAgUAAxkBAAEcWKVpv2xWR_AmaQuF3imPvapfLvZ1FQACAQ5rG1Mg8FWQkXJ9kdQh3gEAAwIAA3MAAzoE"},
{"name":"Simran","age":22,"match":"92%","photo":"AgACAgUAAxkBAAEcWKNpv2xLE3r4uvK9k5e8ZD-qEEy0vQADDmsbUyDwVTXF9MOi_CzKAQADAgADbQADOgQ"},
{"name":"Pooja","age":25,"match":"91%","photo":"AgACAgUAAxkBAAEcWKlpv2xdLTYp22XNmoOsrxrNHjCvigACAg5rG1Mg8FWZsreyO77wigEAAwIAA20AAzoE"},
{"name":"Diya","age":23,"match":"90%","photo":"AgACAgUAAxkBAAEcWKtpv2xnVZIVF2JIHdeDFpdnwsEPXwACAw5rG1Mg8FXDPnsiBEpakAEAAwIAA3kAAzoE"}
],

("Male","Older"): [
{"name":"Meera","age":34,"match":"98%","photo":"AgACAgUAAxkBAAEcVwhpvyY76TbRlbDyLRwDcCHtHDzMjwAC7g1rGxXY-FWyu2h7YqeTLAEAAwIAA3kAAzoE"},
{"name":"Anjali","age":36,"match":"97%","photo":"AgACAgUAAxkBAAEcWM5pv3WK-B7Mv4R_HIjPGoRkdF1XWgAC9g1rG1Mg8FWYIVrfYd731QEAAwIAA3kAAzoE"}
],

("Male","Does not matter"): [],

("Female","Younger"): [
{"name":"Rahul","age":26,"match":"97%","photo":"AgACAgUAAxkBAAEcWKtpv2xnVZIVF2JIHdeDFpdnwsEPXwACAw5rG1Mg8FXDPnsiBEpakAEAAwIAA3kAAzoE"},
{"name":"Arjun","age":27,"match":"96%","photo":"AgACAgUAAxkBAAEcWKlpv2xdLTYp22XNmoOsrxrNHjCvigACAg5rG1Mg8FWZsreyO77wigEAAwIAA20AAzoE"}
],

("Female","Older"): [
{"name":"Amit","age":34,"match":"98%","photo":"AgACAgUAAxkBAAEcWKNpv2xLE3r4uvK9k5e8ZD-qEEy0vQADDmsbUyDwVTXF9MOi_CzKAQADAgADbQADOgQ"}
],

("Female","Does not matter"): []
}

# ================= SHOW PROFILES =================
async def show_profiles(update, context):

    gender = context.user_data["gender"]
    ideal = context.user_data["ideal_type"]

    city = context.user_data["city"]
    state = context.user_data["state"]

    key = (gender, ideal)

    profiles = PROFILES_DB.get(key, [])

    index = context.user_data.get("profile_index",0)

    page = profiles[index:index+PAGE_SIZE]

    if not page:
        await update.message.reply_text("No more profiles found.")
        return ConversationHandler.END

    for p in page:

        caption = f"{p['name']}, {p['age']} yrs\n{city}, {state}\n{p['match']} Match"

        keyboard = InlineKeyboardMarkup([

        [InlineKeyboardButton(f"Chat with {p['name']}",callback_data=f"chat_{p['name']}")]

        ])

        await update.message.reply_photo(photo=p["photo"],caption=caption,reply_markup=keyboard)

    context.user_data["profile_index"] = index + PAGE_SIZE

    keyboard = []

    if context.user_data["profile_index"] < len(profiles):

        keyboard.append([InlineKeyboardButton("Load More Profiles",callback_data="load_more")])

    keyboard.append([InlineKeyboardButton("Unlock Chat / Premium",callback_data="pay")])

    await update.message.reply_text("Choose option:",reply_markup=InlineKeyboardMarkup(keyboard))


# ================= BUTTONS =================
async def button(update,context):

    query = update.callback_query
    await query.answer()

    if query.data == "load_more":

        await show_profiles(query,context)

    else:

        payment_message = (
        "To unlock chat with matches you must join premium.\n\n"
        "Pay securely below:\n\n"
        "https://razorpay.me/@hookupindia"
        )

        await query.message.reply_text(payment_message)

# ================= FLOW =================
async def start(update,context):

    context.user_data.clear()

    await update.message.reply_text(
    "This bot is only for 18+ users.\n\nWhat is your name?",
    reply_markup=ReplyKeyboardRemove()
    )

    return NAME

async def get_name(update,context):

    context.user_data["name"] = update.message.text
    await update.message.reply_text("Your age?")
    return AGE

async def get_age(update,context):

    if not update.message.text.isdigit():

        await update.message.reply_text("Enter numbers only")
        return AGE

    age=int(update.message.text)

    if age < 18:

        await update.message.reply_text("Only 18+ allowed")
        return AGE

    context.user_data["age"]=age

    await update.message.reply_text("Your state?")
    return STATE

async def get_state(update,context):

    context.user_data["state"]=update.message.text
    await update.message.reply_text("Your city?")
    return CITY

async def get_city(update,context):

    context.user_data["city"]=update.message.text

    await update.message.reply_text("Do you smoke or drink?",reply_markup=YES_NO_KEYBOARD)

    return Q1

async def q1(update,context):

    context.user_data["q1"]=update.message.text
    await update.message.reply_text("Casual dating?",reply_markup=YES_NO_KEYBOARD)
    return Q2

async def q2(update,context):

    context.user_data["q2"]=update.message.text
    await update.message.reply_text("Meet soon?",reply_markup=YES_NO_KEYBOARD)
    return Q3

async def q3(update,context):

    context.user_data["q3"]=update.message.text
    await update.message.reply_text("Serious relationship?",reply_markup=YES_NO_KEYBOARD)
    return Q4

async def q4(update,context):

    context.user_data["q4"]=update.message.text
    await update.message.reply_text("Share photos?",reply_markup=YES_NO_KEYBOARD)
    return Q5

async def q5(update,context):

    context.user_data["q5"]=update.message.text
    await update.message.reply_text("Your gender?",reply_markup=GENDER_KEYBOARD)
    return GENDER

async def get_gender(update,context):

    context.user_data["gender"]=update.message.text
    await update.message.reply_text("Looking for?",reply_markup=IDEAL_TYPE_KEYBOARD)
    return IDEAL_TYPE

async def get_ideal(update,context):

    context.user_data["ideal_type"]=update.message.text
    context.user_data["profile_index"]=0

    await show_profiles(update,context)

    return ConversationHandler.END

# ================= MAIN =================
def main():

    TOKEN = "8541678914:AAHWKZZ7vC5Ra8tJqn5jkMUyIeQy-GiBBXo"

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(

    entry_points=[CommandHandler("start",start)],

    states={

    NAME:[MessageHandler(filters.TEXT & ~filters.COMMAND,get_name)],

    AGE:[MessageHandler(filters.TEXT & ~filters.COMMAND,get_age)],

    STATE:[MessageHandler(filters.TEXT & ~filters.COMMAND,get_state)],

    CITY:[MessageHandler(filters.TEXT & ~filters.COMMAND,get_city)],

    Q1:[MessageHandler(filters.TEXT,q1)],

    Q2:[MessageHandler(filters.TEXT,q2)],

    Q3:[MessageHandler(filters.TEXT,q3)],

    Q4:[MessageHandler(filters.TEXT,q4)],

    Q5:[MessageHandler(filters.TEXT,q5)],

    GENDER:[MessageHandler(filters.TEXT,get_gender)],

    IDEAL_TYPE:[MessageHandler(filters.TEXT,get_ideal)]

    },

    fallbacks=[]

    )

    app.add_handler(conv)

    app.add_handler(CallbackQueryHandler(button))

    print("Bot Running...")

    app.run_polling()

if __name__ == "__main__":

    main()
