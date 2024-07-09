from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, filters, CallbackContext, MessageHandler
import config
import database as db

QUESTION_TEXT, EDIT_QUESTION_TEXT = range(2)

async def nameparamlist(update: Update, context: CallbackContext):
    if update.message.from_user.id == config.ADMIN_ID:
        questions = db.get_questions()
        question_buttons = [
            [InlineKeyboardButton(f"Edit {question[1]}", callback_data=f"editquestion_{question[0]}"),
             InlineKeyboardButton(f"Delete", callback_data=f"deletequestion_{question[0]}")]
            for question in questions
        ]
        question_buttons.append([InlineKeyboardButton("Add New Question", callback_data="addquestion")])
        await update.message.reply_text("Profile Questions:", reply_markup=InlineKeyboardMarkup(question_buttons))

async def addquestion_start(update: Update, context: CallbackContext):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("Please enter the new question:")
        return QUESTION_TEXT
    elif update.message.from_user.id == config.ADMIN_ID:
        await update.message.reply_text("Please enter the new question:")
        return QUESTION_TEXT
    else:
        await update.message.reply_text("You are not authorized to add questions.")
        return ConversationHandler.END

async def addquestion_text(update: Update, context: CallbackContext):
    question_text = update.message.text
    db.add_question(question_text)
    await update.message.reply_text(f"Question '{question_text}' has been added.")
    await nameparamlist(update, context)  # Refresh the question list
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

question_handlers = [
    CommandHandler("nameparamlist", nameparamlist),
    CallbackQueryHandler(addquestion_start, pattern='addquestion'),
    ConversationHandler(
        entry_points=[CallbackQueryHandler(addquestion_start, pattern='addquestion')],
        states={
            QUESTION_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, addquestion_text)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
]
