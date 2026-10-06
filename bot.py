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

# ============================================================
# GAME STORAGE
# ============================================================

games = {}


def new_game():
    code = secrets.token_hex(5)

    games[code] = {
        "girl": None,
        "boy": None,
        "active": False,
        "turn_role": None,
        "turn_user_id": None,
        "round": 0,
        "current_type": None,
        "current_question": None,
    }

    return code


# ============================================================
# BUTTONS FOR NEW PANELS
# ============================================================

def next_buttons(code):
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
# INLINE QUERY
# ============================================================

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.inline_query.query.strip()

    print("INLINE:", q)

    # --------------------------------------------------------
    # CREATE GAME
    # --------------------------------------------------------

    if not q:

        code = new_game()
        game = games[code]

        keyboard = InlineKeyboardMarkup([
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

        result = InlineQueryResultArticle(
            id=f"game_{code}",
            title="🎮 START 1-ON-1 GAME",
            description="Play directly inside this private chat",
            input_message_content=InputTextMessageContent(
                "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                "👩 Girl: Waiting...\n"
                "👨 Boy: Waiting...\n\n"
                "Choose your role:"
            ),
            reply_markup=keyboard,
        )

        await update.inline_query.answer(
            [result],
            cache_time=0,
            is_personal=False,
        )

        return

    # --------------------------------------------------------
    # PARSE INLINE COMMAND
    # --------------------------------------------------------

    parts = q.split("|")
    action = parts[0]

    if len(parts) < 2:
        await update.inline_query.answer(
            [],
            cache_time=0,
        )
        return

    code = parts[1]
    game = games.get(code)

    if not game:
        await update.inline_query.answer(
            [],
            cache_time=0,
        )
        return

    user = update.inline_query.from_user

    # --------------------------------------------------------
    # TRUTH / DARE / RANDOM
    # --------------------------------------------------------

    if action in ("truth", "dare", "random"):

        if not game["active"]:
            await update.inline_query.answer(
                [],
                cache_time=0,
            )
            return

        # Only current player can create the next panel.
        if user.id != game["turn_user_id"]:

            result = InlineQueryResultArticle(
                id=f"not_turn_{secrets.token_hex(4)}",
                title="⏳ NOT YOUR TURN",
                description="Wait for the other player.",
                input_message_content=InputTextMessageContent(
                    "⏳ It's not your turn yet."
                ),
            )

            await update.inline_query.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )

            return

        # Pick challenge.
        if action == "truth":
            question = random.choice(TRUTHS)
            challenge_type = "truth"
            title = "😈 TRUTH"

        elif action == "dare":
            question = random.choice(DARES)
            challenge_type = "dare"
            title = "🔥 DARE"

        else:
            if random.choice([True, False]):
                question = random.choice(TRUTHS)
                challenge_type = "truth"
                title = "😈 TRUTH"
            else:
                question = random.choice(DARES)
                challenge_type = "dare"
                title = "🔥 DARE"

        # Advance round.
        game["round"] += 1
        game["current_type"] = challenge_type
        game["current_question"] = question

        # Switch player for the NEW panel.
        if game["turn_role"] == "girl":
            game["turn_role"] = "boy"
        else:
            game["turn_role"] = "girl"

        game["turn_user_id"] = game[
            game["turn_role"]
        ]["user_id"]

        player = game[game["turn_role"]]

        role_text = (
            "👩 GIRL"
            if game["turn_role"] == "girl"
            else "👨 BOY"
        )

        text = (
            f"🔥 ROUND {game['round']} 🔥\n\n"
            f"🎯 {role_text}'S TURN\n"
            f"👤 {player['name']}\n\n"
            f"{title}\n\n"
            f"{question}"
        )

        # Truth gets an answer button.
        if challenge_type == "truth":
            keyboard = answer_button(code)
        else:
            # For dares, the player can immediately choose
            # the next challenge after completing it.
            keyboard = next_buttons(code)

        result = InlineQueryResultArticle(
            id=f"question_{code}_{secrets.token_hex(4)}",
            title=f"{title} — ROUND {game['round']}",
            description=question[:100],
            input_message_content=InputTextMessageContent(
                text
            ),
            reply_markup=keyboard,
        )

        await update.inline_query.answer(
            [result],
            cache_time=0,
            is_personal=False,
        )

        return

    # --------------------------------------------------------
    # ANSWER
    # --------------------------------------------------------

    if action == "answer":

        if len(parts) < 3:
            return

        answer = parts[2].strip()

        if not answer:

            result = InlineQueryResultArticle(
                id=f"type_{secrets.token_hex(4)}",
                title="✍️ TYPE YOUR ANSWER",
                description="Write your answer after the bot username.",
                input_message_content=InputTextMessageContent(
                    "✍️ Type your answer after @NAUGHTYDARE_bot."
                ),
            )

            await update.inline_query.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )

            return

        if not game["active"]:
            return

        # Only current player can answer.
        if user.id != game["turn_user_id"]:

            result = InlineQueryResultArticle(
                id=f"wrong_{secrets.token_hex(4)}",
                title="⏳ NOT YOUR TURN",
                description="Wait for the other player.",
                input_message_content=InputTextMessageContent(
                    "⏳ It's not your turn yet."
                ),
            )

            await update.inline_query.answer(
                [result],
                cache_time=0,
                is_personal=True,
            )

            return

        answer = answer[:1000]

        text = (
            f"📝 {user.first_name}'s ANSWER\n\n"
            f"{answer}\n\n"
            "🔥 Ready for the next round?"
        )

        result = InlineQueryResultArticle(
            id=f"answer_{code}_{secrets.token_hex(4)}",
            title="📨 SEND ANSWER",
            description=answer[:100],
            input_message_content=InputTextMessageContent(
                text
            ),
            reply_markup=next_buttons(code),
        )

        await update.inline_query.answer(
            [result],
            cache_time=0,
            is_personal=True,
        )

        return

    await update.inline_query.answer(
        [],
        cache_time=0,
    )


# ============================================================
# ROLE BUTTONS
# ============================================================

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data
    parts = data.split(":")

    action = parts[0]
    code = parts[-1]

    game = games.get(code)

    if not game:
        await query.answer(
            "❌ Game expired.",
            show_alert=True,
        )
        return

    user = query.from_user

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

        # Check if user already joined.
        for r in ("girl", "boy"):

            if (
                game[r]
                and game[r]["user_id"] == user.id
            ):
                await query.answer(
                    "You already chose a role.",
                    show_alert=True,
                )
                return

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

        # Only edit the lobby during joining.
        if game["girl"] and game["boy"]:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🎮 START GAME",
                        callback_data=f"begin:{code}",
                    )
                ]
            ])

            text = (
                "🔥 BOTH PLAYERS ARE READY! 🔥\n\n"
                f"👩 Girl: {game['girl']['name']}\n"
                f"👨 Boy: {game['boy']['name']}\n\n"
                "Press START GAME."
            )

        else:

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

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "👩 GIRL"
                        if not game["girl"]
                        else "👩 GIRL — TAKEN",
                        callback_data=(
                            f"role:g:{code}"
                            if not game["girl"]
                            else f"taken:{code}"
                        ),
                    ),
                    InlineKeyboardButton(
                        "👨 BOY"
                        if not game["boy"]
                        else "👨 BOY — TAKEN",
                        callback_data=(
                            f"role:b:{code}"
                            if not game["boy"]
                            else f"taken:{code}"
                        ),
                    ),
                ]
            ])

            text = (
                "🔥 NAUGHTY TRUTH OR DARE 🔥\n\n"
                f"{girl}\n"
                f"{boy}\n\n"
                "Choose your role:"
            )

        if query.inline_message_id:

            await context.bot.edit_message_text(
                inline_message_id=query.inline_message_id,
                text=text,
                reply_markup=keyboard,
            )

        return

    # --------------------------------------------------------
    # TAKEN
    # --------------------------------------------------------

    if action == "taken":

        await query.answer(
            "❌ That role is already taken.",
            show_alert=True,
        )

        return

    # --------------------------------------------------------
    # START GAME
    # --------------------------------------------------------

    if action == "begin":

        if not game["girl"] or not game["boy"]:

            await query.answer(
                "Both players must join first.",
                show_alert=True,
            )

            return

        game["active"] = True
        game["round"] = 1

        game["turn_role"] = random.choice(
            ["girl", "boy"]
        )

        game["turn_user_id"] = game[
            game["turn_role"]
        ]["user_id"]

        # The first question is displayed by
        # switching the user into inline mode.
        #
        # This button stays in the same chat.
        keyboard = InlineKeyboardMarkup([
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

        player = game[game["turn_role"]]

        role_text = (
            "👩 GIRL"
            if game["turn_role"] == "girl"
            else "👨 BOY"
        )

        text = (
            "🔥 GAME STARTED! 🔥\n\n"
            f"🎯 {role_text}'S TURN\n"
            f"👤 {player['name']}\n\n"
            "Choose a challenge:"
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
        "🔥 NAUGHTYDARE INLINE GAME RUNNING 🔥"
    )

    app.run_polling()


if __name__ == "__main__":
    main()
