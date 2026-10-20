# ================================================
# ИГРА «СОЛЯНЫЕ ШАХТЫ»
# Автор: Александр Алиев
# Дата: сентябрь 2026
# Решение о равенстве: при наличии одинаковых по силе
# максимальных ударов врага, функция max возвращает
# первую такую строку благодаря свойству устойчивости.
# Это осознанный выбор для сохранения хронологии.
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
            raise ValueError(f"Здоровье должно быть больше нуля, а введено {health}")
        if health > 500:
            raise ValueError(f"Здоровье слишком огромно (максимум 500), а введено {health}")
        if strength < 0 or agility < 0 or endurance < 0 or max_stamina < 0:
            raise ValueError("Характеристики персонажа не могут быть отрицательными")
        if strength > 100:
            raise ValueError(f"Предел силы превышен (максимум 100), а введено {strength}")
            
        break
    except ValueError as e:
        print(f"\n[Ошибка]: {e}. Введите все пять характеристик снова:\n")

stamina = max_stamina  
print()

enemies = ["ghoul", "skeleton", "spider", "bat"]
log = []

base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2

def hero_hit(strike_n):
    """
    Принимает: порядковый номер удара strike_n (int).
    Возвращает: кортеж (hit_damage: float, is_crit: bool).
    Ничего не печатает и не меняет глобальное состояние.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False

def fight(enemy, hero_health):
    """
    Принимает: имя врага enemy (str), текущее здоровье героя hero_health (int).
    Возвращает: кортеж (rounds: list, won: bool, hero_health: int).
    Печатает: ход сражения по раундам. Глобальные переменные не меняет.
    """
    enemy_hp = 45.0
    rounds = []
    round_n = 0
    print(f"You descend the stairs. Out of the darkness comes {enemy}!")
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
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
            line += f" {enemy} health: {enemy_hp:.1f}. {enemy.capitalize()} hits for {blow}."
            rounds.append([round_n, hit, blow])
        print(line)
    return rounds, enemy_hp <= 0, hero_health

def print_leaderboard(log):
    """
    Принимает: журнал боя log (list).
    Возвращает: None.
    Печатает: топ-3 раундов по урону героя и самый сильный пропущенный удар.
    """
    if not log:
        print("You haven't fought yet.")
        return
    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
    print("Leaderboard (hero damage):")
    for i in range(len(top)):
        print(f"{i + 1}. Round {top[i][0]}: {top[i][1]:.1f}")
    worst = max(log, key=lambda r: r[2])
    print(f"Strongest enemy hit: {worst[2]} (round {worst[0]}).")

def print_run_summary(log):
    """
    Принимает: журнал боя log (list).
    Возвращает: None.
    Печатает: суммарный и средний нанесенный урон героя за весь забег.
    """
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Damage: {total:.1f} across {rounds} rounds, average {total / rounds:.1f}.")
    else:
        print("No battles this run.")

print("Как зовут героя?")
hero_name = input()
print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.")
print()

menu_last = 8
running = True
actions = 0

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
        print("0 - выйти из подземелья")
        print()

        while True:
            choice = input("Выберите действие: ")
            try:
                menu_number = int(choice)
            except ValueError:
                print("Ошибка: нужно ввести числовой номер пункта меню. Попробуйте снова.")
                continue
            if 0 <= menu_number <= menu_last:
                choice = str(menu_number)
                break
            print(f"Такого пункта нет. Введите число от 0 до {menu_last}.")

        match choice:
            case "1":
                print("Вы осмотрелись. Комната пуста, только пыль на полу.")
            case "2":
                cost = 2
                if stamina >= cost:
                    stamina -= cost
                    print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
                else:
                    health -= (cost - stamina)
                    stamina = 0
                    print("Сил больше нет — вы идёте на одном упорстве.")
            case "3":
                if stamina < max_stamina:
                    stamina += 1
                    print("Вы присели отдохнуть на соляной блок. Усталость постепенно уходит.")
                else:
                    print("Вы полны сил и готовы к действиям! Отдыхать больше нет смысла.")
            case "4":
                print("Вы замерли и прислушались. Где-то вдалеке капает вода, опасности не слышно.")
            case "5":
                stamina = stamina - 1
                print("Вы чиркнули кресалом и зажгли факел. Тратится энергия, но стало гораздо светлее.")
            case "6":
                strikes = 6
                print("Вы подходите к массивной глыбе соли, испещрённой старыми сколами.")
                print("Предыдущие рабочие использовали её для проверки остроты кирок и своей силы.")
                print()
                print(f"Наносите серию из {strikes} ударов.")
                
                total_damage = 0.0
                crit_count = 0

                for i in range(1, strikes + 1):
                    hit_damage, crit = hero_hit(i)
                    if crit:
                        crit_count += 1
                        print(f"Удар {i}: {hit_damage:.1f} урона — критический!")
                    else:
                        print(f"Удар {i}: {hit_damage:.1f} урона")
                    total_damage += hit_damage
                
                average_damage = total_damage / strikes
                stamina_cost = 4
                stamina = stamina - stamina_cost

                print()
                print(f"Итог: {strikes} ударов, критических ударов: {crit_count}")
                print(f"Общий нанесённый урон: {total_damage:.1f}")
                print(f"Средний урон за удар: {average_damage:.1f}")
                print(f"Затраты сил на тренировку: {stamina_cost}")
                
            case "7":
                if not enemies:
                    print("You descend the stairs. But the dungeon is empty.")
                else:
                    enemy = random.choice(enemies)
                    rounds, won, health = fight(enemy, health)
                    for r in rounds:
                        log.append(r)
                    if won:
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon.")
                    print(f"Battle: {len(rounds)} rounds.")

            case "8":
                print_leaderboard(log)

            case "0":
                print("Вы поднимаетесь из глубоких соляных шахт обратно к солнцу.")
                print("Свежий воздух приятно обдувает лицо после душных пещер.")
                outcome = "выход"
                running = False

        if health <= 0:
            print(f"{hero_name} падает без сил на холодный пол. Шахты забирают ещё одну жизнь.")
            outcome = "гибель"
            running = False

        if running:
            actions += 1

        print()
        print(f"[ Состояние героя — Здоровье: {max(0, health)} | Запас сил: {stamina} ]")
        print("-" * 50)
        print()

except KeyboardInterrupt:
    print()
    print("Игрок прервал сеанс.")
finally:
    print(frame)
    if outcome == "гибель":
        print(f"Ты не дошёл, {hero_name}. Соляные шахты оказались сильнее.")
        print(f"Увы, подземный поход окончен трагически. Действий совершено: {actions}.")
    elif outcome == "выход":
        print(f"Забег окончен, {hero_name}. Вы успешно выбрались на поверхность!")
        print(f"Отличная работа, возвращайтесь в лагерь с добычей. Действий совершено: {actions}.")
    else:
        print(f"Сеанс прерван, {hero_name}. Твоё путешествие внезапно оборвалось.")
        print(f"Вынужденная остановка посреди темноты. Действий совершено: {actions}.")
        
    print_run_summary(log)
    print(frame)
