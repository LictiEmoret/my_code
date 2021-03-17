
"""
Игра змейка в консоли. 
Управление: стрелочками на клавиатуре.
"""

import time
import os
import random
from pynput import keyboard
import sys


class Field():
    def __init__(self, score, size):
        # объект класса Score
        self.score = score

        # разрешение нюанса с очищением консоли в windows и linux
        if os.name == 'nt':
            self.clear_console = 'cls'
        else:
            self.clear_console = 'clear'

        # задержка между отрисовками поля
        self.delay = 0.15

        # наполнение поля с размерами size_of_field х size_of_field
        self.size_of_field = size
        self.field = [['.' for j in range(size_of_field)] for i in range(size_of_field)]
        for i in range(2):
            self.field[i][1] = '*'

    def sleep(self, delay):
        time.sleep(delay)

    def dec_delay(self, decrement):
        if (self.delay - decrement) < 0:
            pass
        else:
            self.delay -= decrement

    # отрисовка поля в консоли
    def view_field(self):
        os.system(self.clear_console)
        s = ''
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                s += self.field[i][j]
                s += '  '
            s += '\n'
        print(s)
        print('score: ', self.score.score)
        self.sleep(self.delay)
        

class Stuff():
    def __init__(self, field):
        self.stuff_coord = [0, 0]
        self.field = field

    # ставит частичку змеи * в рандомное место на поле 
    def make_stuff(self):
        is_norm = True
        while is_norm:

            x1 = int(random.uniform(1, len(self.field.field) - 1))
            y1 = int(random.uniform(1, len(self.field.field[0]) - 1))

            if self.field.field[x1][y1] == '*':
                continue
            else:
                self.field.field[x1][y1] = '*'
                self.stuff_coord[0], self.stuff_coord[1] = x1, y1
                is_norm = False

    # проверяет есть ли впереди головы змеи координаты рандомной частички змеи *
    def its_coord_stuff(self, current_soord, stuff_coord):
        if current_soord == stuff_coord:
            return True
        else:
            return False



class Moves():
    def __init__(self, field, stuff, score):
        self.field = field
        self.stuff = stuff
        self.score = score
        self.snake = ['*','*']
        self.coord_for_seconds_move = [['just']]
        self.ls_for_seconds_moves = [len(self.snake)]
        self.global_y1 = 1
        self.global_x1 = 1
        # массив с функциями для перемещений
        self.move_list = [self.fvd]
        # словарь соответствия клавишам функций для перемещения
        self.dict_moves = {'d':self.fhr, 's':self.fvd, 'w':self.fvu, 'a':self.fhl}

    # декоратор для обработки врезания змеи в край поля
    def dec_for_clash(func):
        def wrap(self, *args):
            try:
                func(self, *args)
            except:
                os.system(field.clear_console)
                print('YOU DIED!!!1', 'YOUR SCORE: {}\n'.format(self.score.score), sep='\n')
                sys.exit()
        return wrap

    #перемещение частички змеи по горизонтали вправо 
    @dec_for_clash
    def fhr(self, len_section, coord_kor, flag_for_seconds_or_main_foo):
        x1 = coord_kor[0]
        y1 = coord_kor[1]

        stuff = False

        if self.field.field[x1][y1 + 1] == '*' and flag_for_seconds_or_main_foo:

            if self.stuff.its_coord_stuff([x1, y1 + 1], self.stuff.stuff_coord):
                y1 += 1
                len_section += 1
                self.snake.append('*')
                self.ls_for_seconds_moves[0] = len(self.snake)
                stuff = True
                self.stuff.make_stuff()
                self.score.inc_score()
            else:
                raise Exception 
        
        self.field.field[x1][y1 + 1], self.field.field[x1][y1 - (len_section - 1)] = self.field.field[x1][y1 - (len_section - 1)], self.field.field[x1][y1 + 1]
        
        if flag_for_seconds_or_main_foo:
            self.global_y1 += 1

        if stuff:
            self.global_y1 += 1

    # перемещение частички змеи по горизонтали влево
    @dec_for_clash
    def fhl(self, len_section, coord_kor, flag_for_seconds_or_main_foo):
        x1 = coord_kor[0]
        y1 = coord_kor[1]
        
        stuff = False

        if self.field.field[x1][y1 - 1] == '*' and flag_for_seconds_or_main_foo:

            if self.stuff.its_coord_stuff([x1, y1 - 1], self.stuff.stuff_coord):
                y1 -= 1
                len_section += 1
                self.snake.append('*')
                self.ls_for_seconds_moves[0] = len(self.snake)
                stuff = True
                self.stuff.make_stuff()
                self.score.inc_score()
            else:
                raise Exception

        if y1 == 0:
            raise Exception

        self.field.field[x1][y1 - 1], self.field.field[x1][y1 + (len_section - 1)] = self.field.field[x1][y1 + (len_section - 1)], self.field.field[x1][y1 - 1]
            
        if flag_for_seconds_or_main_foo:
            self.global_y1 -= 1

        if stuff:
            self.global_y1 -= 1    

    # перемещение частички змеи по вертикали вниз
    @dec_for_clash
    def fvd(self, len_section, coord_kor, flag_for_seconds_or_main_foo):
        x1 = coord_kor[0]
        y1 = coord_kor[1]

        stuff = False

        if self.field.field[x1 + 1][y1] == '*' and flag_for_seconds_or_main_foo:

            if self.stuff.its_coord_stuff([x1 + 1, y1], self.stuff.stuff_coord):
                x1 += 1
                len_section += 1
                self.snake.append('*')
                self.ls_for_seconds_moves[0] = len(self.snake)
                stuff = True
                self.stuff.make_stuff()
                self.score.inc_score()
            else:
                raise Exception

        self.field.field[x1 + 1][y1], self.field.field[x1 - (len_section - 1)][y1] = self.field.field[x1 - (len_section - 1)][y1], self.field.field[x1 + 1][y1]
            
        if flag_for_seconds_or_main_foo:
            self.global_x1 += 1

        if stuff:
            self.global_x1 += 1
    
    # перемещение частички змеи по вертикали вверх
    @dec_for_clash
    def fvu(self, len_section, coord_kor, flag_for_seconds_or_main_foo):
        x1 = coord_kor[0]
        y1 = coord_kor[1]

        stuff = False

        if self.field.field[x1 - 1][y1] == '*' and flag_for_seconds_or_main_foo:

            if self.stuff.its_coord_stuff([x1 - 1, y1], self.stuff.stuff_coord):
                x1 -= 1
                len_section += 1
                self.snake.append('*')
                self.ls_for_seconds_moves[0] = len(self.snake)
                stuff = True
                self.stuff.make_stuff()
                self.score.inc_score()
            else:
                raise Exception

        if x1 == 0:
            raise Exception

        self.field.field[x1 - 1][y1], self.field.field[x1 + (len_section - 1)][y1] = self.field.field[x1 + (len_section - 1)][y1], self.field.field[x1 - 1][y1]
            
        if flag_for_seconds_or_main_foo:
            self.global_x1 -= 1

        if stuff:
            self.global_x1 -= 1

    # определяет координаты начала секции где произошел поворот змеи
    def previous_coord(self, move, previous_move):
        if (move == self.fhr or move == self.fhl) and previous_move == self.fvd:
            self.coord_for_seconds_move.append([self.global_x1 - 1, self.global_y1])

        if (move == self.fhr or move == self.fhl) and previous_move == self.fvu:
            self.coord_for_seconds_move.append([self.global_x1 + 1, self.global_y1])

        if (move == self.fvu or move == self.fvd) and previous_move == self.fhr:
            self.coord_for_seconds_move.append([self.global_x1, self.global_y1 - 1])

        if (move == self.fvu or move == self.fvd) and previous_move == self.fhl:
            self.coord_for_seconds_move.append([self.global_x1, self.global_y1 + 1])

    # проверка, являются ли две функции противоположны по направлению движения 
    def def_opposite_move(self, one, two):
        op_1 = (self.fhr, self.fhl)
        op_2 = (self.fvu, self.fvd)

        if one in op_1 and two in op_1:
            return False

        if one in op_2 and two in op_2:
            return False
        
        return True

    
class Snake():
    def __init__(self, moves):
        # объект класса Moves
        self.moves = moves
        
    def make_move(self, move):
        # проверка на то, чтобы не было поторяющихся ходов и ходов в разных направлениях
        if (self.moves.dict_moves[move] != self.moves.move_list[-1]) and self.moves.def_opposite_move(self.moves.dict_moves[move], self.moves.move_list[-1]):
            move = self.moves.dict_moves[move]
            self.moves.move_list.append(move)

            # так как ходы вставляются в конец, то мне нужно проверить послдний и предпоследний вставленные элементы
            # чтобы правильным образом вычислить координаты где происходит поворот частей змеи
            self.moves.previous_coord(move, self.moves.move_list[-2])

            if len(self.moves.move_list) == 2:
                ls_for_more_seconds_moves = self.moves.ls_for_seconds_moves[0] - 1
                self.moves.ls_for_seconds_moves.append(ls_for_more_seconds_moves) #!!!!!!!
                    
            else:
                ls_for_more_seconds_moves = len(self.moves.snake) - sum(self.moves.ls_for_seconds_moves[1:]) - 1
                self.moves.ls_for_seconds_moves.append(ls_for_more_seconds_moves)

        count_for_seconds_move = len(self.moves.move_list)

        for i in range(len(self.moves.move_list) - 1, -1, -1):
        
            ls_for_head = len(self.moves.snake) - sum(self.moves.ls_for_seconds_moves[1:])

            if i == len(self.moves.move_list) - 1:
                foo = self.moves.move_list[i]
                foo(ls_for_head, [self.moves.global_x1, self.moves.global_y1], True) 

            else:
                # счетчик для получения длин и координат не главных секций
                count_for_seconds_move -= 1
                foo = self.moves.move_list[i]
                foo(self.moves.ls_for_seconds_moves[count_for_seconds_move], self.moves.coord_for_seconds_move[count_for_seconds_move], False)

                if i == 0:
                    # в конце цикла проверяется длина самой последней секции, (только она декрементится) если она нулевая то удаляется все связанные с ней вещи 
                    self.moves.ls_for_seconds_moves[count_for_seconds_move] -= 1

                    if self.moves.ls_for_seconds_moves[count_for_seconds_move] == 0:
                        del self.moves.move_list[i]
                        del self.moves.coord_for_seconds_move[count_for_seconds_move]
                        del self.moves.ls_for_seconds_moves[count_for_seconds_move]


class Score():
    def __init__(self):
        self.score = 0
        self.field = None

    # инкремент очков
    def inc_score(self):
        self.score += 1
        if not (self.score % 5):
            self.field.dec_delay(0.05)


class Qeue():
    def __init__(self, field, stuff, score):
        Qeue.Moves = Moves(field, stuff, score)

    qeue = ['s']
    fl_for_qeue = False

    # если в очереди один элемент то заменяет его на более новый, 
    # если в очереди уже имеются элементы то просто добавляет новые элементы в конец 
    def ap_qeue(key):
        if Qeue.fl_for_qeue and Qeue.qeue[0] != key and Qeue.Moves.def_opposite_move(Qeue.Moves.dict_moves[key], Qeue.Moves.dict_moves[Qeue.qeue[0]]):
            Qeue.qeue.insert(0, key)

        if not Qeue.fl_for_qeue and Qeue.Moves.def_opposite_move(Qeue.Moves.dict_moves[key], Qeue.Moves.dict_moves[Qeue.qeue[0]]):
            Qeue.qeue[0] = key
            Qeue.fl_for_qeue = True
    
    def get_move(self):
        move = None
        if len(Qeue.qeue) > 1:
            move = Qeue.qeue.pop()

            if len(Qeue.qeue) == 1:
                Qeue.fl_for_qeue = False

        else:
            move = Qeue.qeue[0]
            Qeue.fl_for_qeue = False

        return move

    
class KeyProcess():
    def __init__(self, keyboard):
        self.listener = keyboard.Listener(on_press=KeyProcess.onPress)
        self.listener.start()

    # обработчик нажатий клавиатуры
    def onPress(key):
        if key == keyboard.Key.up:
            Qeue.ap_qeue('w')

        if key == keyboard.Key.down:
            Qeue.ap_qeue('s')

        if key == keyboard.Key.right:
            Qeue.ap_qeue('d')

        if key == keyboard.Key.left:
            Qeue.ap_qeue('a')


score = Score()
size_of_field = 20
field = Field(score, size_of_field)
score.field = field
stuff = Stuff(field)
moves = Moves(field, stuff, score)
qeue = Qeue(field, stuff, score)
key = KeyProcess(keyboard)
snake = Snake(moves)
stuff.make_stuff()

while True:
    move = qeue.get_move()
    snake.make_move(move)
    field.view_field()
    
