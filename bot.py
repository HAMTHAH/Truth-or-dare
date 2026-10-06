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
    "What is the first thing you would do if I walked through your door right now?",
    "What is the most intense dream you've ever had about me?",
    "Have you ever gotten distracted while we were texting or calling?",
    "What is your favorite physical feature of mine?",
    "If I told you I was outside your house right now, how would you get ready to meet me?",
    "What's the dirtiest thought you've had about me today?",
    "What's a secret fantasy you've never told anyone?",
    "Do you prefer spicy photos or flirty voice notes?",
    "What's the most adventurous thing you've ever done in public?",
    "If we were stuck in an elevator for 20 minutes, what would you want to happen?",
    "What's the most intense attraction you've ever felt toward someone?",
    "What's your favorite romantic accessory or outfit?",
    "Describe exactly how it feels when someone kisses your neck.",
    "What's the most daring romantic thing you've ever wanted to try?",
    "Have you ever imagined someone you liked while watching a romantic scene?",
    "What part of your personality gets the most attention from someone you like?",
    "What's the most distracting thought you've had about me?",
    "Do you prefer being in control or letting the other person take the lead?",
    "What's your favorite outfit for a date?",
    "What's the fastest someone has ever made you blush through text?",
    "If you could choose one outfit for me to wear, what would it be?",
    "What word or phrase instantly makes you blush?",
    "Have you ever taken a flirty photo and been too shy to send it?",
    "What's your favorite kind of romantic chemistry?",
    "Do you prefer playful flirting or serious romantic talk?",
    "What's the most embarrassing thing you've done while flirting?",
    "If we had 24 hours together with no phones, what would we do?",
    "When did you first realize you were attracted to me?",
    "Do you prefer slow and romantic or spontaneous and playful?",
    "What's your guilty pleasure when it comes to romance?",
    "What's the sexiest compliment you've ever received?",
    "What's the riskiest place you've ever flirted with someone?",
    "What is one thing I do that makes you lose your composure?",
    "What's the most daring thing you've ever done for a dare?",
    "What's the best way for someone to wake you up on a date trip?",
    "What kind of romantic roleplay would you find fun?",
    "If I gave you 10 minutes to impress me, what would you do?",
    "What's a physical sensation you really enjoy?",
    "Do you prefer gentle affection or intense flirting?",
    "What's the first thing you would do when we meet again?",
    "On a scale of 1–10, how much do you want to see me right now?",
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
