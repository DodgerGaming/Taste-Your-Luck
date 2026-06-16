
def get_ai_choice(player, enemy, shotgun, current_fate, level):
    state = build_game_state(player, enemy, shotgun, current_fate, level)

    prompt = build_prompt

    response = call_api(prompt)
    
    return response

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
You are the enemy AI in Taste Your Luck.

Current Game State:

Player HP: {state["player_hp"]}
Enemy HP: {state["enemy_hp"]}

Current Level: {state["level"]}

Chance of Live Round: {state["live_chance"]}%
Chance of Blank Round: {state["blank_chance"]}%

Current Fate Card: {state["current_fate"]}

Actions:
1 = Shoot Enemy
2 = Shoot Yourself

IMPORTANT:
Respond with ONLY one character.

Valid responses:
1
2
"""