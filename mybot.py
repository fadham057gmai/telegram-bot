from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatType

TOKEN = '7645757964:AAFgpwXlzRFQelXBoP1LheMfxgg93DOVbHM'  # استبدل بالتوكن الحقيقي
OWNER_ID = 828393212  # استبدل بمعرفك الرقمي

KEYWORDS = ['اشتراك', 'طلب', 'سجل', 'اريد']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أنا بوت أراقب الكلمات المهمة في المجموعات والخاص وأرسل تنبيهات لصاحب البوت.")

async def monitor_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    sender = update.effective_user
    chat = update.message.chat
    chat_type = chat.type
    group_title = chat.title if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP] else None

    for keyword in KEYWORDS:
        if keyword in text:
            location = f"📍 المجموعة: {group_title}" if group_title else "📍 الدردشة الخاصة"
            try:
                await context.bot.send_message(
                    chat_id=OWNER_ID,
                    text=(
                        f"🚨 تم الكشف عن كلمة: '{keyword}'\n"
                        f"👤 المستخدم: {sender.full_name} (@{sender.username or 'لايوجد اسم مستخدم'})\n"
                        f"{location}\n"
                        f"💬 الرسالة: {update.message.text}"
                    )
                )
                print(f"📨 تنبيه أرسل إلى المالك: {OWNER_ID}")
            except Exception as e:
                print(f"❌ فشل الإرسال إلى المالك: {e}")

            if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                await update.message.reply_text(f"تم استلام رسالتك، {sender.first_name}. سيتم التعامل معها.")
            elif chat_type == ChatType.PRIVATE:
                await update.message.reply_text(f"شكرًا لتواصلك! كيف يمكنني مساعدتك أكثر؟")
            break

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), monitor_messages))

    print("🤖 البوت يعمل ويراقب القروبات والخاص...")
    app.run_polling()
