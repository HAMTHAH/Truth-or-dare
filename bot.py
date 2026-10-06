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
    CallbackQueryHandler,
    InlineQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

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


def create_game():
    code = secrets.token_hex(6)

    games[code] = {
        "player1": None,
        "player2": None,

        # Whose turn it is RIGHT NOW.
        "turn": None,

        "active": False,
        "round": 0,

        # Current unfinished challenge.
        "challenge_id": None,
        "challenge_type": None,
        "challenge_text": None,
        "challenge_player": None,
    }

    return code


# ============================================================
# HELPERS
# ============================================================

def get_player(game, user_id):
    if game["player1"] and game["player1"]["id"] == user_id:
        return "player1"

    if game["player2"] and game["player2"]["id"] == user_id:
        return "player2"

    return None


def other_player(player):
    return "player2" if player == "player1" else "player1"


def player_name(game, player):
    if not game.get(player):
        return "Unknown"

    return game[player]["name"]


# ============================================================
# CHALLENGE BUTTONS
# ============================================================

def next_challenge_buttons(code, previous_challenge_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "😈 TRUTH",
                switch_inline_query_current_chat=(
                    f"truth|{code}|{previous_challenge_id}"
                ),
            ),
            InlineKeyboardButton(
                "🔥 DARE",
                switch_inline_query_current_chat=(
                    f"dare|{code}|{previous_challenge_id}"
                ),
            ),
        ],
        [
            InlineKeyboardButton(
                "🎲 RANDOM",
                switch_inline_query_current_chat=(
                    f"random|{code}|{previous_challenge_id}"
                ),
            )
        ],
    ])


def answer_button(code, challenge_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✍️ ANSWER",
                switch_inline_query_current_chat=(
                    f"answer|{code}|{challenge_id}|"
                ),
            )
        ]
    ])


# ============================================================
# /START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
        "Type @NAUGHTYDARE_bot in a private chat "
        "to start a game."
    )


# ============================================================
# INLINE QUERY
# ============================================================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    iq = update.inline_query
    q = iq.query.strip()

    # ========================================================
    # NEW GAME
    # ========================================================

    if not q:

        code = create_game()

        result = InlineQueryResultArticle(
            id=f"lobby_{code}",
            title="🎮 START 1-ON-1 GAME",
            description="Start a private Truth or Dare game",
            input_message_content=InputTextMessageContent(
                "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                "👤 Player 1: Waiting...\n"
                "👤 Player 2: Waiting...\n\n"
                "Tap JOIN GAME."
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🎮 JOIN GAME",
                        callback_data=f"join:{code}",
                    )
                ]
            ]),
        )

        await iq.answer(
            [result],
            cache_time=0,
            is_personal=False,
        )

        return

    parts = q.split("|")
    action = parts[0]

    if len(parts) < 2:
        await iq.answer([], cache_time=0)
        return

    code = parts[1]
    game = games.get(code)

    if not game:
        await iq.answer([], cache_time=0)
        return

    user = iq.from_user

    # ========================================================
    # TRUTH / DARE / RANDOM
    # ========================================================

    if action in ("truth", "dare", "random"):

        if not game["active"]:
            await iq.answer([], cache_time=0)
            return

        player = get_player(game, user.id)

        if not player:

            result = InlineQueryResultArticle(
                id=f"notplayer_{secrets.token_hex(5)}",
                title="❌ YOU ARE NOT IN THIS GAME",
                description="Only the two players can play.",
                input_message_content=InputTextMessageContent(
                    "❌ You are not one of the players."
                ),
            )

            await iq.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )
            return

        # ----------------------------------------------------
        # CURRENT PLAYER MUST MATCH
        # ----------------------------------------------------

        if player != game["turn"]:

            result = InlineQueryResultArticle(
                id=f"wrongturn_{secrets.token_hex(5)}",
                title="⏳ NOT YOUR TURN",
                description=(
                    f"It's {player_name(game, game['turn'])}'s turn."
                ),
                input_message_content=InputTextMessageContent(
                    f"⏳ It's {player_name(game, game['turn'])}'s turn."
                ),
            )

            await iq.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )
            return

        # ----------------------------------------------------
        # WAS THIS BUTTON PRESSED FROM A PREVIOUS CHALLENGE?
        # ----------------------------------------------------

        previous_id = parts[2] if len(parts) >= 3 else None

        # If there is an active challenge, the only legal way
        # to choose another challenge is from that challenge's
        # own buttons.
        if game["challenge_id"]:

            if previous_id != game["challenge_id"]:

                result = InlineQueryResultArticle(
                    id=f"oldpanel_{secrets.token_hex(5)}",
                    title="⚠️ OLD GAME PANEL",
                    description="Use the newest challenge panel.",
                    input_message_content=InputTextMessageContent(
                        "⚠️ That button belongs to an older challenge.\n\n"
                        "Please use the newest game panel."
                    ),
                )

                await iq.answer(
                    [result],
                    cache_time=0,
                    is_personal=True,
                )
                return

            # ------------------------------------------------
            # A NEW CHALLENGE SELECTION COMPLETES THE OLD
            # DARE.
            #
            # For Truth, the answer button is used instead,
            # so this path normally means the old challenge
            # was a Dare.
            # ------------------------------------------------

            if game["challenge_type"] != "dare":

                result = InlineQueryResultArticle(
                    id=f"needsanswer_{secrets.token_hex(5)}",
                    title="✍️ ANSWER THE TRUTH FIRST",
                    description="Complete the current Truth first.",
                    input_message_content=InputTextMessageContent(
                        "✍️ You need to answer the current Truth first."
                    ),
                )

                await iq.answer(
                    [result],
                    cache_time=0,
                    is_personal=True,
                )
                return

            # ------------------------------------------------
            # DARE COMPLETED
            # ------------------------------------------------

            old_player = game["challenge_player"]

            if player != old_player:

                result = InlineQueryResultArticle(
                    id=f"wrongdareplayer_{secrets.token_hex(5)}",
                    title="⏳ NOT YOUR TURN",
                    description="This dare belongs to the other player.",
                    input_message_content=InputTextMessageContent(
                        "⏳ This dare belongs to the other player."
                    ),
                )

                await iq.answer(
                    [result],
                    cache_time=0,
                    is_personal=True,
                )
                return

            # Switch turn ONLY NOW.
            new_player = other_player(old_player)

            game["turn"] = new_player

            # Clear the old challenge.
            game["challenge_id"] = None
            game["challenge_type"] = None
            game["challenge_text"] = None
            game["challenge_player"] = None

            # The new challenge will be generated below
            # for the new player.

            player = new_player

        else:

            # No current challenge means this is the beginning
            # of a new turn.
            if player != game["turn"]:
                await iq.answer([], cache_time=0)
                return

        # ----------------------------------------------------
        # CREATE NEW CHALLENGE
        # ----------------------------------------------------

        challenge_id = secrets.token_hex(8)

        if action == "truth":

            challenge = random.choice(TRUTHS)
            challenge_type = "truth"

        elif action == "dare":

            challenge = random.choice(DARES)
            challenge_type = "dare"

        else:

            if random.choice([True, False]):

                challenge = random.choice(TRUTHS)
                challenge_type = "truth"

            else:

                challenge = random.choice(DARES)
                challenge_type = "dare"

        game["round"] += 1

        game["challenge_id"] = challenge_id
        game["challenge_type"] = challenge_type
        game["challenge_text"] = challenge
        game["challenge_player"] = player

        name = player_name(game, player)

        title = (
            "😈 TRUTH"
            if challenge_type == "truth"
            else "🔥 DARE"
        )

        text = (
            f"🔥 ROUND {game['round']} 🔥\n\n"
            f"🎯 {name}'S TURN\n\n"
            f"{title}\n\n"
            f"{challenge}"
        )

        if challenge_type == "truth":

            keyboard = answer_button(
                code,
                challenge_id,
            )

        else:

            keyboard = next_challenge_buttons(
                code,
                challenge_id,
            )

        result = InlineQueryResultArticle(
            id=f"challenge_{code}_{challenge_id}",
            title=f"{title} — {name}",
            description=challenge[:100],
            input_message_content=InputTextMessageContent(text),
            reply_markup=keyboard,
        )

        await iq.answer(
            [result],
            cache_time=0,
            is_personal=False,
        )

        return

    # ========================================================
    # ANSWER
    # ========================================================

    if action == "answer":

        if len(parts) < 3:
            await iq.answer([], cache_time=0)
            return

        challenge_id = parts[2]
        answer = parts[3].strip() if len(parts) >= 4 else ""

        # ----------------------------------------------------
        # ASK FOR ANSWER
        # ----------------------------------------------------

        if not answer:

            result = InlineQueryResultArticle(
                id=f"typeanswer_{secrets.token_hex(5)}",
                title="✍️ TYPE YOUR ANSWER",
                description="Type your answer after the bot username.",
                input_message_content=InputTextMessageContent(
                    "✍️ Type your answer after @NAUGHTYDARE_bot."
                ),
            )

            await iq.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )
            return

        if not game["active"]:

            await iq.answer([], cache_time=0)
            return

        player = get_player(game, user.id)

        if not player:

            result = InlineQueryResultArticle(
                id=f"notplayer_{secrets.token_hex(5)}",
                title="❌ YOU ARE NOT IN THIS GAME",
                description="You are not one of the players.",
                input_message_content=InputTextMessageContent(
                    "❌ You are not one of the two players."
                ),
            )

            await iq.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )
            return

        # ----------------------------------------------------
        # TURN CHECK
        # ----------------------------------------------------

        if player != game["turn"]:

            result = InlineQueryResultArticle(
                id=f"wronganswerturn_{secrets.token_hex(5)}",
                title="⏳ NOT YOUR TURN",
                description=(
                    f"It's {player_name(game, game['turn'])}'s turn."
                ),
                input_message_content=InputTextMessageContent(
                    f"⏳ It's {player_name(game, game['turn'])}'s turn."
                ),
            )

            await iq.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )
            return

        # ----------------------------------------------------
        # EXACT CHALLENGE CHECK
        # ----------------------------------------------------

        if game["challenge_id"] != challenge_id:

            result = InlineQueryResultArticle(
                id=f"oldtruth_{secrets.token_hex(5)}",
                title="⚠️ OLD QUESTION",
                description="That question is no longer active.",
                input_message_content=InputTextMessageContent(
                    "⚠️ That question is no longer active.\n\n"
                    "Please use the newest question."
                ),
            )

            await iq.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )
            return

        if game["challenge_type"] != "truth":

            await iq.answer([], cache_time=0)
            return

        if game["challenge_player"] != player:

            result = InlineQueryResultArticle(
                id=f"wrongtruthplayer_{secrets.token_hex(5)}",
                title="⏳ THIS TRUTH BELONGS TO THE OTHER PLAYER",
                description="Wait for your turn.",
                input_message_content=InputTextMessageContent(
                    "⏳ This Truth belongs to the other player."
                ),
            )

            await iq.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )
            return

        # ----------------------------------------------------
        # COMPLETE TRUTH
        # ----------------------------------------------------

        answer = answer[:1000]

        current_name = player_name(
            game,
            player,
        )

        next_player = other_player(player)

        next_name = player_name(
            game,
            next_player,
        )

        # Clear current challenge.
        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_text"] = None
        game["challenge_player"] = None

        # NOW switch turn.
        game["turn"] = next_player

        text = (
            f"📝 {current_name}'S ANSWER\n\n"
            f"{answer}\n\n"
            "✅ Truth completed!\n\n"
            f"🎯 NEXT TURN: {next_name}"
        )

        # The answer panel gets buttons for the NEW turn.
        # Because there is no active challenge now, these
        # buttons create the first challenge for the next player.
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "😈 TRUTH",
                    switch_inline_query_current_chat=(
                        f"truth|{code}"
                    ),
                ),
                InlineKeyboardButton(
                    "🔥 DARE",
                    switch_inline_query_current_chat=(
                        f"dare|{code}"
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    "🎲 RANDOM",
                    switch_inline_query_current_chat=(
                        f"random|{code}"
                    ),
                )
            ],
        ])

        result = InlineQueryResultArticle(
            id=f"answer_{code}_{secrets.token_hex(5)}",
            title="📨 ANSWER SENT",
            description=answer[:100],
            input_message_content=InputTextMessageContent(text),
            reply_markup=keyboard,
        )

        await iq.answer(
            [result],
            cache_time=0,
            is_personal=False,
        )

        return

    await iq.answer([], cache_time=0)


# ============================================================
# CALLBACKS
# ============================================================

async def callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    data = query.data
    parts = data.split(":")

    if len(parts) < 2:
        await query.answer()
        return

    action = parts[0]
    code = parts[1]

    game = games.get(code)

    if not game:

        await query.answer(
            "❌ Game expired.",
            show_alert=True,
        )
        return

    user = query.from_user

    # ========================================================
    # JOIN GAME
    # ========================================================

    if action == "join":

        if game["player1"] and game["player1"]["id"] == user.id:

            await query.answer(
                "You're already Player 1."
            )

        elif game["player2"] and game["player2"]["id"] == user.id:

            await query.answer(
                "You're already Player 2."
            )

        elif not game["player1"]:

            game["player1"] = {
                "id": user.id,
                "name": user.first_name,
            }

            await query.answer(
                "✅ You are Player 1!"
            )

        elif not game["player2"]:

            game["player2"] = {
                "id": user.id,
                "name": user.first_name,
            }

            await query.answer(
                "✅ You are Player 2!"
            )

        else:

            await query.answer(
                "❌ This game already has two players.",
                show_alert=True,
            )
            return

        if game["player1"] and game["player2"]:

            text = (
                "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                f"👤 Player 1: "
                f"{player_name(game, 'player1')}\n"
                f"👤 Player 2: "
                f"{player_name(game, 'player2')}\n\n"
                "✅ Both players joined!\n\n"
                "Player 1 will start."
            )

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔥 START GAME",
                        callback_data=f"start:{code}",
                    )
                ]
            ])

        else:

            text = (
                "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                f"👤 Player 1: "
                f"{player_name(game, 'player1')}\n"
                f"👤 Player 2: "
                f"{player_name(game, 'player2')}\n\n"
                "Waiting for the second player..."
            )

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🎮 JOIN GAME",
                        callback_data=f"join:{code}",
                    )
                ]
            ])

        if query.inline_message_id:

            await context.bot.edit_message_text(
                inline_message_id=query.inline_message_id,
                text=text,
                reply_markup=keyboard,
            )

        return

    # ========================================================
    # START GAME
    # ========================================================

    if action == "start":

        if not game["player1"] or not game["player2"]:

            await query.answer(
                "Both players must join first.",
                show_alert=True,
            )
            return

        game["active"] = True

        # PLAYER 1 ALWAYS STARTS.
        game["turn"] = "player1"

        game["round"] = 0

        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_text"] = None
        game["challenge_player"] = None

        name = player_name(
            game,
            "player1",
        )

        text = (
            "🔥 GAME STARTED! 🔥\n\n"
            f"🎯 {name}'S TURN\n\n"
            "Choose Truth, Dare, or Random."
        )

        await query.answer(
            "🔥 Player 1 starts!"
        )

        if query.inline_message_id:

            await context.bot.edit_message_text(
                inline_message_id=query.inline_message_id,
                text=text,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "😈 TRUTH",
                            switch_inline_query_current_chat=(
                                f"truth|{code}"
                            ),
                        ),
                        InlineKeyboardButton(
                            "🔥 DARE",
                            switch_inline_query_current_chat=(
                                f"dare|{code}"
                            ),
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "🎲 RANDOM",
                            switch_inline_query_current_chat=(
                                f"random|{code}"
                            ),
                        )
                    ],
                ]),
            )

        return

    await query.answer()


# ============================================================
# MAIN
# ============================================================

def main():

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        InlineQueryHandler(inline_query)
    )

    app.add_handler(
        CallbackQueryHandler(callback)
    )

    print(
        "🔥 NAUGHTYDARE BOT RUNNING — "
        "LOCKED TURN SYSTEM ENABLED 🔥"
    )

    app.run_polling()


if __name__ == "__main__":
    main()
