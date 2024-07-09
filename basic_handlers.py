from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext
import database as db
import config

async def help_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    commands = db.get_all_commands() if db.get_admin(user_id) else db.get_user_accesses(user_id)
    command_list = "\n".join([f"/{command[0]}" for command in commands])
    await update.message.reply_text(f"Available commands:\n{command_list}")

async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    user = db.get_user(user_id)
    
    if not user:
        questions = db.get_questions()
        if questions:
            context.user_data.update({'questions': questions, 'profile': {}, 'question_index': 0})
            await update.message.reply_text(questions[0][1])
        else:
            db.add_user(user_id, username, "No profile information provided.")
            await notify_admin(context, user_id, username, "No profile information provided.")
            await update.message.reply_text("No questions available. Your profile has been sent to the admin.")
    else:
        await update.message.reply_text("You are already registered.")

async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if not db.get_user(user_id) and 'questions' in context.user_data:
        question_index = context.user_data['question_index']
        context.user_data['profile'][context.user_data['questions'][question_index][1]] = update.message.text
        if question_index + 1 < len(context.user_data['questions']):
            context.user_data['question_index'] += 1
            await update.message.reply_text(context.user_data['questions'][context.user_data['question_index']][1])
        else:
            profile = str(context.user_data['profile'])
            db.add_user(user_id, update.message.from_user.username, profile)
            context.user_data.clear()
            await notify_admin(context, user_id, update.message.from_user.username, profile)
            await update.message.reply_text("Thank you for registering. Your profile will be reviewed by an admin.")

async def notify_admin(context, user_id, username, profile):
    await context.bot.send_message(config.ADMIN_ID, f"New user registered: @{username}\nTelegram ID: {user_id}\nProfile: {profile}")
    photos = await context.bot.get_user_profile_photos(user_id, limit=1)
    if photos.total_count > 0:
        await context.bot.send_photo(config.ADMIN_ID, photos.photos[0][-1].file_id)

basic_handlers = [
    CommandHandler("start", start),
    CommandHandler("help", help_command),
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
]
