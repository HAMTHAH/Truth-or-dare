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


def create_game(user_id):
    code = secrets.token_hex(5)

    games[code] = {
        "creator": user_id,
        "girl": None,
        "boy": None,
        "active": False,
        "turn": None,
        "round": 0,
    }

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


def start_keyboard(code):
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
    for role in ["girl", "boy"]:
        player = game.get(role)

        if player:
            try:
                await context.bot.send_message(
                    chat_id=player["chat_id"],
                    text=text,
                    reply_markup=keyboard,
                )
            except Exception as error:
                print("Message error:", error)


async def send_challenge(context, code, challenge_type="random"):
    game = games.get(code)

    if not game:
        return

    if not game["girl"] or not game["boy"]:
        return

    if game["turn"] == "girl":
        game["turn"] = "boy"
    elif game["turn"] == "boy":
        game["turn"] = "girl"
    else:
        game["turn"] = random.choice(["girl", "boy"])

    game["round"] += 1

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

    if game["turn"] == "girl":
        player = "👩 GIRL"
    else:
        player = "👨 BOY"

    text = (
        f"🔥 ROUND {game['round']}\n\n"
        f"🎯 TURN: {player}\n\n"
        f"{title}\n\n"
        f"{question}"
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
        game = games.get(code)

        if not game:
            await update.message.reply_text(
                "❌ Game not found or expired."
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
        "Type @NAUGHTYDARE_bot in a chat to start."
    )


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query
    code = secrets.token_hex(5)

    results = [
        InlineQueryResultArticle(
            id="start_game",
            title="🎮 START 1-ON-1 GAME",
            description="Play Truth or Dare with another person",
            input_message_content=InputTextMessageContent(
                "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                "Tap OPEN GAME to start your 1-on-1 game!"
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🎮 OPEN GAME",
                        url=f"https://t.me/NAUGHTYDARE_bot?start={code}"
                    )
                ]
            ])
        )
    ]

    # Add the normal Truth/Dare results underneath
    for i in range(5):
        truth = random.choice(TRUTHS)

        results.append(
            InlineQueryResultArticle(
                id=f"truth_{i}_{secrets.token_hex(4)}",
                title="😈 TRUTH",
                description=truth,
                input_message_content=InputTextMessageContent(
                    f"😈 TRUTH\n\n{truth}"
                )
            )
        )

    await query.answer(
        results=results,
        cache_time=0,
        is_personal=True
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split(":")
    action = parts[0]
    code = parts[-1]

    game = games.get(code)

    if not game:
        await query.message.reply_text(
            "❌ Game expired."
        )
        return

    user = query.from_user

    if action == "role":
        role = parts[1]

        if game[role]:
            await query.answer(
                "That role is already taken.",
                show_alert=True,
            )
            return

        if (
            game["girl"]
            and game["girl"]["user_id"] == user.id
        ):
            await query.answer(
                "You already joined this game.",
                show_alert=True,
            )
            return

        if (
            game["boy"]
            and game["boy"]["user_id"] == user.id
        ):
            await query.answer(
                "You already joined this game.",
                show_alert=True,
            )
            return

        game[role] = {
            "user_id": user.id,
            "name": user.first_name,
            "chat_id": update.effective_chat.id,
        }

        await query.message.reply_text(
            "✅ You joined successfully!"
        )

        if game["girl"] and game["boy"]:
            text = (
                "🔥 BOTH PLAYERS ARE READY!\n\n"
                f"👩 Girl: {game['girl']['name']}\n"
                f"👨 Boy: {game['boy']['name']}\n\n"
                "Ready to play?"
            )

            await send_to_players(
                context,
                game,
                text,
                start_keyboard(code),
            )

        else:
            bot_name = context.bot.username
            link = f"https://t.me/{bot_name}?start={code}"

            await query.message.reply_text(
                "⏳ Waiting for the other player.\n\n"
                "Send them this link:\n\n"
                f"{link}"
            )

        return

    if action == "begin":
        if not game["girl"] or not game["boy"]:
            await query.answer(
                "Both players must join first.",
                show_alert=True,
            )
            return

        game["active"] = True

        await send_to_players(
            context,
            game,
            "🔥 GAME STARTED! 🔥\n\n"
            "👩 Girl vs 👨 Boy",
        )

        await send_challenge(
            context,
            code,
            "random",
        )

        return

    if action in ["truth", "dare", "random"]:
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

    if action == "next":
        if game["active"]:
            await send_challenge(
                context,
                code,
                "random",
            )
        return

    if action == "done":
        await query.message.reply_text(
            "✅ Challenge completed!\n\n"
            "Ready for another one?",
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

    print("NAUGHTYDARE BOT IS RUNNING")

    app.run_polling()


if __name__ == "__main__":
    main()
