import os
import random
import uuid

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

# ============================================================
# QUESTIONS
# ============================================================

TRUTHS = [
    "Have you ever kissed someone in a bathroom?",
    "Have you ever hooked up somewhere you definitely shouldn't have?",
    "Have you ever had a secret crush on your best friend?",
    "Have you ever been caught making out?",
    "Have you ever flirted with someone just to make another person jealous?",
    "Have you ever secretly wanted someone you weren't supposed to want?",
    "Have you ever lied about where you were because you were with someone?",
    "Have you ever kissed someone you barely knew?",
    "Have you ever had a secret relationship?",
    "Have you ever regretted turning someone down?",
    "What's the most scandalous place you've ever kissed someone?",
    "Have you ever had feelings for a friend's partner?",
    "Have you ever sent a risky message and immediately regretted it?",
    "Have you ever been attracted to someone your friends would never expect?",
    "Have you ever had chemistry with someone you absolutely shouldn't?",
    "Have you ever kept talking to an ex because you still wanted them?",
    "Have you ever fantasized about dating someone you see regularly?",
    "Have you ever made the first move on someone?",
    "Who was your most unexpected crush?",
    "Who is the person you would have the hardest time saying no to?",
    "Have you ever kissed someone and pretended you didn't like it?",
    "Have you ever had a crush on someone who was already taken?",
    "Have you ever flirted with someone through text and denied it later?",
    "Have you ever deleted messages so someone wouldn't find them?",
    "Have you ever lied about your relationship status?",
    "Have you ever had a crush on a coworker?",
    "Have you ever had a crush on a teacher or professor?",
    "Have you ever fallen for someone you met online?",
    "Have you ever secretly checked someone's social media every day?",
    "Have you ever posted something hoping one specific person would see it?",
    "Have you ever pretended not to care about someone you actually liked?",
    "Have you ever gotten jealous over someone you weren't dating?",
    "Have you ever kissed more than one person in the same night?",
    "Have you ever regretted a late-night text?",
    "Have you ever flirted with someone while someone else was watching?",
    "Have you ever had a crush on your friend's sibling?",
    "Have you ever lied about how many people you've dated?",
    "Have you ever kept an old romantic message because you couldn't delete it?",
    "Have you ever gone somewhere mainly because you knew your crush would be there?",
    "Have you ever dressed specifically to impress someone?",
    "Have you ever changed your appearance because of a crush?",
    "Have you ever practiced what you were going to say before approaching someone?",
    "Have you ever been rejected by someone you really liked?",
    "Have you ever rejected someone and later regretted it?",
    "Have you ever kissed someone you shouldn't have?",
    "Have you ever secretly wished an ex would come back?",
    "Have you ever compared two people you've dated?",
    "Have you ever pretended to be busy to make someone chase you?",
    "Have you ever ignored someone's message because you wanted them to worry?",
    "Have you ever purposely made someone jealous?",
    "Have you ever had a crush on someone in this chat?",
    "Have you ever imagined going on a date with someone in this chat?",
    "Have you ever lied to your friends about who you liked?",
    "Have you ever had a crush that lasted for years?",
    "Have you ever fallen for someone after saying you never would?",
    "Have you ever kissed someone at a party?",
    "Have you ever met someone and immediately felt attracted to them?",
    "Have you ever stayed awake thinking about someone?",
    "Have you ever smiled at your phone because of one person's message?",
    "Have you ever saved someone's photo because you found them attractive?",
    "Have you ever secretly hoped someone would text you?",
    "Have you ever checked your phone repeatedly waiting for someone's reply?",
    "Have you ever written a message and deleted it because you were nervous?",
    "Have you ever used a fake excuse to spend time with someone?",
    "Have you ever pretended to dislike someone you actually liked?",
    "Have you ever had a crush on someone much older than you?",
    "Have you ever had a crush on someone much younger than you who was an adult?",
    "Have you ever flirted with someone you knew was bad news?",
    "Have you ever gone back to someone you knew was trouble?",
    "Have you ever secretly hoped a friendship would become romantic?",
    "Have you ever confused friendship with attraction?",
    "Have you ever had feelings for someone who only saw you as a friend?",
    "Have you ever tried to make someone fall for you?",
    "Have you ever stayed in a relationship longer than you should have?",
    "Have you ever broken someone's heart?",
    "Have you ever had your heart broken and pretended you were fine?",
    "Have you ever cried over someone you weren't dating?",
    "Have you ever missed someone but refused to contact them?",
    "Have you ever stalked an ex's social media?",
    "Have you ever checked who your crush follows?",
    "Have you ever gotten jealous over a comment on someone's post?",
    "Have you ever flirted with someone you met at a party?",
    "Have you ever given someone a fake name while flirting?",
    "Have you ever received a message that made your heart race?",
    "Have you ever sent a message that made someone else's heart race?",
    "Have you ever been caught staring at someone attractive?",
    "Have you ever pretended you didn't notice someone checking you out?",
    "Have you ever had a secret admirer?",
    "Have you ever secretly been someone's admirer?",
    "Have you ever kissed someone and immediately wanted to do it again?",
    "Have you ever wished you could relive a romantic moment?",
    "Have you ever had a crush on someone you couldn't date?",
    "Have you ever fallen for someone who was completely wrong for you?",
    "Have you ever had a secret that would shock your partner?",
    "Have you ever hidden a conversation from your partner?",
    "Have you ever been tempted to text an ex?",
    "Have you ever thought about giving someone a second chance?",
    "What's the boldest move you've ever made on someone?",
    "What's your biggest secret attraction?",
    "Who was your most unforgettable kiss?",
    "What's one romantic thing you've always wanted someone to do for you?"
]

DARES = [
    "Send someone a 😏 emoji with no explanation.",
    "Text your crush: 'Be honest... have you ever thought about me that way?'",
    "Send someone 'I had a dream about you last night 👀.'",
    "Call someone and tell them you miss them.",
    "Let another player choose someone for you to text.",
    "Send your most-used flirting emoji to the last person you messaged.",
    "Tell the group your biggest secret attraction.",
    "Give someone your best flirty stare for 10 seconds.",
    "Send someone a mysterious 'Are you alone?' message.",
    "Text someone: 'We need to talk 👀' and wait five minutes before explaining.",
    "Send a compliment to someone you find attractive.",
    "Call a friend and ask them who they think your crush is.",
    "Change your profile picture for 10 minutes to something chosen by the group.",
    "Send 'I have something to tell you...' to someone and make them guess.",
    "Tell another player who you'd take on a dream date.",
    "Send a heart emoji to someone you rarely text.",
    "Text someone: 'You looked really good today.'",
    "Let another player write a harmless flirty message for you.",
    "Send a voice message saying 'I miss you' dramatically.",
    "Tell the group your most embarrassing flirting story.",
    "Send a 😈 emoji to someone and don't explain it.",
    "Call someone and ask them to rate your flirting skills.",
    "Tell someone in the chat one thing you find attractive about them.",
    "Send your crush a simple 'Hey stranger 👀'.",
    "Let another player choose your next status for 10 minutes.",
    "Send someone a compliment without using the words 'beautiful' or 'handsome'.",
    "Tell the group your most embarrassing date story.",
    "Send a mysterious selfie to a friend with the caption 'Guess what I'm thinking.'",
    "Text someone 'You crossed my mind today.'",
    "Call someone and give them your best pickup line.",
    "Send a flirty GIF to the last person you chatted with.",
    "Tell someone why you think they are attractive.",
    "Let another player choose one person for you to compliment.",
    "Send 'I have a question for you 👀' and wait for their reply.",
    "Tell the group your ideal date.",
    "Send someone a goodnight message even if it's not nighttime.",
    "Call a friend and ask who their celebrity crush is.",
    "Tell the group the most attractive personality trait.",
    "Send a heart to the person you last argued with.",
    "Text someone 'Don't get too attached 😏'.",
    "Let another player choose your next emoji-only message.",
    "Send someone a compliment in exactly five words.",
    "Tell the group what your biggest dating red flag is.",
    "Send a playful 'I know you like me' message to a friend.",
    "Call someone and ask them to describe your personality in three words.",
    "Send someone 'You owe me a date.'",
    "Tell the group your biggest green flag.",
    "Send a voice note saying your best pickup line.",
    "Let another player choose your next profile bio for 10 minutes.",
    "Text someone 'I have a confession...' and reveal something harmless.",
    "Tell the group what makes someone instantly attractive to you.",
    "Send someone a random compliment.",
    "Call a friend and ask them who you should date.",
    "Send someone a message containing only three heart emojis.",
    "Tell another player their best feature.",
    "Text someone 'Would you ever go on a date with me?'",
    "Let another player choose someone for you to compliment.",
    "Send a selfie with your best confident expression.",
    "Tell the group about your most awkward romantic moment.",
    "Send someone 'Guess who I was thinking about 👀'.",
    "Call someone and say 'I have a confession' before laughing and hanging up.",
    "Tell the group your dream date location.",
    "Send a flirty compliment to someone you haven't talked to recently.",
    "Let another player choose one emoji you must use in your next five messages.",
    "Text someone 'You have dangerous energy 😏'.",
    "Tell the group your biggest dating turn-off.",
    "Tell the group your biggest dating green flag.",
    "Send someone 'Rate my flirting from 1-10.'",
    "Call someone and ask what their first impression of you was.",
    "Send a message to someone saying 'I think we'd have fun together.'",
    "Let another player choose your next status message.",
    "Tell the group the last person who made you blush.",
    "Send someone a compliment about their personality.",
    "Text someone 'I dare you to be honest with me.'",
    "Call a friend and ask them to describe your ideal partner.",
    "Send someone a playful wink emoji.",
    "Tell the group your most memorable first date.",
    "Send someone 'You're trouble, aren't you? 😏'.",
    "Let another player choose someone for you to send a compliment to.",
    "Tell the group your biggest relationship fear.",
    "Send someone a message starting with 'Confession:'",
    "Call someone and ask what their biggest red flag is.",
    "Send someone 'I think you owe me a coffee.'",
    "Tell the group what instantly makes you lose interest in someone.",
    "Send someone a random romantic song recommendation.",
    "Let another player choose your next social media caption.",
    "Text someone 'I bet you can't guess who I like.'",
    "Tell the group the most attractive thing someone has ever said to you.",
    "Send someone a compliment using only emojis.",
    "Call someone and ask them to rate your sense of humor.",
    "Tell the group the weirdest place you've ever had a crush.",
    "Send someone 'You looked suspiciously good today 👀.'",
    "Let another player choose a harmless nickname for you for the next round.",
    "Tell the group your ideal partner's personality.",
    "Send someone 'We should hang out sometime.'",
    "Call someone and give them your funniest pickup line.",
    "Tell the group who would be your celebrity dream date.",
    "Send someone a message containing three compliments.",
    "Let another player choose someone you must compliment.",
    "Tell the group the boldest thing you've ever done for someone you liked.",
    "Send someone 'Okay, be honest... do you like me? 👀'",
    "End your turn by giving another player a sincere compliment."
]

# ============================================================
# GAMES
# ============================================================

games = {}


def create_game(player_id, player_name):
    return {
        "p1_id": player_id,
        "p1_name": player_name,

        "p2_id": None,
        "p2_name": None,

        "started": False,

        # Always 1 -> 2 -> 1 -> 2
        "turn": 1,

        # Current challenge
        "challenge_id": None,
        "challenge_type": None,
        "challenge_player": None,
    }


def get_player(game, user_id):
    if user_id == game["p1_id"]:
        return 1

    if user_id == game["p2_id"]:
        return 2

    return None


def get_name(game, player):
    if player == 1:
        return game["p1_name"]
    return game["p2_name"]


def next_player(player):
    return 2 if player == 1 else 1


# ============================================================
# BUTTONS
# ============================================================

def choice_buttons(code, challenge_id=""):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 TRUTH",
                switch_inline_query_current_chat=
                f"truth {code} {challenge_id}"
            ),
            InlineKeyboardButton(
                "😈 DARE",
                switch_inline_query_current_chat=
                f"dare {code} {challenge_id}"
            ),
            InlineKeyboardButton(
                "🎲 RANDOM",
                switch_inline_query_current_chat=
                f"random {code} {challenge_id}"
            ),
        ]
    ])


def join_button(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 JOIN GAME",
                callback_data=f"join:{code}"
            )
        ]
    ])


def start_button(code):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "▶️ START GAME",
                callback_data=f"start:{code}"
            )
        ]
    ])


# ============================================================
# /START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎮 <b>NAUGHTY TRUTH OR DARE</b>\n\n"
        "Open a private chat and type:\n\n"
        "<code>@NAUGHTYDARE_bot</code>\n\n"
        "Then choose the game.",
        parse_mode="HTML"
    )


# ============================================================
# INLINE
# ============================================================

async def inline_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.inline_query
    user = query.from_user

    text = query.query.strip()

    # --------------------------------------------------------
    # CREATE NEW GAME
    # --------------------------------------------------------

    if not text:

        code = uuid.uuid4().hex[:8]

        games[code] = create_game(
            user.id,
            user.first_name or "Player 1"
        )

        game = games[code]

        result = InlineQueryResultArticle(
            id=f"game_{code}",
            title="🎮 START 1-ON-1 GAME",
            description="Create a private Truth or Dare game",
            input_message_content=InputTextMessageContent(
                "🎮 <b>TRUTH OR DARE</b>\n\n"
                f"👤 Player 1: <b>{game['p1_name']}</b>\n"
                "👤 Player 2: <b>Waiting...</b>\n\n"
                "Send this game to the chat.\n"
                "Your partner can tap JOIN GAME.",
                parse_mode="HTML"
            ),
            reply_markup=join_button(code)
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # READ COMMAND
    # --------------------------------------------------------

    parts = text.split()

    if len(parts) < 2:
        await query.answer([], cache_time=0)
        return

    action = parts[0].lower()
    code = parts[1]

    game = games.get(code)

    if not game:
        await query.answer([], cache_time=0)
        return

    old_challenge_id = ""

    if len(parts) >= 3:
        old_challenge_id = parts[2]

    # --------------------------------------------------------
    # PLAYER CHECK
    # --------------------------------------------------------

    player = get_player(game, user.id)

    if player is None:

        result = InlineQueryResultArticle(
            id=f"notplayer_{uuid.uuid4().hex}",
            title="⚠️ NOT A PLAYER",
            description="You are not part of this game",
            input_message_content=InputTextMessageContent(
                "⚠️ You are not one of the players in this game."
            )
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # GAME NOT STARTED
    # --------------------------------------------------------

    if not game["started"]:

        result = InlineQueryResultArticle(
            id=f"waiting_{uuid.uuid4().hex}",
            title="⏳ GAME NOT STARTED",
            description="Player 1 must start the game",
            input_message_content=InputTextMessageContent(
                "⏳ The game has not started yet."
            )
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # OLD BUTTON
    # --------------------------------------------------------

    if (
        old_challenge_id
        and game["challenge_id"]
        and old_challenge_id != game["challenge_id"]
    ):

        current_player = game["turn"]
        current_name = get_name(game, current_player)

        result = InlineQueryResultArticle(
            id=f"old_{uuid.uuid4().hex}",
            title="⚠️ OLD PANEL",
            description=f"Current turn: {current_name}",
            input_message_content=InputTextMessageContent(
                "⚠️ <b>That is an old challenge.</b>\n\n"
                f"🎯 Current turn: <b>{current_name}</b>\n\n"
                "Use the buttons below."
            ),
            reply_markup=choice_buttons(
                code,
                game["challenge_id"]
            )
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # WRONG PLAYER
    # --------------------------------------------------------

    if player != game["turn"]:

        current_name = get_name(game, game["turn"])

        result = InlineQueryResultArticle(
            id=f"wait_{uuid.uuid4().hex}",
            title="⏳ WAIT FOR YOUR TURN",
            description=f"{current_name}'s turn",
            input_message_content=InputTextMessageContent(
                "⏳ <b>WAIT FOR YOUR TURN</b>\n\n"
                f"🎯 It is <b>{current_name}</b>'s turn."
            ),
            reply_markup=choice_buttons(
                code,
                game["challenge_id"] or ""
            )
        )

        await query.answer(
            [result],
            cache_time=0,
            is_personal=True
        )

        return

    # --------------------------------------------------------
    # ONLY THESE 3 COMMANDS ARE VALID
    # --------------------------------------------------------

    if action not in ("truth", "dare", "random"):

        await query.answer([], cache_time=0)
        return

    # --------------------------------------------------------
    # BUTTON PRESS = FINISH CURRENT TURN
    #
    # If there was already a challenge, move to the other
    # player BEFORE creating the new challenge.
    # --------------------------------------------------------

    if game["challenge_id"] is not None:
        game["turn"] = next_player(game["turn"])

    current_player = game["turn"]
    current_name = get_name(game, current_player)

    # --------------------------------------------------------
    # CREATE CHALLENGE
    # --------------------------------------------------------

    if action == "truth":

        challenge = random.choice(TRUTHS)
        emoji = "🔥"
        title = "TRUTH"

    elif action == "dare":

        challenge = random.choice(DARES)
        emoji = "😈"
        title = "DARE"

    else:

        if random.choice([True, False]):
            challenge = random.choice(TRUTHS)
            emoji = "🔥"
            title = "TRUTH"
        else:
            challenge = random.choice(DARES)
            emoji = "😈"
            title = "DARE"

    challenge_id = uuid.uuid4().hex[:10]

    game["challenge_id"] = challenge_id
    game["challenge_type"] = title.lower()
    game["challenge_player"] = current_player

    # --------------------------------------------------------
    # NEW PANEL
    # --------------------------------------------------------

    message = (
        f"{emoji} <b>{title}</b>\n\n"
        f"<b>{challenge}</b>\n\n"
        f"🎯 <b>{current_name}'s turn</b>\n\n"
        "When you're finished, choose the next challenge:"
    )

    result = InlineQueryResultArticle(
        id=f"challenge_{challenge_id}",
        title=f"{emoji} {title} — {current_name}",
        description=challenge[:100],
        input_message_content=InputTextMessageContent(
            message,
            parse_mode="HTML"
        ),
        reply_markup=choice_buttons(
            code,
            challenge_id
        )
    )

    await query.answer(
        [result],
        cache_time=0,
        is_personal=True
    )


# ============================================================
# CALLBACKS
# ============================================================

async def callbacks(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    data = query.data

    await query.answer()

    # ========================================================
    # JOIN
    # ========================================================

    if data.startswith("join:"):

        code = data.split(":", 1)[1]
        game = games.get(code)

        if not game:
            await query.edit_message_text(
                "❌ This game no longer exists."
            )
            return

        user = query.from_user

        # Player 1
        if user.id == game["p1_id"]:

            await query.answer(
                "You are already Player 1.",
                show_alert=True
            )
            return

        # Player 2
        if game["p2_id"] is None:

            game["p2_id"] = user.id
            game["p2_name"] = user.first_name or "Player 2"

            await query.edit_message_text(
                "🎮 <b>TRUTH OR DARE</b>\n\n"
                f"👤 Player 1: <b>{game['p1_name']}</b>\n"
                f"👤 Player 2: <b>{game['p2_name']}</b>\n\n"
                "✅ <b>Both players joined!</b>\n\n"
                "Player 1 can start the game.",
                parse_mode="HTML",
                reply_markup=start_button(code)
            )

            return

        await query.answer(
            "This game already has two players.",
            show_alert=True
        )

        return

    # ========================================================
    # START
    # ========================================================

    if data.startswith("start:"):

        code = data.split(":", 1)[1]
        game = games.get(code)

        if not game:
            await query.edit_message_text(
                "❌ This game no longer exists."
            )
            return

        user = query.from_user

        if user.id != game["p1_id"]:

            await query.answer(
                "Only Player 1 can start the game.",
                show_alert=True
            )
            return

        if game["p2_id"] is None:

            await query.answer(
                "Waiting for Player 2.",
                show_alert=True
            )
            return

        # Reset game
        game["started"] = True
        game["turn"] = 1
        game["challenge_id"] = None
        game["challenge_type"] = None
        game["challenge_player"] = None

        # IMPORTANT:
        # First panel already has Truth/Dare/Random.
        message = (
            "🔥 <b>GAME STARTED!</b>\n\n"
            f"👤 Player 1: <b>{game['p1_name']}</b>\n"
            f"👤 Player 2: <b>{game['p2_name']}</b>\n\n"
            f"🎯 <b>{game['p1_name']}'s turn</b>\n\n"
            "Choose your challenge:"
        )

        await query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=choice_buttons(code, "")
        )

        return


# ============================================================
# RUN BOT
# ============================================================

def main():

    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing from environment variables."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        InlineQueryHandler(inline_query)
    )

    app.add_handler(
        CallbackQueryHandler(callbacks)
    )

    print("🔥 NAUGHTYDARE BOT IS RUNNING")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
