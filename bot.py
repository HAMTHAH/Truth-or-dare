import os
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ============================================================
# 50 SPICY TRUTHS
# ============================================================

TRUTHS = [
    "Who is the most attractive person you've ever had a crush on?",
    "Have you ever secretly liked a friend?",
    "Who was your last crush?",
    "What's the first thing you notice about someone you're attracted to?",
    "Have you ever flirted with someone just to make another person jealous?",
    "What's your biggest weakness when you like someone?",
    "Have you ever liked someone who didn't know you existed?",
    "Would you date someone your best friend used to like?",
    "What's the boldest move you've ever made on a crush?",
    "Have you ever pretended not to like someone when you actually did?",
    "Who was the last person who made your heart beat faster?",
    "What's your biggest dating red flag?",
    "What's your biggest green flag?",
    "Have you ever fallen for someone unexpectedly?",
    "Would you choose looks or personality?",
    "What's your ideal first date?",
    "Have you ever checked someone's profile repeatedly because you liked them?",
    "What's the most attractive personality trait?",
    "Have you ever sent a message and immediately regretted it?",
    "Who was the last person you wanted to impress?",
    "Would you date someone significantly different from your usual type?",
    "What's the most romantic thing someone could do for you?",
    "Have you ever had a crush on someone unavailable?",
    "What's the longest you've secretly liked someone?",
    "Have you ever flirted through texting but acted shy in person?",
    "What's the most attractive thing someone can wear?",
    "Have you ever caught feelings after saying you wouldn't?",
    "Would you make the first move or wait?",
    "What's your favorite kind of compliment?",
    "Have you ever reread an old conversation with someone you liked?",
    "Who would you want to receive a surprise date invitation from?",
    "What's something that instantly makes someone more attractive to you?",
    "Have you ever tried to look extra good because someone you liked was going to be there?",
    "Would you date your exact opposite?",
    "What's the most embarrassing thing you've done because you liked someone?",
    "Have you ever gotten jealous even though you weren't dating the person?",
    "What's your favorite flirting style?",
    "Have you ever practiced what to say before talking to your crush?",
    "What makes you lose interest in someone immediately?",
    "Would you rather receive flowers or a surprise date?",
    "Have you ever intentionally waited before replying to someone you liked?",
    "What's your dream date location?",
    "Have you ever liked someone your friends warned you about?",
    "What's more attractive: confidence or shyness?",
    "Have you ever had chemistry with someone you barely knew?",
    "What's one thing you'd love your future partner to understand about you?",
    "Would you rather make the first move or have someone surprise you?",
    "What's the sweetest thing someone has ever said to you?",
    "If you could go on a date with anyone you know, who would you choose?",
]

# ============================================================
# 50 SPICY DARES
# ============================================================

DARES = [
    "Give someone in the group your best pickup line.",
    "Send a cute selfie to someone you trust.",
    "Give the person above you a genuine compliment.",
    "Send someone: 'Be honest... would you date me? 👀'",
    "Describe your ideal partner without saying their name.",
    "Send a flirty emoji to someone you secretly like.",
    "Give someone a rating out of 10 for their flirting skills.",
    "Send a voice message saying your best pickup line.",
    "Tell the group your first impression of your crush.",
    "Change your profile picture to your best dressed-up photo for 10 minutes.",
    "Write a cheesy romantic message and send it to the group.",
    "Tell someone what you find most attractive about their personality.",
    "Send someone: 'I have a question for you 👀'",
    "Give the person above you a ridiculous romantic nickname.",
    "Describe your perfect date in three sentences.",
    "Send your best non-explicit selfie to the group.",
    "Give someone your best celebrity-style introduction.",
    "Tell the group what your dream partner looks like.",
    "Write a pickup line using the person's name above you.",
    "Send a heart emoji to the person you think has the best smile.",
    "Tell someone one thing that makes them attractive.",
    "Record a 5-second voice message saying 'I think you're cute.'",
    "Let another player choose your status for 10 minutes.",
    "Give someone a dramatic compliment like you're in a romance movie.",
    "Tell the group your most embarrassing crush story.",
    "Send a selfie making your best confident expression.",
    "Give someone your best 'first date' invitation.",
    "Tell another player what your ideal first date would be with them.",
    "Send a message saying 'We need to talk 👀' to a friend, then reveal it's a dare.",
    "Give the person above you a rating for their sense of humor.",
    "Say three things you find attractive in a person.",
    "Send your favorite romantic emoji combination.",
    "Give someone a compliment without mentioning their appearance.",
    "Pretend to propose to another player for 10 seconds.",
    "Create a fake dating-app bio for yourself and read it aloud.",
    "Send a voice message introducing yourself as someone's future date.",
    "Tell the group your most attractive quality.",
    "Give someone a cheesy movie-style compliment.",
    "Send someone: 'Quick question... what's your type? 👀'",
    "Let another player choose one harmless emoji you must use in your next five messages.",
    "Describe your perfect partner using only five words.",
    "Give someone a playful compliment.",
    "Tell the group what would make you instantly interested in someone.",
    "Send a selfie with your best smile.",
    "Give someone a fake award for being the most attractive personality.",
    "Tell another player their best quality.",
    "Make up a romantic movie title about you and your crush.",
    "Send a voice message saying your most dramatic love confession.",
    "Tell the group your dream date activity.",
    "Choose someone and give them your best harmless flirting attempt.",
]

# ============================================================
# KEYBOARDS
# ============================================================

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("😈 TRUTH", callback_data="truth"),
            InlineKeyboardButton("🔥 DARE", callback_data="dare"),
        ],
        [
            InlineKeyboardButton("🎲 RANDOM", callback_data="random"),
        ],
    ])


def challenge_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 NEXT", callback_data="random"),
            InlineKeyboardButton("😈 TRUTH", callback_data="truth"),
        ],
        [
            InlineKeyboardButton("🔥 DARE", callback_data="dare"),
            InlineKeyboardButton("🎭 MENU", callback_data="menu"),
        ],
    ])


# ============================================================
# START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 *TRUTH OR DARE* 🔥\n\n"
        "😈 Spicy questions\n"
        "💋 Flirty challenges\n"
        "👀 Awkward confessions\n"
        "❤️ Dating & attraction\n\n"
        "Choose your challenge 👇",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


# ============================================================
# SEND CHALLENGE
# ============================================================

async def send_challenge(query, challenge_type):

    if challenge_type == "truth":
        question = random.choice(TRUTHS)
        title = "😈 TRUTH"

    elif challenge_type == "dare":
        question = random.choice(DARES)
        title = "🔥 DARE"

    else:
        if random.choice([True, False]):
            question = random.choice(TRUTHS)
            title = "😈 TRUTH"
        else:
            question = random.choice(DARES)
            title = "🔥 DARE"

    player = query.from_user.first_name

    await query.message.reply_text(
        f"🎯 *{title}*\n\n"
        f"👤 Player: *{player}*\n\n"
        f"👉 {question}",
        parse_mode="Markdown",
        reply_markup=challenge_keyboard(),
    )


# ============================================================
# BUTTON HANDLER
# ============================================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "menu":

        await query.message.reply_text(
            "🎭 *TRUTH OR DARE*\n\n"
            "Choose your challenge 👇",
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )

        return

    if query.data == "truth":
        await send_challenge(query, "truth")

    elif query.data == "dare":
        await send_challenge(query, "dare")

    elif query.data == "random":
        await send_challenge(query, "random")


# ============================================================
# START BOT
# ============================================================

def main():

    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is not set!")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("🔥 Truth or Dare bot is running!")

    app.run_polling()


if __name__ == "__main__":
    main()
