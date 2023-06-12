from enum  import Enum

class Position(tuple):
    max_valid_x: int = 5 #default overridable
    max_valid_y: int = 5 #default overridable
    x: int
    y: int
    def __new__(cls, iterable):
        if len(iterable) != 2:
            raise ValueError("引数は2つの要素を持つTupleです")
        if not (0 <= iterable[0] <= Position.max_valid_x and 0 <= iterable[1] <= Position.max_valid_y):
            raise ValueError("座標が範囲外です")
        return super().__new__(cls, iterable)

    @property
    def x(self):
        return self[0]
    
    @property
    def y(self):
        return self[1]
    
    def print(self):
        print(f'{self.x}, {self.y}')

class Direction(Enum):
    UP = 0
    UP_RIGHT = 1
    RIGHT = 2
    DOWN_RIGHT = 3
    DOWN = 4
    DOWN_LEFT = 5
    LEFT = 6
    UP_LEFT = 7

    def next(self, current: Position, inc: int)-> Position:
        match self:
            case self.UP:
                return Position((current.x, current.y-inc))
            case self.UP_RIGHT:
                return Position((current.x+inc, current.y-inc))
            case self.RIGHT:
                return Position((current.x+inc, current.y ))
            case self.DOWN_RIGHT:
                return Position((current.x+inc, current.y+inc))
            case self.DOWN:
                return Position((current.x, current.y+inc))
            case self.DOWN_LEFT:
                return Position((current.x-inc, current.y+inc))
            case self.LEFT:
                return Position((current.x-inc, current.y))
            case self.UP_LEFT:
                return Position((current.x-inc, current.y-inc))

class Course:
    def __init__(self, start_position: Position, direction: Direction, size):
        self.direction = direction
        self.positions = [direction.next(start_position, i) for i in range(size)]

    def is_matched(self, target_word, char_to_positions):
        return all(
            [position in char_to_positions[target_word[idx]] 
             for idx, position in enumerate(self.positions)
            ]
        )  
    
    @classmethod
    def create_and_valdate_courses(cls, position, target_word, char_to_positions):
        courses = []
        for direction in Direction: # 全方向で作成
            try:
                course = Course(position, direction, len(target_word))
                if course.is_matched(target_word, char_to_positions):
                    courses.append(course)
            except ValueError:
                next
        return courses

class ResultPrinter():
    def __init__(self, matched)->None:
        self.matched = matched
    
    def print(self):
        for course in matched:
            for p in course.positions:
                p.print()
            print('-----')

target_word = 'snuke'
target_map = [
    ['s', 'b', 'c', 'd', 'e', 'f'],
    ['n', 's', 'c', 'd', 'e', 'f'],
    ['u', 'b', 'n', 'd', 'e', 'f'],
    ['k', 's', 'n', 'u', 'k', 'e'],
    ['e', 'b', 'c', 'd', 'k', 'f'],
    ['a', 'b', 'c', 'd', 'e', 'e'],
]

char_to_positions = {char: set() for char in target_word}

for y_idx, row in enumerate(target_map):
    for x_idx, char in enumerate(row):
        if char in char_to_positions:
            char_to_positions[char].add(Position((x_idx, y_idx)))

matched = []
first_char_idx = 0
first_char = target_word[first_char_idx]
first_char_positions: set = char_to_positions[first_char]
for position in first_char_positions:
    matched += Course.create_and_valdate_courses(position, target_word, char_to_positions)

printer = ResultPrinter(matched)
printer.print()
