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
    # Helper — snapshot current state into a tagged message
    # ------------------------------------------------------------------

    def _snap(self, text):
        """Wrap a message with the current game state snapshot."""
        return {
            "text":      text,
            "player_hp": self.game.player.currentHp,
            "enemy_hp":  self.game.enemy.currentHp,
            "turn":      self.current_turn,
        }

    # ------------------------------------------------------------------
    # Reload
    # ------------------------------------------------------------------

    def reload(self):
        messages = []

        self.game.shotgun.damage = 1
        self.game.player.damage_multiplier = 1
        self.game.shotgun.reload()

        live  = self.game.shotgun.bullets.count("live")
        blank = self.game.shotgun.bullets.count("blank")
        messages.append(self._snap(f"Shotgun loaded — Live: {live} | Blank: {blank}"))

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
            apply_fate_card(self.current_fate, self.game.player, self.game.shotgun)
            messages.append(self._snap(f"A Fate Card appears: {card_name}!"))

        return messages

    def _check_final_showdown(self):
        if self.final_showdown:
            return []

        if self.game.level == 3 and (self.game.player.currentHp <= 2 or self.game.enemy.currentHp <= 2):
            self.final_showdown = True
            self.current_fate = "death"
            apply_fate_card("death", self.game.player, self.game.shotgun)
            return [self._snap("The Death card reveals itself... this is the final showdown!")]

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
            messages.append(self._snap("What will you do?"))
            return messages, self.check_game_over()

        if result == "blank":
            self.current_turn = "player"
            messages.append(self._snap("You pull the trigger... click. Nothing."))
            messages.append(self._snap("What will you do?"))
            return messages, self.check_game_over()

        # Live — set turn to enemy BEFORE snapping so label shows correctly
        self.current_turn = "enemy"
        messages.append(self._snap("Bang! You shot yourself."))

        game_over = self.check_game_over()
        if game_over:
            return messages, game_over

        enemy_messages = self._run_full_enemy_turn()
        messages.extend(enemy_messages)

        game_over = self.check_game_over()
        if not game_over:
            messages.append(self._snap("What will you do?"))

        return messages, game_over

    def player_shoot_enemy(self):
        messages = []

        result = shoot(self.game.player, self.game.enemy, self.game.shotgun)
        messages.extend(self._check_final_showdown())

        if result is None:
            messages.extend(self.reload())
            messages.append(self._snap("What will you do?"))
            return messages, self.check_game_over()

        # Set turn to enemy BEFORE snapping so label shows correctly
        self.current_turn = "enemy"

        if result == "blank":
            messages.append(self._snap("You fire at the enemy... click. Nothing."))
        else:
            messages.append(self._snap("Direct hit! The enemy takes damage."))

        game_over = self.check_game_over()
        if game_over:
            return messages, game_over

        enemy_messages = self._run_full_enemy_turn()
        messages.extend(enemy_messages)

        game_over = self.check_game_over()
        if not game_over:
            messages.append(self._snap("What will you do?"))

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

            # Check the chamber BEFORE doing anything else. If it's empty,
            # reload right away and let the enemy act on a fresh chamber —
            # don't queue "thinking" or any action messages for a shot
            # that was never actually going to happen.
            if not self.game.shotgun.bullets:
                messages.extend(self.reload())
                continue

            choice = get_ai_choice(
                self.game.player,
                self.game.enemy,
                self.game.shotgun,
                self.current_fate,
                self.game.level
            )

            # Chamber is guaranteed non-empty here, so this is a real shot
            messages.append(self._snap("The enemy is thinking..."))

            if choice == 1:
                result = shoot(self.game.enemy, self.game.player, self.game.shotgun)
                messages.extend(self._check_final_showdown())

                self.current_turn = "player"
                if result == "blank":
                    messages.append(self._snap("Enemy fires at you... click. Nothing."))
                else:
                    messages.append(self._snap("The enemy shoots you!"))

            else:
                result = shoot(self.game.enemy, self.game.enemy, self.game.shotgun)
                messages.extend(self._check_final_showdown())

                if result == "blank":
                    # Keep enemy turn — don't change current_turn
                    messages.append(self._snap("Enemy gambles on itself... click. Nothing."))
                else:
                    self.current_turn = "player"
                    messages.append(self._snap("The enemy shoots itself!"))

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

        return [self._snap(f"Level {self.game.level}! Max HP increased to {self.game.player.maxHp}.")]

    # ------------------------------------------------------------------
    # Win / lose check
    # ------------------------------------------------------------------

    def check_game_over(self):
        if not self.game.enemy.is_alive():
            return "player_win"
        if not self.game.player.is_alive():
            return "enemy_win"
        return None