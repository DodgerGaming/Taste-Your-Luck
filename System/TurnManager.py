from Logic.Combat import shoot
from AI_Logic.AI import get_ai_choice
from System.Fate import draw_fate_card, apply_fate_card


FATE_CARD_NAMES = {
    "fortune": "Fortune",
    "devil": "Devil",
    "hanged_man": "Hanged Man",
    "death": "Death",
}


class TurnManager:

    def __init__(self, game):
        self.game           = game
        self.current_turn   = "player"
        self.current_fate   = None
        self.final_showdown = False

    # ------------------------------------------------------------------
    # Reload
    # ------------------------------------------------------------------

    def reload(self):
        """Returns a list of messages (shotgun load info + fate card, if any)."""
        messages = []

        self.game.shotgun.damage = 1
        self.game.player.damage_multiplier = 1
        self.game.shotgun.reload()

        live  = self.game.shotgun.bullets.count("live")
        blank = self.game.shotgun.bullets.count("blank")
        messages.append(f"Shotgun loaded — Live: {live} | Blank: {blank}")

        messages.extend(self._draw_and_apply_fate_card())

        return messages

    def _draw_and_apply_fate_card(self):
        messages = []

        if self.final_showdown:
            self.current_fate = "death"
            apply_fate_card("death", self.game.player, self.game.shotgun)
            return messages

        self.current_fate = draw_fate_card(self.game.level)

        if self.current_fate:
            card_name = FATE_CARD_NAMES.get(self.current_fate, self.current_fate)
            messages.append(f"A Fate Card appears: {card_name}!")
            apply_fate_card(self.current_fate, self.game.player, self.game.shotgun)

        return messages

    def _check_final_showdown(self):
        if self.final_showdown:
            return []

        if self.game.level == 3 and (self.game.player.currentHp <= 2 or self.game.enemy.currentHp <= 2):
            self.final_showdown = True
            self.current_fate = "death"
            apply_fate_card("death", self.game.player, self.game.shotgun)
            return ["The Death card reveals itself... this is the final showdown!"]

        return []

    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------

    def player_shoot_self(self):
        messages = []

        result = shoot(self.game.player, self.game.player, self.game.shotgun)
        messages.extend(self._check_final_showdown())

        if result is None:
            messages.extend(self.reload())
            messages.append("What will you do?")
            return messages, self.check_game_over()

        if result == "blank":
            self.current_turn = "player"
            messages.append("You pull the trigger... click. Nothing.")
            messages.append("What will you do?")
            return messages, self.check_game_over()

        messages.append("Bang! You shot yourself.")
        self.current_turn = "enemy"

        game_over = self.check_game_over()
        if game_over:
            return messages, game_over

        enemy_messages = self._run_full_enemy_turn()
        messages.extend(enemy_messages)

        game_over = self.check_game_over()
        if not game_over:
            messages.append("What will you do?")

        return messages, game_over

    def player_shoot_enemy(self):
        messages = []

        result = shoot(self.game.player, self.game.enemy, self.game.shotgun)
        messages.extend(self._check_final_showdown())

        if result is None:
            messages.extend(self.reload())
            messages.append("What will you do?")
            return messages, self.check_game_over()

        if result == "blank":
            messages.append("You fire at the enemy... click. Nothing.")
        else:
            messages.append("Direct hit! The enemy takes damage.")

        self.current_turn = "enemy"

        game_over = self.check_game_over()
        if game_over:
            return messages, game_over

        enemy_messages = self._run_full_enemy_turn()
        messages.extend(enemy_messages)

        game_over = self.check_game_over()
        if not game_over:
            messages.append("What will you do?")

        return messages, game_over

    # ------------------------------------------------------------------
    # Enemy turn (internal)
    # ------------------------------------------------------------------

    def _run_full_enemy_turn(self):
        messages = []

        while self.current_turn == "enemy":

            if not self.game.enemy.is_alive():
                self.current_turn = "player"
                break

            choice = get_ai_choice(
                self.game.player,
                self.game.enemy,
                self.game.shotgun,
                self.current_fate,
                self.game.level
            )

            if choice == 1:
                result = shoot(self.game.enemy, self.game.player, self.game.shotgun)
                messages.extend(self._check_final_showdown())

                if result is None:
                    messages.extend(self.reload())
                    self.current_turn = "player"
                elif result == "blank":
                    messages.append("Enemy fires at you... click. Nothing.")
                    self.current_turn = "player"
                else:
                    messages.append("The enemy shoots you!")
                    self.current_turn = "player"

            else:
                result = shoot(self.game.enemy, self.game.enemy, self.game.shotgun)
                messages.extend(self._check_final_showdown())

                if result is None:
                    messages.extend(self.reload())
                    self.current_turn = "player"
                elif result == "blank":
                    messages.append("Enemy gambles on itself... click. Nothing.")
                else:
                    messages.append("The enemy shoots itself!")
                    self.current_turn = "player"

            if self.check_game_over():
                self.current_turn = "player"
                break

        return messages

    # ------------------------------------------------------------------
    # Level progression
    # ------------------------------------------------------------------

    def advance_level(self):
        self.game.level += 1

        self.game.player.maxHp += 2
        self.game.player.currentHp = self.game.player.maxHp

        self.game.enemy.maxHp += 2
        self.game.enemy.currentHp = self.game.enemy.maxHp

        self.current_turn = "player"
        self.current_fate = None

        return [f"Level {self.game.level}! Max HP increased to {self.game.player.maxHp}."]

    # ------------------------------------------------------------------
    # Win / lose check
    # ------------------------------------------------------------------

    def check_game_over(self):
        if not self.game.enemy.is_alive():
            return "player_win"
        if not self.game.player.is_alive():
            return "enemy_win"
        return None