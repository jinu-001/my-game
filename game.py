# ================================================
# ИГРА «СОЛЯНЫЕ ШАХТЫ»
# Автор: Александр Алиев
# Дата: сентябрь 2026
# ================================================

import os
import json
import dungeon
import random

try:
    from colorama import Fore, Style, init
    init()
    COLOR = True
except ImportError:
    COLOR = False

title = "СОЛЯНЫЕ ШАХТЫ"
frame = "=" * 19
print(frame)
print(" " + title + " ")
print(frame)

loaded = None
if os.path.exists("save.json"):
    print("A save was found. Continue the run? (yes/no)")
    answer = input().strip().lower()
    if answer == "yes":
        try:
            with open("save.json", "r", encoding="utf-8") as f:
                loaded = json.load(f)
        except json.JSONDecodeError:
            print("Save file is corrupted! Starting a new game.")
            loaded = None

if loaded is None:
    while True:
        try:
            print("Введите начальные характеристики героя.")
            health = int(input("Здоровье: "))
            strength = int(input("Сила: "))
            agility = int(input("Ловкость: "))
            endurance = int(input("Выносливость: "))
            max_stamina = int(input("Запас сил: "))

            if health <= 0 or health > 500 or strength < 0 or agility < 0 or endurance < 0 or max_stamina < 0 or strength > 100:
                raise ValueError("Некорректные значения характеристик.")
            break
        except ValueError:
            print("\n[Ошибка]. Введите все характеристики снова:\n")

    print("Как зовут героя?")
    hero_name = input()
    
    hero = dungeon.Hero(hero_name, health, strength, agility, endurance)
    hero.max_health = hero.health 
else:
    hero = dungeon.Hero.from_dict(loaded["hero"])
    
    hero.max_health = hero.health
    
    gold_total = loaded["gold"]
    actions = loaded["actions"]
    enemies = loaded["enemies"]
    hero_r, hero_c = loaded["position"]
    visited = {tuple(p) for p in loaded["visited"]}
    found_loot = set(loaded["loot"])
    
    print(f"Run continued: {hero}")


enemies = ["ghoul", "skeleton", "spider", "bat"]
log = []

base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2


def print_leaderboard(log):
    """Выводит таблицу лидеров по урону раундов.

    Параметры:
        log (list): Лог всех совершённых раундов боя.

    Ничего не возвращает (None).

    Печатает топ-3 раундов по урону и самый сильный удар врага.
    """
    if not log:
        print("You haven't fought yet.")
        return

    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]

    print("Leaderboard (hero damage):")

    for i, record in enumerate(top, start=1):
        print(f"{i}. Round {record[0]}: {record[1]:.1f}")

    worst = max(log, key=lambda r: r[2])
    print(f"Strongest enemy hit: {worst[2]} (round {worst[0]}).")


def print_run_summary(log):
    """Выводит суммарную статистику забега по урону.

    Параметры:
        log (list): Лог всех совершённых раундов боя.

    Ничего не возвращает (None).

    Печатает суммарный урон, количество раундов и средний урон за раунд.
    """
    total = sum(record[1] for record in log)
    rounds = len(log)

    if rounds > 0:
        print(
            f"Damage: {total:.1f} across {rounds} rounds, "
            f"average {total / rounds:.1f}."
        )
    else:
        print("No battles this run.")


def scout(r, c, seen):
    if (r, c) in seen or MAP[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    
    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)
    return total

def write_save():
    """Собирает состояние забега и пишет его в save.json."""
    save = {}
    save["hero"] = hero.to_dict()
    
    save["gold"] = gold_total
    save["actions"] = actions
    save["enemies"] = enemies
    save["position"] = [hero_r, hero_c]
    save["visited"] = [list(p) for p in visited]
    save["loot"] = sorted(found_loot)

    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(save, f, ensure_ascii=False, indent=2)

print("Как зовут героя?")
hero_name = input()

print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.")
print()

menu_last = 10
running = True
actions = 0
gold_total = 0
ability_bonus = 0
inventory = {}
prices = {"potion": 15, "torch_oil": 10, "war_elixir": 25}

outcome = "прерывание"

enemy_stats = {
"skeleton": {"hp": 45, "damage": 6, "loot": 25},
"ghoul": {"hp": 30, "damage": 4, "loot": 15},
"spider": {"hp": 20, "damage": 3, "loot": 10},
"bat": {"hp": 12, "damage": 2, "loot": 5},
}

num_to_verb = {
    "1": "look", "2": "go", "3": "rest", "4": "listen",
    "5": "torch", "6": "train", "7": "descend", "8": "leaders",
    "9": "shop", "10": "backpack", "11": "drink", "0": "exit"
}

commands = [
    "look", "go", "rest", "listen", "torch", "train", "descend",
    "leaders", "shop", "backpack", "drink potion",
    "buy <item> [count]", "map", "scout", "newgame", "exit"
]

MENU = [
    "What do you do? (number or command; help for help)",
    "1 - look around (look)",
    "2 - go forward (go)",
    "3 - rest (rest)",
    "4 - listen (listen)",
    "5 - light a torch (torch)",
    "6 - train (train)",
    "7 - descend deeper (descend)",
    "8 - leaderboard (leaders)",
    "9 - shop (shop)",
    "10 - backpack (backpack)",
    "11 - drink potion (drink)",
    "12 - show map (map)",
    "13 - scout dungeon (scout)",
    "newgame - start a new game (newgame)",
    "0 - exit the dungeon (exit)"
]

MAP = [
["#", "#", "#", "#", "#"],
["#", ".", ".", "#", "#"],
["#", ".", "#", ".", "#"],
["#", ".", ".", ".", "#"],
["#", "#", "S", ".", "#"],
]

DIRECTIONS = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}

hero_r, hero_c = 4, 2
visited = {(4, 2)}

LOOT = {(1, 1): "old coin", (2, 3): "dusty potion", (3, 3): "guard's gem"}
found_loot = set()

try:
    while running:
        print("\n".join(MENU))
        print()


        print()

        line = input()
        cmd = line.strip().lower()
        while cmd == "":
            print("Empty command. Type a command or number.")
            line = input()
            cmd = line.strip().lower()
        
        words = cmd.split()
        verb = words[0]
        
        if cmd in num_to_verb:
            verb = num_to_verb[cmd]


        match verb:
            case "look":
                print(
                    "Вы осмотрелись. Комната пуста, только пыль на полу."
                )

            case "go":
                if len(words) > 1 and words[1] in DIRECTIONS:
                    dr, dc = DIRECTIONS[words[1]]
                    nr, nc = hero_r + dr, hero_c + dc
                    
                    if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[nr]) and MAP[nr][nc] != "#":
                        hero_r, hero_c = nr, nc
                        visited.add((hero_r, hero_c))
                        print(f"You step {words[1]}. Room ({hero_r}, {hero_c}).")
                        
                        # Подбор лута после успешного шага
                        if (hero_r, hero_c) in LOOT:
                            item = LOOT[(hero_r, hero_c)]
                            if item not in found_loot:
                                found_loot.add(item)
                                print(f"You found {item}! Unique loot: {len(found_loot)}.")
                    else:
                        print(f"Cannot go {words[1]}: wall or edge.")
                else:
                    cost = 2

                exhausted = hero.spend_stamina(cost)
                if not exhausted:
                    print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
                else:
                    print("Сил больше нет — вы идёте на одном упорстве.")

            case "rest":
                if hero.stamina < hero.max_health // 10 + hero.endurance:
                    hero.stamina += 1
                    print("Вы присели отдохнуть на соляной блок. Усталость постепенно уходит.")
                else:
                    print("Вы полны сил и готовы к действиям! Отдыхать больше нет смысла.")

            case "listen":
                print(
                    "Вы замерли и прислушались. Где-то вдалеке "
                    "капает вода, опасности не слышно."
                )

            case "torch":
                stamina -= 1
                print(
                    "Вы чиркнули кресалом и зажгли факел. "
                    "Тратится энергия, но стало гораздо светлее."
                )

            case "train":
                strikes = 6

                print(
                    "Вы подходите к массивной глыбе соли, "
                    "испещрённой старыми сколами."
                )
                print(
                    "Предыдущие рабочие использовали её для проверки "
                    "остроты кирок и своей силы."
                )
                print()
                print(f"Наносите серию из {strikes} ударов.")

                total_damage = 0.0
                crit_count = 0

                for i in range(1, strikes + 1):
                    hit_damage, crit = hero.strike(i)

                    if crit:
                        crit_count += 1
                        print(
                            f"Удар {i}: {hit_damage:.1f} урона "
                            "— критический!"
                        )
                    else:
                        print(f"Удар {i}: {hit_damage:.1f} урона")

                    total_damage += hit_damage

                average_damage = total_damage / strikes
                stamina_cost = 4
                hero.spend_stamina(stamina_cost)


                print()
                print(
                    f"Итог: {strikes} ударов, "
                    f"критических ударов: {crit_count}"
                )
                print(
                    f"Общий нанесённый урон: {total_damage:.1f}"
                )
                print(
                    f"Средний урон за удар: {average_damage:.1f}"
                )
                print(
                    f"Затраты сил на тренировку: {stamina_cost}"
                )

            case "descend":
                if not enemies:
                    print(
                        "You descend the stairs. "
                        "But the dungeon is empty."
                    )
                else:
                    enemy = random.choice(enemies)

                    rounds, won, health, loot = dungeon.fight(
                        enemy,
                        health,
                        damage,
                        crit_damage,
                        bonus=ability_bonus
                    )

                    for r in rounds:
                        log.append(r)

                    if won:
                        gold_total += loot
                        enemies.remove(enemy)

                        print(
                            f"{enemy.capitalize()} defeated! "
                            f"{len(enemies)} enemies left in the dungeon."
                        )

                    print(f"Battle: {len(rounds)} rounds.")

            case "leaders":
                print_leaderboard(log)

            
            case "shop":
                print("Shop:")
                for name, price in prices.items():
                    print(f"{name}: {price} gold")


            case "buy":
                if len(words) > 1 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = " ".join(words[1:-1])
                else:
                    qty = 1
                    item = " ".join(words[1:])
                if item == "":
                    print("Buy what? Type: buy <item>.")
                    continue
                if item not in prices:
                    print("No such item in the shop.")
                    continue
                gold_total, ok = dungeon.buy(prices[item], gold_total, quantity=qty)
                if ok:
                    inventory[item] = inventory.get(item, 0) + qty
                    print(f"Bought {qty} {item} for {prices[item] * qty} gold. Gold left: {gold_total}.")
                else:
                    print(f"Not enough gold: need {prices[item] * qty}, have {gold_total}.")

            case "scout":
                seen = set()
                print(f"Scout: {scout(hero_r, hero_c, seen)} rooms reachable.")

            case "newgame":
                if os.path.exists("save.json"):
                    os.remove("save.json")
                    print("Save destroyed. The next run starts fresh.")
                else:
                    print("No save to destroy.")
                continue

            case "backpack":
                if not inventory:
                    print("Backpack is empty.")
                else:
                    print("Backpack:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} pcs")

            case "drink":
                item = " ".join(words[1:]) or "potion"
                if inventory.get(item, 0) == 0:
                    print(f"No {item} in the backpack.")
                else:
                    hero.heal(10, hero.max_health)
                    inventory[item] -= 1
                    if inventory[item] == 0:
                        del inventory[item]
                    print(f"You drink a {item}. Health: {health}. Potions left: {inventory.get(item, 0)}")

            case "map":
                print("Map:")
                for i in range(len(MAP)):
                    cells = []
                    for j in range(len(MAP[i])):
                        cell = "@" if (i, j) == (hero_r, hero_c) else MAP[i][j]
                        cells.append(cell)
                    print(" ".join(cells))      

            case "help":
                print("Commands: " + ", ".join(commands) + ".")
                print("Numbers 0-11 work as before.")

            case "exit":
                print("You climb back toward the light. The dungeon stays behind.")
                write_save()
                print("Progress saved.")
                outcome = "exit"
                running = False

            case _:
                print(f"Don't understand command: '{line.strip()}'. Type 'help'.")
                continue


        if health <= 0:
            print(f"{hero_name} falls. The dungeon claims another seeker.")
            if os.path.exists("save.json"):
                os.remove("save.json")
            outcome = "death"
            running = False


        if running:
            actions += 1

        print()
        state = f"Health: {hero.health} Stamina: {hero.stamina} Enemies left: {len(enemies)} Gold: {gold_total}"
        if COLOR:
            print(Fore.GREEN + state + Style.RESET_ALL)
        else:
            print(state)

        print("-" * 50)
        print()

except KeyboardInterrupt:
    print()
    print("The player ended the session.")
    write_save()


finally:
    print(frame)

    if outcome == "гибель":
        print(
            f"Ты не дошёл, {hero_name}. "
            "Соляные шахты оказались сильнее."
        )
        print(
            f"Увы, underground поход окончен трагически. "
            f"Действий совершено: {actions}. "
            f"Золота собрано: {gold_total}"
        )

    elif outcome == "выход":
        print(
            f"Забег окончен, {hero_name}. "
            "Вы успешно выбрались на поверхность!"
        )
        print(
            f"Отличная работа, возвращайтесь в лагерь с добычей. "
            f"Действий совершено: {actions}. "
            f"Золота собрано: {gold_total}"
        )

    else:
        print(
            f"Сеанс прерван, {hero_name}. "
            "Твоё путешествие внезапно оборвалось."
        )
        print(
            f"Вынужденная остановка посреди темноты. "
            f"Действий совершено: {actions}. "
            f"Золота собрано: {gold_total}"
        )

    if inventory:
        print("Left behind in the backpack:")
        for name, qty in inventory.items():
            print(f"{name}: {qty} pcs")
    else:
        print("Left behind in the backpack: nothing.")

    print_run_summary(log)
    print(frame)
