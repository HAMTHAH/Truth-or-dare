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
# QUESTIONS
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
    "Would you date someone different from your usual type?",
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
    "What's something that instantly makes someone more attractive?",
    "Have you ever tried to look extra good because someone you liked was there?",
    "Would you date your exact opposite?",
    "What's the most embarrassing thing you've done because you liked someone?",
    "Have you ever gotten jealous even though you weren't dating?",
    "What's your favorite flirting style?",
    "Have you ever practiced what to say before talking to your crush?",
    "What makes you lose interest in someone immediately?",
    "Would you rather receive flowers or a surprise date?",
    "Have you ever intentionally waited before replying to someone you liked?",
    "What's your dream date location?",
    "Have you ever liked someone your friends warned you about?",
    "What's more attractive: confidence or shyness?",
    "Have you ever had chemistry with someone you barely knew?",
    "What's one thing you'd want your future partner to understand?",
    "Would you rather make the first move or be surprised?",
    "What's the sweetest thing someone has ever said to you?",
    "If you could go on a date with anyone you know, who would you choose?",
]

DARES = [
    "Give someone in the game your best pickup line.",
    "Send a cute selfie to someone you trust.",
    "Give another player a genuine compliment.",
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
    "Give another player a ridiculous romantic nickname.",
    "Describe your perfect date in three sentences.",
    "Send your best non-explicit selfie to the group.",
    "Give someone your best celebrity-style introduction.",
    "Tell the group what your dream partner looks like.",
    "Write a pickup line using another player's name.",
    "Send a heart emoji to the person you think has the best smile.",
    "Tell someone one thing that makes them attractive.",
    "Record a 5-second voice message saying 'I think you're cute.'",
    "Let another player choose your status for 10 minutes.",
    "Give someone a dramatic compliment like you're in a romance movie.",
    "Tell the group your most embarrassing crush story.",
    "Send a selfie making your best confident expression.",
    "Give someone your best first-date invitation.",
    "Tell another player what your ideal first date would be.",
    "Send a message saying 'We need to talk 👀' to a friend, then reveal it's a dare.",
    "Give another player a rating for their sense of humor.",
    "Say three things you find attractive in a person.",
    "Send your favorite romantic emoji combination.",
    "Give someone a compliment without mentioning appearance.",
    "Pretend to propose to another player for 10 seconds.",
    "Create a fake dating-app bio for yourself.",
    "Send a voice message introducing yourself as someone's future date.",
    "Tell the group your most attractive quality.",
    "Give someone a cheesy movie-style compliment.",
    "Send someone: 'Quick question... what's your type? 👀'",
    "Let another player choose one harmless emoji for your next five messages.",
    "Describe your perfect partner using only five words.",
    "Give someone a playful compliment.",
    "Tell the group what would instantly make you interested in someone.",
    "Send a selfie with your best smile.",
    "Give someone a fake award for having the best personality.",
    "Tell another player their best quality.",
    "Make up a romantic movie title about you and your crush.",
    "Send a voice message saying your most dramatic love confession.",
    "Tell the group your dream date activity.",
    "Choose someone and give them your best harmless flirting attempt.",
]

# ============================================================
# GAME STORAGE
# ============================================================

games = {}


def get_game(chat_id):
    if chat_id not in games:
        games[chat_id] = {
            "players": [],
            "current_player": None,
            "started": False,
        }

    return games[chat_id]


# ============================================================
# MAIN GAME PANEL
# ============================================================

def main_panel(chat_id):

    game = get_game(chat_id)
    players = game["players"]

    if players:
        player_text = "\n".join(
            f"• {p['name']}" for p in players
        )
    else:
        player_text = "No players yet."

    status = "🟢 Game ready" if len(players) >= 2 else "🟡 Waiting for players"

    text = (
        "🔥 *TRUTH OR DARE* 🔥\n\n"
        f"{status}\n\n"
        f"👥 *Players ({len(players)}):*\n"
        f"{player_text}\n\n"
        "Join the game and wait for everyone to be ready!"
    )

    keyboard = [
        [
            InlineKeyboardButton("👥 JOIN", callback_data="join"),
            InlineKeyboardButton("🚪 LEAVE", callback_data="leave"),
        ],
        [
            InlineKeyboardButton("🎮 START GAME", callback_data="start_game"),
        ],
        [
            InlineKeyboardButton("🔄 REFRESH", callback_data="panel"),
        ],
    ]

    return text, InlineKeyboardMarkup(keyboard)


# ============================================================
# CHALLENGE PANEL
# ============================================================

def challenge_panel():

    keyboard = [
        [
            InlineKeyboardButton("🔄 NEXT", callback_data="next"),
            InlineKeyboardButton("😈 TRUTH", callback_data="truth"),
        ],
        [
            InlineKeyboardButton("🔥 DARE", callback_data="dare"),
            InlineKeyboardButton("🎲 RANDOM", callback_data="random"),
        ],
        [
            InlineKeyboardButton("✅ DONE", callback_data="done"),
            InlineKeyboardButton("🏠 GAME PANEL", callback_data="panel"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# START COMMAND
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    text, keyboard = main_panel(chat_id)

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


# ============================================================
# SEND NEW CHALLENGE
# ============================================================

async def send_challenge(query, challenge_type="random"):

    chat_id = query.message.chat_id
    game = get_game(chat_id)

    if not game["players"]:
        await query.answer(
            "Nobody has joined the game yet!",
            show_alert=True,
        )
        return

    # Choose player
    if game["current_player"] is None:
        player = random.choice(game["players"])
    else:
        current_index = next(
            (
                i for i, p in enumerate(game["players"])
                if p["id"] == game["current_player"]
            ),
            -1,
        )

        if current_index == -1:
            player = random.choice(game["players"])
        else:
            next_index = (current_index + 1) % len(game["players"])
            player = game["players"][next_index]

    game["current_player"] = player["id"]

    # Choose challenge
    if challenge_type == "truth":
        challenge = random.choice(TRUTHS)
        title = "😈 TRUTH"

    elif challenge_type == "dare":
        challenge = random.choice(DARES)
        title = "🔥 DARE"

    else:
        if random.choice([True, False]):
            challenge = random.choice(TRUTHS)
            title = "😈 TRUTH"
        else:
            challenge = random.choice(DARES)
            title = "🔥 DARE"

    text = (
        f"{title}\n\n"
        f"👤 *{player['name']}'s turn!*\n\n"
        f"🎯 {challenge}\n\n"
        "Choose an action below:"
    )

    await query.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=challenge_panel(),
    )


# ============================================================
# BUTTON HANDLER
# ============================================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    user = query.from_user
    game = get_game(chat_id)

    # --------------------------------------------------------
    # MAIN PANEL
    # --------------------------------------------------------

    if query.data == "panel":

        text, keyboard = main_panel(chat_id)

        await query.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

        return

    # --------------------------------------------------------
    # JOIN
    # --------------------------------------------------------

    if query.data == "join":

        already_joined = any(
            p["id"] == user.id
            for p in game["players"]
        )

        if already_joined:
            await query.answer(
                "You're already in the game!",
                show_alert=True,
            )
            return

        game["players"].append({
            "id": user.id,
            "name": user.first_name,
        })

        await query.answer(
            f"{user.first_name} joined! 🎉",
            show_alert=True,
        )

        text, keyboard = main_panel(chat_id)

        await query.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

        return

    # --------------------------------------------------------
    # LEAVE
    # --------------------------------------------------------

    if query.data == "leave":

        game["players"] = [
            p for p in game["players"]
            if p["id"] != user.id
        ]

        if game["current_player"] == user.id:
            game["current_player"] = None

        await query.answer(
            "You left the game.",
            show_alert=True,
        )

        text, keyboard = main_panel(chat_id)

        await query.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

        return

    # --------------------------------------------------------
    # START GAME
    # --------------------------------------------------------

    if query.data == "start_game":

        if len(game["players"]) < 2:
            await query.answer(
                "You need at least 2 players!",
                show_alert=True,
            )
            return

        game["started"] = True
        game["current_player"] = None

        await query.answer("Game started! 🔥")

        await send_challenge(query, "random")

        return

    # --------------------------------------------------------
    # TRUTH
    # --------------------------------------------------------

    if query.data == "truth":

        await send_challenge(query, "truth")

        return

    # --------------------------------------------------------
    # DARE
    # --------------------------------------------------------

    if query.data == "dare":

        await send_challenge(query, "dare")

        return

    # --------------------------------------------------------
    # RANDOM
    # --------------------------------------------------------

    if query.data == "random":

        await send_challenge(query, "random")

        return

    # --------------------------------------------------------
    # NEXT
    # --------------------------------------------------------

    if query.data == "next":

        await send_challenge(query, "random")

        return

    # --------------------------------------------------------
    # DONE
    # --------------------------------------------------------

    if query.data == "done":

        await query.answer(
            "Challenge completed! 🔥",
            show_alert=True,
        )

        await send_challenge(query, "random")

        return


# ============================================================
# BOT
# ============================================================

def main():

    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is not set!")

    app = Application.builder().token(token).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button)
    )

    print("🔥 Multiplayer Truth or Dare bot is running!")

    app.run_polling()


if __name__ == "__main__":
    main()
