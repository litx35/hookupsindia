import logging
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

TOKEN = "8541678914:AAFV91wTj2hAvu-mQop8m8bIhznOii60g7I"

logging.basicConfig(level=logging.WARNING)

NAME, AGE, STATE, CITY, Q1, Q2, Q3, Q4, Q5, GENDER, IDEAL = range(11)

PAGE_SIZE = 5

PROFILES_DB = { ("Male","Younger"):[
{"name":"Ananya","age":22,"photo":"AgACAgUAAxkBAAEcddJpw9ak33qqwA_jKats6xwztCq2igACWQ9rGz0eIVbNWMCGIjnTkQEAAwIAA3MAAzoE"},
{"name":"Priya","age":23,"photo":"AgACAgUAAxkBAAEcdeVpw9eOh6IFL2KkzDpwwYHUJgMi0QACXg9rGz0eIVYoS2rPbNJRKQEAAwIAA3MAAzoE"},
{"name":"Riya","age":21,"photo":"AgACAgUAAxkBAAEcddtpw9bgmN4Z07-twq9HzaGgL3eFTAACWg9rGz0eIVahUpL5_IOj6gEAAwIAA3MAAzoE"},
{"name":"Sneha","age":24,"photo":"AgACAgUAAxkBAAEcdedpw9e8mCugZGpr_A5fngQRqg2ZqgACXw9rGz0eIVab-Q3Y1EAY5gEAAwIAA20AAzoE"},
{"name":"Megha","age":23,"photo":"AgACAgUAAxkBAAEcde1pw9gySP9GzkY31b5VXzK1O4EV5AACYQ9rGz0eIVavQj-hDJGWswEAAwIAA3MAAzoE"},
{"name":"Divya","age":22,"photo":"AgACAgUAAxkBAAEcdetpw9gIcWjdCTOoGAmGe4U0LewmSAACYA9rGz0eIVa9o5t8FGG6jQEAAwIAA3MAAzoE"},
{"name":"Aisha","age":25,"photo":"AgACAgUAAxkBAAEcdeFpw9dYnCYPAg8d90849zcqIw3bwAACXA9rGz0eIVaqa3PCOnzkpgEAAwIAA3MAAzoE"},
{"name":"Nisha","age":27,"photo":"AgACAgUAAxkBAAEcde9pw9hcTYZZenS1I2zcC76k_OhAtwACYg9rGz0eIVZYYGvAVrKe1gEAAwIAA3kAAzoE"},
{"name":"Shreya","age":26,"photo":"AgACAgUAAxkBAAEcdw1pw_SSYnrlOCxxun8rlbU0DXMgmQACrg9rGz0eIVbpkEdZnFF3DAEAAwIAA3kAAzoE"}
],

("Male","Older"):[
{"name":"Pooja","age":29,"photo":"AgACAgUAAxkBAAEcdgFpw9qLEPMh4E1XbWm0dopp253rzQACaA9rGz0eIVZWbIJgKNwkiQEAAwIAA3MAAzoE"},
{"name":"krupa","age":31,"photo":"AgACAgUAAxkBAAEceE5pxBaCcMna-BVMo_YfojI2ea9rqgAC6QxrG1cSIVbVFTFx8PS7xgEAAwIAA3MAAzoE"},
{"name":"geeta","age":33,"photo":"AgACAgUAAxkBAAEcdg9pw9tAZn90uDTDXi7jamh9RtRtDwACbQ9rGz0eIVbFcMa4YDHDzgEAAwIAA3MAAzoE"},
{"name":"meena","age":30,"photo":"AgACAgUAAxkBAAEcdg1pw9sVFuNuNpab0CuPgbw-RsvMtgACbA9rGz0eIVYx_zBYLaRKvgEAAwIAA3MAAzoE"},
{"name":"asha","age":32,"photo":"AgACAgUAAxkBAAEcdh1pw9vSssHmo6bzEgLiu55ATzbCtgACcQ9rGz0eIVb32JbmdTTjLgEAAwIAA3MAAzoE"},
{"name":"kavita","age":36,"photo":"AgACAgUAAxkBAAEceEZpxBY1DCyQTdsTwE7xG-BjkA_u5QAC1w9rGz0eIVbFnCIi1kvicQEAAwIAA3MAAzoE"},
{"name":"sangeeta","age":34,"photo":"AgACAgUAAxkBAAEceERpxBYfK0K7bVEvvp0plof61jUVlwAC1g9rGz0eIVYrLYQndhkP1gEAAwIAA20AAzoE"},
{"name":"sudha","age":40,"photo":"AgACAgUAAxkBAAEcdiFpw9wNbIH9Dfrn5Vh8JS8s_TbXowACcg9rGz0eIVbFn2QZc-WVqAEAAwIAA3MAAzoE"},
{"name":"kalyani","age":37,"photo":"AgACAgUAAxkBAAEcdhtpw9ugP907vtGiOyhYjU5kWYEJHwACcA9rGz0eIVbt1WyUrnqqqgEAAwIAA3MAAzoE"},
{"name":"Kavya","age":38,"photo":"AgACAgUAAxkBAAEcdiVpw9xRS4jiu325WgcMqKDiW6c3bgACcw9rGz0eIVad168bR0L6MQEAAwIAA3MAAzoE"}
],

("Male","Does not matter"):[
{"name":"Ananya","age":22,"photo":"AgACAgUAAxkBAAEcddJpw9ak33qqwA_jKats6xwztCq2igACWQ9rGz0eIVbNWMCGIjnTkQEAAwIAA3MAAzoE"},
{"name":"Priya","age":23,"photo":"AgACAgUAAxkBAAEcdeVpw9eOh6IFL2KkzDpwwYHUJgMi0QACXg9rGz0eIVYoS2rPbNJRKQEAAwIAA3MAAzoE"},
{"name":"Riya","age":21,"photo":"AgACAgUAAxkBAAEcddtpw9bgmN4Z07-twq9HzaGgL3eFTAACWg9rGz0eIVahUpL5_IOj6gEAAwIAA3MAAzoE"},
{"name":"Sneha","age":24,"photo":"AgACAgUAAxkBAAEcdedpw9e8mCugZGpr_A5fngQRqg2ZqgACXw9rGz0eIVab-Q3Y1EAY5gEAAwIAA20AAzoE"},
{"name":"Megha","age":23,"photo":"AgACAgUAAxkBAAEcde1pw9gySP9GzkY31b5VXzK1O4EV5AACYQ9rGz0eIVavQj-hDJGWswEAAwIAA3MAAzoE"},
{"name":"Divya","age":22,"photo":"AgACAgUAAxkBAAEcdetpw9gIcWjdCTOoGAmGe4U0LewmSAACYA9rGz0eIVa9o5t8FGG6jQEAAwIAA3MAAzoE"},
{"name":"Aisha","age":25,"photo":"AgACAgUAAxkBAAEcdeFpw9dYnCYPAg8d90849zcqIw3bwAACXA9rGz0eIVaqa3PCOnzkpgEAAwIAA3MAAzoE"},
{"name":"Nisha","age":27,"photo":"AgACAgUAAxkBAAEcde9pw9hcTYZZenS1I2zcC76k_OhAtwACYg9rGz0eIVZYYGvAVrKe1gEAAwIAA3kAAzoE"},
{"name":"Shreya","age":26,"photo":"AgACAgUAAxkBAAEcdw1pw_SSYnrlOCxxun8rlbU0DXMgmQACrg9rGz0eIVbpkEdZnFF3DAEAAwIAA3kAAzoE"},
{"name":"Pooja","age":29,"photo":"AgACAgUAAxkBAAEcdgFpw9qLEPMh4E1XbWm0dopp253rzQACaA9rGz0eIVZWbIJgKNwkiQEAAwIAA3MAAzoE"},
{"name":"krupa","age":31,"photo":"AgACAgUAAxkBAAEceE5pxBaCcMna-BVMo_YfojI2ea9rqgAC6QxrG1cSIVbVFTFx8PS7xgEAAwIAA3MAAzoE"},
{"name":"geeta","age":33,"photo":"AgACAgUAAxkBAAEcdg9pw9tAZn90uDTDXi7jamh9RtRtDwACbQ9rGz0eIVbFcMa4YDHDzgEAAwIAA3MAAzoE"},
{"name":"meena","age":30,"photo":"AgACAgUAAxkBAAEcdg1pw9sVFuNuNpab0CuPgbw-RsvMtgACbA9rGz0eIVYx_zBYLaRKvgEAAwIAA3MAAzoE"},
{"name":"asha","age":32,"photo":"AgACAgUAAxkBAAEcdh1pw9vSssHmo6bzEgLiu55ATzbCtgACcQ9rGz0eIVb32JbmdTTjLgEAAwIAA3MAAzoE"},
{"name":"kavita","age":36,"photo":"AgACAgUAAxkBAAEceEZpxBY1DCyQTdsTwE7xG-BjkA_u5QAC1w9rGz0eIVbFnCIi1kvicQEAAwIAA3MAAzoE"},
{"name":"sangeeta","age":34,"photo":"AgACAgUAAxkBAAEceERpxBYfK0K7bVEvvp0plof61jUVlwAC1g9rGz0eIVYrLYQndhkP1gEAAwIAA20AAzoE"},
{"name":"sudha","age":40,"photo":"AgACAgUAAxkBAAEcdiFpw9wNbIH9Dfrn5Vh8JS8s_TbXowACcg9rGz0eIVbFn2QZc-WVqAEAAwIAA3MAAzoE"},
{"name":"kalyani","age":37,"photo":"AgACAgUAAxkBAAEcdhtpw9ugP907vtGiOyhYjU5kWYEJHwACcA9rGz0eIVbt1WyUrnqqqgEAAwIAA3MAAzoE"},
{"name":"Kavya","age":38,"photo":"AgACAgUAAxkBAAEcdiVpw9xRS4jiu325WgcMqKDiW6c3bgACcw9rGz0eIVad168bR0L6MQEAAwIAA3MAAzoE"}
],
("Female","Younger"):[
{"name":"Rahul","age":21,"photo":"AgACAgUAAxkBAAEcdj9pw9_WM7vpBC-0R7wz5iveheT-ZQACdQ9rGz0eIVbOahOSgZQnrwEAAwIAA3gAAzoE"},
{"name":"Arjun","age":23,"photo":"AgACAgUAAxkBAAEcdjtpw9-aG5-FbzQzuKHrfGQY-p6uYQACdA9rGz0eIVaVClDL40QVTQEAAwIAA3MAAzoE"},
{"name":"Vikram","age":27,"photo":"AgACAgUAAxkBAAEcdklpw-BgkU1ij2aigVyJ6-iHTG4RIQACeg9rGz0eIVYd3iGKB3GTmgEAAwIAA20AAzoE"},
{"name":"Amit","age":28,"photo":"AgACAgUAAxkBAAEcdkdpw-Azsrd3ERY0OOzxVWrz8rFc6AACeQ9rGz0eIVY2l3yuyumwEwEAAwIAA3MAAzoE"},
{"name":"Karan","age":25,"photo":"AgACAgUAAxkBAAEcdkVpw-AFncZibwqCwraXwt0Ru0JTYgACdg9rGz0eIVYAAUAN97fRy0ABAAMCAAN5AAM6BA"}
],

("Female","Older"):[
{"name":"Sukesh","age":30,"photo":"AgACAgUAAxkBAAEcdkxpw-DK9Qw8GdfozLjiThOQAAFJN44AAnsPaxs9HiFWxWLKSGqzUBkBAAMCAANzAAM6BA"},
{"name":"Sunil","age":34,"photo":"AgACAgUAAxkBAAEcdlhpw-Eo3VknYfYelHma9S-HH3twPwACfA9rGz0eIVaP5J0pskWUtQEAAwIAA3gAAzoE"},
{"name":"Joseph","age":42,"photo":"AgACAgUAAxkBAAEcdmBpw-HQIHiqnWjrZxGjt5IbCHKQhQACfw9rGz0eIVZJCWhVAsMz3gEAAwIAA3MAAzoE"},
{"name":"Anil","age":38,"photo":"AgACAgUAAxkBAAEcdmRpw-KAGjI44q7Bz85AEm-UQIRdnQACgQ9rGz0eIVaAzMdHUOGM4wEAAwIAA3MAAzoE"},
{"name":"Vijay","age":48,"photo":"AgACAgUAAxkBAAEcdmhpw-KujLbg7sWHOcBLTkmrpJrKEgACgg9rGz0eIVaUAAFTvE0WN78BAAMCAAN5AAM6BA"}
],

("Female","Does not matter"):[
{"name":"Rahul","age":21,"photo":"AgACAgUAAxkBAAEcdj9pw9_WM7vpBC-0R7wz5iveheT-ZQACdQ9rGz0eIVbOahOSgZQnrwEAAwIAA3gAAzoE"},
{"name":"Arjun","age":23,"photo":"AgACAgUAAxkBAAEcdjtpw9-aG5-FbzQzuKHrfGQY-p6uYQACdA9rGz0eIVaVClDL40QVTQEAAwIAA3MAAzoE"},
{"name":"Vikram","age":27,"photo":"AgACAgUAAxkBAAEcdklpw-BgkU1ij2aigVyJ6-iHTG4RIQACeg9rGz0eIVYd3iGKB3GTmgEAAwIAA20AAzoE"},
{"name":"Amit","age":28,"photo":"AgACAgUAAxkBAAEcdkdpw-Azsrd3ERY0OOzxVWrz8rFc6AACeQ9rGz0eIVY2l3yuyumwEwEAAwIAA3MAAzoE"},
{"name":"Karan","age":25,"photo":"AgACAgUAAxkBAAEcdkVpw-AFncZibwqCwraXwt0Ru0JTYgACdg9rGz0eIVYAAUAN97fRy0ABAAMCAAN5AAM6BA"},
{"name":"Sukesh","age":30,"photo":"AgACAgUAAxkBAAEcdkxpw-DK9Qw8GdfozLjiThOQAAFJN44AAnsPaxs9HiFWxWLKSGqzUBkBAAMCAANzAAM6BA"},
{"name":"Sunil","age":34,"photo":"AgACAgUAAxkBAAEcdlhpw-Eo3VknYfYelHma9S-HH3twPwACfA9rGz0eIVaP5J0pskWUtQEAAwIAA3gAAzoE"},
{"name":"Joseph","age":42,"photo":"AgACAgUAAxkBAAEcdmBpw-HQIHiqnWjrZxGjt5IbCHKQhQACfw9rGz0eIVZJCWhVAsMz3gEAAwIAA3MAAzoE"},
{"name":"Anil","age":38,"photo":"AgACAgUAAxkBAAEcdmRpw-KAGjI44q7Bz85AEm-UQIRdnQACgQ9rGz0eIVaAzMdHUOGM4wEAAwIAA3MAAzoE"},
{"name":"Vijay","age":48,"photo":"AgACAgUAAxkBAAEcdmhpw-KujLbg7sWHOcBLTkmrpJrKEgACgg9rGz0eIVaUAAFTvE0WN78BAAMCAAN5AAM6BA"}
],
}



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter your name:")
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Enter your age:")
    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("Enter your state:")
    return STATE


async def state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = update.message.text
    await update.message.reply_text("Enter your city:")
    return CITY


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text

    keyboard=[["Yes","No"]]

    await update.message.reply_text(
        "Are you interested in having s*x  with strangers?",
        reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    )

    return Q1


async def q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q1"]=update.message.text
    keyboard=[["Yes","No"]]
    await update.message.reply_text(
        "Are you interested in having s*x with multiple partners?",
        reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    )
    return Q2


async def q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q2"]=update.message.text
    keyboard=[["Yes","No"]]
    await update.message.reply_text(
        "Are you interested in recording while having s*x?",
        reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    )
    return Q3


async def q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q3"]=update.message.text
    keyboard=[["Yes","No"]]
    await update.message.reply_text(
        "Are you interested in having s*x in public places?",
        reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    )
    return Q4


async def q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q4"]=update.message.text
    keyboard=[["Yes","No"]]
    await update.message.reply_text(
        "Are you interested in sharing photos and video calls?",
        reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    )
    return Q5


async def q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q5"]=update.message.text

    keyboard=[["Male","Female"]]

    await update.message.reply_text(
        "Select gender",
        reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["gender"]=update.message.text

    keyboard=[["Younger","Older","Does not matter"]]

    await update.message.reply_text(
        "Ideal type?",
        reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    )

    return IDEAL


async def ideal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["ideal_type"]=update.message.text
    context.user_data["profile_index"]=0

    await show_profiles(update,context)

    return ConversationHandler.END


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

    profiles=PROFILES_DB.get(key)

    if not profiles:
        profiles=PROFILES_DB[("Male","Younger")]

    index=context.user_data.get("profile_index",0)

    page=profiles[index:index+PAGE_SIZE]

    for p in page:

        caption=f"{p['name']}, {p['age']}\n{city}, {state}"

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
        buttons.append([InlineKeyboardButton("Load More",callback_data="load")])

    await message.reply_text(
        "Options:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    await query.answer()

    if query.data=="load":
        await show_profiles(update,context)

    if query.data=="pay":

        await query.message.reply_text(
            "This bot ensures privacy and safety of all users.\n\n"
            "Become a member of the premium group to directly chat with your interested matches."
        )

        await query.message.reply_text(
            "Complete payment to unlock chat:\n\nhttps://razorpay.me/@hookupindia?amount=hs5%2BhsUaIlsmW%2BfZKlAvnw%3D%3D"
        )


def main():

    app=Application.builder().token(TOKEN).build()

    conv=ConversationHandler(

        entry_points=[CommandHandler("start",start)],

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

    print("Bot running...")

    app.run_polling()


if __name__=="__main__":
    main()
