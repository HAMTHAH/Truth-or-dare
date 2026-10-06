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

# =========================================================
# QUESTIONS
# =========================================================

TRUTHS = [
    "Who was your last crush?",
    "Have you ever had a crush on a friend?",
    "What is your biggest red flag?",
    "What is your biggest green flag?",
    "Have you ever flirted just to get attention?",
    "Who was your first serious crush?",
    "What instantly makes someone attractive to you?",
    "What is your biggest dating turn-off?",
    "Have you ever pretended not to like someone you actually liked?",
    "What's the boldest move you've made on someone?",
    "Have you ever stalked someone's social media?",
    "What is your guilty pleasure?",
    "Have you ever fallen for a friend?",
    "What is the cutest thing someone has done for you?",
    "What's the worst pickup line you've heard?",
    "Have you ever lied about being busy to avoid someone?",
    "What personality trait attracts you most?",
    "What do you find irresistible?",
    "Have you ever sent a message and regretted it?",
    "What's your biggest dating insecurity?",
    "Have you ever liked two people at once?",
    "What's your ideal first date?",
    "Have you ever caught feelings unexpectedly?",
    "How long was your longest crush?",
    "Would you date someone completely different from your usual type?",
    "What would you never tolerate in a relationship?",
    "Have you ever flirted with someone you just met?",
    "What's your favorite compliment?",
    "Have you ever hoped someone would make the first move?",
    "What's the most attractive thing someone can wear?",
    "Would you rather make the first move or be approached?",
    "Have you ever liked someone who was unavailable?",
    "What's your weakness when someone flirts with you?",
    "Have you ever ignored someone's message on purpose?",
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
    "Who would you choose for a date if you had to choose?",
    "What is your biggest weakness in dating?",
    "What's the first thing you notice about someone?",
    "What makes someone unforgettable?",
    "What's something you've never admitted to a crush?",
]

DARES = [
    "Send the other player your best pickup line.",
    "Give the other player a cute nickname.",
    "Send three flirty emojis.",
    "Write a ridiculously romantic compliment.",
    "Send a voice message saying 'You're dangerous.'",
    "Describe your perfect date in three words.",
    "Tell the other player their most attractive quality.",
    "Send a mysterious message that makes them curious.",
    "Write a two-line romantic poem.",
    "Pretend you're asking the other player on a first date.",
    "Send your smoothest compliment.",
    "Describe your dream date using only emojis.",
    "Send a dramatic 'I miss you' message.",
    "Give the other player a compliment without saying beautiful or handsome.",
    "Write a message you'd normally be too shy to send.",
    "Pretend you're jealous and explain why.",
    "Send five different heart emojis.",
    "Tell the other player what you noticed first.",
    "Write a fake love confession.",
    "Send a voice message saying something sweet.",
    "Describe your ideal romantic evening.",
    "Give the other player your best one-liner.",
    "Write a three-word confession.",
    "Describe the other player like a movie character.",
    "Pretend you're trying to impress them at a party.",
    "Give them a compliment using exactly five words.",
    "Write the beginning of a romance movie.",
    "Tell them one thing you would do on a perfect date.",
    "Send a message beginning with 'Don't get used to this, but...'",
    "Give the other player a playful challenge.",
    "Send a romantic emoji combination.",
    "Tell them something you find attractive.",
    "Pretend you're meeting them for the first time and flirt.",
    "Write a cheesy proposal.",
    "Give them a cute nickname and use it for the next round.",
    "Say 'I think you're trouble' in a voice message.",
    "Describe your dream relationship.",
    "Send a message that would make someone blush.",
    "Tell them your first impression of them.",
    "Write a fake dramatic breakup message.",
    "Give the other player your smoothest compliment.",
    "Pretend you're their secret admirer.",
    "Describe your perfect partner in five words.",
    "Send a playful 'I have a confession...' message.",
    "Tell them what makes someone irresistible.",
    "Write a romantic text without using the word love.",
    "Give the other player a rating out of 10 for their flirting.",
    "Send a message ending with '...and that's why you're dangerous.'",
    "Create a new nickname for the other player.",
]

# =========================================================
# GAME STORAGE
# =========================================================

games = {}


def create_game(creator_id):
    code = secrets.token_hex(5)

    games[code] = {
        "creator_id": creator_id,
        "girl": None,
        "boy": None,
        "active": False,
        "round": 0,
        "turn": None,
    }

    return code


# =========================================================
# KEYBOARDS
# =========================================================

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
        ]
    ])


# =========================================================
# SEND TO BOTH PLAYERS
# =========================================================

async def send_to_players(context, game, text, keyboard=None):

    for role in ("girl", "boy"):

        player = game.get(role)

        if not player:
            continue

        try:
            await context.bot.send_message(
                chat_id=player["chat_id"],
                text=text,
                reply_markup=keyboard,
            )
        except Exception as e:
            print("Could not message player:", e)


# =========================================================
# SEND CHALLENGE
# =========================================================

async def send_challenge(context, code, challenge_type):

    game = games.get(code)

    if not game:
        return

    if not game["girl"] or not game["boy"]:
        return

    # Alternate turns
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
        turn_text = "👩 GIRL"
    else:
        turn_text = "👨 BOY"

    text = (
        f"🔥 ROUND {game['round']}\n\n"
        f"🎯 TURN: {turn_text}\n\n"
        f"{title}\n\n"
        f"{question}\n\n"
        f"Choose your challenge:"
    )

    await send_to_players(
        context,
        game,
        text,
        challenge_keyboard(code)
    )


# =========================================================
# /START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    # Deep-link game
    if context.args:

        code = context.args[0]
        game = games.get(code)

        if not game:
            await update.message.reply_text(
                "❌ This game has expired.\n\n"
                "Start a new game using @NAUGHTYDARE_bot."
            )
            return

        await update.message.reply_text(
            "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
            "👩 GIRL vs 👨 BOY\n\n"
            "Choose your role:",
            reply_markup=role_keyboard(code)
        )

        return

    # Normal start
    await update.message.reply_text(
        "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
        "👩 Girl vs 👨 Boy\n"
        "😈 Truth\n"
        "🔥 Dare\n"
        "🎲 Random\n\n"
        "To start a game:\n\n"
        "Type @NAUGHTYDARE_bot in a chat."
    )


# =========================================================
# INLINE MODE
# =========================================================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    inline = update.inline_query

    if not inline:
        return

    query = inline.query.strip().lower()

    print("INLINE QUERY RECEIVED:", query)

    results = []

    # -----------------------------------------------------
    # EMPTY QUERY
    # -----------------------------------------------------

    if query == "":

        code = create_game(inline.from_user.id)

        # Normal inline result
        results.append(
            InlineQueryResultArticle(
                id="start_game_" + secrets.token_hex(4),
                title="🎮 START 1-ON-1 GAME",
                description="Start a private Girl vs Boy game",
                input_message_content=InputTextMessageContent(
                    "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                    "Start a private Girl vs Boy game."
                ),
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "🎮 OPEN GAME",
                            url=f"https://t.me/{context.bot.username}?start={code}"
                        )
                    ]
                ])
            )
        )

        # Add a few random results
        for i in range(5):

            if random.choice([True, False]):

                text = random.choice(TRUTHS)
                title = "😈 TRUTH"

            else:

                text = random.choice(DARES)
                title = "🔥 DARE"

            results.append(
                InlineQueryResultArticle(
                    id=f"random_{i}_{secrets.token_hex(4)}",
                    title=title,
                    description=text,
                    input_message_content=InputTextMessageContent(
                        f"{title}\n\n{text}"
                    )
                )
            )

        # THIS IS THE SPECIAL TELEGRAM BUTTON
        await inline.answer(
            results=results,
            cache_time=0,
            is_personal=True,
            switch_pm_text="🎮 START 1-ON-1 GAME",
            switch_pm_parameter=code,
        )

        return

    # -----------------------------------------------------
    # TRUTH
    # -----------------------------------------------------

    if "truth" in query:

        for i in range(10):

            text = random.choice(TRUTHS)

            results.append(
                InlineQueryResultArticle(
                    id=f"truth_{i}_{secrets.token_hex(4)}",
                    title="😈 TRUTH",
                    description=text,
                    input_message_content=InputTextMessageContent(
                        f"😈 TRUTH\n\n{text}"
                    )
                )
            )

    # -----------------------------------------------------
    # DARE
    # -----------------------------------------------------

    elif "dare" in query:

        for i in range(10):

            text = random.choice(DARES)

            results.append(
                InlineQueryResultArticle(
                    id=f"dare_{i}_{secrets.token_hex(4)}",
                    title="🔥 DARE",
                    description=text,
                    input_message_content=InputTextMessageContent(
                        f"🔥 DARE\n\n{text}"
                    )
                )
            )

    # -----------------------------------------------------
    # OTHER SEARCH
    # -----------------------------------------------------

    else:

        for i in range(10):

            if random.choice([True, False]):

                text = random.choice(TRUTHS)
                title = "😈 TRUTH"

            else:

                text = random.choice(DARES)
                title = "🔥 DARE"

            results.append(
                InlineQueryResultArticle(
                    id=f"mixed_{i}_{secrets.token_hex(4)}",
                    title=title,
                    description=text,
                    input_message_content=InputTextMessageContent(
                        f"{title}\n\n{text}"
                    )
                )

    await inline.answer(
        results=results,
        cache_time=0,
        is_personal=True
    )


# =========================================================
# BUTTON HANDLER
# =========================================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data.split(":")

    action = data[0]

    code = data[-1]

    game = games.get(code)

    if not game:

        await query.message.reply_text(
            "❌ This game has expired."
        )

        return

    user = query.from_user

    # =====================================================
    # ROLE
    # =====================================================

    if action == "role":

        role = data[1]

        # Already playing
        if game["girl"] and game["girl"]["user_id"] == user.id:
            if role != "girl":
                await query.answer(
                    "You already joined as Girl.",
                    show_alert=True
                )
                return

        if game["boy"] and game["boy"]["user_id"] == user.id:
            if role != "boy":
                await query.answer(
                    "You already joined as Boy.",
                    show_alert=True
                )
                return

        # Role occupied
        if game[role]:

            await query.answer(
                "That role is already taken.",
                show_alert=True
            )

            return

        game[role] = {
            "user_id": user.id,
            "name": user.first_name,
            "chat_id": update.effective_chat.id
        }

        role_name = "👩 GIRL" if role == "girl" else "👨 BOY"

        await query.message.reply_text(
            f"✅ You joined as {role_name}!"
        )

        # Both players ready
        if game["girl"] and game["boy"]:

            ready_text = (
                "🔥 BOTH PLAYERS ARE READY! 🔥\n\n"
                f"👩 Girl: {game['girl']['name']}\n"
                f"👨 Boy: {game['boy']['name']}\n\n"
                "Get ready 😈🔥"
            )

            await send_to_players(
                context,
                game,
                ready_text,
                start_keyboard(code)
            )

        else:

            bot_username = context.bot.username

            link = f"https://t.me/{bot_username}?start={code}"

            await query.message.reply_text(
                "⏳ Waiting for the other player...\n\n"
                "📤 Send this link to them:\n\n"
                f"{link}"
            )

        return

    # =====================================================
    # START
    # =====================================================

    if action == "begin":

        if not game["girl"] or not game["boy"]:

            await query.answer(
                "Both players must join first.",
                show_alert=True
            )

            return

        if game["active"]:

            await query.answer(
                "Game already started."
            )

            return

        game["active"] = True

        await send_to_players(
            context,
            game,
            "🔥 GAME STARTED! 🔥\n\n"
            "👩 Girl vs 👨 Boy\n\n"
            "Let's see who survives 😈"
        )

        await send_challenge(
            context,
            code,
            "random"
        )

        return

    # =====================================================
    # TRUTH
    # =====================================================

    if action == "truth":

        if not game["active"]:
            await query.answer(
                "Start the game first.",
                show_alert=True
            )
            return

        await send_challenge(
            context,
            code,
            "truth"
        )

        return

    # =====================================================
    # DARE
    # =====================================================

    if action == "dare":

        if not game["active"]:
            await query.answer(
                "Start the game first.",
                show_alert=True
            )
            return

        await send_challenge(
            context,
            code,
            "dare"
        )

        return

    # =====================================================
    # RANDOM
    # =====================================================

    if action == "random":

        if not game["active"]:
            await query.answer(
                "Start the game first.",
                show_alert=True
            )
            return

        await send_challenge(
            context,
            code,
            "random"
        )

        return

    # =====================================================
    # NEXT
    # =====================================================

    if action == "next":

        if not game["active"]:
            return

        await send_challenge(
            context,
            code,
            "random"
        )

        return

    # =====================================================
    # DONE
    # =====================================================

    if action == "done":

        await query.message.reply_text(
            "✅ Challenge completed! 😈🔥\n\n"
            "Ready for the next one?",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔥 NEXT",
                        callback_data=f"next:{code}"
                    )
                ]
            ])
        )

        return


# =========================================================
# MAIN
# =========================================================

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

    print("🔥 NAUGHTYDARE BOT RUNNING 🔥")

    app.run_polling()


if __name__ == "__main__":
    main()
