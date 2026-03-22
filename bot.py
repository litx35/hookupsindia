from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8541678914:AAHWKZZ7vC5Ra8tJqn5jkMUyIeQy-GiBBXo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()