import tkinter as tk
from tkinter import messagebox
import random
import configparser


class Character:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

    def attack(self, other_character):
        damage = random.randint(1, self.atk)
        other_character.take_damage(damage)
        return f"{self.name} attacks {other_character.name} for {damage} damage."


class GameConfig:
    def __init__(self):
        self.characters = []

        config = configparser.ConfigParser()
        config.read('characters.ini')
        for section in config.sections():
            self.characters.append(
                Character(
                    config.get(section, 'name'),
                    int(config.get(section, 'hp')),
                    int(config.get(section, 'atk'))
                )
            )

    def GetCharacter(self, exclude_character_name="") -> Character:
        if exclude_character_name:
            while True:
                character = random.choice(self.characters)
                if character.name != exclude_character_name:
                    return character
        else:
            return random.choice(self.characters)


class RPGGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("RPG Game")
        self.master.geometry("400x300")

        config = GameConfig()
        self.player = config.GetCharacter()
        self.enemy = config.GetCharacter(self.player.name)

        self.player_info = tk.Label(self.master, text=f"{self.player.name} (❤ {self.player.hp} / 🪓 {self.player.atk})")
        self.player_info.pack()

        self.enemy_info = tk.Label(self.master, text=f"{self.enemy.name} (❤ {self.enemy.hp} / 🪓 {self.enemy.atk})")
        self.enemy_info.pack()

        self.attack_button = tk.Button(self.master, text="Attack", command=self.attack)
        self.attack_button.pack()

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_game)
        self.quit_button.pack()

        self.info_label = tk.Label(self.master, text="")
        self.info_label.pack()

    def attack(self):
        player_attack_info = self.player.attack(self.enemy)
        enemy_attack_info = self.enemy.attack(self.player)

        self.player_info.config(text=f"{self.player.name} (❤ {self.player.hp} / 🪓 {self.player.atk})")
        self.enemy_info.config(text=f"{self.enemy.name} (❤ {self.enemy.hp} / 🪓 {self.enemy.atk})")

        if not self.enemy.is_alive():
            messagebox.showinfo("Victory", f"You defeated {self.enemy.name}! Congratulations!")
            self.master.destroy()
        elif not self.player.is_alive():
            messagebox.showinfo("Defeat", "You were defeated. Game over!")
            self.master.destroy()
        else:
            self.info_label.config(text=f"{player_attack_info}\n{enemy_attack_info}")

    def quit_game(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    game_gui = RPGGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
