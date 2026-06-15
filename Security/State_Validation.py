def validate_hp(actor):

    if actor.currentHp < 0:
        actor.currentHp = 0

    if actor.currentHp > actor.maxHp:
        actor.currentHp = actor.maxHp

try:
    response = gemini_response

    action = validate_ai_response(response)

except Exception:
    action = "SHOOT_SELF"