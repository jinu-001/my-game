# ================================================
# ИГРА «СОЛЯНЫЕ ШАХТЫ»
# Автор: Александр Алиев
# Дата: сентябрь 2026
# ================================================

import os
import json
import random
import dungeon
import functools

print = functools.partial(print, flush=True)

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

MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
]

DIRECTIONS = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}
LOOT = {(1, 1): "old coin", (2, 3): "dusty potion", (3, 3): "guard's gem"}

hero = None
gold_total = 0
actions = 0
enemies = ["ghoul", "skeleton", "spider", "bat"]
hero_r, hero_c = 4, 2
visited = {(4, 2)}
found_loot = set()
inventory = {}
ability_bonus = 0
log = []
running = True
outcome = "прерывание"


def print_leaderboard(battle_log):
    """Выводит таблицу лидеров по урону раундов."""
    if not battle_log:
        print("You haven't fought yet.")
        return

    top = sorted(battle_log, key=lambda r: r[1], reverse=True)[:3]
    print("Leaderboard (hero damage):")

    for i, record in enumerate(top, start=1):
        print(f"{i}. Round {record[0]}: {record[1]:.1f}")

    worst = max(battle_log, key=lambda r: r[2])
    print(f"Strongest enemy hit: {worst[2]} (round {worst[0]}).")


def print_run_summary(battle_log):
    """Выводит суммарную статистику забега по урону."""
    total = sum(record[1] for record in battle_log)
    rounds = len(battle_log)

    if rounds > 0:
        print(
            f"Damage: {total:.1f} across {rounds} rounds, "
            f"average {total / rounds:.1f}."
        )
    else:
        print("No battles this run.")


def scout(r, c, seen):
    """Рекурсивно подсчитывает количество доступных комнат."""
    if r < 0 or r >= len(MAP) or c < 0 or c >= len(MAP[r]):
        return 0
    if (r, c) in seen or MAP[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    
    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)
    return total


def write_save():
    """Собирает состояние забега и пишет его в save.json."""
    if hero is None:
        return
    save = {
        "hero": hero.to_dict(),
        "gold": gold_total,
        "actions": actions,
        "enemies": enemies,
        "position": [hero_r, hero_c],
        "visited": [list(p) for p in visited],
        "loot": sorted(found_loot),
        "inventory": inventory,
        "ability_bonus": ability_bonus
    }

    try:
        with open("save.json", "w", encoding="utf-8") as f:
            json.dump(save, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ошибка при сохранении игры: {e}")


num_to_verb = {
    "1": "look", "2": "go", "3": "rest", "4": "listen",
    "5": "torch", "6": "train", "7": "descend", "8": "leaders",
    "9": "shop", "10": "backpack", "11": "drink", "12": "map",
    "13": "scout", "0": "exit"
}

commands = [
    "look", "go <north/south/west/east>", "rest", "listen", "torch", 
    "train", "descend", "leaders", "shop", "backpack", "drink <item>",
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

try:
    loaded = None
    if os.path.exists("save.json"):
        print("A save was found. Continue the run? (yes/no)")
        answer = input().strip().lower()
        if answer == "yes":
            try:
                with open("save.json", "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                hero = dungeon.Hero.from_dict(loaded["hero"])
                gold_total = loaded.get("gold", 0)
                actions = loaded.get("actions", 0)
                enemies = loaded.get("enemies", ["ghoul", "skeleton", "spider", "bat"])
                hero_r, hero_c = loaded.get("position", [4, 2])
                visited = {tuple(p) for p in loaded.get("visited", [])}
                found_loot = set(loaded.get("loot", []))
                inventory = loaded.get("inventory", {})
                ability_bonus = loaded.get("ability_bonus", 0)
                print(f"Run continued: {hero}")
            except (json.JSONDecodeError, KeyError, TypeError, OSError):
                print("Save file is corrupted or unreadable! Starting a new game.")
                loaded = None
                hero = None

    if loaded is None:
        while True:
            try:
                print("Введите начальные характеристики героя.")
                health = int(input("Здоровье (1-500): "))
                strength = int(input("Сила (0-100): "))
                agility = int(input("Ловкость (>=0): "))
                endurance = int(input("Выносливость (>=0): "))
                max_stamina = int(input("Запас сил (>0): "))

                if (
                    health <= 0 or health > 500 
                    or strength < 0 or strength > 100 
                    or agility < 0 or endurance < 0 
                    or max_stamina <= 0
                ):
                    raise ValueError("Некорректные значения характеристик.")
                break
            except ValueError:
                print("\n[Ошибка]. Проверьте границы значений и введите все характеристики снова:\n")

        print("Как зовут героя?")
        hero_name = input().strip() or "Безымянный"
        hero = dungeon.Hero(hero_name, health, strength, agility, endurance, max_stamina)

        print(f"\nДобро пожаловать, {hero.name}!")
        print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.\n")

    while running:
        print("\n".join(MENU))
        print()

        line = input("> ")
        cmd = line.strip().lower()
        while cmd == "":
            print("Empty command. Type a command or number.")
            line = input()
            cmd = line.strip().lower()
        
        words = cmd.split()
        verb = words[0]
        
        if verb in num_to_verb:
            verb = num_to_verb[verb]

        match verb:
            case "look":
                print("Вы осмотрелись. Комната пуста, только пыль на полу.")

            case "go":
                cost = 1
                if len(words) > 1 and words[1] in DIRECTIONS:
                    dr, dc = DIRECTIONS[words[1]]
                    nr, nc = hero_r + dr, hero_c + dc
                    
                    if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[nr]) and MAP[nr][nc] != "#":
                        hero_r, hero_c = nr, nc
                        visited.add((hero_r, hero_c))
                        print(f"You step {words[1]}. Room ({hero_r}, {hero_c}).")
                        
                        if (hero_r, hero_c) in LOOT:
                            item = LOOT[(hero_r, hero_c)]
                            if item not in found_loot:
                                found_loot.add(item)
                                print(f"You found {item}! Unique loot: {len(found_loot)}.")
                    else:
                        print(f"Cannot go {words[1]}: wall or edge.")
                        continue
                elif len(words) > 1:
                    print(f"Unknown direction: '{words[1]}'. Use north, south, west, or east.")
                    continue
                else:
                    cost = 2

                exhausted = hero.spend_stamina(cost)
                if not exhausted:
                    print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
                else:
                    print("Сил больше нет — вы идёте на одном упорстве.")

            case "rest":
                if hero.stamina < hero.max_stamina:
                    hero.restore_stamina(1)
                    print("Вы присели отдохнуть на соляной блок. Усталость постепенно уходит.")
                else:
                    print("Вы полны сил и готовы к действиям! Отдыхать больше нет смысла.")

            case "listen":
                print("Вы замерли и прислушались. Где-то вдалеке капает вода, опасности не слышно.")

            case "torch":
                hero.spend_stamina(1)
                print("Вы чиркнули кресалом и зажгли факел. Тратится энергия, но стало гораздо светлее.")

            case "train":
                strikes = 6
                print("Вы подходите к массивной глыбе соли, испещрённой старыми сколами.")
                print("Предыдущие рабочие использовали её для проверки остроты кирок и своей силы.\n")
                print(f"Наносите серию из {strikes} ударов.")

                total_damage = 0.0
                crit_count = 0

                for i in range(1, strikes + 1):
                    hit_damage, crit = hero.strike(i)
                    if crit:
                        crit_count += 1
                        print(f"Удар {i}: {hit_damage:.1f} урона — критический!")
                    else:
                        print(f"Удар {i}: {hit_damage:.1f} урона")
                    total_damage += hit_damage

                average_damage = total_damage / strikes
                stamina_cost = 4
                hero.spend_stamina(stamina_cost)

                print(f"\nИтог: {strikes} ударов, критических ударов: {crit_count}")
                print(f"Общий нанесённый урон: {total_damage:.1f}")
                print(f"Средний урон за удар: {average_damage:.1f}")
                print(f"Затраты сил на тренировку: {stamina_cost}")

            case "descend":
                if not enemies:
                    print("You descend the stairs. But the dungeon is empty.")
                else:
                    enemy = random.choice(enemies)

                    rounds, won, hero.health, loot = dungeon.fight(
                        enemy,
                        hero.health,
                        ability_bonus,
                        hero.damage,
                        hero.crit_damage
                    )

                    log.extend(rounds)

                    if won:
                        gold_total += loot
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon.")

                    print(f"Battle: {len(rounds)} rounds.")

            case "leaders":
                print_leaderboard(log)

            case "shop":
                print("Shop:")
                for name, price in dungeon.prices.items():
                    print(f"{name}: {price} gold")

            case "buy":
                if len(words) > 2 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = " ".join(words[1:-1])
                else:
                    qty = 1
                    item = " ".join(words[1:])
                
                if item == "":
                    print("Buy what? Type: buy <item> [count].")
                    continue
                if qty <= 0:
                    print("Quantity must be at least 1.")
                    continue
                if item not in dungeon.prices:
                    print("No such item in the shop.")
                    continue
                
                gold_total, ok = dungeon.buy(dungeon.prices[item], gold_total, quantity=qty)
                if ok:
                    inventory[item] = inventory.get(item, 0) + qty
                    print(f"Bought {qty} {item} for {dungeon.prices[item] * qty} gold. Gold left: {gold_total}.")
                else:
                    print(f"Not enough gold: need {dungeon.prices[item] * qty}, have {gold_total}.")

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
                    continue

                if item == "potion":
                    hero.heal(15)
                    print(f"You drink a potion. Health: {hero.health}/{hero.max_health}.")
                elif item == "torch_oil":
                    hero.restore_stamina(5)
                    print(f"You use torch oil to refresh yourself. Stamina: {hero.stamina}/{hero.max_stamina}.")
                elif item == "war_elixir":
                    ability_bonus += 3
                    print(f"You drink a war elixir! Attack bonus is now +{ability_bonus}.")
                else:
                    print(f"You can't drink {item}.")
                    continue

                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]

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
                print("Numbers 0-13 work as before.")

            case "exit":
                print("You climb back toward the light. The dungeon stays behind.")
                write_save()
                print("Progress saved.")
                outcome = "выход"
                running = False

            case _:
                print(f"Don't understand command: '{line.strip()}'. Type 'help'.")
                continue

        if hero.health <= 0:
            print(f"{hero.name} falls. The dungeon claims another seeker.")
            if os.path.exists("save.json"):
                os.remove("save.json")
            outcome = "гибель"
            running = False

        if running:
            actions += 1

        print()
        state = (
            f"Health: {hero.health}/{hero.max_health} "
            f"Stamina: {hero.stamina}/{hero.max_stamina} "
            f"Enemies left: {len(enemies)} Gold: {gold_total}"
        )
        if COLOR:
            print(Fore.GREEN + state + Style.RESET_ALL)
        else:
            print(state)

        print("-" * 50)
        print()

except KeyboardInterrupt:
    print("\nThe player ended the session.")
    write_save()

finally:
    print(frame)
    if hero is not None:
        if outcome == "гибель":
            print(f"Ты не дошёл, {hero.name}. Соляные шахты оказались сильнее.")
            print(f"Увы, underground поход окончен трагически. Действий совершено: {actions}. Золота собрано: {gold_total}")
        elif outcome == "выход":
            print(f"Забег окончен, {hero.name}. Вы успешно выбрались на поверхность!")
            print(f"Отличная работа, возвращайтесь в лагерь с добычей. Действий совершено: {actions}. Золота собрано: {gold_total}")
        else:
            print(f"Сеанс прерван, {hero.name}. Твоё путешествие внезапно оборвалось.")
            print(f"Вынужденная остановка посреди темноты. Действий совершено: {actions}. Золота собрано: {gold_total}")

        if inventory:
            print("Left behind in the backpack:")
            for name, qty in inventory.items():
                print(f"{name}: {qty} pcs")
        else:
            print("Left behind in the backpack: nothing.")

        print_run_summary(log)
    else:
        print("Игра завершена до создания персонажа.")
    print(frame)
