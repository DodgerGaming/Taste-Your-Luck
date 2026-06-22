from Logic.Combat import shoot
from AI_Logic.AI import get_ai_choice


class TurnManager:

    def __init__(self, game):
        self.game         = game
        self.current_turn = "player"
        self.current_fate = None
        self.level= self.game.level

    # ------------------------------------------------------------------
    # Reload
    # ------------------------------------------------------------------

    def reload(self):
        # Reset damage and multipliers so they don't carry over between rounds
        self.game.shotgun.damage = 1
        self.game.player.damage_multiplier = 1
        self.game.shotgun.reload()
        live  = self.game.shotgun.bullets.count("live")
        blank = self.game.shotgun.bullets.count("blank")
        return f"Shotgun loaded  —  Live: {live}  |  Blank: {blank}"

    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------

    def player_shoot_self(self):
        """Returns (list of messages, game_over result)."""
        messages = []

        result = shoot(self.game.player, self.game.player, self.game.shotgun)

        if result is None:
            messages.append(self.reload())
            messages.append("What will you do?")
            return messages, self.check_game_over()

        if result == "blank":
            # Blank self-shot = keep turn
            self.current_turn = "player"
            messages.append("You pull the trigger... click. Nothing.")
            messages.append("What will you do?")
            return messages, self.check_game_over()

        # Live self-shot = pass turn to enemy
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
        """Returns (list of messages, game_over result)."""
        messages = []

        result = shoot(self.game.player, self.game.enemy, self.game.shotgun)

        if result is None:
            messages.append(self.reload())
            messages.append("What will you do?")
            return messages, self.check_game_over()

        if result == "blank":
            messages.append("You fire at the enemy... click. Nothing.")
        else:
            messages.append("Direct hit! The enemy takes damage.")

        # Shooting enemy always ends player turn — check game over first
        self.current_turn = "enemy"

        game_over = self.check_game_over()
        if game_over:
            return messages, game_over

        # Only run enemy turn after showing the player's shot result
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
        """
        Runs the enemy turn in a loop until the turn passes back to the player.
        Returns a list of messages.
        """
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
                self.level
            )

            if choice == 1:  # shoot player
                result = shoot(self.game.enemy, self.game.player, self.game.shotgun)

                if result is None:
                    messages.append(self.reload())
                    self.current_turn = "player"
                elif result == "blank":
                    messages.append("Enemy fires at you... click. Nothing.")
                    self.current_turn = "player"
                else:
                    messages.append("The enemy shoots you!")
                    self.current_turn = "player"

            else:  # shoot self
                result = shoot(self.game.enemy, self.game.enemy, self.game.shotgun)

                if result is None:
                    messages.append(self.reload())
                    self.current_turn = "player"
                elif result == "blank":
                    # Enemy keeps turn — loop continues
                    messages.append("Enemy gambles on itself... click. Nothing.")
                else:
                    messages.append("The enemy shoots itself!")
                    self.current_turn = "player"

            if self.check_game_over():
                self.current_turn = "player"
                break

        return messages

    # ------------------------------------------------------------------
    # Win / lose check
    # ------------------------------------------------------------------

    def check_game_over(self):
        if not self.game.enemy.is_alive():
            return "player_win"
        if not self.game.player.is_alive():
            return "enemy_win"
        return None