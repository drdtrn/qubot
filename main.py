from typing import Final
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import asyncio

TOKEN: Final = "6902203932:AAHm0-ggIDPFb-RckZvCe9gzu_Qne7kkrNA"
BOTUSERNAME: Final = "@dm_daily_bot"

app = Application.builder().token(TOKEN).build()

# Load website and parse main news
qubic_info = requests.get("https://rpc.qubic.org/v1/latest-stats").json()
price = f"Çmimi momental i Qubic: ${qubic_info['data']['price']:.9f}"
addresses = f"Numri total i Adresave të QubicWallet: {int(qubic_info['data']['activeAddresses']):,.0f}"
m_c = f"MarketCap: ${int(qubic_info['data']['marketCap']):,.0f}"
burned = f"{int(qubic_info['data']['burnedQus']):,.0f}"
b_in_dollars = (int(qubic_info['data']['burnedQus']) * qubic_info['data']['price'])
numri_i_djegjeve = f"Sasia e Qubic-ave të djegur: {burned} (${b_in_dollars:,.3f})"
epoka = f"Epoka: {qubic_info['data']['epoch']}"


# Command to start the bot and display news titles
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{price} \n{addresses} \n{m_c} \n{numri_i_djegjeve} \n{epoka}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == "group" or "supergroup" or "chat":
        if "/dmprice" in text:
            await update.message.reply_text(f"{price} \n{addresses} \n{m_c} \n{numri_i_djegjeve} \n{epoka}")
        else:
            return
    else:
        return


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("dmprice", start_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Start the bot
    app.run_polling()
