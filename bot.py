import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
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

TOKEN = "8541678914:AAHWKZZ7vC5Ra8tJqn5jkMUyIeQy-GiBBXo"

logging.basicConfig(level=logging.INFO)

NAME, AGE, STATE, CITY, Q1, Q2, Q3, Q4, Q5, GENDER, IDEAL = range(11)

PAGE_SIZE = 5


# -------- PROFILE DATABASE --------

PROFILES_DB = {

("Male","Younger"):[
{"name":"Ananya","age":22,"match":"98%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"},
{"name":"Priya","age":23,"match":"96%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"},
{"name":"Riya","age":21,"match":"95%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"},
{"name":"Sneha","age":22,"match":"94%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"},
{"name":"Megha","age":24,"match":"93%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"},
{"name":"Divya","age":23,"match":"92%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"}
],

("Male","Older"):[
{"name":"Pooja","age":30,"match":"97%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"}
],

("Male","Does not matter"):[
{"name":"Kavya","age":26,"match":"96%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"}
],

("Female","Younger"):[
{"name":"Rahul","age":24,"match":"95%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"}
],

("Female","Older"):[
{"name":"Amit","age":32,"match":"96%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"}
],

("Female","Does not matter"):[
{"name":"Arjun","age":27,"match":"94%","photo":"AgACAgUAAxkBAAEcWLdpv2yYOH5FyimZ6PAWSC7Kle_iUwACCQ5rG1Mg8FWBWZcjctF7VQEAAwIAA3kAAzoE"}
]

}


# -------- START --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! What is your name?")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Your age?")
    return AGE


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("Your state?")
    return STATE


async def get_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = update.message.text
    await update.message.reply_text("Your city?")
    return CITY


async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text("Do you like travelling? (Yes/No)")
    return Q1


async def yesno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Next question (Yes/No)")
    return Q2


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[["Male","Female"]]

    await update.message.reply_text(
        "Select gender",
        reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    )

    return GENDER


async def get_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["gender"]=update.message.text

    keyboard=[["Younger","Older","Does not matter"]]

    await update.message.reply_text(
        "Ideal partner?",
        reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    )

    return IDEAL


async def get_ideal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["ideal_type"]=update.message.text
    context.user_data["profile_index"]=0

    await show_profiles(update,context)

    return ConversationHandler.END


# -------- SHOW PROFILES --------

async def show_profiles(update,context):

    if update.callback_query:
        message=update.callback_query.message
    else:
        message=update.message

    gender=context.user_data["gender"]
    ideal=context.user_data["ideal_type"]

    city=context.user_data["city"]
    state=context.user_data["state"]

    key=(gender,ideal)

    profiles=PROFILES_DB.get(key,[])

    index=context.user_data.get("profile_index",0)

    page=profiles[index:index+PAGE_SIZE]

    if not page:
        await message.reply_text("No profiles found")
        return

    for p in page:

        caption=f"{p['name']}, {p['age']}\n{city}, {state}\n{p['match']} match"

        keyboard=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"Talk with {p['name']}",callback_data="pay")]
        ])

        await message.reply_photo(
            photo=p["photo"],
            caption=caption,
            reply_markup=keyboard
        )

    context.user_data["profile_index"]=index+PAGE_SIZE

    buttons=[]

    if context.user_data["profile_index"]<len(profiles):
        buttons.append([InlineKeyboardButton("Load More Profiles",callback_data="load_more")])

    buttons.append([InlineKeyboardButton("Unlock Chat",callback_data="pay")])

    await message.reply_text(
        "Options:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# -------- BUTTON HANDLER --------

async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    await query.answer()

    if query.data=="load_more":
        await show_profiles(update,context)

    if query.data=="pay":

        await query.message.reply_text(
            "To talk with matches complete payment:\n\nhttps://razorpay.me/yourlink"
        )


# -------- MAIN --------

def main():

    app=Application.builder().token(TOKEN).build()

    conv=ConversationHandler(

        entry_points=[CommandHandler("start",start)],

        states={

        NAME:[MessageHandler(filters.TEXT,get_name)],
        AGE:[MessageHandler(filters.TEXT,get_age)],
        STATE:[MessageHandler(filters.TEXT,get_state)],
        CITY:[MessageHandler(filters.TEXT,get_city)],

        Q1:[MessageHandler(filters.TEXT,yesno)],
        Q2:[MessageHandler(filters.TEXT,yesno)],

        GENDER:[MessageHandler(filters.TEXT,get_gender)],
        IDEAL:[MessageHandler(filters.TEXT,get_ideal)]

        },

        fallbacks=[]
    )

    app.add_handler(conv)

    app.add_handler(CallbackQueryHandler(button))

    print("Bot running...")

    app.run_polling()


if __name__=="__main__":
    main()
