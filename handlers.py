# handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import config
import database as db

async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    user = db.get_user(user_id)
    
    if user is None:
        questions = db.get_questions()
        if questions:
            context.user_data['questions'] = questions
            context.user_data['profile'] = {}
            await update.message.reply_text(questions[0][1])
            context.user_data['question_index'] = 0
        else:
            await update.message.reply_text("No questions available. Please contact the admin.")
    else:
        await update.message.reply_text("You are already registered.")
    
async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user = db.get_user(user_id)
    
    if user is None and 'questions' in context.user_data:
        question_index = context.user_data['question_index']
        question_answer = update.message.text
        context.user_data['profile'][context.user_data['questions'][question_index][1]] = question_answer
        
        question_index += 1
        if question_index < len(context.user_data['questions']):
            context.user_data['question_index'] = question_index
            await update.message.reply_text(context.user_data['questions'][question_index][1])
        else:
            profile = str(context.user_data['profile'])
            db.add_user(user_id, update.message.from_user.username, profile)
            context.user_data.clear()
            await update.message.reply_text("Thank you for registering. Your profile will be reviewed by an admin.")
            await context.bot.send_message(config.ADMIN_ID, f"New user registered: @{username}\nProfile: {profile}")

def main():
    app = Application.builder().token(config.BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()

