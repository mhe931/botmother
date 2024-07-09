from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, filters, CallbackContext, MessageHandler, Application
import config
import database as db

ACCESS_NAME, ACCESS_DESCRIPTION = range(2)

async def accesslist(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        users = db.get_users()
        access_buttons = [[InlineKeyboardButton(f"{user[2]}: {', '.join([a[0] for a in db.get_user_accesses(user[0])])}", callback_data=f"edit_{user[0]}")] for user in users]
        await update.message.reply_text("Users and their accesses:", reply_markup=InlineKeyboardMarkup(access_buttons))

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    action, user_id, *access_id = query.data.split("_")
    user_id = int(user_id)

    if action == 'edit':
        user_accesses = db.get_user_accesses(user_id)
        all_accesses = db.get_all_commands()
        buttons = [[InlineKeyboardButton(f"{'Revoke' if (a[0],) in user_accesses else 'Grant'} {a[0]}", callback_data=f"{'revoke' if (a[0],) in user_accesses else 'grant'}_{user_id}_{a[0]}")] for a in all_accesses]
        await query.edit_message_text(text="Modify accesses:", reply_markup=InlineKeyboardMarkup(buttons))
    elif action in {'grant', 'revoke'}:
        (db.add_user_access if action == 'grant' else db.remove_user_access)(user_id, access_id[0])
        await query.edit_message_text(text=f"Access {action}ed for user {user_id}.")
    elif action == 'deny':
        db.delete_access_request(user_id, access_id[0])
        await query.edit_message_text(text=f"Access request denied for user {user_id}.")

async def userlist(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        users = db.get_users()
        await update.message.reply_text(f"Users:\n" + "\n".join([f"ID: {user[1]}, Username: {user[2]}, Profile: {user[3]}" for user in users]))

async def adminlist(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        admins = db.get_admins()
        await update.message.reply_text(f"Admins:\n" + "\n".join([f"ID: {admin[1]}, Username: {admin[2]}" for admin in admins]))

async def set_admin(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        if context.args:
            db.set_admin(context.args[0])
            await update.message.reply_text(f"User {context.args[0]} has been granted admin rights.")
        else:
            await update.message.reply_text("Please provide the user ID to grant admin rights.")

async def addaccess_start(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        await update.message.reply_text("Please enter the access name:")
        return ACCESS_NAME
    return ConversationHandler.END

async def addaccess_name(update: Update, context: CallbackContext):
    context.user_data['access_name'] = update.message.text
    await update.message.reply_text("Please enter the access description:")
    return ACCESS_DESCRIPTION

async def addaccess_description(update: Update, context: CallbackContext):
    db.add_access(context.user_data['access_name'], update.message.text)
    await update.message.reply_text(f"Access '{context.user_data['access_name']}' added.")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

async def send_startup_message(application: Application):
    await application.bot.send_message(config.ADMIN_ID, "Bot is Up")

admin_handlers = [
    CommandHandler("userlist", userlist),
    CommandHandler("adminlist", adminlist),
    CommandHandler("accesslist", accesslist),
    CommandHandler("setadmin", set_admin),
    CallbackQueryHandler(button, pattern='edit_'),
    CallbackQueryHandler(button, pattern='grant_'),
    CallbackQueryHandler(button, pattern='revoke_'),
    CallbackQueryHandler(button, pattern='deny_'),
    ConversationHandler(
        entry_points=[CommandHandler('addaccess', addaccess_start)],
        states={
            ACCESS_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, addaccess_name)],
            ACCESS_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, addaccess_description)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    ),
]
