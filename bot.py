import os
import random
import uuid

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.constants import ParseMode


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
# GAME STORAGE
# ============================================================

games = {}


def new_game():
    return {
        "p1_id": None,
        "p1_name": None,
        "p2_id": None,
        "p2_name": None,
        "active": False,

        # 1 = Player 1
        # 2 = Player 2
        "turn": 1,

        # Current challenge
        "challenge_id": None,
        "challenge_type": None,
        "challenge_player": None,
        "challenge_text": None,
    }


# ============================================================
# HELPERS
# ============================================================

def get_game(code):
    return games.get(code)


def get_player(game, user_id):
    if user_id == game["p1_id"]:
        return 1

    if user_id == game["p2_id"]:
        return 2

    return None


def player_name(game, number):
    if number == 1:
        return game["p1_name"]

    return game["p2_name"]


def other_player(number):
    return 2 if number == 1 else 1


def game_buttons(code, challenge_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 TRUTH",
                switch_inline_query_current_chat=f"truth {code} {challenge_id}"
            ),
            InlineKeyboardButton(
                "😈 DARE",
                switch_inline_query_current_chat=f"dare {code} {challenge_id}"
            ),
            InlineKeyboardButton(
                "🎲 RANDOM",
                switch_inline_query_current_chat=f"random {code} {challenge_id}"
            ),
        ]
    ])


def lobby_buttons(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 JOIN GAME",
                callback_data=f"join:{code}"
            )
        ]
    ])


def start_buttons(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 START GAME",
                callback_data=f"start:{code}"
            )
        ]
    ])


def make_challenge(game, challenge_type, player):
    if challenge_type == "truth":
        text = random.choice(TRUTHS)
        emoji = "🔥"
        title = "TRUTH"

    elif challenge_type == "dare":
        text = random.choice(DARES)
        emoji = "😈"
        title = "DARE"

    else:
        if random.choice([True, False]):
            text = random.choice(TRUTHS)
            emoji = "🔥"
            title = "TRUTH"
        else:
            text = random.choice(DARES)
            emoji = "😈"
            title = "DARE"

    challenge_id = uuid.uuid4().hex[:10]

    game["challenge_id"] = challenge_id
    game["challenge_type"] = title.lower()
    game["challenge_player"] = player
    game["challenge_text"] = text

    return challenge_id, emoji, title, text


# ============================================================
# /START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🎮 <b>NAUGHTY TRUTH OR DARE</b>\n\n"
        "Play a private 1-on-1 Truth or Dare game.\n\n"
        "To play with someone:\n"
        "1️⃣ Open any private chat\n"
        "2️⃣ Type <code>@NAUGHTYDARE_bot</code>\n"
        "3️⃣ Send the game to the chat\n\n"
        "🔥 No gender selection\n"
        "🔥 Players are saved automatically\n"
        "🔥 Turns are P1 → P2 → P1 → P2"
    )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML
    )


# ============================================================
# INLINE QUERY
# ============================================================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.inline_query
    user = query.from_user

    text = query.query.strip()

    # --------------------------------------------------------
    # Empty inline query = create lobby
    # --------------------------------------------------------

    if not text:

        code = uuid.uuid4().hex[:8]

        games[code] = new_game()

        game = games[code]

        game["p1_id"] = user.id
        game["p1_name"] = user.first_name or "Player 1"

        from telegram import InlineQueryResultArticle, InputTextMessageContent

        result = InlineQueryResultArticle(
            id=f"lobby_{code}",
            title="🎮 START 1-ON-1 GAME",
            description="Start a Truth or Dare game in this chat",
            input_message_content=InputTextMessageContent(
                "🎮 <b>TRUTH OR DARE</b>\n\n"
                f"👤 <b>Player 1:</b> {game['p1_name']}\n"
                "👤 <b>Player 2:</b> Waiting...\n\n"
                "Send this game to your chat and let your partner join.",
                parse_mode=ParseMode.HTML
            ),
            reply_markup=lobby_buttons(code)
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # Parse query
    # --------------------------------------------------------

    parts = text.split()

    if len(parts) < 2:
        await query.answer([], cache_time=0)
        return

    action = parts[0].lower()
    code = parts[1]

    game = get_game(code)

    if not game:
        await query.answer([], cache_time=0)
        return

    previous_id = parts[2] if len(parts) >= 3 else ""

    player = get_player(game, user.id)

    if player is None:
        from telegram import InlineQueryResultArticle, InputTextMessageContent

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

    if not game["active"]:

        from telegram import InlineQueryResultArticle, InputTextMessageContent

        result = InlineQueryResultArticle(
            id=f"waiting_{uuid.uuid4().hex}",
            title="⏳ WAITING FOR GAME",
            description="The game has not started yet",
            input_message_content=InputTextMessageContent(
                "⏳ Waiting for the second player to join."
            )
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # ========================================================
    # OLD PANEL CHECK
    # ========================================================
    #
    # This MUST happen before turn checking.
    #
    # Old buttons remain visible in Telegram, so we identify
    # them using challenge_id.
    # ========================================================

    if previous_id and game["challenge_id"]:

        if previous_id != game["challenge_id"]:

            from telegram import InlineQueryResultArticle, InputTextMessageContent

            current_player = game["turn"]
            current_name = player_name(game, current_player)

            result = InlineQueryResultArticle(
                id=f"old_{uuid.uuid4().hex}",
                title="⚠️ OLD PANEL — CONTINUE GAME",
                description=f"Current turn: {current_name}",
                input_message_content=InputTextMessageContent(
                    "⚠️ <b>This is an old challenge panel.</b>\n\n"
                    f"🎯 It is now <b>{current_name}</b>'s turn.\n\n"
                    "Use the buttons below to choose the next challenge."
                ),
                reply_markup=game_buttons(
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

    # ========================================================
    # TURN CHECK
    # ========================================================

    if player != game["turn"]:

        from telegram import InlineQueryResultArticle, InputTextMessageContent

        current_name = player_name(game, game["turn"])

        result = InlineQueryResultArticle(
            id=f"wait_{uuid.uuid4().hex}",
            title="⏳ WAIT FOR YOUR TURN",
            description=f"{current_name}'s turn",
            input_message_content=InputTextMessageContent(
                f"⏳ <b>Wait for your turn.</b>\n\n"
                f"🎯 It is <b>{current_name}</b>'s turn."
            ),
            reply_markup=game_buttons(
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

    # ========================================================
    # PLAYER CHOOSES NEXT CHALLENGE
    # ========================================================

    if action not in ("truth", "dare", "random"):

        await query.answer([], cache_time=0)
        return

    # --------------------------------------------------------
    # If there is a current challenge:
    #
    # Choosing a button means the current player has finished
    # their challenge and is giving the turn to the other player.
    # --------------------------------------------------------

    if game["challenge_id"]:

        game["turn"] = other_player(game["turn"])

    # --------------------------------------------------------
    # Create challenge for the new/current player
    # --------------------------------------------------------

    challenge_player = game["turn"]

    challenge_id, emoji, title, challenge_text = make_challenge(
        game,
        action,
        challenge_player
    )

    challenge_name = player_name(
        game,
        challenge_player
    )

    from telegram import InlineQueryResultArticle, InputTextMessageContent

    message = (
        f"{emoji} <b>{title}</b>\n\n"
        f"<b>{challenge_text}</b>\n\n"
        f"🎯 <b>{challenge_name}'s turn</b>\n\n"
        "Choose what the next challenge should be:"
    )

    result = InlineQueryResultArticle(
        id=f"challenge_{challenge_id}",
        title=f"{emoji} {title} — {challenge_name}",
        description=challenge_text[:100],
        input_message_content=InputTextMessageContent(
            message,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=game_buttons(
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

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # --------------------------------------------------------
    # JOIN
    # --------------------------------------------------------

    if data.startswith("join:"):

        code = data.split(":", 1)[1]

        game = get_game(code)

        if not game:
            await query.edit_message_text(
                "❌ This game no longer exists."
            )
            return

        user = query.from_user

        # Player 1 clicking join
        if user.id == game["p1_id"]:

            await query.answer(
                "You are already Player 1.",
                show_alert=True
            )
            return

        # Someone else becomes Player 2
        if game["p2_id"] is None:

            game["p2_id"] = user.id
            game["p2_name"] = user.first_name or "Player 2"

            text = (
                "🎮 <b>TRUTH OR DARE</b>\n\n"
                f"👤 Player 1: <b>{game['p1_name']}</b>\n"
                f"👤 Player 2: <b>{game['p2_name']}</b>\n\n"
                "✅ Both players joined!\n\n"
                "Player 1 can start the game."
            )

            await query.edit_message_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=start_buttons(code)
            )

            return

        # Game already has two players
        await query.answer(
            "This game already has two players.",
            show_alert=True
        )

        return

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    if data.startswith("start:"):

        code = data.split(":", 1)[1]

        game = get_game(code)

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

        game["active"] = True
        game["turn"] = 1

        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_player"] = None
        game["challenge_text"] = None

        text = (
            "🔥 <b>GAME STARTED!</b>\n\n"
            f"👤 Player 1: <b>{game['p1_name']}</b>\n"
            f"👤 Player 2: <b>{game['p2_name']}</b>\n\n"
            f"🎯 <b>{game['p1_name']}'s turn</b>\n\n"
            "Type <code>@NAUGHTYDARE_bot</code> "
            "in this chat and choose:\n\n"
            "🔥 Truth\n"
            "😈 Dare\n"
            "🎲 Random"
        )

        await query.edit_message_text(
            text,
            parse_mode=ParseMode.HTML
        )

        return


# ============================================================
# MAIN
# ============================================================

def main():

    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        InlineQueryHandler(inline_query)
    )

    app.add_handler(
        CallbackQueryHandler(callback)
    )

    print("NAUGHTYDARE bot is running...")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
