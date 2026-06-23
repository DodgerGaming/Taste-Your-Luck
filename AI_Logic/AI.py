USE_GEMINI = False

def get_ai_choice(player, enemy, shotgun, current_fate, level):
    
    state = build_game_state(player, enemy, shotgun, current_fate, level) # getting the game state


    if not USE_GEMINI:
        from AI_Logic.Gemini_Client import ask_gemini

        return local_ai_choice(state)

    prompt = build_prompt(state) # passing the game state to builder to create a prompt containing the game state

    try:
        
        response = ask_gemini(prompt)
    
        print(f"Prompt: {prompt}\nAI Response: {response}")

        if response == "1":
            return 1

        elif response == "2":
            return 2
        
        print("Invalid AI response. Using fallback")
    except Exception as e:
        print(f"AI Error: {e}")

    return local_ai_choice(state)


def build_game_state(player, enemy, shotgun, current_fate, level):
    live = shotgun.bullets.count("live")
    blank = shotgun.bullets.count("blank")

    total = len(shotgun.bullets)

    # --- Risk Calculation ---
    if total > 0:
        live_chance = round((live / total) * 100)
        blank_chance = round((blank / total) * 100)
    else:
        live_chance = 0
        blank_chance = 0


    return {
        "player_hp": player.currentHp,
        "enemy_hp": enemy.currentHp,
        "level": level,
        "live_chance": live_chance,
        "blank_chance": blank_chance,
        "current_fate": current_fate,
        "health_difference": enemy.currentHp - player.currentHp,
        "bullets_remaining": len(shotgun.bullets),
        "live_count": live,
        "blank_count": blank,
        "damage": shotgun.damage,
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

def local_ai_choice(state): # risk-dependent fall-back

    live_chance = state["live_chance"]
    player_hp = state["player_hp"]

    # If player is lowhealth and has high chance of live bullet, shoot
    if player_hp <= 1 and live_chance >= 75:
        return 1

    # if likely blank, shoot self for extra turn
    if live_chance <= 25:
        return 2

    # if likely live, shoot enemy
    if live_chance >= 75:
        return 1

    # if not all condition, shoot enemy and don't take any risk
    return 1