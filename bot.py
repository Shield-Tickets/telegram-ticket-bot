import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

tickets = {}
ticket_counter = 1

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /ticket <your message> to open a new support ticket.")

def new_ticket(update: Update, context: CallbackContext):
    global ticket_counter
    user = update.message.from_user
    text = " ".join(context.args)
    if not text:
        update.message.reply_text("Please describe your issue after /ticket command.")
        return
    ticket_id = ticket_counter
    ticket_counter += 1
    tickets[ticket_id] = {"user": user.id, "text": text, "status": "open"}
    context.bot.send_message(chat_id=GROUP_ID, text=f"New ticket #{ticket_id} from {user.first_name}:\n{text}")
    update.message.reply_text(f"Ticket #{ticket_id} created! Our admins will reply soon.")

def close_ticket(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /close <ticket_id>")
        return
    try:
        tid = int(context.args[0])
        if tid in tickets and tickets[tid]["status"] == "open":
            tickets[tid]["status"] = "closed"
            context.bot.send_message(chat_id=tickets[tid]["user"], text=f"Your ticket #{tid} has been closed.")
            update.message.reply_text(f"Ticket #{tid} closed.")
        else:
            update.message.reply_text("Ticket not found or already closed.")
    except:
        update.message.reply_text("Invalid ticket ID.")

dispatcher.add_handler(CommandHandler("start"_
