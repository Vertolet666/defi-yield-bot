
import requests, time, telebot
from config import TELEGRAM_TOKEN, CHAT_ID

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_stable_pools(min_apy=10):
    url = "https://yields.llama.fi/pools"
    res = requests.get(url).json()
    return [p for p in res["data"]
            if any(s in p["symbol"].lower() for s in ["usdt","usdc","dai","busd"])
            and p.get("apy", 0)>=min_apy]

def format_pool(p):
    return f"🔥 Новый пул: {p['symbol']} на {p['project']}\nAPY: {p['apy']:.2f}% | TVL: ${p['tvlUsd']:.0f}"

sent = set()
while True:
    for pool in get_stable_pools():
        uid = f"{pool['project']}-{pool['symbol']}"
        if uid not in sent:
            bot.send_message(CHAT_ID, format_pool(pool))
            sent.add(uid)
    time.sleep(1800)
