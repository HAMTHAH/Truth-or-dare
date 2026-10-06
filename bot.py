import os
import random
import uuid

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    Application,
    CommandHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

# ============================================================
# QUESTIONS
# ============================================================

TRUTHS = [
    "What is the first thing you would do if I walked through your door right now?",
    "What is the most intense dream you've ever had about me?",
    "Have you ever gotten distracted while we were texting or calling?",
    "What is your favorite physical feature of mine?",
    "If I told you I was outside your house right now, how would you get ready to meet me?",
    "What's the dirtiest thought you've had about me today?",
    "What's a secret fantasy you've never told anyone?",
    "Do you prefer spicy photos or flirty voice notes?",
    "What kind of romantic roleplay would you find fun?",
    "Describe exactly how it feels when someone kisses your neck.",
    "Have you ever smiled at your phone because of me?",
    "What's the most attractive thing about me?",
    "Have you ever imagined us going on a romantic date?",
    "What's something you've wanted to tell me but never had the courage to?",
    "What's one thing I do that instantly gets your attention?",
    "Have you ever gotten jealous because of me?",
    "What's the boldest thing you'd do on a date with me?",
    "What kind of compliment from me would make your whole day?",
    "What is one secret you've been keeping from me?",
    "Have you ever had a crush on someone you shouldn't have?",
    "What's the most embarrassing thing you've done because you liked someone?",
    "What is your biggest weakness when it comes to flirting?",
    "Do you prefer someone making the first move or making you make it?",
    "What's your favorite kind of romantic attention?",
    "What's something that instantly makes someone attractive to you?",
    "Have you ever pretended not to like someone when you actually did?",
    "What's the sweetest thing someone has ever done for you?",
    "What's something you've always wanted to try on a romantic date?",
    "What's the most attractive thing someone can whisper to you?",
    "Have you ever imagined kissing someone while talking to them?",
    "What kind of date would make you fall for someone?",
    "What's one thing that can instantly make you nervous around someone?",
    "Have you ever flirted with someone just for fun?",
    "What's the most romantic place you'd want to kiss someone?",
    "What is your biggest turn-on when it comes to personality?",
    "What kind of outfit do you find most attractive?",
    "What's the longest you've ever had a crush on someone?",
    "What is one thing you would love to hear from me right now?",
    "What is your favorite memory involving me?",
    "If we were alone together for a whole day, what would you want to do?",
    "What's something about me you find impossible to ignore?",
]

DARES = [
    "Send a voice note saying something dangerously flirty.",
    "Give the other player a ridiculously cute nickname.",
    "Send your best flirty selfie.",
    "Write a three-line romantic poem about the other player.",
    "Tell the other player three things you find attractive about them.",
    "Send a voice note saying their name in your most charming voice.",
    "Describe your perfect date with the other player.",
    "Send a message that would make the other player blush.",
    "Give the other player your best pickup line.",
    "Pretend you're asking the other player on a first date.",
    "Write a cheesy romantic confession.",
    "Send a voice note pretending you're nervous because you like them.",
    "Give the other player a compliment without using the words beautiful, cute, or attractive.",
    "Describe the other player using only five words.",
    "Tell the other player what their ideal romantic nickname should be.",
    "Send a voice note saying 'I miss you' dramatically.",
    "Write a fake romantic movie scene starring you two.",
    "Tell the other player what your first impression of them was.",
    "Give the other player a ridiculous but romantic proposal.",
    "Send three emojis that describe your feelings toward the other player.",
    "Tell the other player what song reminds you of them.",
    "Write a flirty text that starts with 'I probably shouldn't tell you this, but...'",
    "Pretend you are jealous and send a dramatic message.",
    "Give the other player your most creative compliment.",
    "Describe what your dream evening together would look like.",
    "Send a voice note saying something sweet without laughing.",
    "Write a romantic message using only emojis.",
    "Tell the other player why they would be difficult to forget.",
    "Make up a secret code word that means 'I want your attention.'",
    "Send the other player a message that starts with 'Confession:'",
    "Describe your perfect hug.",
    "Give the other player a new nickname and explain it.",
    "Pretend you're texting them after the best date of your life.",
    "Write a short love letter in exactly five sentences.",
    "Tell the other player what you would notice first if they walked into a room.",
    "Send a voice note saying the sweetest thing you can think of.",
    "Create a romantic couple name for you two.",
    "Tell the other player something you've never complimented them on before.",
    "Write a flirty message without using the word 'love'.",
    "Pretend you're trying to convince the other player to go on a date with you.",
    "Give the other player a rating out of 10 and explain your score.",
    "Describe their personality using three romantic comparisons.",
    "Send a message that would make someone think you're secretly in love.",
    "Tell the other player one thing you hope happens between you two someday.",
    "Write a dramatic 'goodnight' message as if you're completely obsessed with them.",
    "Send your best innocent-but-flirty pickup line.",
    "Tell the other player what kind of date outfit you would wear.",
    "Pretend you're meeting them for the first time and flirt with them.",
    "Send a voice note saying their name three different ways.",
    "Write the most cheesy romantic sentence you can think of.",
]

# ============================================================
# GAMES
# ============================================================

games = {}


def create_game(player_id, player_name):
    return {
        "p1_id": player_id,
        "p1_name": player_name,

        "p2_id": None,
        "p2_name": None,

        "started": False,

        # Always 1 -> 2 -> 1 -> 2
        "turn": 1,

        # Current challenge
        "challenge_id": None,
        "challenge_type": None,
        "challenge_player": None,
    }


def get_player(game, user_id):
    if user_id == game["p1_id"]:
        return 1

    if user_id == game["p2_id"]:
        return 2

    return None


def get_name(game, player):
    if player == 1:
        return game["p1_name"]
    return game["p2_name"]


def next_player(player):
    return 2 if player == 1 else 1


# ============================================================
# BUTTONS
# ============================================================

def choice_buttons(code, challenge_id=""):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 TRUTH",
                switch_inline_query_current_chat=
                f"truth {code} {challenge_id}"
            ),
            InlineKeyboardButton(
                "😈 DARE",
                switch_inline_query_current_chat=
                f"dare {code} {challenge_id}"
            ),
            InlineKeyboardButton(
                "🎲 RANDOM",
                switch_inline_query_current_chat=
                f"random {code} {challenge_id}"
            ),
        ]
    ])


def join_button(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 JOIN GAME",
                callback_data=f"join:{code}"
            )
        ]
    ])


def start_button(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "▶️ START GAME",
                callback_data=f"start:{code}"
            )
        ]
    ])


# ============================================================
# /START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎮 <b>NAUGHTY TRUTH OR DARE</b>\n\n"
        "Open a private chat and type:\n\n"
        "<code>@NAUGHTYDARE_bot</code>\n\n"
        "Then choose the game.",
        parse_mode="HTML"
    )


# ============================================================
# INLINE
# ============================================================

async def inline_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.inline_query
    user = query.from_user

    text = query.query.strip()

    # --------------------------------------------------------
    # CREATE NEW GAME
    # --------------------------------------------------------

    if not text:

        code = uuid.uuid4().hex[:8]

        games[code] = create_game(
            user.id,
            user.first_name or "Player 1"
        )

        game = games[code]

        result = InlineQueryResultArticle(
            id=f"game_{code}",
            title="🎮 START 1-ON-1 GAME",
            description="Create a private Truth or Dare game",
            input_message_content=InputTextMessageContent(
                "🎮 <b>TRUTH OR DARE</b>\n\n"
                f"👤 Player 1: <b>{game['p1_name']}</b>\n"
                "👤 Player 2: <b>Waiting...</b>\n\n"
                "Send this game to the chat.\n"
                "Your partner can tap JOIN GAME.",
                parse_mode="HTML"
            ),
            reply_markup=join_button(code)
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # READ COMMAND
    # --------------------------------------------------------

    parts = text.split()

    if len(parts) < 2:
        await query.answer([], cache_time=0)
        return

    action = parts[0].lower()
    code = parts[1]

    game = games.get(code)

    if not game:
        await query.answer([], cache_time=0)
        return

    old_challenge_id = ""

    if len(parts) >= 3:
        old_challenge_id = parts[2]

    # --------------------------------------------------------
    # PLAYER CHECK
    # --------------------------------------------------------

    player = get_player(game, user.id)

    if player is None:

        result = InlineQueryResultArticle(
            id=f"notplayer_{uuid.uuid4().hex}",
            title="⚠️ NOT A PLAYER",
            description="You are not part of this game",
            input_message_content=InputTextMessageContent(
                "⚠️ You are not one of the players in this game."
            )
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # GAME NOT STARTED
    # --------------------------------------------------------

    if not game["started"]:

        result = InlineQueryResultArticle(
            id=f"waiting_{uuid.uuid4().hex}",
            title="⏳ GAME NOT STARTED",
            description="Player 1 must start the game",
            input_message_content=InputTextMessageContent(
                "⏳ The game has not started yet."
            )
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # OLD BUTTON
    # --------------------------------------------------------

    if (
        old_challenge_id
        and game["challenge_id"]
        and old_challenge_id != game["challenge_id"]
    ):

        current_player = game["turn"]
        current_name = get_name(game, current_player)

        result = InlineQueryResultArticle(
            id=f"old_{uuid.uuid4().hex}",
            title="⚠️ OLD PANEL",
            description=f"Current turn: {current_name}",
            input_message_content=InputTextMessageContent(
                "⚠️ <b>That is an old challenge.</b>\n\n"
                f"🎯 Current turn: <b>{current_name}</b>\n\n"
                "Use the buttons below."
            ),
            reply_markup=choice_buttons(
                code,
                game["challenge_id"]
            )
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # WRONG PLAYER
    # --------------------------------------------------------

    if player != game["turn"]:

        current_name = get_name(game, game["turn"])

        result = InlineQueryResultArticle(
            id=f"wait_{uuid.uuid4().hex}",
            title="⏳ WAIT FOR YOUR TURN",
            description=f"{current_name}'s turn",
            input_message_content=InputTextMessageContent(
                "⏳ <b>WAIT FOR YOUR TURN</b>\n\n"
                f"🎯 It is <b>{current_name}</b>'s turn."
            ),
            reply_markup=choice_buttons(
                code,
                game["challenge_id"] or ""
            )
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # ONLY THESE 3 COMMANDS ARE VALID
    # --------------------------------------------------------

    if action not in ("truth", "dare", "random"):

        await query.answer([], cache_time=0)
        return

    # --------------------------------------------------------
    # BUTTON PRESS = FINISH CURRENT TURN
    #
    # If there was already a challenge, move to the other
    # player BEFORE creating the new challenge.
    # --------------------------------------------------------

    if game["challenge_id"] is not None:
        game["turn"] = next_player(game["turn"])

    current_player = game["turn"]
    current_name = get_name(game, current_player)

    # --------------------------------------------------------
    # CREATE CHALLENGE
    # --------------------------------------------------------

    if action == "truth":

        challenge = random.choice(TRUTHS)
        emoji = "🔥"
        title = "TRUTH"

    elif action == "dare":

        challenge = random.choice(DARES)
        emoji = "😈"
        title = "DARE"

    else:

        if random.choice([True, False]):
            challenge = random.choice(TRUTHS)
            emoji = "🔥"
            title = "TRUTH"
        else:
            challenge = random.choice(DARES)
            emoji = "😈"
            title = "DARE"

    challenge_id = uuid.uuid4().hex[:10]

    game["challenge_id"] = challenge_id
    game["challenge_type"] = title.lower()
    game["challenge_player"] = current_player

    # --------------------------------------------------------
    # NEW PANEL
    # --------------------------------------------------------

    message = (
        f"{emoji} <b>{title}</b>\n\n"
        f"<b>{challenge}</b>\n\n"
        f"🎯 <b>{current_name}'s turn</b>\n\n"
        "When you're finished, choose the next challenge:"
    )

    result = InlineQueryResultArticle(
        id=f"challenge_{challenge_id}",
        title=f"{emoji} {title} — {current_name}",
        description=challenge[:100],
        input_message_content=InputTextMessageContent(
            message,
            parse_mode="HTML"
        ),
        reply_markup=choice_buttons(
            code,
            challenge_id
        )
    )

    await query.answer(
        [result],
        cache_time=0,
        is_personal=True
    )


# ============================================================
# CALLBACKS
# ============================================================

async def callbacks(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    data = query.data

    await query.answer()

    # ========================================================
    # JOIN
    # ========================================================

    if data.startswith("join:"):

        code = data.split(":", 1)[1]
        game = games.get(code)

        if not game:
            await query.edit_message_text(
                "❌ This game no longer exists."
            )
            return

        user = query.from_user

        # Player 1
        if user.id == game["p1_id"]:

            await query.answer(
                "You are already Player 1.",
                show_alert=True
            )
            return

        # Player 2
        if game["p2_id"] is None:

            game["p2_id"] = user.id
            game["p2_name"] = user.first_name or "Player 2"

            await query.edit_message_text(
                "🎮 <b>TRUTH OR DARE</b>\n\n"
                f"👤 Player 1: <b>{game['p1_name']}</b>\n"
                f"👤 Player 2: <b>{game['p2_name']}</b>\n\n"
                "✅ <b>Both players joined!</b>\n\n"
                "Player 1 can start the game.",
                parse_mode="HTML",
                reply_markup=start_button(code)
            )

            return

        await query.answer(
            "This game already has two players.",
            show_alert=True
        )

        return

    # ========================================================
    # START
    # ========================================================

    if data.startswith("start:"):

        code = data.split(":", 1)[1]
        game = games.get(code)

        if not game:
            await query.edit_message_text(
                "❌ This game no longer exists."
            )
            return

        user = query.from_user

        if user.id != game["p1_id"]:

            await query.answer(
                "Only Player 1 can start the game.",
                show_alert=True
            )
            return

        if game["p2_id"] is None:

            await query.answer(
                "Waiting for Player 2.",
                show_alert=True
            )
            return

        # Reset game
        game["started"] = True
        game["turn"] = 1
        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_player"] = None

        # IMPORTANT:
        # First panel already has Truth/Dare/Random.
        message = (
            "🔥 <b>GAME STARTED!</b>\n\n"
            f"👤 Player 1: <b>{game['p1_name']}</b>\n"
            f"👤 Player 2: <b>{game['p2_name']}</b>\n\n"
            f"🎯 <b>{game['p1_name']}'s turn</b>\n\n"
            "Choose your challenge:"
        )

        await query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=choice_buttons(code, "")
        )

        return


# ============================================================
# RUN BOT
# ============================================================

def main():

    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing from environment variables."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        InlineQueryHandler(inline_query)
    )

    app.add_handler(
        CallbackQueryHandler(callbacks)
    )

    print("🔥 NAUGHTYDARE BOT IS RUNNING")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
