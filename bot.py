import os
import secrets
import random

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


# ============================================================
# TOKEN
# ============================================================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing.")


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
    "What is the sweetest thing someone has ever done for you?",
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


def make_id():
    return secrets.token_hex(8)


def create_game():
    code = secrets.token_hex(6)

    games[code] = {
        "player1_id": None,
        "player1_name": None,

        "player2_id": None,
        "player2_name": None,

        "active": False,

        # ALWAYS player1 first
        "turn": "player1",

        "round": 0,

        # Current challenge
        "challenge_id": None,
        "challenge_type": None,
        "challenge_text": None,
        "challenge_player": None,
    }

    return code


def get_player(game, user_id):
    if game["player1_id"] == user_id:
        return "player1"

    if game["player2_id"] == user_id:
        return "player2"

    return None


def other_player(player):
    return "player2" if player == "player1" else "player1"


def get_name(game, player):
    if player == "player1":
        return game["player1_name"]

    return game["player2_name"]


# ============================================================
# BUTTONS
# ============================================================

def challenge_buttons(code, previous_id=""):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📝 TRUTH",
                switch_inline_query_current_chat=
                f"truth|{code}|{previous_id}"
            ),

            InlineKeyboardButton(
                "🎯 DARE",
                switch_inline_query_current_chat=
                f"dare|{code}|{previous_id}"
            ),

            InlineKeyboardButton(
                "🎲 RANDOM",
                switch_inline_query_current_chat=
                f"random|{code}|{previous_id}"
            ),
        ]
    ])


def answer_button(code, challenge_id):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✍️ ANSWER",
                switch_inline_query_current_chat=
                f"answer|{code}|{challenge_id}|"
            )
        ]
    ])


# ============================================================
# /START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 NAUGHTY DARE\n\n"
        "Type @NAUGHTYDARE_bot in a private chat to start a game."
    )


# ============================================================
# INLINE MODE
# ============================================================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.inline_query
    text = query.query.strip()

    # ========================================================
    # CREATE GAME
    # ========================================================

    if not text:

        code = create_game()

        result = InlineQueryResultArticle(
            id=f"lobby_{code}",

            title="🔥 START 1-ON-1 GAME",

            description="Start a private Truth or Dare game.",

            input_message_content=InputTextMessageContent(
                "🔥 <b>TRUTH OR DARE</b>\n\n"
                "👤 Player 1: waiting...\n"
                "👤 Player 2: waiting...\n\n"
                "Tap JOIN GAME.",
                parse_mode="HTML",
            ),

            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "👥 JOIN GAME",
                        callback_data=f"join|{code}"
                    )
                ]
            ]),
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    parts = text.split("|", 3)

    action = parts[0]

    # ========================================================
    # ANSWER
    # ========================================================

    if action == "answer":

        if len(parts) < 3:
            return

        code = parts[1]
        challenge_id = parts[2]

        answer_text = ""

        if len(parts) >= 4:
            answer_text = parts[3].strip()

        game = games.get(code)

        if not game:
            await query.answer([], cache_time=0)
            return

        # ----------------------------------------------------
        # ASK USER TO TYPE ANSWER
        # ----------------------------------------------------

        if not answer_text:

            result = InlineQueryResultArticle(
                id=f"answer_help_{make_id()}",

                title="✍️ TYPE YOUR ANSWER",

                description="Type your answer after the command.",

                input_message_content=InputTextMessageContent(
                    "✍️ Type your answer in the inline box."
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True
            )

            return

        player = get_player(game, query.from_user.id)

        if not player:

            result = InlineQueryResultArticle(
                id=f"error_{make_id()}",
                title="❌ YOU ARE NOT IN THIS GAME",
                input_message_content=InputTextMessageContent(
                    "❌ You are not one of the players."
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True
            )

            return

        # ====================================================
        # IMPORTANT:
        # CHECK OLD CHALLENGE FIRST
        # ====================================================

        if game["challenge_id"] != challenge_id:

    # The question is old, but give the player
    # a NEW usable panel instead of a dead-end message.

    player = get_player(game, query.from_user.id)

    if not player:

        result = InlineQueryResultArticle(
            id=f"old_answer_{make_id()}",
            title="⚠️ OLD QUESTION",
            description="You are not part of this game.",
            input_message_content=InputTextMessageContent(
                "⚠️ You are not one of the players."
            ),
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # If it is this player's turn, give them
    # the actual current challenge buttons.
    if player == game["turn"]:

        result = InlineQueryResultArticle(
            id=f"new_panel_{make_id()}",

            title="🎮 CONTINUE GAME",

            description="Choose the next Truth, Dare or Random.",

            input_message_content=InputTextMessageContent(
                f"⚠️ <b>That question is already closed.</b>\n\n"
                f"🎯 <b>{get_name(game, player)}'s turn</b>\n\n"
                f"Choose your next challenge.",
                parse_mode="HTML",
            ),

            reply_markup=challenge_buttons(code)
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # It is the other player's turn.
    # Still show the current game state, but don't pretend
    # that this player can play.

    result = InlineQueryResultArticle(
        id=f"waiting_panel_{make_id()}",

        title="⏳ WAIT FOR YOUR TURN",

        description=f"It's {get_name(game, game['turn'])}'s turn.",

        input_message_content=InputTextMessageContent(
            f"⚠️ <b>That question is already closed.</b>\n\n"
            f"⏳ It's <b>{get_name(game, game['turn'])}'s turn</b>.\n\n"
            f"Use the newest game panel when it's your turn.",
            parse_mode="HTML",
        ),

        reply_markup=challenge_buttons(code)
    )

    await query.answer(
        [result],
        cache_time=0,
        is_personal=True
    )

    return

        # Now check challenge type
        if game["challenge_type"] != "truth":

            result = InlineQueryResultArticle(
                id=f"invalid_{make_id()}",
                title="⚠️ THIS QUESTION IS CLOSED",
                input_message_content=InputTextMessageContent(
                    "⚠️ This question is already closed."
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True
            )

            return

        # Now check whose turn
        if player != game["turn"]:

            result = InlineQueryResultArticle(
                id=f"turn_{make_id()}",

                title="⏳ NOT YOUR TURN",

                description=f"It's {get_name(game, game['turn'])}'s turn.",

                input_message_content=InputTextMessageContent(
                    f"⏳ It's <b>{get_name(game, game['turn'])}</b>'s turn.",
                    parse_mode="HTML",
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True
            )

            return

        # ----------------------------------------------------
        # COMPLETE TRUTH
        # ----------------------------------------------------

        answered_by = get_name(game, player)

        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_text"] = None
        game["challenge_player"] = None

        game["turn"] = other_player(player)

        next_player = game["turn"]

        result = InlineQueryResultArticle(
            id=f"answer_sent_{make_id()}",

            title="✅ ANSWER",

            input_message_content=InputTextMessageContent(
                f"💬 <b>{answered_by}</b> answered:\n\n"
                f"{answer_text}\n\n"
                f"👉 <b>{get_name(game, next_player)}'s turn</b>",
                parse_mode="HTML",
            ),

            reply_markup=challenge_buttons(code)
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # ========================================================
    # TRUTH / DARE / RANDOM
    # ========================================================

    if action not in ("truth", "dare", "random"):

        await query.answer([], cache_time=0)
        return

    if len(parts) < 2:
        await query.answer([], cache_time=0)
        return

    code = parts[1]
    previous_id = parts[2] if len(parts) >= 3 else ""

    game = games.get(code)

    if not game or not game["active"]:
        await query.answer([], cache_time=0)
        return

    player = get_player(game, query.from_user.id)

    if not player:
        await query.answer([], cache_time=0)
        return

    # ========================================================
    # MOST IMPORTANT FIX
    #
    # CHECK OLD PANEL BEFORE CHECKING TURN
    # ========================================================

    if game["challenge_id"]:

        if previous_id != game["challenge_id"]:

            result = InlineQueryResultArticle(
                id=f"old_panel_{make_id()}",

                title="⚠️ OLD GAME PANEL",

                description="Use the newest panel.",

                input_message_content=InputTextMessageContent(
                    "⚠️ <b>OLD GAME PANEL</b>\n\n"
                    "This button belongs to an earlier round.\n\n"
                    "Use the buttons on the newest panel.",
                    parse_mode="HTML",
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True
            )

            return

    else:

        # No active challenge.
        # If an old panel supplied a previous ID,
        # it is automatically stale.

        if previous_id:

            result = InlineQueryResultArticle(
                id=f"old_panel_{make_id()}",

                title="⚠️ OLD GAME PANEL",

                description="Use the newest panel.",

                input_message_content=InputTextMessageContent(
                    "⚠️ <b>OLD GAME PANEL</b>\n\n"
                    "Use the newest game panel.",
                    parse_mode="HTML",
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True
            )

            return

    # ========================================================
    # NOW CHECK TURN
    # ========================================================

    if player != game["turn"]:

        result = InlineQueryResultArticle(
            id=f"wrong_turn_{make_id()}",

            title="⏳ NOT YOUR TURN",

            description=f"It's {get_name(game, game['turn'])}'s turn.",

            input_message_content=InputTextMessageContent(
                f"⏳ <b>{get_name(game, game['turn'])}</b>'s turn.\n\n"
                f"Please wait.",
                parse_mode="HTML",
            ),
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # ========================================================
    # IF CURRENT CHALLENGE IS TRUTH
    # ========================================================

    if game["challenge_id"]:

        if game["challenge_type"] == "truth":

            result = InlineQueryResultArticle(
                id=f"must_answer_{make_id()}",

                title="✍️ ANSWER THE CURRENT TRUTH",

                description="You must answer the current Truth first.",

                input_message_content=InputTextMessageContent(
                    "✍️ <b>Answer the current Truth first.</b>",
                    parse_mode="HTML",
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True
            )

            return

        # ----------------------------------------------------
        # CURRENT CHALLENGE IS DARE
        #
        # Choosing a new challenge completes the Dare.
        # ----------------------------------------------------

        if game["challenge_type"] == "dare":

            game["turn"] = other_player(game["turn"])

            player = game["turn"]

            game["challenge_id"] = None
            game["challenge_type"] = None
            game["challenge_text"] = None
            game["challenge_player"] = None

    # ========================================================
    # CHOOSE TYPE
    # ========================================================

    if action == "random":
        challenge_type = random.choice(["truth", "dare"])
    else:
        challenge_type = action

    if challenge_type == "truth":
        challenge_text = random.choice(TRUTHS)
    else:
        challenge_text = random.choice(DARES)

    # ========================================================
    # NEW CHALLENGE ID
    # ========================================================

    challenge_id = make_id()

    game["round"] += 1

    game["challenge_id"] = challenge_id
    game["challenge_type"] = challenge_type
    game["challenge_text"] = challenge_text
    game["challenge_player"] = player

    # ========================================================
    # TRUTH PANEL
    # ========================================================

    if challenge_type == "truth":

        message = (
            f"📝 <b>TRUTH</b>\n\n"
            f"👤 <b>{get_name(game, player)}</b>'s turn\n\n"
            f"{challenge_text}"
        )

        keyboard = answer_button(
            code,
            challenge_id
        )

        result = InlineQueryResultArticle(
            id=f"truth_{challenge_id}",

            title=f"📝 TRUTH — {get_name(game, player)}",

            description=challenge_text[:100],

            input_message_content=InputTextMessageContent(
                message,
                parse_mode="HTML",
            ),

            reply_markup=keyboard,
        )

    # ========================================================
    # DARE PANEL
    # ========================================================

    else:

        message = (
            f"🎯 <b>DARE</b>\n\n"
            f"👤 <b>{get_name(game, player)}</b>'s turn\n\n"
            f"{challenge_text}\n\n"
            f"Complete the dare, then choose the next challenge."
        )

        keyboard = challenge_buttons(
            code,
            challenge_id
        )

        result = InlineQueryResultArticle(
            id=f"dare_{challenge_id}",

            title=f"🎯 DARE — {get_name(game, player)}",

            description=challenge_text[:100],

            input_message_content=InputTextMessageContent(
                message,
                parse_mode="HTML",
            ),

            reply_markup=keyboard,
        )

    await query.answer(
        [result],
        cache_time=0,
        is_personal=True
    )


# ============================================================
# CALLBACK HANDLER
# ============================================================

async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data

    if not data:
        return

    parts = data.split("|", 1)

    action = parts[0]

    if len(parts) < 2:
        return

    code = parts[1]

    game = games.get(code)

    if not game:

        await query.edit_message_text(
            "❌ This game no longer exists."
        )

        return

    # ========================================================
    # JOIN
    # ========================================================

    if action == "join":

        user_id = query.from_user.id
        name = query.from_user.first_name

        # Already player 1
        if game["player1_id"] == user_id:

            await query.answer(
                "You are already Player 1.",
                show_alert=True
            )

            return

        # Already player 2
        if game["player2_id"] == user_id:

            await query.answer(
                "You are already Player 2.",
                show_alert=True
            )

            return

        # First player
        if game["player1_id"] is None:

            game["player1_id"] = user_id
            game["player1_name"] = name

        # Second player
        elif game["player2_id"] is None:

            game["player2_id"] = user_id
            game["player2_name"] = name

        else:

            await query.answer(
                "This game already has two players.",
                show_alert=True
            )

            return

        # ----------------------------------------------------
        # WAITING
        # ----------------------------------------------------

        if game["player2_id"] is None:

            await query.edit_message_text(
                f"🔥 <b>TRUTH OR DARE</b>\n\n"
                f"👤 Player 1: <b>{game['player1_name']}</b>\n"
                f"👤 Player 2: waiting...\n\n"
                f"Waiting for Player 2.",
                parse_mode="HTML",

                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "👥 JOIN GAME",
                            callback_data=f"join|{code}"
                        )
                    ]
                ])
            )

            return

        # ----------------------------------------------------
        # BOTH PLAYERS READY
        # ----------------------------------------------------

        game["turn"] = "player1"

        await query.edit_message_text(
            f"🔥 <b>TRUTH OR DARE</b>\n\n"
            f"👤 Player 1: <b>{game['player1_name']}</b>\n"
            f"👤 Player 2: <b>{game['player2_name']}</b>\n\n"
            f"🎮 Both players are ready!\n\n"
            f"▶️ <b>{game['player1_name']}</b> starts.",
            parse_mode="HTML",

            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "▶️ START GAME",
                        callback_data=f"start|{code}"
                    )
                ]
            ])
        )

        return

    # ========================================================
    # START GAME
    # ========================================================

    if action == "start":

        user_id = query.from_user.id

        if user_id not in (
            game["player1_id"],
            game["player2_id"]
        ):

            await query.answer(
                "You are not one of the players.",
                show_alert=True
            )

            return

        if not game["player1_id"] or not game["player2_id"]:

            await query.answer(
                "Both players need to join first.",
                show_alert=True
            )

            return

        # Reset game
        game["active"] = True

        game["turn"] = "player1"

        game["round"] = 0

        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_text"] = None
        game["challenge_player"] = None

        await query.edit_message_text(
            f"🔥 <b>GAME STARTED</b>\n\n"
            f"👤 Player 1: <b>{game['player1_name']}</b>\n"
            f"👤 Player 2: <b>{game['player2_name']}</b>\n\n"
            f"🎯 <b>{game['player1_name']}'s turn</b>",
            parse_mode="HTML",

            reply_markup=challenge_buttons(code)
        )

        return


# ============================================================
# MAIN
# ============================================================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        InlineQueryHandler(inline_query)
    )

    app.add_handler(
        CallbackQueryHandler(callback_handler)
    )

    print("🔥 NAUGHTYDARE BOT RUNNING")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
