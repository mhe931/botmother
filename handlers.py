# handlers.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import config
import database as db

# States for the conversation
ACCESS_NAME, ACCESS_DESCRIPTION, COMMAND_NAME, COMMAND_DESCRIPTION = range(4)

# Function to show help commands
async def help_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    commands = db.get_user_accesses(user_id)
    command_list = "\n".join([f"/{command[0]}" for command in commands])
    await update.message.reply_text(f"Available commands:\n{command_list}")

# Function to handle /accesslist
async def accesslist(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        users = db.get_users()
        access_buttons = []
        
        for user in users:
            user_accesses = db.get_user_accesses(user[0])
            access_text = "\n".join([f"/{access[0]}" for access in user_accesses])
            access_buttons.append([InlineKeyboardButton(f"{user[2]}: {access_text}", callback_data=f"edit_access_{user[0]}")])
        
        reply_markup = InlineKeyboardMarkup(access_buttons)
        await update.message.reply_text("Users and their accesses:", reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = int(query.data.split("_")[-1])
    
    accesses = db.get_access_list()
    user_accesses = db.get_user_accesses(user_id)
    user_access_ids = [access[0] for access in user_accesses]
    
    buttons = []
    for access in accesses:
        if access[0] in user_access_ids:
            buttons.append([InlineKeyboardButton(f"Revoke {access[1]}", callback_data=f"revoke_{user_id}_{access[0]}")])
        else:
            buttons.append([InlineKeyboardButton(f"Grant {access[1]}", callback_data=f"grant_{user_id}_{access[0]}")])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(text="Modify accesses:", reply_markup=reply_markup)

async def grant_access(update: Update, context: CallbackContext):
    query = update.callback_query
    _, user_id, access_id = query.data.split("_")
    db.add_user_access(user_id, access_id)
    await query.edit_message_text(text=f"Access granted to user {user_id}")

async def revoke_access(update: Update, context: CallbackContext):
    query = update.callback_query
    _, user_id, access_id = query.data.split("_")
    db.remove_user_access(user_id, access_id)
    await query.edit_message_text(text=f"Access revoked from user {user_id}")

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
            all_commands = db.get_all_commands()
            buttons = [[InlineKeyboardButton(command[0], callback_data=f"grant_{user_id}_{command[0]}")] for command in all_commands]
            reply_markup = InlineKeyboardMarkup(buttons)
            await context.bot.send_message(config.ADMIN_ID, f"New user registered: @{update.message.from_user.username}\nProfile: {profile}", reply_markup=reply_markup)

async def userlist(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        users = db.get_users()
        user_list = "\n".join([f"ID: {user[1]}, Username: {user[2]}, Profile: {user[3]}" for user in users])
        await update.message.reply_text(f"Users:\n{user_list}")

async def adminlist(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        admins = db.get_admins()
        admin_list = "\n".join([f"ID: {admin[1]}, Username: {admin[2]}" for admin in admins])
        await update.message.reply_text(f"Admins:\n{admin_list}")

async def nameparamlist(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        questions = db.get_questions_list()
        question_list = "\n".join([f"ID: {question[0]}, Question: {question[1]}" for question in questions])
        await update.message.reply_text(f"Profile Questions:\n{question_list}")

async def set_admin(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        if context.args:
            target_user_id = context.args[0]
            db.set_admin(target_user_id)
            await update.message.reply_text(f"User {target_user_id} has been granted admin rights.")
        else:
            await update.message.reply_text("Please provide the user ID to grant admin rights.")

async def addaccess_start(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        await update.message.reply_text("Please enter the access name:")
        return ACCESS_NAME
    else:
        await update.message.reply_text("You are not authorized to add access entries.")
        return ConversationHandler.END

async def addaccess_name(update: Update, context: CallbackContext):
    context.user_data['access_name'] = update.message.text
    await update.message.reply_text("Please enter the access description:")
    return ACCESS_DESCRIPTION

async def addaccess_description(update: Update, context: CallbackContext):
    access_name = context.user_data['access_name']
    access_description = update.message.text
    db.add_access(access_name, access_description)
    await update.message.reply_text(f"Access '{access_name}' with description '{access_description}' has been added.")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

async def addcommand_start(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        await update.message.reply_text("Please enter the command name:")
        return COMMAND_NAME
    else:
        await update.message.reply_text("You are not authorized to add commands.")
        return ConversationHandler.END

async def addcommand_name(update: Update, context: CallbackContext):
    context.user_data['command_name'] = update.message.text
    await update.message.reply_text("Please enter the command description:")
    return COMMAND_DESCRIPTION

async def addcommand_description(update: Update, context: CallbackContext):
    command_name = context.user_data['command_name']
    command_description = update.message.text
    db.add_command(command_name, command_description)
    await update.message.reply_text(f"Command '/{command_name}' with description '{command_description}' has been added.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(config.BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_handler(CommandHandler("userlist", userlist))
    app.add_handler(CommandHandler("adminlist", adminlist))
    app.add_handler(CommandHandler("accesslist", accesslist))
    app.add_handler(CommandHandler("nameparamlist", nameparamlist))
    app.add_handler(CommandHandler("setadmin", set_admin))

    # Conversation handler for adding access
    addaccess_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addaccess', addaccess_start)],
        states={
            ACCESS_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, addaccess_name)],
            ACCESS_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, addaccess_description)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Conversation handler for adding commands
    addcommand_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addcommand', addcommand_start)],
        states={
            COMMAND_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, addcommand_name)],
            COMMAND_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, addcommand_description)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(addaccess_conv_handler)
    app.add_handler(addcommand_conv_handler)
    app.add_handler(CallbackQueryHandler(button, pattern='edit_access_'))
    app.add_handler(CallbackQueryHandler(grant_access, pattern='grant_'))
    app.add_handler(CallbackQueryHandler(revoke_access, pattern='revoke_'))

    app.run_polling()
