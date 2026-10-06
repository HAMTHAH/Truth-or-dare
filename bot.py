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
    "Who was your last crush?",
    "What is your biggest red flag?",
    "What is your biggest green flag?",
    "Have you ever had a crush on a friend?",
    "Have you ever flirted just for attention?",
    "What instantly makes someone attractive to you?",
    "What is your biggest dating turn-off?",
    "Have you ever pretended not to like someone you actually liked?",
    "What's the boldest move you've made on someone?",
    "Have you ever stalked someone's social media?",
    "What is your guilty pleasure?",
    "Have you ever fallen for a friend?",
    "What is the cutest thing someone has done for you?",
    "What's the worst pickup line you've heard?",
    "What personality trait attracts you most?",
    "What do you find irresistible?",
    "What's your biggest dating insecurity?",
    "Have you ever liked two people at once?",
    "What's your ideal first date?",
    "Have you ever caught feelings unexpectedly?",
    "How long was your longest crush?",
    "Would you date someone completely different from your usual type?",
    "What would you never tolerate in a relationship?",
    "What's your favorite compliment?",
    "Have you ever hoped someone would make the first move?",
    "What's the most attractive thing someone can wear?",
    "Would you rather make the first move or be approached?",
    "What's your weakness when someone flirts with you?",
    "What's your favorite kind of attention?",
    "What makes you instantly lose interest?",
    "Have you ever practiced what to say before talking to a crush?",
    "What's the most romantic thing you'd actually do?",
    "Would you date someone you met online?",
    "What's your biggest relationship fear?",
    "What makes you feel special?",
    "Have you ever flirted through texting for hours?",
    "What is perfect chemistry to you?",
    "Would you rather have a secret admirer or openly flirt?",
    "What's one question you've wanted to ask your crush?",
    "Who would you choose for a date?",
    "What's the first thing you notice about someone?",
    "What makes someone unforgettable?",
    "What's something you've never admitted to a crush?",
    "What is your biggest weakness in dating?",
    "What makes someone instantly attractive?",
    "Have you ever hidden your feelings?",
    "Would you make the first move?",
    "What is your ideal romantic evening?",
    "What is one secret you would tell a crush?",
]

DARES = [
    "Send a voice note saying your smoothest pickup line.",
    "Give the other player a dangerously cute nickname.",
    "Send three emojis that describe your attraction to them.",
    "Write a compliment that would instantly make them blush.",
    "Send a voice note saying, 'You're seriously distracting me.'",
    "Describe your perfect date in exactly five words.",
    "Tell the other player the first thing you noticed about them.",
    "Send a mysterious message that makes them curious about you.",
    "Write a two-line romantic poem about them.",
    "Pretend you're asking them on a first date.",
    "Send your smoothest compliment without using the word 'beautiful.'",
    "Describe your dream date entirely with emojis.",
    "Send a dramatic 'I miss you' message.",
    "Write a message you'd normally be too shy to send.",
    "Pretend you're jealous and explain why.",
    "Send five different heart emojis and explain your favorite one.",
    "Tell them one thing about them that you find irresistible.",
    "Write a fake romantic confession.",
    "Send a voice note saying something sweet in your best romantic voice.",
    "Describe your ideal romantic evening together.",
    "Give your best romantic one-liner.",
    "Write a three-word confession.",
    "Describe the other player as if they're the main character in a romance movie.",
    "Pretend you're trying to impress them at a party.",
    "Give them a compliment using exactly five words.",
    "Write the opening scene of a romance movie starring both of you.",
    "Tell them one thing you'd want to do together on a perfect date.",
    "Start a message with: 'Don't get used to this, but...'",
    "Give the other player a playful challenge.",
    "Send a combination of three emojis that secretly describes your mood.",
    "Tell them something about their personality that you find attractive.",
    "Pretend you're meeting them for the first time and flirt with them.",
    "Write a fake proposal in one sentence.",
    "Give them a nickname that only you would use.",
    "Send a voice note saying, 'I think you're trouble.'",
    "Describe your dream relationship in three sentences.",
    "Send a message designed specifically to make them blush.",
    "Tell them your first impression of them.",
    "Write a dramatic fake breakup message, then end it with 'Just kidding.'",
    "Give the other player your smoothest compliment.",
    "Pretend you're their secret admirer and leave them a mysterious message.",
    "Describe your perfect partner in exactly five words.",
    "Send a playful confession beginning with 'Okay, I'll admit it...'",
    "Tell them what quality makes someone irresistible to you.",
    "Write a romantic text without using the words 'love' or 'like.'",
    "Rate their flirting from 1 to 10 and explain your score.",
    "Pretend you're trying to win them over in 30 seconds.",
    "Send a voice note saying their name in your most dramatic voice.",
    "Finish this sentence: 'If we went on a date tonight, I would...'",
    "End your next message with: '...and that's why you're dangerous.'",
]

# ============================================================
# GAME STORAGE
# ============================================================

games = {}


def create_game():
    code = secrets.token_hex(5)

    games[code] = {
        "girl": None,
        "boy": None,
        "inline_message_id": None,
        "active": False,
        "turn_role": None,
        "turn_user_id": None,
        "round": 0,
        "current_type": None,
        "current_challenge": None,
    }

    print("GAME CREATED:", code)
    return code


# ============================================================
# INLINE MESSAGE EDITOR
# ============================================================

async def edit_game(context, game, text, keyboard=None):
    inline_id = game.get("inline_message_id")

    if not inline_id:
        print("NO INLINE MESSAGE ID")
        return

    try:
        await context.bot.edit_message_text(
            inline_message_id=inline_id,
            text=text,
            reply_markup=keyboard,
        )
    except Exception as error:
        print("EDIT ERROR:", error)


# ============================================================
# LOBBY
# ============================================================

def lobby_keyboard(code, game):
    girl_text = (
        "👩 GIRL — TAKEN"
        if game["girl"]
        else "👩 GIRL"
    )

    boy_text = (
        "👨 BOY — TAKEN"
        if game["boy"]
        else "👨 BOY"
    )

    buttons = []

    if game["girl"]:
        buttons.append(
            InlineKeyboardButton(
                girl_text,
                callback_data=f"taken:{code}",
            )
        )
    else:
        buttons.append(
            InlineKeyboardButton(
                girl_text,
                callback_data=f"role:g:{code}",
            )
        )

    if game["boy"]:
        buttons.append(
            InlineKeyboardButton(
                boy_text,
                callback_data=f"role:b:{code}",
            )
        )
    else:
        buttons.append(
            InlineKeyboardButton(
                boy_text,
                callback_data=f"role:b:{code}",
            )
        )

    keyboard = [buttons]

    if game["girl"] and game["boy"]:
        keyboard.append([
            InlineKeyboardButton(
                "🎮 START GAME",
                callback_data=f"begin:{code}",
            )
        ])

    return InlineKeyboardMarkup(keyboard)


def lobby_text(game):
    girl = (
        f"👩 Girl: {game['girl']['name']}"
        if game["girl"]
        else "👩 Girl: Waiting..."
    )

    boy = (
        f"👨 Boy: {game['boy']['name']}"
        if game["boy"]
        else "👨 Boy: Waiting..."
    )

    return (
        "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
        f"{girl}\n"
        f"{boy}\n\n"
        "Choose your role:"
    )


# ============================================================
# GAME BUTTONS
# ============================================================

def challenge_keyboard(code, game):
    buttons = []

    # ANSWER button
    if game["current_type"] == "truth":
        buttons.append([
            InlineKeyboardButton(
                "✍️ ANSWER",
                switch_inline_query_current_chat=f"answer|{code}|",
            )
        ])

    elif game["current_type"] == "dare":
        buttons.append([
            InlineKeyboardButton(
                "✅ DONE",
                callback_data=f"done:{code}",
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            "😈 TRUTH",
            callback_data=f"truth:{code}",
        ),
        InlineKeyboardButton(
            "🔥 DARE",
            callback_data=f"dare:{code}",
        ),
    ])

    buttons.append([
        InlineKeyboardButton(
            "🎲 RANDOM",
            callback_data=f"random:{code}",
        )
    ])

    return InlineKeyboardMarkup(buttons)


# ============================================================
# CHALLENGE GENERATOR
# ============================================================

async def show_challenge(context, code, challenge_type):
    game = games.get(code)

    if not game:
        return

    if not game["girl"] or not game["boy"]:
        return

    # First challenge chooses a random player.
    if game["turn_role"] is None:
        game["turn_role"] = random.choice(["girl", "boy"])

    if challenge_type == "truth":
        challenge = random.choice(TRUTHS)
        title = "😈 TRUTH"
        current_type = "truth"

    elif challenge_type == "dare":
        challenge = random.choice(DARES)
        title = "🔥 DARE"
        current_type = "dare"

    else:
        if random.choice([True, False]):
            challenge = random.choice(TRUTHS)
            title = "😈 TRUTH"
            current_type = "truth"
        else:
            challenge = random.choice(DARES)
            title = "🔥 DARE"
            current_type = "dare"

    game["round"] += 1
    game["current_type"] = current_type
    game["current_challenge"] = challenge

    player = game[game["turn_role"]]

    role_name = (
        "👩 GIRL"
        if game["turn_role"] == "girl"
        else "👨 BOY"
    )

    text = (
        f"🔥 ROUND {game['round']} 🔥\n\n"
        f"🎯 TURN: {role_name}\n"
        f"👤 {player['name']}\n\n"
        f"{title}\n\n"
        f"{challenge}"
    )

    await edit_game(
        context,
        game,
        text,
        challenge_keyboard(code, game),
    )


# ============================================================
# INLINE QUERY
# ============================================================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline = update.inline_query
    query_text = inline.query.strip()

    print("INLINE QUERY:", query_text)

    # --------------------------------------------------------
    # ANSWER MODE
    #
    # Button inserts:
    # @NAUGHTYDARE_bot answer|GAMECODE|
    #
    # User then types:
    # @NAUGHTYDARE_bot answer|GAMECODE|My answer
    #
    # The bot returns a result which the player taps to send.
    # --------------------------------------------------------

    if query_text.startswith("answer|"):
        parts = query_text.split("|", 2)

        if len(parts) < 3:
            await inline.answer(
                results=[],
                cache_time=0,
            )
            return

        code = parts[1]
        answer = parts[2].strip()

        game = games.get(code)

        if not game or not game["active"]:
            await inline.answer(
                results=[],
                cache_time=0,
            )
            return

        user = inline.from_user

        # Only the player whose turn it is can answer.
        if user.id != game["turn_user_id"]:
            result = InlineQueryResultArticle(
                id=f"wrong_{code}_{user.id}",
                title="⛔ NOT YOUR TURN",
                description="Wait for your turn.",
                input_message_content=InputTextMessageContent(
                    "⛔ It's not your turn yet."
                ),
            )

            await inline.answer(
                results=[result],
                cache_time=0,
                is_personal=True,
            )
            return

        if not answer:
            result = InlineQueryResultArticle(
                id=f"empty_{code}_{user.id}",
                title="✍️ TYPE YOUR ANSWER",
                description="Type your answer after the bot username.",
                input_message_content=InputTextMessageContent(
                    "✍️ Please type an answer first."
                ),
            )

            await inline.answer(
                results=[result],
                cache_time=0,
                is_personal=True,
            )
            return

        # Limit extremely long answers.
        answer = answer[:1000]

        result = InlineQueryResultArticle(
            id=f"answer_{code}_{user.id}_{secrets.token_hex(3)}",
            title="📨 SEND YOUR ANSWER",
            description=answer[:100],
            input_message_content=InputTextMessageContent(
                f"📝 {user.first_name}'s answer:\n\n{answer}"
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "➡️ CONTINUE",
                        callback_data=f"submitted:{code}",
                    )
                ]
            ]),
        )

        await inline.answer(
            results=[result],
            cache_time=0,
            is_personal=True,
        )

        return

    # --------------------------------------------------------
    # NORMAL GAME CREATION
    # --------------------------------------------------------

    code = create_game()

    game = games[code]

    start_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👩 GIRL",
                callback_data=f"role:g:{code}",
            ),
            InlineKeyboardButton(
                "👨 BOY",
                callback_data=f"role:b:{code}",
            ),
        ]
    ])

    start_result = InlineQueryResultArticle(
        id=f"game_{code}",
        title="🎮 START 1-ON-1 GAME",
        description="Play directly inside this private chat",
        input_message_content=InputTextMessageContent(
            lobby_text(game)
        ),
        reply_markup=start_keyboard,
    )

    await inline.answer(
        results=[start_result],
        cache_time=0,
        is_personal=False,
    )


# ============================================================
# CALLBACK BUTTONS
# ============================================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    data = query.data
    parts = data.split(":")

    action = parts[0]
    code = parts[-1]

    game = games.get(code)

    print("BUTTON:", data)

    if not game:
        await query.answer(
            "❌ Game expired.",
            show_alert=True,
        )
        return

    user = query.from_user

    # Save inline message ID the first time somebody presses
    # a button on the game.
    if query.inline_message_id:
        game["inline_message_id"] = query.inline_message_id

    # --------------------------------------------------------
    # TAKEN ROLE
    # --------------------------------------------------------

    if action == "taken":
        await query.answer(
            "❌ That role is already taken.",
            show_alert=True,
        )
        return

    # --------------------------------------------------------
    # ROLE
    # --------------------------------------------------------

    if action == "role":
        role_code = parts[1]

        role = (
            "girl"
            if role_code == "g"
            else "boy"
        )

        # Prevent same person taking both roles.
        for existing_role in ("girl", "boy"):
            existing = game.get(existing_role)

            if existing and existing["user_id"] == user.id:
                await query.answer(
                    "You already joined this game.",
                    show_alert=True,
                )
                return

        # Role already taken.
        if game[role]:
            await query.answer(
                "❌ That role is already taken.",
                show_alert=True,
            )
            return

        game[role] = {
            "user_id": user.id,
            "name": user.first_name,
        }

        print(
            "PLAYER JOINED:",
            role,
            user.first_name,
            code,
        )

        if game["girl"] and game["boy"]:

            await edit_game(
                context,
                game,
                (
                    "🔥 BOTH PLAYERS ARE READY! 🔥\n\n"
                    f"👩 Girl: {game['girl']['name']}\n"
                    f"👨 Boy: {game['boy']['name']}\n\n"
                    "Ready to start?"
                ),
                InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "🎮 START GAME",
                            callback_data=f"begin:{code}",
                        )
                    ]
                ]),
            )

        else:

            await edit_game(
                context,
                game,
                lobby_text(game),
                lobby_keyboard(code, game),
            )

        return

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    if action == "begin":

        if not game["girl"] or not game["boy"]:
            await query.answer(
                "Both players must join first.",
                show_alert=True,
            )
            return

        game["active"] = True
        game["round"] = 0

        # Randomly choose who goes first.
        game["turn_role"] = random.choice(
            ["girl", "boy"]
        )

        game["turn_user_id"] = game[
            game["turn_role"]
        ]["user_id"]

        await show_challenge(
            context,
            code,
            "random",
        )

        return

    # --------------------------------------------------------
    # TRUTH / DARE / RANDOM
    # --------------------------------------------------------

    if action in ("truth", "dare", "random"):

        if not game["active"]:
            await query.answer(
                "Start the game first.",
                show_alert=True,
            )
            return

        # Only current player can choose.
        if user.id != game["turn_user_id"]:
            await query.answer(
                "⏳ It's not your turn.",
                show_alert=True,
            )
            return

        await show_challenge(
            context,
            code,
            action,
        )

        return

    # --------------------------------------------------------
    # ANSWER SUBMITTED
    # --------------------------------------------------------

    if action == "submitted":

        if not game["active"]:
            return

        if user.id != game["turn_user_id"]:
            await query.answer(
                "⛔ That's not your answer button.",
                show_alert=True,
            )
            return

        # After answering, let the current player move on.
        await edit_game(
            context,
            game,
            (
                f"✅ {user.first_name} answered!\n\n"
                "Ready for the next turn?"
            ),
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "➡️ NEXT TURN",
                        callback_data=f"next:{code}",
                    )
                ]
            ]),
        )

        return

    # --------------------------------------------------------
    # DONE DARE
    # --------------------------------------------------------

    if action == "done":

        if not game["active"]:
            return

        if user.id != game["turn_user_id"]:
            await query.answer(
                "⏳ It's not your turn.",
                show_alert=True,
            )
            return

        await edit_game(
            context,
            game,
            (
                f"✅ {user.first_name} completed the dare!\n\n"
                "Ready for the next turn?"
            ),
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "➡️ NEXT TURN",
                        callback_data=f"next:{code}",
                    )
                ]
            ]),
        )

        return

    # --------------------------------------------------------
    # NEXT TURN
    # --------------------------------------------------------

    if action == "next":

        if not game["active"]:
            return

        if user.id != game["turn_user_id"]:
            await query.answer(
                "⏳ The current player must press NEXT.",
                show_alert=True,
            )
            return

        # Switch player.
        if game["turn_role"] == "girl":
            game["turn_role"] = "boy"
        else:
            game["turn_role"] = "girl"

        game["turn_user_id"] = game[
            game["turn_role"]
        ]["user_id"]

        await show_challenge(
            context,
            code,
            "random",
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
        CallbackQueryHandler(button)
    )

    print(
        "🔥 NAUGHTYDARE INLINE GAME IS RUNNING 🔥"
    )

    app.run_polling()


if __name__ == "__main__":
    main()
