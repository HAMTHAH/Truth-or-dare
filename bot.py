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
    "Send your best pickup line.",
    "Give the other player a cute nickname.",
    "Send three flirty emojis.",
    "Write a romantic compliment.",
    "Send a voice message saying 'You're dangerous.'",
    "Describe your perfect date in three words.",
    "Tell the other player their most attractive quality.",
    "Send a mysterious message.",
    "Write a two-line romantic poem.",
    "Pretend you're asking the other player on a first date.",
    "Send your smoothest compliment.",
    "Describe your dream date using emojis.",
    "Send a dramatic 'I miss you' message.",
    "Give a compliment without saying beautiful or handsome.",
    "Write a message you'd normally be too shy to send.",
    "Pretend you're jealous and explain why.",
    "Send five different heart emojis.",
    "Tell the other player what you noticed first.",
    "Write a fake love confession.",
    "Send a voice message saying something sweet.",
    "Describe your ideal romantic evening.",
    "Give your best romantic one-liner.",
    "Write a three-word confession.",
    "Describe the other player like a movie character.",
    "Pretend you're trying to impress them at a party.",
    "Give them a compliment using exactly five words.",
    "Write the beginning of a romance movie.",
    "Tell them one thing you would do on a perfect date.",
    "Start a message with 'Don't get used to this, but...'",
    "Give the other player a playful challenge.",
    "Send a romantic emoji combination.",
    "Tell them something you find attractive.",
    "Pretend you're meeting them for the first time and flirt.",
    "Write a fake proposal.",
    "Give them a cute nickname.",
    "Say 'I think you're trouble' in a voice message.",
    "Describe your dream relationship.",
    "Send a message that would make someone blush.",
    "Tell them your first impression of them.",
    "Write a dramatic fake breakup message.",
    "Give the other player your smoothest compliment.",
    "Pretend you're their secret admirer.",
    "Describe your perfect partner in five words.",
    "Send a playful confession.",
    "Tell them what makes someone irresistible.",
    "Write a romantic text without using the word love.",
    "Rate their flirting from 1 to 10.",
    "Pretend you're trying to win them over.",
    "End your message with '...and that's why you're dangerous.'",
]

games = {}


def create_game():
    code = secrets.token_hex(5)

    games[code] = {
        "girl": None,
        "boy": None,
        "active": False,
        "turn": None,
        "round": 0,
    }

    print("GAME CREATED:", code)
    return code


def role_keyboard(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👩 GIRL",
                callback_data=f"role:g:{code}"
            ),
            InlineKeyboardButton(
                "👨 BOY",
                callback_data=f"role:b:{code}"
            ),
        ]
    ])


def start_game_keyboard(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 START GAME",
                callback_data=f"begin:{code}"
            )
        ]
    ])


def challenge_keyboard(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "😈 TRUTH",
                callback_data=f"truth:{code}"
            ),
            InlineKeyboardButton(
                "🔥 DARE",
                callback_data=f"dare:{code}"
            ),
        ],
        [
            InlineKeyboardButton(
                "🎲 RANDOM",
                callback_data=f"random:{code}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 NEXT",
                callback_data=f"next:{code}"
            ),
            InlineKeyboardButton(
                "✅ DONE",
                callback_data=f"done:{code}"
            ),
        ],
    ])


async def send_to_players(context, game, text, keyboard=None):
    for role in ("girl", "boy"):
        player = game.get(role)

        if player:
            try:
                await context.bot.send_message(
                    chat_id=player["chat_id"],
                    text=text,
                    reply_markup=keyboard,
                )
            except Exception as error:
                print("SEND ERROR:", error)


async def send_challenge(context, code, challenge_type="random"):
    game = games.get(code)

    if not game:
        return

    if not game["girl"] or not game["boy"]:
        return

    # Alternate turns
    if game["turn"] == "girl":
        game["turn"] = "boy"
    else:
        game["turn"] = "girl"

    game["round"] += 1

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

    if game["turn"] == "girl":
        player_name = game["girl"]["name"]
        role_name = "👩 GIRL"
    else:
        player_name = game["boy"]["name"]
        role_name = "👨 BOY"

    text = (
        f"🔥 ROUND {game['round']} 🔥\n\n"
        f"🎯 TURN: {role_name}\n"
        f"👤 {player_name}\n\n"
        f"{title}\n\n"
        f"{challenge}"
    )

    await send_to_players(
        context,
        game,
        text,
        challenge_keyboard(code),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if context.args:
        code = context.args[0]

        print("JOIN REQUEST:", code)

        game = games.get(code)

        if not game:
            await update.message.reply_text(
                "❌ Game not found or expired.\n\n"
                "Please create a new game."
            )
            return

        await update.message.reply_text(
            "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
            "Choose your role:",
            reply_markup=role_keyboard(code),
        )

        return

    await update.message.reply_text(
        "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
        "Use @NAUGHTYDARE_bot in a chat to start a 1-on-1 game."
    )


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline = update.inline_query

    print("INLINE QUERY:", inline.query)

    code = create_game()

    bot_username = context.bot.username

    results = [
        InlineQueryResultArticle(
            id=f"start_{code}",
            title="🎮 START 1-ON-1 GAME",
            description="Start a private game with another person",
            input_message_content=InputTextMessageContent(
                "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                "🎮 1-on-1 game created!\n"
                "Tap OPEN GAME to join."
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🎮 OPEN GAME",
                        url=f"https://t.me/{bot_username}?start={code}",
                    )
                ]
            ]),
        )
    ]

    # Normal Truth results
    for i in range(5):
        truth = random.choice(TRUTHS)

        results.append(
            InlineQueryResultArticle(
                id=f"truth_{code}_{i}",
                title="😈 TRUTH",
                description=truth,
                input_message_content=InputTextMessageContent(
                    f"😈 TRUTH\n\n{truth}"
                ),
            )
        )

    # Normal Dare results
    for i in range(5):
        dare = random.choice(DARES)

        results.append(
            InlineQueryResultArticle(
                id=f"dare_{code}_{i}",
                title="🔥 DARE",
                description=dare,
                input_message_content=InputTextMessageContent(
                    f"🔥 DARE\n\n{dare}"
                ),
            )
        )

    await inline.answer(
        results=results,
        cache_time=0,
        is_personal=True,
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    data = query.data
    parts = data.split(":")

    action = parts[0]
    code = parts[-1]

    print("BUTTON:", data)

    game = games.get(code)

    if not game:
        await query.answer(
            "❌ Game expired.",
            show_alert=True,
        )
        return

    user = query.from_user
    chat_id = update.effective_chat.id

    # -------------------------
    # ROLE SELECTION
    # -------------------------

    if action == "role":

        role_code = parts[1]

        role = "girl" if role_code == "g" else "boy"

        # Check if this user already joined
        for existing_role in ("girl", "boy"):
            existing = game.get(existing_role)

            if existing and existing["user_id"] == user.id:
                await query.answer(
                    "You already joined this game.",
                    show_alert=True,
                )
                return

        # Check if role already taken
        if game[role]:
            await query.answer(
                "That role is already taken.",
                show_alert=True,
            )
            return

        game[role] = {
            "user_id": user.id,
            "name": user.first_name,
            "chat_id": chat_id,
        }

        await query.message.reply_text(
            "✅ You joined successfully!"
        )

        print(
            "PLAYER JOINED:",
            role,
            user.first_name,
            code,
        )

        # Both players are ready
        if game["girl"] and game["boy"]:

            await send_to_players(
                context,
                game,
                "🔥 BOTH PLAYERS ARE READY! 🔥\n\n"
                f"👩 Girl: {game['girl']['name']}\n"
                f"👨 Boy: {game['boy']['name']}\n\n"
                "Press START GAME when you're ready.",
                start_game_keyboard(code),
            )

        else:

            bot_username = context.bot.username

            link = (
                f"https://t.me/{bot_username}"
                f"?start={code}"
            )

            await query.message.reply_text(
                "⏳ Waiting for the other player.\n\n"
                "Send this link to them:\n\n"
                f"{link}"
            )

        return

    # -------------------------
    # START GAME
    # -------------------------

    if action == "begin":

        if not game["girl"] or not game["boy"]:
            await query.answer(
                "Both players must join first.",
                show_alert=True,
            )
            return

        game["active"] = True
        game["turn"] = None
        game["round"] = 0

        await send_to_players(
            context,
            game,
            "🔥 GAME STARTED! 🔥\n\n"
            "👩 GIRL vs 👨 BOY\n\n"
            "Let the chaos begin. 😈",
        )

        await send_challenge(
            context,
            code,
            "random",
        )

        return

    # -------------------------
    # TRUTH / DARE / RANDOM
    # -------------------------

    if action in ("truth", "dare", "random"):

        if not game["active"]:
            await query.answer(
                "Start the game first.",
                show_alert=True,
            )
            return

        await send_challenge(
            context,
            code,
            action,
        )

        return

    # -------------------------
    # NEXT
    # -------------------------

    if action == "next":

        if not game["active"]:
            return

        await send_challenge(
            context,
            code,
            "random",
        )

        return

    # -------------------------
    # DONE
    # -------------------------

    if action == "done":

        await query.message.reply_text(
            "✅ Challenge completed!\n\n"
            "Ready for the next one?",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔥 NEXT",
                        callback_data=f"next:{code}",
                    )
                ]
            ]),
        )


def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button)
    )

    app.add_handler(
        InlineQueryHandler(inline_query)
    )

    print("🔥 NAUGHTYDARE BOT IS RUNNING 🔥")

    app.run_polling()


if __name__ == "__main__":
    main()
