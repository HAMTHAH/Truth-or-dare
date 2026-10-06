import os
import random
import secrets

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

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")


TRUTHS = [
    "What is the first thing you would do if I walked through your door right now?",
    "What is the most intense dream you've ever had about me?",
    "Have you ever gotten distracted while we were texting or calling?",
    "What is your favorite physical feature of mine?",
    "If I told you I was outside your house right now, how would you get ready to meet me?",
    "What's the dirtiest thought you've had about me today?",
    "What's a secret fantasy you've never told anyone?",
    "Do you prefer spicy photos or flirty voice notes?",
    "What is the most attractive thing about me?",
    "Have you ever gotten jealous because of me?",
    "What's the boldest thing you'd do on a date with me?",
    "What's your biggest weakness when it comes to flirting?",
    "What's your favorite kind of romantic attention?",
    "What's something that instantly makes someone attractive to you?",
    "What's the sweetest thing someone has ever done for you?",
    "What's something you've always wanted to try on a romantic date?",
    "Have you ever imagined kissing someone while talking to them?",
    "What kind of date would make you fall for someone?",
    "Have you ever flirted with someone just for fun?",
    "What is one thing you would love to hear from me right now?",
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
    "Give the other player a compliment without using beautiful, cute, or attractive.",
    "Describe the other player using only five words.",
    "Tell the other player what their ideal romantic nickname should be.",
    "Send a voice note saying I miss you dramatically.",
    "Write a fake romantic movie scene starring you two.",
    "Tell the other player what your first impression of them was.",
    "Give the other player a ridiculous but romantic proposal.",
    "Send three emojis that describe your feelings toward the other player.",
    "Tell the other player what song reminds you of them.",
    "Pretend you are jealous and send a dramatic message.",
    "Give the other player your most creative compliment.",
    "Describe your dream evening together.",
    "Write a romantic message using only emojis.",
    "Tell the other player why they would be difficult to forget.",
    "Describe your perfect hug.",
    "Create a romantic couple name for you two.",
    "Write a flirty message without using the word love.",
    "Give the other player a rating out of 10 and explain your score.",
    "Send your best innocent-but-flirty pickup line.",
]


games = {}


def uid():
    return secrets.token_hex(8)


def new_game():
    code = secrets.token_hex(6)

    games[code] = {
        "p1_id": None,
        "p1_name": None,
        "p2_id": None,
        "p2_name": None,
        "active": False,
        "turn": "p1",
        "challenge_id": None,
        "challenge_type": None,
        "challenge_player": None,
        "challenge_text": None,
    }

    return code


def get_player(game, user_id):
    if game["p1_id"] == user_id:
        return "p1"

    if game["p2_id"] == user_id:
        return "p2"

    return None


def other(player):
    return "p2" if player == "p1" else "p1"


def name(game, player):
    if player == "p1":
        return game["p1_name"]

    return game["p2_name"]


def game_buttons(code, challenge_id=""):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📝 TRUTH",
                switch_inline_query_current_chat=
                f"truth|{code}|{challenge_id}"
            ),
            InlineKeyboardButton(
                "🎯 DARE",
                switch_inline_query_current_chat=
                f"dare|{code}|{challenge_id}"
            ),
            InlineKeyboardButton(
                "🎲 RANDOM",
                switch_inline_query_current_chat=
                f"random|{code}|{challenge_id}"
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 NAUGHTY DARE\n\n"
        "Type @NAUGHTYDARE_bot in a private chat to start."
    )


async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.inline_query
    text = q.query.strip()

    # --------------------------------------------------------
    # NEW GAME
    # --------------------------------------------------------

    if not text:
        code = new_game()

        result = InlineQueryResultArticle(
            id=f"lobby_{code}",
            title="🔥 START 1-ON-1 GAME",
            description="Create a game",
            input_message_content=InputTextMessageContent(
                "🔥 <b>TRUTH OR DARE</b>\n\n"
                "👤 Player 1: waiting...\n"
                "👤 Player 2: waiting...",
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

        await q.answer(
            [result],
            cache_time=0,
            is_personal=True
        )
        return

    parts = text.split("|", 3)
    action = parts[0]

    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    if action == "answer":

        if len(parts) < 3:
            return

        code = parts[1]
        challenge_id = parts[2]
        answer = parts[3].strip() if len(parts) > 3 else ""

        game = games.get(code)

        if not game:
            return

        player = get_player(game, q.from_user.id)

        if not player:
            await q.answer([], cache_time=0)
            return

        if not answer:
            result = InlineQueryResultArticle(
                id=f"answer_help_{uid()}",
                title="✍️ TYPE YOUR ANSWER",
                description="Type your answer",
                input_message_content=InputTextMessageContent(
                    "✍️ Type your answer above."
                ),
            )

            await q.answer(
                [result],
                cache_time=0,
                is_personal=True
            )
            return

        # OLD QUESTION CHECK FIRST
        if game["challenge_id"] != challenge_id:

            # Give the player a usable current panel if it
            # is actually their turn.
            if player == game["turn"]:

                result = InlineQueryResultArticle(
                    id=f"continue_{uid()}",
                    title="🎮 CONTINUE GAME",
                    description="Choose your next challenge",
                    input_message_content=InputTextMessageContent(
                        f"⚠️ <b>That question is already closed.</b>\n\n"
                        f"🎯 <b>{name(game, player)}'s turn</b>",
                        parse_mode="HTML",
                    ),
                    reply_markup=game_buttons(code)
                )

            else:

                result = InlineQueryResultArticle(
                    id=f"wait_{uid()}",
                    title="⏳ WAIT FOR YOUR TURN",
                    description=f"It's {name(game, game['turn'])}'s turn",
                    input_message_content=InputTextMessageContent(
                        f"⏳ It's <b>{name(game, game['turn'])}'s turn</b>.",
                        parse_mode="HTML",
                    ),
                    reply_markup=game_buttons(code)
                )

            await q.answer(
                [result],
                cache_time=0,
                is_personal=True
            )
            return

        # WRONG TURN
        if player != game["turn"]:

            result = InlineQueryResultArticle(
                id=f"wrong_{uid()}",
                title="⏳ NOT YOUR TURN",
                input_message_content=InputTextMessageContent(
                    f"⏳ It's <b>{name(game, game['turn'])}'s turn</b>.",
                    parse_mode="HTML",
                ),
            )

            await q.answer(
                [result],
                cache_time=0,
                is_personal=True
            )
            return

        # COMPLETE TRUTH
        if game["challenge_type"] != "truth":
            return

        old_player = player

        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_player"] = None
        game["challenge_text"] = None

        game["turn"] = other(old_player)

        result = InlineQueryResultArticle(
            id=f"answer_done_{uid()}",
            title="✅ SEND ANSWER",
            input_message_content=InputTextMessageContent(
                f"💬 <b>{name(game, old_player)}</b> answered:\n\n"
                f"{answer}\n\n"
                f"👉 <b>{name(game, game['turn'])}'s turn</b>",
                parse_mode="HTML",
            ),
            reply_markup=game_buttons(code)
        )

        await q.answer(
            [result],
            cache_time=0,
            is_personal=True
        )
        return

    # --------------------------------------------------------
    # TRUTH / DARE / RANDOM
    # --------------------------------------------------------

    if action not in ("truth", "dare", "random"):
        await q.answer([], cache_time=0)
        return

    if len(parts) < 2:
        return

    code = parts[1]
    previous_id = parts[2] if len(parts) > 2 else ""

    game = games.get(code)

    if not game or not game["active"]:
        await q.answer([], cache_time=0)
        return

    player = get_player(game, q.from_user.id)

    if not player:
        await q.answer([], cache_time=0)
        return

    # --------------------------------------------------------
    # OLD PANEL CHECK FIRST
    # --------------------------------------------------------

    if game["challenge_id"]:

        if previous_id != game["challenge_id"]:

            result = InlineQueryResultArticle(
                id=f"old_{uid()}",
                title="⚠️ OLD PANEL",
                description="Use the newest panel",
                input_message_content=InputTextMessageContent(
                    "⚠️ <b>This is an old panel.</b>\n\n"
                    "Use the newest game panel.",
                    parse_mode="HTML",
                ),
            )

            await q.answer(
                [result],
                cache_time=0,
                is_personal=True
            )
            return

    # --------------------------------------------------------
    # TURN CHECK
    # --------------------------------------------------------

    if player != game["turn"]:

        result = InlineQueryResultArticle(
            id=f"turn_{uid()}",
            title="⏳ NOT YOUR TURN",
            description=f"It's {name(game, game['turn'])}'s turn",
            input_message_content=InputTextMessageContent(
                f"⏳ It's <b>{name(game, game['turn'])}'s turn</b>.",
                parse_mode="HTML",
            ),
        )

        await q.answer(
            [result],
            cache_time=0,
            is_personal=True
        )
        return

    # --------------------------------------------------------
    # TRUTH MUST BE ANSWERED
    # --------------------------------------------------------

    if game["challenge_id"] and game["challenge_type"] == "truth":

        result = InlineQueryResultArticle(
            id=f"must_answer_{uid()}",
            title="✍️ ANSWER CURRENT TRUTH",
            description="Answer the current Truth first",
            input_message_content=InputTextMessageContent(
                "✍️ <b>Answer the current Truth first.</b>",
                parse_mode="HTML",
            ),
        )

        await q.answer(
            [result],
            cache_time=0,
            is_personal=True
        )
        return

    # --------------------------------------------------------
    # DARE COMPLETED
    # --------------------------------------------------------

    if game["challenge_id"] and game["challenge_type"] == "dare":

        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_player"] = None
        game["challenge_text"] = None

        game["turn"] = other(player)
        player = game["turn"]

    # --------------------------------------------------------
    # CREATE NEW CHALLENGE
    # --------------------------------------------------------

    if action == "random":
        challenge_type = random.choice(["truth", "dare"])
    else:
        challenge_type = action

    if challenge_type == "truth":
        challenge_text = random.choice(TRUTHS)
    else:
        challenge_text = random.choice(DARES)

    challenge_id = uid()

    game["challenge_id"] = challenge_id
    game["challenge_type"] = challenge_type
    game["challenge_player"] = player
    game["challenge_text"] = challenge_text

    if challenge_type == "truth":

        message = (
            f"📝 <b>TRUTH</b>\n\n"
            f"👤 <b>{name(game, player)}'s turn</b>\n\n"
            f"{challenge_text}"
        )

        result = InlineQueryResultArticle(
            id=f"truth_{challenge_id}",
            title=f"📝 TRUTH — {name(game, player)}",
            description=challenge_text,
            input_message_content=InputTextMessageContent(
                message,
                parse_mode="HTML",
            ),
            reply_markup=answer_button(
                code,
                challenge_id
            ),
        )

    else:

        message = (
            f"🎯 <b>DARE</b>\n\n"
            f"👤 <b>{name(game, player)}'s turn</b>\n\n"
            f"{challenge_text}\n\n"
            f"Complete the dare, then choose the next challenge."
        )

        result = InlineQueryResultArticle(
            id=f"dare_{challenge_id}",
            title=f"🎯 DARE — {name(game, player)}",
            description=challenge_text,
            input_message_content=InputTextMessageContent(
                message,
                parse_mode="HTML",
            ),
            reply_markup=game_buttons(
                code,
                challenge_id
            ),
        )

    await q.answer(
        [result],
        cache_time=0,
        is_personal=True
    )


# ============================================================
# CALLBACKS
# ============================================================

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    parts = q.data.split("|", 1)

    if len(parts) != 2:
        return

    action = parts[0]
    code = parts[1]

    game = games.get(code)

    if not game:
        await q.edit_message_text("❌ Game not found.")
        return

    # --------------------------------------------------------
    # JOIN
    # --------------------------------------------------------

    if action == "join":

        user_id = q.from_user.id
        username = q.from_user.first_name

        if game["p1_id"] == user_id or game["p2_id"] == user_id:
            await q.answer(
                "You already joined.",
                show_alert=True
            )
            return

        if game["p1_id"] is None:

            game["p1_id"] = user_id
            game["p1_name"] = username

        elif game["p2_id"] is None:

            game["p2_id"] = user_id
            game["p2_name"] = username

        else:

            await q.answer(
                "Game is full.",
                show_alert=True
            )
            return

        if game["p2_id"] is None:

            await q.edit_message_text(
                f"🔥 <b>TRUTH OR DARE</b>\n\n"
                f"👤 Player 1: <b>{game['p1_name']}</b>\n"
                f"👤 Player 2: waiting...",
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

        game["turn"] = "p1"

        await q.edit_message_text(
            f"🔥 <b>TRUTH OR DARE</b>\n\n"
            f"👤 Player 1: <b>{game['p1_name']}</b>\n"
            f"👤 Player 2: <b>{game['p2_name']}</b>\n\n"
            f"🎮 Both players are ready!\n\n"
            f"▶️ <b>{game['p1_name']} starts.</b>",
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

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    if action == "start":

        if q.from_user.id not in (
            game["p1_id"],
            game["p2_id"]
        ):
            await q.answer(
                "You are not in this game.",
                show_alert=True
            )
            return

        if not game["p1_id"] or not game["p2_id"]:
            return

        game["active"] = True
        game["turn"] = "p1"

        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_player"] = None
        game["challenge_text"] = None

        await q.edit_message_text(
            f"🔥 <b>GAME STARTED</b>\n\n"
            f"👤 Player 1: <b>{game['p1_name']}</b>\n"
            f"👤 Player 2: <b>{game['p2_name']}</b>\n\n"
            f"🎯 <b>{game['p1_name']}'s turn</b>",
            parse_mode="HTML",
            reply_markup=game_buttons(code)
        )


# ============================================================
# MAIN
# ============================================================

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        InlineQueryHandler(inline)
    )

    app.add_handler(
        CallbackQueryHandler(callback)
    )

    print("🔥 NAUGHTYDARE BOT RUNNING")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
