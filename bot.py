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
    "Have you ever imagined us going on a romantic trip together?",
    "What is something you've wanted to tell me but never had the courage to?",
    "What is the most attractive thing about me?",
    "Have you ever reread our old messages?",
    "What's one thing I do that instantly gets your attention?",
    "Have you ever smiled at your phone because of me?",
    "What is your favorite memory involving me?",
    "If we were alone together for a whole day, what would you want to do?",
    "What's something about me you find impossible to ignore?",
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
    "What's one thing you would change about our relationship?",
    "What's something you've always wanted to try on a romantic date?",
    "What kind of romantic roleplay would you find fun?",
    "Do you prefer spicy photos or flirty voice notes?",
    "What's the most attractive thing someone can whisper to you?",
    "Have you ever imagined kissing someone while talking to them?",
    "What kind of date would make you fall for someone?",
    "What's one thing that can instantly make you nervous around someone?",
    "Have you ever flirted with someone just for fun?",
    "What's the most romantic place you'd want to kiss someone?",
    "What is your biggest turn-on when it comes to personality?",
    "What's a secret fantasy you've never told anyone?",
    "What kind of outfit do you find most attractive?",
    "What's the longest you've ever had a crush on someone?",
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
    code = secrets.token_hex(5)

    games[code] = {
        "player1": None,
        "player2": None,

        # Player whose challenge is currently active.
        "turn": None,

        "round": 0,

        # Current challenge information
        "challenge_type": None,
        "challenge": None,

        "active": False,
    }

    return code


# ============================================================
# HELPERS
# ============================================================

def player_name(game, player_number):
    player = game[player_number]

    if not player:
        return "Waiting..."

    return player["name"]


def get_player_number(game, user_id):
    if game["player1"] and game["player1"]["id"] == user_id:
        return "player1"

    if game["player2"] and game["player2"]["id"] == user_id:
        return "player2"

    return None


def other_player(player):
    if player == "player1":
        return "player2"

    return "player1"


def turn_name(game):
    if game["turn"] == "player1":
        return player_name(game, "player1")

    return player_name(game, "player2")


# ============================================================
# BUTTONS
# ============================================================

def challenge_buttons(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "😈 TRUTH",
                switch_inline_query_current_chat=f"truth|{code}",
            ),
            InlineKeyboardButton(
                "🔥 DARE",
                switch_inline_query_current_chat=f"dare|{code}",
            ),
        ],
        [
            InlineKeyboardButton(
                "🎲 RANDOM",
                switch_inline_query_current_chat=f"random|{code}",
            )
        ],
    ])


def answer_button(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✍️ ANSWER",
                switch_inline_query_current_chat=f"answer|{code}|",
            )
        ]
    ])


# ============================================================
# /START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
        "Open a private chat and type:\n\n"
        "@NAUGHTYDARE_bot\n\n"
        "Then choose START 1-ON-1 GAME."
    )


# ============================================================
# INLINE MODE
# ============================================================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.inline_query
    q = query.query.strip()

    # --------------------------------------------------------
    # START GAME
    # --------------------------------------------------------

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
                "Tap JOIN GAME to enter."
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

        await query.answer(
            [result],
            cache_time=0,
            is_personal=False,
        )

        return

    # --------------------------------------------------------
    # PARSE QUERY
    # --------------------------------------------------------

    parts = q.split("|")

    action = parts[0]

    if len(parts) < 2:
        await query.answer([], cache_time=0)
        return

    code = parts[1]

    game = games.get(code)

    if not game:
        await query.answer([], cache_time=0)
        return

    user = query.from_user

    # --------------------------------------------------------
    # TRUTH / DARE / RANDOM
    # --------------------------------------------------------

    if action in ("truth", "dare", "random"):

        if not game["active"]:
            await query.answer([], cache_time=0)
            return

        player = get_player_number(game, user.id)

        # ----------------------------------------------------
        # ONLY CURRENT PLAYER CAN CHOOSE
        # ----------------------------------------------------

        if player != game["turn"]:

            result = InlineQueryResultArticle(
                id=f"wrongturn_{secrets.token_hex(5)}",
                title="⏳ NOT YOUR TURN",
                description="Wait for the other player.",
                input_message_content=InputTextMessageContent(
                    f"⏳ It's {turn_name(game)}'s turn."
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )

            return

        # ----------------------------------------------------
        # SELECT CHALLENGE
        #
        # IMPORTANT:
        # TURN DOES NOT CHANGE HERE.
        # ----------------------------------------------------

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

        game["challenge_type"] = challenge_type
        game["challenge"] = challenge

        current_player = game["turn"]

        name = player_name(game, current_player)

        if challenge_type == "truth":
            title = "😈 TRUTH"
        else:
            title = "🔥 DARE"

        text = (
            f"🔥 ROUND {game['round']} 🔥\n\n"
            f"👤 {name}'S TURN\n\n"
            f"{title}\n\n"
            f"{challenge}"
        )

        if challenge_type == "truth":
            keyboard = answer_button(code)
        else:
            # For a dare, the player completes it and then
            # chooses the next challenge. The turn switches
            # only when the next challenge is selected.
            keyboard = challenge_buttons(code)

        result = InlineQueryResultArticle(
            id=f"challenge_{code}_{secrets.token_hex(5)}",
            title=f"{title} — {name}",
            description=challenge[:100],
            input_message_content=InputTextMessageContent(text),
            reply_markup=keyboard,
        )

        await query.answer(
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
            await query.answer([], cache_time=0)
            return

        answer = parts[2].strip()

        # ----------------------------------------------------
        # ASK USER TO TYPE ANSWER
        # ----------------------------------------------------

        if not answer:

            result = InlineQueryResultArticle(
                id=f"typeanswer_{secrets.token_hex(5)}",
                title="✍️ TYPE YOUR ANSWER",
                description="Type your answer after @NAUGHTYDARE_bot",
                input_message_content=InputTextMessageContent(
                    "✍️ Type your answer after @NAUGHTYDARE_bot."
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )

            return

        if not game["active"]:
            await query.answer([], cache_time=0)
            return

        player = get_player_number(game, user.id)

        # ----------------------------------------------------
        # ONLY CURRENT PLAYER CAN ANSWER
        # ----------------------------------------------------

        if player != game["turn"]:

            result = InlineQueryResultArticle(
                id=f"wronganswer_{secrets.token_hex(5)}",
                title="⏳ NOT YOUR TURN",
                description="Wait for the other player.",
                input_message_content=InputTextMessageContent(
                    f"⏳ It's {turn_name(game)}'s turn."
                ),
            )

            await query.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )

            return

        answer = answer[:1000]

        name = player_name(game, player)

        # ----------------------------------------------------
        # ANSWER COMPLETED
        # ----------------------------------------------------

        next_player = other_player(player)

        # NOW the turn changes.
        game["turn"] = next_player

        text = (
            f"📝 {name}'S ANSWER\n\n"
            f"{answer}\n\n"
            f"✅ Challenge completed!\n\n"
            f"🎯 Next turn: {player_name(game, next_player)}"
        )

        result = InlineQueryResultArticle(
            id=f"answer_{code}_{secrets.token_hex(5)}",
            title="📨 SEND ANSWER",
            description=answer[:100],
            input_message_content=InputTextMessageContent(text),
            reply_markup=challenge_buttons(code),
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=False,
        )

        return

    await query.answer([], cache_time=0)


# ============================================================
# CALLBACKS
# ============================================================

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    data = query.data

    parts = data.split(":")

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

        # ----------------------------------------------------
        # PLAYER 1
        # ----------------------------------------------------

        if not game["player1"]:

            game["player1"] = {
                "id": user.id,
                "name": user.first_name,
            }

            await query.answer(
                "✅ You are Player 1!"
            )

        # ----------------------------------------------------
        # PLAYER 2
        # ----------------------------------------------------

        elif (
            game["player1"]["id"] != user.id
            and not game["player2"]
        ):

            game["player2"] = {
                "id": user.id,
                "name": user.first_name,
            }

            await query.answer(
                "✅ You are Player 2!"
            )

        # ----------------------------------------------------
        # ALREADY JOINED
        # ----------------------------------------------------

        elif (
            game["player1"]["id"] == user.id
            or (
                game["player2"]
                and game["player2"]["id"] == user.id
            )
        ):

            await query.answer(
                "You're already in this game."
            )

        else:

            await query.answer(
                "❌ This game already has two players.",
                show_alert=True,
            )

            return

        # ----------------------------------------------------
        # BOTH PLAYERS READY
        # ----------------------------------------------------

        if game["player1"] and game["player2"]:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔥 START GAME",
                        callback_data=f"start:{code}",
                    )
                ]
            ])

            text = (
                "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                f"👤 Player 1: "
                f"{player_name(game, 'player1')}\n"
                f"👤 Player 2: "
                f"{player_name(game, 'player2')}\n\n"
                "✅ Both players joined!\n\n"
                "Press START GAME."
            )

        else:

            text = (
                "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                f"👤 Player 1: "
                f"{player_name(game, 'player1')}\n"
                f"👤 Player 2: "
                f"{player_name(game, 'player2')}\n\n"
                "Waiting for another player..."
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

        # ----------------------------------------------------
        # LOCK GAME
        # ----------------------------------------------------

        game["active"] = True

        game["round"] = 0

        # ----------------------------------------------------
        # PLAYER 1 ALWAYS STARTS
        # ----------------------------------------------------

        game["turn"] = "player1"

        first_player = player_name(
            game,
            "player1",
        )

        text = (
            "🔥 GAME STARTED! 🔥\n\n"
            f"🎯 {first_player}'S TURN\n\n"
            "Choose your challenge:"
        )

        keyboard = challenge_buttons(code)

        await query.answer(
            "🔥 Player 1 starts!"
        )

        if query.inline_message_id:

            await context.bot.edit_message_text(
                inline_message_id=query.inline_message_id,
                text=text,
                reply_markup=keyboard,
            )

        return


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
        InlineQueryHandler(inline_query)
    )

    app.add_handler(
        CallbackQueryHandler(callback)
    )

    print(
        "🔥 NAUGHTYDARE BOT RUNNING 🔥"
    )

    app.run_polling()


if __name__ == "__main__":
    main()
