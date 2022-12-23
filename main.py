import random


class Ship:
    def __init__(self, location, lives):
        self.location = location
        self.lives = lives

    def is_alive(self):
        return self.lives > 0

    def get_location(self):
        return self.location

    def hit(self):
        self.lives = self.lives - 1


class Dot:
    def __init__(self, x, y, status):
        self.x = x
        self.y = y
        self.status = status

    def set_status(self, new):
        self.status = new
        return self.status

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_status(self):
        return self.status


class Desk:
    def __init__(self, visible):
        self.visible = visible

    def create_dots(self):
        dots_list = []
        for x in range(6):
            for y in range(6):
                d = Dot(x, y, 'empty')
                dots_list.append(d)
        return dots_list

    def draw(self, dots):
        print(' \t| 1 |\t| 2 |\t| 3 |\t| 4 |\t| 5 |\t| 6 |', end=' ')
        count = 0
        for x in range(6):
            print()
            print(f'{x+1}\t', end='')
            for y in range(6):
                if dots[count].status == "hit":
                    print(f'| X |\t', end='')
                elif dots[count].status == "ship" and self.visible:
                    print(f'| ■ |\t', end='')
                elif dots[count].status == "scan":
                    print(f'| T |\t', end='')
                else:
                    print(f'| О |\t', end='')
                count = count + 1
        print()

    def create_ships(self, dots_list):
        # количество палуб на кораблях
        palubs = [3, 2, 2, 1, 1, 1, 1]
        # при таком количестве кораблей иногда возникает ситуация,
        # что для последнего корабля нет места, для этого я создаю список координат всех клеток
        clear_dots = []
        for x in range(6):
            for y in range(6):
                d = (x, y)
                clear_dots.append(d)
        # если места для последнего корабля не найдется, то расставлять корабли сначала
        do_it_again = True
        while do_it_again:
            do_it_again = False
            # список кораблей
            def_ships = []
            # клетки, на которых или стоит корабль, или соседние от корабля
            ban = []
            correct = False
            # отчищаем клетки от предыдущий расставлений
            for dot in dots_list:
                dot.set_status('empty')
            # начинаем расставление кораблей
            for s in palubs:
                while correct is False:
                    correct = True
                    # если все клетки на поле заняты, или соседствуют с кораблем,
                    # то для последнего корабля не будет места, а значит выходим из цикла
                    # и начинаем расставлять корабли заново
                    if len(list(set(clear_dots) - set(ban))) == 0:
                        do_it_again = True
                        if self.visible:
                            input('Больше нет мест для корабля. Начните заново.')
                        break
                    # если доска видимая, значит расставляет пользователь, если нет, то компьютер
                    if self.visible:
                        ship_x = int(input(f'Строчка на которую вы поставите {s}-палубный корабль: ')) - 1
                        ship_y = int(input(f'Столбик на которую вы поставите {s}-палубный корабль: ')) - 1
                        if s == 1:
                            loc = 1
                        else:
                            loc = int(input('Введите 1, если корабль стоит горизонтально и 2 если вертикально: '))
                    else:
                        ship_x = random.randrange(6)
                        ship_y = random.randrange(6)
                        loc = random.randint(1, 2)
                    # проверки на корректность введенных данных, если проверка не пройдена,
                    # то вписываем новую координату
                    if loc >= 3 or loc <= 0:
                        if self.visible:
                            print("Вы ввели неправильную ориентацию корабля.")
                        correct = False
                    if ship_x > 5 or ship_x < 0:
                        if self.visible:
                            print('Вы ввели несуществующую строчку')
                        correct = False
                    if ship_y > 5 or ship_y < 0:
                        if self.visible:
                            print('Вы ввели несуществующий столбик')
                        correct = False
                    if loc == 1 and ship_y+(s-1) >= 6:
                        if self.visible:
                            print('Корабль не помещается')
                        correct = False
                    if loc == 2 and ship_x+(s-1) >= 6:
                        if self.visible:
                            print('Корабль не помещается')
                        correct = False
                    if loc == 1 and ((ship_x, ship_y) in ban or (ship_x, ship_y + s - 1) in ban):
                        if self.visible:
                            print('Корабль пересекается или находится слишком близко с другим кораблем')
                        correct = False
                    if loc == 2 and ((ship_x, ship_y) in ban or (ship_x + s - 1, ship_y) in ban):
                        if self.visible:
                            print('Корабль пересекается или находится слишком близко с другим кораблем')
                        correct = False
                # тут будут храниться точки, на которых стоит корабль
                dots = []
                # жизней у корабля столько же сколько и палуб
                lives = s
                # ищем в цикле нужные точки и меняем их статус
                for dot in dots_list:
                    if s > 0:
                        if dot.get_x() == ship_x and dot.get_y() == ship_y:
                            for i in range(3):
                                for j in range(3):
                                    first = ship_x-1 + i
                                    second = ship_y - 1 + j
                                    ban.append((first, second))
                            dots.append(dot)
                            dot.set_status('ship')
                            if loc == 1:
                                ship_y = ship_y + 1
                            else:
                                ship_x = ship_x + 1
                            s = s - 1
                correct = False
                if do_it_again:
                    break
                # поставленный корабль вписываем в список кораблей
                ship = Ship(dots, lives)
                def_ships.append(ship)
                if self.visible:
                    self.draw(dots_list)
        return def_ships

    def create_vision(self):
        self.visible = True

    def ship_count(self, ships):
        count = 0
        for ship in ships:
            if ship.is_alive():
                count = count + 1
        return count

    def is_visible(self):
        return self.visible


class Game:
    @staticmethod
    def start(user_desk, user_dots, user_ship, ai_desk, ai_dots, ai_ship):
        end_game = True
        winner = None
        while end_game:
            print('Ваше поле: ')
            user_desk.draw(user_dots)
            print(f'Осталось {user_desk.ship_count(user_ship)} кораблей на плаву ')
            print('Мое поле: ')
            ai_desk.draw(ai_dots)
            print(f'Осталось {ai_desk.ship_count(ai_ship)} кораблей на плаву ')
            ai_desk, ai_dots, ai_ship = Game.move(ai_desk, ai_dots,  ai_ship)
            print(f'У меня осталось {Game.statistic(ai_ship)} кораблей')
            if Game.statistic(ai_ship) == 0:
                winner = "Поздравляю, вы победили!"
                break
            user_desk, user_dots, user_ship = Game.move(user_desk, user_dots, user_ship)
            if Game.statistic(ai_ship) == 0:
                winner = "Конец игры, я победил."
                break
        return user_desk, user_dots, user_ship, ai_desk, ai_dots, ai_ship, winner

    @staticmethod
    def move(desk, dots, ships):

        end_move = False

        while end_move is False:
            if desk.is_visible() is False:
                scan_x = int(input('Введите строчку проверяемой ячейки: ')) - 1
                scan_y = int(input('Введите столбик проверяемой ячейки: ')) - 1
            else:
                scan_x = random.randrange(6)
                scan_y = random.randrange(6)
            if scan_x > 5 or scan_x < 0:
                print('Вы ввели несуществующую строчку')
            if scan_y > 5 or scan_y < 0:
                print('Вы ввели несуществующий столбик')
            for dot in dots:
                if dot.get_x() == scan_x and dot.get_y() == scan_y:
                    if dot.get_status() == 'empty':
                        dot.set_status('scan')
                        print(f'Поле {scan_x + 1}, {scan_y +1} было пустым')
                        end_move = True
                    elif dot.get_status() == 'ship':
                        for ship in ships:
                            ship_dots = ship.get_location()
                            if dot in ship_dots:
                                dot.set_status('hit')
                                ship.hit()
                                if desk.is_visible() is False:
                                    if ship.is_alive():
                                        print(f'Вы подбили корабль на поле {scan_x + 1}, {scan_y + 1} ')
                                    else:
                                        print(f'Вы потопили корабль, выстрелив по полю {scan_x + 1}, {scan_y + 1} ')
                                        if Game.statistic(ships) == 0:
                                            end_move = True
                                else:
                                    if ship.is_alive():
                                        print(f'Подбит ваш корабль на поле {scan_x + 1}, {scan_y + 1} ')
                                    else:
                                        print(f'Потоплен ваш корабль выстрелом по полю {scan_x + 1}, {scan_y + 1}')
                    else:
                        if desk.is_visible() is False:
                            print(f'Вы уже стреляли по полю {scan_x + 1}, {scan_y +1}')
                    break
        return desk, dots, ships

    @staticmethod
    def statistic(ships):
        count = 0
        for ship in ships:
            if ship.is_alive():
                count = count + 1
        return count


# Создаем поле игрока, корабли на которой будут отображаться
user_desk = Desk(True)
# На поле создаем точки. У каждой точки есть ее кординаты и статус:
# 'empty' - пустая точка, 'ship' - точка на которой расположен корабль,
# 'hit' - точка на которой был подбит корабль , 'scan' - точка в которую стреляли, но там было пусто
user_dots_list = user_desk.create_dots()
# Расставляем корабли на поле из точек
user_ships_list = user_desk.create_ships(user_dots_list)

# Поле компьютера, на котором не будет видно кораблей, в остальном все тоже самое
ai_desk = Desk(False)
ai_dots_list = ai_desk.create_dots()
ai_ship_list = ai_desk.create_ships(ai_dots_list)
# начинаем игру, передавая все данные
user_desk, user_dots_list, user_ships_list, ai_desk, ai_dots_list, ai_ship_list, message = Game.start(user_desk, user_dots_list, user_ships_list, ai_desk, ai_dots_list, ai_ship_list)

print(message)
print('Ваше поле по окончанию игры:')
user_desk.draw(user_dots_list)
print('Мое поле по окончанию игры: ')
# делаем поле компьютера видимым
ai_desk.create_vision()
ai_desk.draw(ai_dots_list)
