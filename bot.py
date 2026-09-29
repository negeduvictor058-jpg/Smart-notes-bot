import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

notes = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to My Note Bot!\n\n"
        "Commands:\n"
        "/save your note - Save a note\n"
        "/notes - Show your saved notes\n"
        "/explain - Explain your notes simply\n"
        "/clear - Clear all your notes"
    )


async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    note = " ".join(context.args)

    if not note:
        await update.message.reply_text(
            "Please write your note after /save.\n\n"
            "Example:\n"
            "/save Buy a new notebook"
        )
        return

    if user_id not in notes:
        notes[user_id] = []

    notes[user_id].append(note)

    await update.message.reply_text("✅ Your note has been saved!")


async def show_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in notes or not notes[user_id]:
        await update.message.reply_text("📝 You don't have any saved notes yet.")
        return

    message = "📝 Your saved notes:\n\n"

    for number, note in enumerate(notes[user_id], start=1):
        message += f"{number}. {note}\n"

    await update.message.reply_text(message)


async def explain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in notes or not notes[user_id]:
        await update.message.reply_text("📝 You don't have any notes to explain.")
        return

    message = "💡 Here are your notes in a simple format:\n\n"

    for number, note in enumerate(notes[user_id], start=1):
        message += f"{number}. {note}\n"

    message += (
        "\nI can currently organize your notes, "
        "but AI explanations will be added in a later version."
    )

    await update.message.reply_text(message)


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    notes[user_id] = []

    await update.message.reply_text("🗑️ All your notes have been cleared!")


def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is not set.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("save", save))
    app.add_handler(CommandHandler("notes", show_notes))
    app.add_handler(CommandHandler("explain", explain))
    app.add_handler(CommandHandler("clear", clear))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
