from AI_Logic.Gemini_Client import ask_gemini

def get_ai_choice(player, enemy, shotgun, current_fate, level):
    state = build_game_state(player, enemy, shotgun, current_fate, level)

    prompt = build_prompt(state)

    response = ask_gemini(prompt)
    
    print(f"Prompt: {prompt}\nAI Response: {response}")

    return 1

def build_game_state(player, enemy, shotgun, current_fate, level):
    live = shotgun.bullets.count("live")
    blank = shotgun.bullets.count("blank")

    total = len(shotgun.bullets)

    # --- Risk Calculation ---
    live_chance = round(
        (live / total) * 100
    )

    blank_chance = round(
        (blank / total) * 100
    )

    return {
        "player_hp": player.currentHp,
        "enemy_hp": enemy.currentHp,
        "level": level,
        "live_chance": live_chance,
        "blank_chance": blank_chance,
        "current_fate": current_fate
    }

def build_prompt(state):

    return f"""
You are the enemy AI in a game called Taste Your Luck.

Your objective is to survive and defeat the player.

=== GAME RULES ===

A live shell deals damage.
A blank shell deals no damage.
Shooting yourself with a live shell damages you.
Shooting the enemy with a live shell damages the enemy.
If you shoot yourself with a blank shell, you keep your turn.
If you shoot the enemy, your turn ends regardless of the result.
Higher HP means a better chance of surviving.
Your goal is to maximize your chance of winning.

=== CURRENT GAME STATE ===

Player HP: {state["player_hp"]}
Enemy HP: {state["enemy_hp"]}

Health Difference: {state["health_difference"]}

Current Level: {state["level"]}

Remaining Bullets: {state["bullets_remaining"]}

Remaining Live Shells: {state["live_count"]}
Remaining Blank Shells: {state["blank_count"]}

Chance of Live Shell: {state["live_chance"]}%
Chance of Blank Shell: {state["blank_chance"]}%

Current Fate Card: {state["current_fate"]}

Current Shotgun Damage: {state["damage"]}

=== AVAILABLE ACTIONS ===

1 = Shoot the Player
2 = Shoot Yourself

=== DECISION MAKING GUIDELINES ===

Consider both HP values.
Consider the probability of live and blank shells.
Consider whether taking a risk improves your chance of winning.
Consider that shooting yourself with a blank shell allows you to keep your turn.
Consider the current Fate Card effects.
Choose the action that gives you the highest chance of winning.

=== RESPONSE FORMAT ===

IMPORTANT:

Respond with EXACTLY one character.

Valid responses:

1
2

Do not explain.
Do not justify.
Do not include any other text.
"""