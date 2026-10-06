import os
import random
import secrets

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ============================================================
# QUESTIONS
# ============================================================

TRUTHS = [
    "Who is the most attractive person you've ever had a crush on?",
    "Have you ever secretly liked a friend?",
    "Who was your last crush?",
    "What's the first thing you notice about someone you're attracted to?",
    "Have you ever flirted with someone just to make another person jealous?",
    "What's your biggest weakness when you like someone?",
    "Have you ever liked someone who didn't know you existed?",
    "Would you date someone your best friend used to like?",
    "What's the boldest move you've ever made on a crush?",
    "Have you ever pretended not to like someone when you actually did?",
    "Who was the last person who made your heart beat faster?",
    "What's your biggest dating red flag?",
    "What's your biggest green flag?",
    "Have you ever fallen for someone unexpectedly?",
    "Would you choose looks or personality?",
    "What's your ideal first date?",
    "Have you ever checked someone's profile repeatedly because you liked them?",
    "What's the most attractive personality trait?",
    "Have you ever sent a message and immediately regretted it?",
    "Who was the last person you wanted to impress?",
    "Would you date someone different from your usual type?",
    "What's the most romantic thing someone could do for you?",
    "Have you ever had a crush on someone unavailable?",
    "What's the longest you've secretly liked someone?",
    "Have you ever flirted through texting but acted shy in person?",
    "What's the most attractive thing someone can wear?",
    "Have you ever caught feelings after saying you wouldn't?",
    "Would you make the first move or wait?",
    "What's your favorite kind of compliment?",
    "Have you ever reread an old conversation with someone you liked?",
    "Who would you want to receive a surprise date invitation from?",
    "What's something that instantly makes someone more attractive?",
    "Have you ever tried to look extra good because someone you liked was there?",
    "Would you date your exact opposite?",
    "What's the most embarrassing thing you've done because you liked someone?",
    "Have you ever gotten jealous even though you weren't dating?",
    "What's your favorite flirting style?",
    "Have you ever practiced what to say before talking to your crush?",
    "What makes you lose interest in someone immediately?",
    "Would you rather receive flowers or a surprise date?",
    "Have you ever intentionally waited before replying to someone you liked?",
    "What's your dream date location?",
    "Have you ever liked someone your friends warned you about?",
    "What's more attractive: confidence or shyness?",
    "Have you ever had chemistry with someone you barely knew?",
    "What's one thing you'd want your future partner to understand?",
    "Would you rather make the first move or be surprised?",
    "What's the sweetest thing someone has ever said to you?",
    "If you could go on a date with anyone you know, who would you choose?",
]

DARES = [
    "Give your partner your best pickup line.",
    "Send your partner a cute selfie.",
    "Give your partner a genuine compliment.",
    "Tell your partner: 'Be honest... would you date me? 👀'",
    "Describe your ideal partner without saying their name.",
    "Send your partner your favorite flirty emoji combination.",
    "Give your partner a rating out of 10 for their flirting skills.",
    "Send a voice message saying your best pickup line.",
    "Tell your partner your first impression of them.",
    "Change your profile picture to your best dressed-up photo for 10 minutes.",
    "Write a cheesy romantic message for your partner.",
    "Tell your partner what you find most attractive about their personality.",
    "Send your partner: 'I have a question for you 👀'",
    "Give your partner a ridiculous romantic nickname.",
    "Describe your perfect date in three sentences.",
    "Send your best non-explicit selfie to your partner.",
    "Give your partner your best celebrity-style introduction.",
    "Tell your partner what your dream partner looks like.",
    "Write a pickup line using your partner's name.",
    "Send your partner three heart emojis.",
    "Tell your partner one thing that makes them attractive.",
    "Record a 5-second voice message saying 'I think you're cute.'",
    "Let your partner choose your status for 10 minutes.",
    "Give your partner a dramatic compliment like you're in a romance movie.",
    "Tell your partner your most embarrassing crush story.",
    "Send a selfie making your best confident expression.",
    "Give your partner your best first-date invitation.",
    "Tell your partner what your ideal first date with them would be.",
    "Send your partner: 'We need to talk 👀' and then reveal it's a dare.",
    "Give your partner a rating for their sense of humor.",
    "Tell your partner three things you find attractive in a person.",
    "Send your partner your favorite romantic emoji combination.",
    "Give your partner a compliment without mentioning appearance.",
    "Pretend to propose to your partner for 10 seconds.",
    "Create a fake dating-app bio for yourself.",
    "Send a voice message introducing yourself as your partner's future date.",
    "Tell your partner your most attractive quality.",
    "Give your partner a cheesy movie-style compliment.",
    "Send your partner: 'Quick question... what's your type? 👀'",
    "Let your partner choose one harmless emoji for your next five messages.",
    "Describe your perfect partner using only five words.",
    "Give your partner a playful compliment.",
    "Tell your partner what would instantly make you interested in someone.",
    "Send your partner a selfie with your best smile.",
    "Give your partner a fake award for having the best personality.",
    "Tell your partner their best quality.",
    "Make up a romantic movie title about the two of you.",
    "Send a voice message saying your most dramatic love confession.",
    "Tell your partner your dream date activity.",
    "Give your partner your best harmless flirting attempt.",
]

# ============================================================
# GAME STORAGE
# ============================================================

games = {}


def create_game():
    code = secrets.token_urlsafe(6)

    games[code] = {
        "girl": None,
        "boy": None,
        "turn": None,
        "round": 0,
        "active": False,
    }

    return code


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 CREATE GAME",
                callback_data="create"
            )
        ]
    ])


# ============================================================
# ROLE SELECTION
# ============================================================

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


# ============================================================
# GAME PANEL
# ============================================================

def game_panel(code):

    game = games[code]

    girl = game["girl"]
    boy = game["boy"]

    girl_name = girl["name"] if girl else "Waiting..."
    boy_name = boy["name"] if boy else "Waiting..."

    if girl and boy:
        status = "🟢 READY TO PLAY"
    else:
        status = "🟡 WAITING FOR PLAYERS"

    return (
        "🔥 *PRIVATE TRUTH OR DARE* 🔥\n\n"
        f"{status}\n\n"
        f"👩 Girl: *{girl_name}*\n"
        f"👨 Boy: *{boy_name}*\n\n"
        "Only two players can join this game.\n"
        "Choose your role below."
    )


def game_keyboard(code):

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
        ],
        [
            InlineKeyboardButton(
                "🎮 START",
                callback_data=f"begin:{code}"
            )
        ]
    ])


# ============================================================
# CHALLENGE BUTTONS
# ============================================================

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
            ),
            InlineKeyboardButton(
                "🔄 NEXT",
                callback_data=f"next:{code}"
            ),
        ],
        [
            InlineKeyboardButton(
                "✅ DONE",
                callback_data=f"done:{code}"
            )
        ],
    ])


# ============================================================
# START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 *PRIVATE TRUTH OR DARE* 🔥\n\n"
        "Create a private 1-on-1 game and invite another player.\n\n"
        "👩 Girl vs 👨 Boy\n"
        "😈 Truth\n"
        "🔥 Dare\n"
        "🎲 Random challenges\n"
        "🔄 Automatic turns",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


# ============================================================
# SEND CHALLENGE
# ============================================================

async def send_challenge(query, code, challenge_type="random"):

    if code not in games:
        await query.answer(
            "This game no longer exists.",
            show_alert=True
        )
        return

    game = games[code]

    if not game["girl"] or not game["boy"]:
        await query.answer(
            "Both players must join first!",
            show_alert=True
        )
        return

    # Determine whose turn it is
    if game["turn"] is None:
        player = random.choice([
            game["girl"],
            game["boy"]
        ])
    else:
        if game["turn"] == "girl":
            player = game["boy"]
        else:
            player = game["girl"]

    game["turn"] = player["role"]
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

    role_icon = "👩" if player["role"] == "girl" else "👨"

    text = (
        f"🔥 *ROUND {game['round']}* 🔥\n\n"
        f"{role_icon} *{player['name']}'s turn!*\n\n"
        f"*{title}*\n\n"
        f"🎯 {challenge}\n\n"
        "Complete the challenge, then press DONE."
    )

    await query.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=challenge_keyboard(code),
    )


# ============================================================
# BUTTON HANDLER
# ============================================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user

    # --------------------------------------------------------
    # CREATE GAME
    # --------------------------------------------------------

    if data == "create":

        code = create_game()

        await query.message.reply_text(
            "🎮 *GAME CREATED!*\n\n"
            "Choose your role:",
            parse_mode="Markdown",
            reply_markup=role_keyboard(code),
        )

        return

    # --------------------------------------------------------
    # ROLE SELECTION
    # --------------------------------------------------------

    if data.startswith("role:"):

        _, role, code = data.split(":")

        if code not in games:
            await query.answer(
                "Game not found.",
                show_alert=True
            )
            return

        game = games[code]

        selected_role = "girl" if role == "g" else "boy"

        # Prevent same user taking both roles
        other_role = "boy" if selected_role == "girl" else "girl"

        if game[other_role] and game[other_role]["id"] == user.id:
            await query.answer(
                "You already selected the other role!",
                show_alert=True
            )
            return

        # Check whether role is occupied
        if game[selected_role]:

            if game[selected_role]["id"] != user.id:
                await query.answer(
                    "That role is already taken!",
                    show_alert=True
                )
                return

        game[selected_role] = {
            "id": user.id,
            "name": user.first_name,
            "role": selected_role,
        }

        await query.answer(
            "Role selected! 🎉",
            show_alert=True
        )

        await query.message.reply_text(
            game_panel(code),
            parse_mode="Markdown",
            reply_markup=game_keyboard(code),
        )

        return

    # --------------------------------------------------------
    # START GAME
    # --------------------------------------------------------

    if data.startswith("begin:"):

        code = data.split(":")[1]

        if code not in games:
            await query.answer(
                "Game not found.",
                show_alert=True
            )
            return

        game = games[code]

        if not game["girl"] or not game["boy"]:
            await query.answer(
                "You need both a girl and a boy!",
                show_alert=True
            )
            return

        game["active"] = True
        game["round"] = 0
        game["turn"] = None

        await query.answer("Game started! 🔥")

        await send_challenge(
            query,
            code,
            "random"
        )

        return

    # --------------------------------------------------------
    # TRUTH / DARE / RANDOM / NEXT / DONE
    # --------------------------------------------------------

    if ":" not in data:
        return

    action, code = data.split(":", 1)

    if code not in games:
        await query.answer(
            "This game no longer exists.",
            show_alert=True
        )
        return

    game = games[code]

    if not game["active"]:
        await query.answer(
            "The game hasn't started yet!",
            show_alert=True
        )
        return

    # Make sure only the two players can control the game
    player_ids = []

    if game["girl"]:
        player_ids.append(game["girl"]["id"])

    if game["boy"]:
        player_ids.append(game["boy"]["id"])

    if user.id not in player_ids:
        await query.answer(
            "You're not one of the players.",
            show_alert=True
        )
        return

    if action == "truth":

        await send_challenge(
            query,
            code,
            "truth"
        )

    elif action == "dare":

        await send_challenge(
            query,
            code,
            "dare"
        )

    elif action == "random":

        await send_challenge(
            query,
            code,
            "random"
        )

    elif action == "next":

        await send_challenge(
            query,
            code,
            "random"
        )

    elif action == "done":

        await query.answer(
            "Completed! 🔥 Next turn!",
            show_alert=True
        )

        await send_challenge(
            query,
            code,
            "random"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError(
            "BOT_TOKEN environment variable is missing!"
        )

    app = Application.builder().token(token).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button)
    )

    print("🔥 Private Truth or Dare bot is running!")

    app.run_polling()


if __name__ == "__main__":
    main()
