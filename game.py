# ================================================
# ИГРА «СОЛЯНЫЕ ШАХТЫ»
# Автор: Александр Алиев
# Дата: сентябрь 2026
# ================================================

import random

title = "СОЛЯНЫЕ ШАХТЫ"
frame = "=" * 19
print(frame)
print(" " + title + " ")
print(frame)

while True:
    try:
        print("Введите начальные характеристики героя.")
        health = int(input("Здоровье: "))
        strength = int(input("Сила: "))
        agility = int(input("Ловкость: "))
        endurance = int(input("Выносливость: "))
        max_stamina = int(input("Запас сил: "))

        if health <= 0:
            raise ValueError(
                f"Здоровье должно быть больше нуля, а введено {health}"
            )
        if health > 500:
            raise ValueError(
                f"Здоровье слишком огромное (максимум 500), а введено {health}"
            )
        if strength < 0 or agility < 0 or endurance < 0 or max_stamina < 0:
            raise ValueError(
                "Характеристики персонажа не могут быть отрицательными"
            )
        if strength > 100:
            raise ValueError(
                f"Предел силы превышен (максимум 100), а введено {strength}"
            )

        break
    except ValueError as e:
        print(f"\n[Ошибка]: {e}. Введите все пять характеристик снова:\n")

max_health = health
stamina = max_stamina
print()

enemies = ["ghoul", "skeleton", "spider", "bat"]
log = []

base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2


def hero_hit(strike_n):
    """Рассчитывает урон героя за удар.

    Параметры:
        strike_n (int): Номер текущего удара.

    Возвращает:
        tuple:
            damage (float): Нанесённый урон.
            is_crit (bool): Флаг критического удара.

    Ничего не печатает.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health, bonus=0):
    """Проводит бой героя с противником.

    Параметры:
        enemy (str): Имя противника.
        hero_health (int): Текущее здоровье героя.
        bonus (float, по умолчанию 0): Дополнительный бонус к урону героя.

    Возвращает:
        tuple:
            rounds (list): Список записей раундов боя.
            won (bool): Флаг победы героя (True, если враг повержен).
            hero_health (int): Остаток здоровья героя после боя.
            loot (int): Количество добытого золота.

    Печатает лог каждого раунда боя.
    """
    enemy_hp = 45.0
    rounds = []
    round_n = 0

    print(f"You descend the stairs. Out of the darkness comes {enemy}!")

    while enemy_hp > 0 and hero_health > 0:
        round_n += 1

        hit, crit = hero_hit(round_n)
        hit += bonus
        enemy_hp -= hit

        line = f"Round {round_n}: hero deals {hit:.1f}"

        if crit:
            line += " - critical!"

        if enemy_hp <= 0:
            line += " Enemy falls."
            rounds.append([round_n, hit, 0])
        else:
            blow = random.randint(2, 6)
            hero_health -= blow

            line += (
                f" {enemy} health: {enemy_hp:.1f}."
                f" {enemy.capitalize()} hits for {blow}."
            )
            rounds.append([round_n, hit, blow])

        print(line)

    won = enemy_hp <= 0

    if won:
        loot = 10 + 5 * round_n
    else:
        loot = 0

    return rounds, won, hero_health, loot


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


def buy(price, gold, quantity=1):
    """Оформляет покупку товара в магазине.

    Параметры:
        price (int): Цена одной единицы товара.
        gold (int): Текущее количество золота у героя.
        quantity (int, по умолчанию 1): Количество покупаемого товара.

    Возвращает:
        tuple:
            remaining_gold (int): Остаток золота после покупки.
            success (bool): Флаг успешности покупки (True, если золота хватило).

    Ничего не печатает.
    """
    cost = price * quantity

    if gold >= cost:
        return gold - cost, True

    return gold, False


print("Как зовут героя?")
hero_name = input()

print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.")
print()

menu_last = 9
running = True
actions = 0
gold_total = 0
ability_bonus = 0

outcome = "прерывание"

try:
    while running:
        print("Что делаешь?")
        print("1 - осмотреться")
        print("2 - идти вперёд")
        print("3 - отдохнуть")
        print("4 - прислушаться")
        print("5 - зажечь факел")
        print("6 - тренировка")
        print("7 - descend deeper")
        print("8 - leaderboard")
        print("9 - shop")
        print("0 - выйти из подземелья")
        print()

        while True:
            choice = input("Выберите действие: ")

            try:
                menu_number = int(choice)
            except ValueError:
                print(
                    "Ошибка: нужно ввести числовой номер пункта меню. "
                    "Попробуйте снова."
                )
                continue

            if 0 <= menu_number <= menu_last:
                choice = str(menu_number)
                break

            print(
                f"Такого пункта нет. Введите число от 0 до {menu_last}."
            )

        match choice:
            case "1":
                print(
                    "Вы осмотрелись. Комната пуста, только пыль на полу."
                )

            case "2":
                cost = 2

                if stamina >= cost:
                    stamina -= cost
                    print(
                        "Вы осторожно идёте вперёд. Пол скрипит под ногами."
                    )
                else:
                    health -= cost - stamina
                    stamina = 0
                    print(
                        "Сил больше нет — вы идёте на одном упорстве."
                    )

            case "3":
                if stamina < max_stamina:
                    stamina += 1
                    print(
                        "Вы присели отдохнуть на соляной блок. "
                        "Усталость постепенно уходит."
                    )
                else:
                    print(
                        "Вы полны сил и готовы к действиям! "
                        "Отдыхать больше нет смысла."
                    )

            case "4":
                print(
                    "Вы замерли и прислушались. Где-то вдалеке "
                    "капает вода, опасности не слышно."
                )

            case "5":
                stamina -= 1
                print(
                    "Вы чиркнули кресалом и зажгли факел. "
                    "Тратится энергия, но стало гораздо светлее."
                )

            case "6":
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
                    hit_damage, crit = hero_hit(i)

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
                stamina -= stamina_cost

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

            case "7":
                if not enemies:
                    print(
                        "You descend the stairs. "
                        "But the dungeon is empty."
                    )
                else:
                    enemy = random.choice(enemies)

                    rounds, won, health, loot = fight(
                        enemy,
                        health,
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

            case "8":
                print_leaderboard(log)

            case "9":
                print("Shop:")
                print("1 - potion (+10 health): 10 gold")
                print("2 - torch oil (+5 stamina): 15 gold")
                print("3 - war elixir (+2 damage for the run): 40 gold")
                print("Item number (0 - not buying):")

                item = input()

                prices = (10, 15, 40)
                names = ("potion", "torch oil", "war elixir")

                if item in ("1", "2", "3"):
                    price = prices[int(item) - 1]
                    name = names[int(item) - 1]

                    print("Quantity (Enter for one):")
                    qty_line = input()

                    if qty_line == "":
                        qty = 1
                    else:
                        try:
                            qty = int(qty_line)
                        except ValueError:
                            qty = 0
                            print(
                                "Quantity must be a positive whole number."
                            )

                    if qty <= 0:
                        if qty_line != "":
                            print(
                                "Quantity must be a positive whole number."
                            )
                    else:
                        new_gold, ok = buy(
                            price,
                            gold_total,
                            quantity=qty
                        )

                        if ok:

                            gold_total = new_gold

                            if item == "1":
                                health = min(
                                    health + 10 * qty,
                                    max_health
                                )

                            elif item == "2":
                                stamina = min(
                                    stamina + 5 * qty,
                                    max_stamina
                                )

                            elif item == "3":
                                ability_bonus += 2 * qty

                            print(
                                f"Bought {qty} {name} for "
                                f"{price * qty} gold. "
                                f"Gold left: {gold_total}."
                            )
                        else:
                            print(
                                f"Not enough gold: need {price * qty}, "
                                f"have {gold_total}."
                            )

                elif item != "0":
                    print("No such item in the shop.")

            case "0":
                print(
                    "Вы поднимаетесь из глубоких соляных шахт "
                    "обратно к солнцу."
                )
                print(
                    "Свежий воздух приятно обдувает лицо "
                    "после душных пещер."
                )

                outcome = "выход"
                running = False

        if health <= 0:
            print(
                f"{hero_name} падает без сил на холодный пол. "
                "Шахты забирают ещё одну жизнь."
            )

            outcome = "гибель"
            running = False

        if running:
            actions += 1

        print()
        print(
            f"Health: {health} Stamina: {stamina} "
            f"Enemies left: {len(enemies)} Gold: {gold_total}"
        )
        print("-" * 50)
        print()

except KeyboardInterrupt:
    print()
    print("Игрок прервал сеанс.")

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

    print_run_summary(log)
    print(frame)
