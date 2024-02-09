import sqlite3
import datetime

from typing import Optional, Self, Iterable, ParamSpec, TypeVar

try:
    from digit import digit
except ImportError:
    from new_classes.digit import digit
from parser.parser import parser, parser_to_disp

F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")

class Calculator:
    operations: str
    result: digit|str

    def __init__(self, *, options: Optional[str] = None) -> None:
        if not options:
            self.operations = ""
            self.result = digit(0)
        else:
            self.operations, self.result = self.parse_repr_data(options)

    def __str__(self) -> str:
        return f"{self.result} " + ''.join([f"{i} " for i in self.operations.values()])

    def __repr__(self) -> str:
        try: self.result = parser(str(''.join(self.operations)))
        except: return ""
        if not self.with_operations(): return ""
        return f"{self.operations}  :  {self.result}"

    def with_operations(self) -> bool:
        """
        False - нет операций
        True - есть операции
        """
        try:
            digit(self.operations)
        except Exception:
            return True
        return False

    def is_literal_operation(self):
        return any(x.isalpha() for x in self.operations)

    def init_operation(self, operation: str) -> None:
        self.operations = f"{operation}"

    def get_digit_from_operation(self) -> digit:
        x = ""
        nab = [*set("0123456789.-")]
        for i in self.operations:
            if i in nab:
                if i == '.' or i == '-':
                    ind = nab.index(i)
                    nab.pop(ind)
                x += i
        return digit(x)

    def swap_operation_to(self, new_operation: str) -> None:
        x = self.get_digit_from_operation()
        self.operations = f"{new_operation}"
        if self.is_literal_operation():
            self.operations = f"{new_operation}({x},"
        else:
            self.operations = f"{x}{new_operation}"

    def get_without_operation(self) -> digit:
        return digit(('-' if self.operations[0] == '-' else "") + \
                     ''.join([x for x in self.operations if x in set('0123456789.')]))

    def add_to_operation(self, operation: str) -> None:
        flag = self.is_literal_operation()
        self.operations += f"{operation}" + (")" if flag else "")

    def clear(self) -> None:
        self.__init__()

    def calculate(self) -> bool:
        """
        True - были ошибки
        False - всё хорошо, ответ получен
        """
        try: self.result = parser(str(''.join(self.operations)))
        except OverflowError:
            self.result = "Слишком большое число."
            self.operations = ""
            return True
        except Exception as e:
            # raise e
            self.result = f'{e}'
            self.operations = ""
            return True
        self.operations = ""
        return False

    @classmethod
    def parse_repr_data(cls, self_repr: str) -> tuple[str, str]:
        return (x for x in self_repr.split('  :  '))

class HistoryElement(Calculator):
    def __init__(self, *, options: str|None = None) -> None:
        super().__init__(options=options)

    def parse_to_display(self) -> dict[str, str]:
        return parser_to_disp(self.operations), self.result

class History:
    __start: int
    __iter: list[HistoryElement]

    def __init__(self, start: Optional[int] = 0, *, item: Optional[any] = None,
                 items: Optional[Iterable[any]] = None, id: datetime.datetime|str = None) -> None:
        super().__init__()
        if not id:
            self.__id = datetime.datetime.now()
        elif isinstance(id, datetime.datetime):
            self.__id = id
        else:
            x = id.split()
            x = x[0].split('-') + x[1].split(':')
            x = x[:-1] + x[-1].split('.')
            x = [int(i) for i in x]
            self.__id = datetime.datetime(*x)
        self.__start = start
        self.__index = 0
        if item and items:
            raise ValueError("Нельзя указывать и 'item', и 'items' одновременно.")
        self.__iter = [HistoryElement(options=item)] if item else \
            list(HistoryElement(options=i) for i in items) if items else []

    def __str__(self) -> str:
        return '\n'.join(f"{x.parse_to_display()}" for x in self.__iter)

    def __len__(self) -> int:
        return len(self.__iter)

    def __contains__(self, __value: HistoryElement) -> bool:
        return __value in self.__iter

    def __next__(self) -> str:
        if self.__index < len(self.__iter):
            value = self.__index + self.__start, self.__iter[self.__index]
            self.__index += 1
            return value
        else:
            raise StopIteration

    def __reversed__(self) -> Self:
        new = History(self.__start, items=self.__iter[::-1])
        return new

    def __iter__(self) -> Self:
        self.__index = 0
        return self

    def __add__(self, __value: any) -> Self:
        self.__iter.append(HistoryElement(options=__value))
        return self

    def get_id(self) -> datetime.datetime:
        return self.__id

    def empty(self) -> bool:
        return len(self) == 0

    def save_to_database(self):
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                    id TEXT,
                    start INT,
                    item TEXT
                )''')

        cursor.execute('SELECT * FROM history WHERE id = ?', (str(self.__id),))
        existing_record = cursor.fetchone()

        if existing_record:
            for item in self.__iter:
                cursor.execute('UPDATE history SET start = ? item = ? WHERE id = ?', (self.__start, repr(item), str(self.__id)))
        else:
            for item in self.__iter:
                cursor.execute('INSERT INTO history (id, start, item) VALUES (?, ?, ?)', (str(self.__id), self.__start, repr(item)))

        conn.commit()
        conn.close()

        with open("ids.txt", "a") as f:
            print(f"Saved succesfully! Your ID is {self.__id}", file=f)

    def load_from_database(self, id: str):
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM history WHERE id = ?', (str(id),))
        data = cursor.fetchall()

        items, x = [], set()
        for i in data:
            items.append(i[2])
            x.add(i[1])
        for i in x:
            start = i

        conn.close()

        return History(id=id, start=start, items=items)

    def delete_from_database(self, id: str):
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM history WHERE id = ?', (str(id),))

        conn.commit()
        conn.close()

        s = ""
        with open("ids.txt", "r") as f:
            a = f.readlines()

        for i in a:
            if s in a: continue
            s += i + '\n'

        with open("ids.txt", "w") as f:
            f.write(s)

    def get_all_from_database_lazy(self):
        try:
            with open("ids.txt", "r") as f:
                s = [x for x in f.readlines()][::-1]
            for i in s:
                yield self.load_from_database(' '.join(i.split()[-2:]))
        except FileNotFoundError:
            yield

    def get_all_from_database(self):
        return [*self.get_all_from_database_lazy()]

    def delete_all_from_database(self):
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM history;')
        cursor.execute('VACUUM;')

        conn.commit()
        conn.close()

        with open("ids.txt", "w") as f:
            f.write("")
