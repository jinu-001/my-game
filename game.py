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

print("Как зовут героя?")
hero_name = input()
print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.")
print()

menu_last = 7
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
                    if i % 3 == 0:
                        hit_damage = crit_damage
                        crit_marker = " — критический!"
                        crit_count += 1
                    else:
                        hit_damage = damage
                        crit_marker = ""
                    
                    total_damage += hit_damage
                    print(f"Удар {i}: {hit_damage:.1f} урона{crit_marker}")
                
                average_damage = total_damage / strikes
                stamina_cost = 4
                stamina = stamina - stamina_cost

                print()
                print(f"Итог: {strikes} ударов, критических ударов: {crit_count}")
                print(f"Общий нанесённый урон: {total_damage:.1f}")
                print(f"Средний урон за удар: {average_damage:.1f}")
                print(f"Затраты сил на тренировку: {stamina_cost}")
                
            case "7":
                print("You descend the stairs...")
                if not enemies:
                    print("but the dungeon is empty")
                else:
                    enemy = random.choice(enemies)
                    enemy_hp = 45.0
                    round_n = 0
                    print(f"A {enemy} emerges from the darkness!")
                    print()
                    
                    hero_hits = 0
                    while enemy_hp > 0 and health > 0:
                        round_n += 1
                        hero_hits += 1
                        
                        if hero_hits % 3 == 0:
                            hit_damage = crit_damage
                            is_crit = True
                        else:
                            hit_damage = damage
                            is_crit = False
                            
                        enemy_hp -= hit_damage
                        
                        if enemy_hp <= 0:
                            enemy_damage = 0
                            if is_crit:
                                print(f"Round {round_n}: hero hits {hit_damage:.1f}, enemy hp: 0.0. critical! The enemy falls.")
                            else:
                                print(f"Round {round_n}: hero hits {hit_damage:.1f}, enemy hp: 0.0. The enemy falls.")
                            log.append(f"round {round_n}: hero -{hit_damage:.1f}, {enemy} -{enemy_damage}")
                            break
                        else:
                            enemy_damage = random.randint(2, 6)
                            health -= enemy_damage
                            print(f"Round {round_n}: hero hits {hit_damage:.1f}, enemy hp: {enemy_hp:.1f}, enemy hits back: {enemy_damage}")
                            log.append(f"round {round_n}: hero -{hit_damage:.1f}, {enemy} -{enemy_damage}")
                    
                    print()
                    if enemy_hp <= 0:
                        enemies.remove(enemy)
                        print(f"The {enemy} is defeated! {len(enemies)} enemies left in the dungeon.")
                    
                    print(f"Combat: {round_n} rounds.")
                    print(f"Последняя строка боя из журнала: {log[-1]}")

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
    print(frame)
