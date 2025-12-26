import os

# Read environment variables
BOT_TOKEN = os.environ["BOT_TOKEN"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
from pypdf import PdfReader

client = Groq(api_key=GROQ_API_KEY)

pdf_text = ""
if os.path.exists("your.pdf"):
    reader = PdfReader("your.pdf")
    for page in reader.pages[:10]:
        pdf_text += page.extract_text() + "\n"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 AI PDF Chat Bot Ready! Ask anything from PDF or normally.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    prompt = f"PDF CONTENT:\n{pdf_text}\nQUESTION:\n{user_msg}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("🤖 Bot is running...")
app.run_polling()
