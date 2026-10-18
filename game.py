# ================================================
# ИГРА «СОЛЯНЫЕ ШАХТЫ»
# Автор: Александр Алиев
# Дата: сентябрь 2026
# ================================================

# --- Заголовок ------------------------------------
title = "СОЛЯНЫЕ ШАХТЫ"
frame = "=" * 19
print(frame)
print(" " + title + " ")
print(frame)

# --- Настройка героя -------------------------------
print("Введите начальные характеристики героя.")
health = int(input("Здоровье: "))
strength = int(input("Сила: "))
agility = int(input("Ловкость: "))
endurance = int(input("Выносливость: "))
max_stamina = int(input("Запас сил: "))
stamina = max_stamina  
print()

# --- Расчёт базового урона -------------------------
base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2

# --- Знакомство с героем --------------------------
print("Как зовут героя?")
hero_name = input()
print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.")
print()

# --- Главный цикл игры -----------------------------
running = True
actions = 0

while running:
    # --- Меню действий ---------------------------------
    print("Что делаешь?")
    print("1 - осмотреться")
    print("2 - идти вперёд")
    print("3 - отдохнуть")
    print("4 - прислушаться")
    print("5 - зажечь факел")
    print("6 - тренировка")
    print("0 - выйти из подземелья")
    print()

    # --- Выбор героя и защита от неверного ввода -------
    valid = ("0", "1", "2", "3", "4", "5", "6")
    choice = input("Выберите действие: ")
    
    while choice not in valid:
        print("Такого пункта нет. Введи номер пункта из меню.")
        choice = input("Выберите действие: ")

    # --- Обработка действий ----------------------------
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
            
        case "0":
            print("Вы поднимаетесь из глубоких соляных шахт обратно к солнцу.")
            print("Свежий воздух приятно обдувает лицо после душных пещер.")
            running = False

    # --- Проверка гибели героя -------------------------
    if health <= 0:
        print(f"{hero_name} падает без сил на холодный пол. Шахты забирают ещё одну жизнь.")
        running = False

    # --- Подсчёт действий ------------------------------
    if running:
        actions += 1

    # --- Строка состояния героя ------------------------
    print()
    print(f"[ Состояние героя — Здоровье: {max(0, health)} | Запас сил: {stamina} ]")
    print("-" * 50)
    print()

# --- Прощание с разветвлением -----------------------
print(frame)
if health <= 0:
    print(f"Ты не дошёл, {hero_name}. Соляные шахты оказались сильнее.")
    print(f"Действий совершено: {actions}.")
else:
    print(f"Забег окончен, {hero_name}. Вы успешно выбрались на поверхность!")
    print(f"Действий совершено: {actions}.")
print(frame)
