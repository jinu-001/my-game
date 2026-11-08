import random

class Hero:
    def __init__(self, name, health, strength, agility, endurance):
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.endurance = endurance
        
        self.damage = 10 + strength * 1.5
        self.crit_damage = self.damage * 2
        self.stamina = health // 10 + endurance

    def __str__(self):
        return f"{self.name}: health {self.health}, damage {self.damage:.1f}, stamina {self.stamina}"

    def strike(self, n):
        """Возвращает пару (урон, критический_ли). Каждая 3-я атака критует."""
        if n % 3 == 0:
            return self.crit_damage, True
        return self.damage, False

    def spend_stamina(self, cost):
        """Тратит выносливость. Если её не хватает, списывает остаток из здоровья.
        
        Возвращает True, если герой шёл на чистом упорстве (здоровье уменьшилось).
        Возвращает False, если сил хватило на обычное действие.
        """
        if self.stamina >= cost:
            self.stamina -= cost
            return False
        
        self.health -= (cost - self.stamina)
        self.stamina = 0
        return True

    def heal(self, amount, cap):
        """Лечит героя на amount единиц, но не выше потолка cap."""
        self.health = min(self.health + amount, cap)

    def to_dict(self):
        """Превращает объект героя в словарь для сохранения."""
        return {
            "name": self.name,
            "health": self.health,
            "stamina": self.stamina,
            "strength": self.strength,
            "agility": self.agility,
            "endurance": self.endurance
        }

    @staticmethod
    def from_dict(data):
        """Фабричный метод: создает объект героя из словаря сохранения 
        и восстанавливает точное состояние характеристик.
        """
        hero = Hero(
            data["name"], 
            data["health"], 
            data["strength"], 
            data["agility"], 
            data["endurance"]
        )
        hero.stamina = data["stamina"]
        return hero

class Enemy:
    def __init__(self, name, stats):
        self.name = name
        self.hp = stats["hp"]
        self.damage = stats["damage"]
        self.loot = stats["loot"]


prices = {"potion": 15, "torch_oil": 10, "war_elixir": 25}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "ghoul": {"hp": 30, "damage": 4, "loot": 15},
    "spider": {"hp": 20, "damage": 3, "loot": 10},
    "bat": {"hp": 12, "damage": 2, "loot": 5},
}

def hero_hit(strike_n, damage, crit_damage):
    """Урон героя в удар strike_n; возвращает пару (hit, crit)."""
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False

def buy(price, gold, quantity=1):
    """Оформляет покупку товара в магазине."""
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False

def fight(enemy, hero_health, bonus, damage, crit_damage):
    """Бой с enemy до гибели одного из двоих.
    
    Принимает параметры базового и критического урона героя для расчета ударов.
    """
    stats = enemy_stats[enemy]
    enemy_hp = float(stats["hp"])
    rounds = []
    round_n = 0

    print(f"You descend the stairs. Out of the darkness comes {enemy}!")

    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n, damage, crit_damage)
        hit += bonus
        enemy_hp -= hit

        line = f"Round {round_n}: hero deals {hit:.1f}"

        if crit:
            line += " - critical!"

        if enemy_hp <= 0:
            line += " Enemy falls."
            rounds.append([round_n, hit, 0])
        else:
            blow = stats["damage"]
            hero_health -= blow

            line += (
                f" {enemy} health: {enemy_hp:.1f}."
                f" {enemy.capitalize()} hits for {blow}."
            )
            rounds.append([round_n, hit, blow])

        print(line)

    won = enemy_hp <= 0
    loot = stats["loot"] if won else 0

    return rounds, won, hero_health, loot

if __name__ == "__main__":
    test_hero = Hero(name="Тестовый Рыцарь", health=100, strength=10, agility=10, endurance=10)
    
    test_foe = Enemy("skeleton", enemy_stats["skeleton"])
    
    print("--- Запуск автономного теста боя ---")
    rounds, won, loot = fight(test_foe, test_hero, bonus=0)
    
    print()
    print(f"self-test: {len(rounds)} rounds, won={won}, loot={loot}")
    print(f"Состояние героя после теста: {test_hero}")
    print("-------------------------------------")