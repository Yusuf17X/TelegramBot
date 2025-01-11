from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

SECRET_PASSWORD_HOMEWORK = "key46427"
SECRET_PASSWORD_SEND = "key57773"
OWNER_CHAT_ID = 1364250523
BIT_GROUP_ID = -4703409969
homework = "ما عدنه شي..."


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type == "private":
        user_first_name = " " + update.effective_user.first_name + " " if update.effective_user else ""
        private_suggest = ""
    else:
        user_first_name = " شباب"
        private_suggest = " بالخاص.."

    welcome_message = (
        f"هلو{user_first_name}! 😇\n"
        "اني سچاچ 😎💪\n"
        "بوت يساعد طلاب ال BIT 👨‍💻\n\n"
        "اكتب 'الدراسة' حتى تعرف شعدنه دراسة هذا الاسبوع..\n"
        "اكتب 'الجدول' حتى تشوف جدول محاضراتنه..\n\n"
        f"اذا عندك اقتراح لتطوير البوت دز /suggest{private_suggest}\n\n"
    )
    await update.message.reply_text(welcome_message)


async def handle_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type == "private":
        if update.message.chat.type != "private":
            await update.message.reply_text("دز اقتراحك على الخاص رجاءا 🙂")
        else:
            await update.message.reply_text("رجاءا اكتب اقتراحك و رح يتم ارساله لمطور البوت.. 📝")
            context.user_data["awaiting_suggestion"] = True


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global homework
    text = update.message.text.lower()
    print(update.effective_chat.id)

    user_username = update.effective_user.username if update.effective_user.username else str(update.effective_user.id)

    if update.message.chat.type == "private":
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"يتم استخدام البوت بواسطة:\n @{user_username}")

    if context.user_data.get("awaiting_suggestion", False):
        suggestion = update.message.text
        await context.bot.send_message(chat_id=OWNER_CHAT_ID,
                                       text=f"اقتراح لتطوير البوت من: @{user_username}:\n\n{suggestion}")
        await update.message.reply_text("شكرا على المقترح 😊\n دزيته لمطور البوت و رح يتم معالجته قريبا ان شاء الله..")

        context.user_data["awaiting_suggestion"] = False
    elif text in ["الدراسة", "الدراسه", "الواجبات"]:
        await update.message.reply_text(f"الدراسة لهذا الاسبوع:\n{homework}")
    elif text == "الجدول":
        img_url = "https://drive.google.com/uc?id=1wLKfjUXaJtbzui1YN5t26JKvesmilg6b&export=download"
        await update.message.reply_photo(img_url)
    elif text == SECRET_PASSWORD_HOMEWORK.lower() and update.message.chat.type == "private":
        await update.message.reply_text("اكتب الواجبات الجديدة... 📝")
        context.user_data["awaiting_homework"] = True
    elif update.message.chat.type == "private" and context.user_data.get("awaiting_homework", False):
        homework = update.message.text
        context.user_data["awaiting_homework"] = False
        await update.message.reply_text("تم تحديث الواجبات.. 😊")
    elif text == SECRET_PASSWORD_SEND.lower() and update.message.chat.type == "private":
        await update.message.reply_text("اكتب الرساله التي تريد ارسالها الى كروب الدفعه...👻")
        context.user_data["awaiting_send"] = True
    elif update.message.chat.type == "private" and context.user_data.get("awaiting_send", False):
        if text == "OFF":
            context.user_data["awaiting_send"] = False
            await update.message.reply_text("تم تعطيل الامر...💯")
        else:
            global_message = update.message.text
            context.user_data["awaiting_send"] = False
            await context.bot.send_message(chat_id=BIT_GROUP_ID, text=global_message)
            await update.message.reply_text("تم ارسال الرسالة...✅")
    elif update.message.chat.type == "private":
        if not text.startswith("/"):
            await update.message.reply_text("ما افهم المكتوب...\n استخدم وحده من الاوامر او الكلمات الموجودة مسبقا..")


async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message and "اقتراح لتطوير البوت من" in update.message.reply_to_message.text:
        if "@" in update.message.reply_to_message.text:
            user_info = update.message.reply_to_message.text.split('@')[1]
            username = user_info.split(':')[0]
        else:
            username = None

        if username:
            try:
                await context.bot.send_message(chat_id=f"@{username}", text=f"رد المطور:\n\n{update.message.text}")
            except Exception as e:
                await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=f"Error sending message to @{username}: {e}")
        else:
            await context.bot.send_message(chat_id=OWNER_CHAT_ID, text="Could not extract a valid username.")
    else:
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text="No valid reply_to_message or message format is incorrect.")


if __name__ == "__main__":
    TOKEN = "7650529985:AAEx94vntqZ-fBcnhkaz1gmPyVhecO9pGxg"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("suggest", handle_suggest))
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY & filters.Chat(OWNER_CHAT_ID), handle_reply))

    print("Bot is running...")
    app.run_polling()
