import datetime
import tkinter as tk

from typing import Optional
from functools import partial
from tkinter import ttk
from tkinter import messagebox as mb

from new_classes.digit import digit
from new_classes.buttons import DigitButton, OperationButton, PointButton, ResultButton
from new_classes.calculator import Calculator, History

class view_history(tk.Toplevel):
    def __init__(self, id_history: Optional[datetime.datetime], root: tk.Tk,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        try:
            self.id = id_history
            self.history = History().load_from_database(id_history)
        except:
            self.history = root.history
            self.id = root.history.get_id()
            if root.history.empty():
                return
            mb.showwarning(title="Предупреждение", message="Если вы произвели новые вычисления, то для корректного отображения истории вычислений вам нужно снова открыть данный раздел из главной программы.")
        self.title(f"История от {self.id}")
        self.iconbitmap(default="favicon.ico")
        self.geometry("400x400+400+200")
        self.resizable(False, False)
        self.update_idletasks()
        self.attributes("-toolwindow", True)

        self.main_canvas = tk.Canvas(self, borderwidth=0)
        self.main_frame = ttk.Frame(self.main_canvas)

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")

        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.main_canvas.xview)
        self.main_canvas.configure(xscrollcommand=self.hsb.set)
        self.hsb.pack(side="bottom", fill="x")

        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_canvas.create_window((4, 4), window=self.main_frame, anchor="nw")

        sep = ttk.Separator(self.main_frame, orient=tk.HORIZONTAL)
        sep.pack(side=tk.TOP, fill=tk.X)

        for i, j in self.history:
            op, rs = j.parse_to_display()
            frame_i = ttk.Frame(self.main_frame)

            label_i = ttk.Label(frame_i, text=f"{i}", justify='left')
            label_i.pack(side=tk.LEFT)

            sep = ttk.Separator(frame_i, orient=tk.VERTICAL)
            sep.pack(side=tk.LEFT, fill=tk.Y)

            frame_disp_out = ttk.Frame(frame_i)

            label_x_op = ttk.Label(frame_disp_out, text=f"{op}", justify='left')
            label_x_op.pack(anchor=tk.NW, padx=10, pady=5)

            frame_disp_in = ttk.Frame(frame_disp_out)

            label_x_rs = ttk.Label(frame_disp_in, text=f"Вычислено: {rs}", justify='right', borderwidth=1)
            label_x_rs.pack(side=tk.LEFT)

            btn_append = ttk.Button(frame_disp_in, text="Подставить результат", command=partial(self.__append_cmd, rs))
            btn_append.pack(side=tk.RIGHT)

            frame_disp_in.pack(side=tk.BOTTOM, ipadx=10, ipady=5)

            frame_disp_out.pack(side=tk.LEFT, ipadx=10)

            frame_i.pack(side=tk.TOP, fill=tk.X, ipadx=10, ipady=5)

            sep = ttk.Separator(self.main_frame, orient=tk.HORIZONTAL)
            sep.pack(side=tk.TOP, fill=tk.X)

        self.main_canvas.update_idletasks() 
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

        self.update()

    def __append_cmd(self, res: str):
        self.root.input_lb["text"] = f"{res}"

class main_root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.geometry("415x380+400+200") # размер, но лучше автоматический
        self.title('Калькулятор')
        self.iconbitmap(default="favicon.ico")
        self.update_idletasks()
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.__finish)
        self.attributes("-alpha", 1.0)

        self.bind('<Left>', lambda e: self.attributes("-alpha", 0.5))
        self.bind('<Enter>', lambda e: self.attributes("-alpha", 1))

        # self.attributes("-toolwindow", True) # Только крестик - в диалогах

        self.main = True
        self.arg2 = None
        self.history = History(1)
        self.calc = Calculator()
        self.first_page = True
        self.first_page_buf = None
        self.pinned = False

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_command(label='Закрепить окно', command=self.__pin_window)
        self.menubar.add_cascade(label='Вид', menu=self.view_menu)

        self.history_menu = tk.Menu(self.menubar, tearoff=0)
        self.history_menu.add_command(label=f'Очистить историю вычислений',
                                      command=lambda: History.delete_all_from_database())
        self.history_menu.add_separator()
        self.history_menu.add_command(label=f'Просмотреть текущую историю',
                                    command=lambda: view_history(self.history.get_id(), root=self) \
                                        if not self.history.empty() else mb.showinfo(title=f"Текущая история", message="На данный момент ещё не было произведено вычислений."))
        flag = True
        for i in self.history.get_all_from_database():
            if i:
                if flag:
                    self.history_menu.add_separator()
                    flag = False
                self.history_menu.add_command(label=f'От {i.get_id()}...',
                                              command=partial(self.__summon_win, f"{i.get_id()}"))
        self.menubar.add_cascade(label='История вычислений...', menu=self.history_menu)

        self.input_lb = ttk.Label(text="0", justify='left')
        self.input = ttk.Entry(width=30, justify='right')
        self.input.bind('<KeyPress>', self.__on_key_press_entry)
        self.bind('<KeyPress>', self.__on_key_press)

        self.swap_interface = ttk.Button(command=self.__swap_cmd)
        self.C_button = ttk.Button(text="Очистить всё", command=self.__C_cmd)
        self.CE_button = ttk.Button(text="Очистить число", command=self.__CE_cmd)
        self.del_button = ttk.Button(text="Удалить символ", command=self.__del_cmd)

        self.input_lb.grid(column=0, columnspan=4, row=1, rowspan=1,
                           sticky=tk.NW, padx=10, pady=10)
        self.input.grid(column=0, columnspan=4, row=2, rowspan=1,
                        sticky=tk.NE, padx=10, pady=10)
        self.swap_interface.grid(column=0, columnspan=1, row=3, rowspan=1,
                                 padx=10, pady=10)
        self.C_button.grid(column=1, columnspan=1, row=3, rowspan=1,
                           padx=10, pady=10)
        self.CE_button.grid(column=2, columnspan=1, row=3, rowspan=1,
                            padx=10, pady=10)
        self.del_button.grid(column=3, columnspan=1, row=3, rowspan=1,
                             padx=10, pady=10)

        self.calc_buttons_first = []
        self.calc_buttons_second = {0: [], 1: [], 2: []}
        self.__render_first()

        self.update()

    def __summon_win(self, id: str):
        x = view_history(id_history=id, root=self)

    def __pin_window(self):
        self.pinned = ~self.pinned
        a, b = "Закрепить окно", "Открепить окно"
        if not self.pinned: a, b = b, a
        self.view_menu.entryconfigure(a, label=b)
        self.attributes("-topmost", self.pinned)

    def __on_key_press_entry(self, event):
        if event.keysym == 'Return':
            self.__result_cmd()
            return 'break'
        allowed_chars = set('0123456789.')
        symbol = event.char
        if symbol in allowed_chars or event.keysym in ['BackSpace', 'Delete']:
            current_value = self.input.get()
            if current_value.count('.') >= 1 and symbol == '.':
                return 'break'
            if event.keysym in ['BackSpace', 'Delete']:
                current_value = current_value[:-1]
            self.input.delete(0, tk.END)
            self.input.insert(0, current_value)
        else:
            return 'break'

    def __on_key_press(self, event):
        self.input.focus_set()
        if event.keysym == 'Return':
            self.__result_cmd()
            return 'break'

    def __render_first(self):
        self.input.focus_set()
        self.swap_interface["text"] = "Другое"
        for i in self.calc_buttons_second[0]:
            i.grid_remove()
        for i in self.calc_buttons_second[1]:
            i.grid_remove()
        for i in self.calc_buttons_second[2]:
            i.grid_remove()
        self.first_page = True
        self.first_page_buf = None
        if len(self.calc_buttons_first) == 0:
            for i in range(5, 8):
                for j in range(0, 3):
                    self.calc_buttons_first.append(DigitButton(7 + j - 3 * (i - 5),
                        command=partial(self.__digit_cmd, f"{7 + j - 3 * (i - 5)}")))
                    self.calc_buttons_first[-1].grid(column=j, columnspan=1, row=i, rowspan=1,
                                                     padx=10, pady=10)

            self.calc_buttons_first.append(OperationButton("1/x", command=self.__1dx_cmd))
            self.calc_buttons_first[-1].grid(column=0, columnspan=1, row=4, rowspan=1,
                                             padx=10, pady=10)
            self.calc_buttons_first.append(OperationButton("x ** 2", command=self.__pow2_cmd))
            self.calc_buttons_first[-1].grid(column=1, columnspan=1, row=4, rowspan=1,
                                             padx=10, pady=10)
            self.calc_buttons_first.append(OperationButton("sqrt(x)", command=partial(self.__cmd_f_x, "sqrt")))
            self.calc_buttons_first[-1].grid(column=2, columnspan=1, row=4, rowspan=1,
                                             padx=10, pady=10)

            self.calc_buttons_first.append(OperationButton("+/-", command=self.__posneg_cmd))
            self.calc_buttons_first[-1].grid(column=0, columnspan=1, row=8, rowspan=1,
                                             padx=10, pady=10)
            self.calc_buttons_first.append(DigitButton(0, command=partial(self.__digit_cmd, "0")))
            self.calc_buttons_first[-1].grid(column=1, columnspan=1, row=8, rowspan=1,
                                             padx=10, pady=10)
            self.calc_buttons_first.append(PointButton(".", command=self.__point_cmd))
            self.calc_buttons_first[-1].grid(column=2, columnspan=1, row=8, rowspan=1,
                                             padx=10, pady=10)

            self.calc_buttons_first.append(OperationButton("/", command=self.__div_cmd))
            self.calc_buttons_first[-1].grid(column=3, columnspan=1, row=4, rowspan=1,
                                             padx=10, pady=10)
            self.calc_buttons_first.append(OperationButton("*", command=self.__mul_cmd))
            self.calc_buttons_first[-1].grid(column=3, columnspan=1, row=5, rowspan=1,
                                             padx=10, pady=10)
            self.calc_buttons_first.append(OperationButton("-", command=self.__sub_cmd))
            self.calc_buttons_first[-1].grid(column=3, columnspan=1, row=6, rowspan=1,
                                             padx=10, pady=10)
            self.calc_buttons_first.append(OperationButton("+", command=self.__add_cmd))
            self.calc_buttons_first[-1].grid(column=3, columnspan=1, row=7, rowspan=1,
                                             padx=10, pady=10)

            self.calc_buttons_first.append(ResultButton(command=self.result_cmd))
            self.calc_buttons_first[-1].grid(column=3, columnspan=1, row=8, rowspan=1,
                                             padx=10, pady=10)
        else:
            for i in self.calc_buttons_first:
                i.grid()

    def __render_part(self):
        if self.first_page == self.first_page_buf: return
        cnt = 0
        a, b = tk.DISABLED, tk.NORMAL
        flag = True
        for i in self.calc_buttons_second[0]:
            if cnt > 1 and flag:
                a, b = b, a
                flag = False
            i["state"] = a if self.first_page else b
            cnt += 1
        if self.first_page:
            for i in self.calc_buttons_second[2]:
                i.grid_remove()
            if len(self.calc_buttons_second[1]) == 0:
                self.calc_buttons_second[1].append(OperationButton("sin(x)", command=partial(self.__cmd_f_x, "sin")))
                self.calc_buttons_second[1][-1].grid(column=0, columnspan=1, row=5, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("sinh(x)", command=partial(self.__cmd_f_x, "sinh")))
                self.calc_buttons_second[1][-1].grid(column=1, columnspan=1, row=5, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("asin(x)", command=partial(self.__cmd_f_x, "asin")))
                self.calc_buttons_second[1][-1].grid(column=2, columnspan=1, row=5, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("asinh(x)", command=partial(self.__cmd_f_x, "asinh")))
                self.calc_buttons_second[1][-1].grid(column=3, columnspan=1, row=5, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[1].append(OperationButton("cos(x)", command=partial(self.__cmd_f_x, "cos")))
                self.calc_buttons_second[1][-1].grid(column=0, columnspan=1, row=6, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("cosh(x)", command=partial(self.__cmd_f_x, "cosh")))
                self.calc_buttons_second[1][-1].grid(column=1, columnspan=1, row=6, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("acos(x)", command=partial(self.__cmd_f_x, "acos")))
                self.calc_buttons_second[1][-1].grid(column=2, columnspan=1, row=6, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("acosh(x)", command=partial(self.__cmd_f_x, "acosh")))
                self.calc_buttons_second[1][-1].grid(column=3, columnspan=1, row=6, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[1].append(OperationButton("tg(x)", command=partial(self.__cmd_f_x, "tg")))
                self.calc_buttons_second[1][-1].grid(column=0, columnspan=1, row=7, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("tgh(x)", command=partial(self.__cmd_f_x, "tgh")))
                self.calc_buttons_second[1][-1].grid(column=1, columnspan=1, row=7, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("atg(x)", command=partial(self.__cmd_f_x, "atg")))
                self.calc_buttons_second[1][-1].grid(column=2, columnspan=1, row=7, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("atgh(x)", command=partial(self.__cmd_f_x, "atgh")))
                self.calc_buttons_second[1][-1].grid(column=3, columnspan=1, row=7, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[1].append(OperationButton("ctg(x)", command=partial(self.__cmd_f_x, "ctg")))
                self.calc_buttons_second[1][-1].grid(column=0, columnspan=1, row=8, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("ctgh(x)", command=partial(self.__cmd_f_x, "ctgh")))
                self.calc_buttons_second[1][-1].grid(column=1, columnspan=1, row=8, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("actg(x)", command=partial(self.__cmd_f_x, "actg")))
                self.calc_buttons_second[1][-1].grid(column=2, columnspan=1, row=8, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("actgh(x)", command=partial(self.__cmd_f_x, "actgh")))
                self.calc_buttons_second[1][-1].grid(column=3, columnspan=1, row=8, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[1].append(OperationButton("sec(x)", command=partial(self.__cmd_f_x, "sec")))
                self.calc_buttons_second[1][-1].grid(column=0, columnspan=1, row=9, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("sech(x)", command=partial(self.__cmd_f_x, "sech")))
                self.calc_buttons_second[1][-1].grid(column=1, columnspan=1, row=9, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("asec(x)", command=partial(self.__cmd_f_x, "asec")))
                self.calc_buttons_second[1][-1].grid(column=2, columnspan=1, row=9, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("asech(x)", command=partial(self.__cmd_f_x, "asech")))
                self.calc_buttons_second[1][-1].grid(column=3, columnspan=1, row=9, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[1].append(OperationButton("csc(x)", command=partial(self.__cmd_f_x, "csc")))
                self.calc_buttons_second[1][-1].grid(column=0, columnspan=1, row=10, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("csch(x)", command=partial(self.__cmd_f_x, "csch")))
                self.calc_buttons_second[1][-1].grid(column=1, columnspan=1, row=10, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("acsc(x)", command=partial(self.__cmd_f_x, "acsc")))
                self.calc_buttons_second[1][-1].grid(column=2, columnspan=1, row=10, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[1].append(OperationButton("acsch(x)", command=partial(self.__cmd_f_x, "acsch")))
                self.calc_buttons_second[1][-1].grid(column=3, columnspan=1, row=10, rowspan=1,
                                                     padx=10, pady=10)
            else:
                for i in self.calc_buttons_second[1]:
                    i.grid()
        else:
            for i in self.calc_buttons_second[1]:
                i.grid_remove()
            if len(self.calc_buttons_second[2]) == 0:
                self.calc_buttons_second[2].append(OperationButton("a ** x",
                    command=partial(self.__f2_x_cmd, "pow", "возвести в спепень")))
                self.calc_buttons_second[2][-1].grid(column=0, columnspan=1, row=5, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("e ** x",
                    command=partial(self.__cmd_f_x, "exp")))
                self.calc_buttons_second[2][-1].grid(column=1, columnspan=1, row=5, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("//",
                    command=partial(self.__f2_x_cmd, "div", "делить нацело на")))
                self.calc_buttons_second[2][-1].grid(column=2, columnspan=1, row=5, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("%",
                    command=partial(self.__f2_x_cmd, "mod", "на", "Остаток от деления числа")))
                self.calc_buttons_second[2][-1].grid(column=3, columnspan=1, row=5, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[2].append(OperationButton("ln(x)",
                    command=partial(self.__cmd_f_x, "ln")))
                self.calc_buttons_second[2][-1].grid(column=0, columnspan=1, row=6, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("lg(x)",
                    command=partial(self.__cmd_f_x, "lg")))
                self.calc_buttons_second[2][-1].grid(column=1, columnspan=1, row=6, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("log_2(x)",
                    command=partial(self.__cmd_f_x, "log2")))
                self.calc_buttons_second[2][-1].grid(column=2, columnspan=1, row=6, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("log_a(x)",
                    command=partial(self.__f2_x_cmd, "log", "от числа", "Логарифм по основанию")))
                self.calc_buttons_second[2][-1].grid(column=3, columnspan=1, row=6, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[2].append(OperationButton("Округлить вверх",
                    command=partial(self.__cmd_f_x, "ceil")))
                self.calc_buttons_second[2][-1].grid(column=0, columnspan=1, row=7, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("Округлить вниз",
                    command=partial(self.__cmd_f_x, "floor")))
                self.calc_buttons_second[2][-1].grid(column=1, columnspan=1, row=7, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("Округлить до знака",
                    command=partial(self.__f2_x_cmd, "round", "округлить до знака после запятой номер")))
                self.calc_buttons_second[2][-1].grid(column=2, columnspan=1, row=7, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("!x",
                    command=partial(self.__cmd_f_x, "factorial")))
                self.calc_buttons_second[2][-1].grid(column=3, columnspan=1, row=7, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[2].append(OperationButton("Модуль",
                    command=partial(self.__cmd_f_x, "abs")))
                self.calc_buttons_second[2][-1].grid(column=0, columnspan=1, row=8, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("Поменять знак",
                    command=partial(self.__cmd_f_x, "swapsign")))
                self.calc_buttons_second[2][-1].grid(column=1, columnspan=1, row=8, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("В радианы",
                    command=partial(self.__cmd_f_x, "radians")))
                self.calc_buttons_second[2][-1].grid(column=2, columnspan=1, row=8, rowspan=1,
                                                    padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("В градусы",
                    command=partial(self.__cmd_f_x, "degrees")))
                self.calc_buttons_second[2][-1].grid(column=3, columnspan=1, row=8, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[2].append(OperationButton("Инверсия",
                    command=partial(self.__cmd_f_x, "~")))
                self.calc_buttons_second[2][-1].grid(column=0, columnspan=1, row=9, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("a & x",
                    command=partial(self.__f2_x_cmd, "&", "И")))
                self.calc_buttons_second[2][-1].grid(column=1, columnspan=1, row=9, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("a | x",
                    command=partial(self.__f2_x_cmd, "|", "ИЛИ")))
                self.calc_buttons_second[2][-1].grid(column=2, columnspan=1, row=9, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("a -> x",
                    command=partial(self.__f2_x_cmd, "imp", "следует", "Из")))
                self.calc_buttons_second[2][-1].grid(column=3, columnspan=1, row=9, rowspan=1,
                                                     padx=10, pady=10)

                self.calc_buttons_second[2].append(OperationButton("Е",
                    command=partial(self.__const_cmd, "E")))
                self.calc_buttons_second[2][-1].grid(column=0, columnspan=1, row=10, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("ПИ",
                    command=partial(self.__const_cmd, "PI")))
                self.calc_buttons_second[2][-1].grid(column=1, columnspan=1, row=10, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("a << x",
                    command=partial(self.__f2_x_cmd, "lshift", "побитово сдвинуть влево на")))
                self.calc_buttons_second[2][-1].grid(column=2, columnspan=1, row=10, rowspan=1,
                                                     padx=10, pady=10)
                self.calc_buttons_second[2].append(OperationButton("a >> x",
                    command=partial(self.__f2_x_cmd, "rshift", "побитово сдвинуть вправо на")))
                self.calc_buttons_second[2][-1].grid(column=3, columnspan=1, row=10, rowspan=1,
                                                     padx=10, pady=10)
            else:
                for i in self.calc_buttons_second[2]:
                    i.grid()

    def __render_1_cmd(self):
        self.first_page_buf = self.first_page
        self.first_page = True
        self.__render_part()

    def __render_2_cmd(self):
        self.first_page_buf = self.first_page
        self.first_page = False
        self.__render_part()

    def __render_second(self):
        self.input.focus_set()
        self.swap_interface["text"] = "Назад"
        for i in self.calc_buttons_first:
            i.grid_remove()
        if len(self.calc_buttons_second[0]) == 0:
                self.calc_buttons_second[0].append(ttk.Button(text="<<", state=tk.DISABLED,
                                                              command=self.__render_1_cmd))
                self.calc_buttons_second[0][-1].grid(column=0, columnspan=1, row=4, rowspan=1,
                                                padx=10, pady=10)
                self.calc_buttons_second[0].append(ttk.Button(text="1", state=tk.DISABLED,
                                                              command=self.__render_1_cmd))
                self.calc_buttons_second[0][-1].grid(column=1, columnspan=1, row=4, rowspan=1,
                                                padx=10, pady=10)
                self.calc_buttons_second[0].append(ttk.Button(text="2", state=tk.NORMAL,
                                                              command=self.__render_2_cmd))
                self.calc_buttons_second[0][-1].grid(column=2, columnspan=1, row=4, rowspan=1,
                                                padx=10, pady=10)
                self.calc_buttons_second[0].append(ttk.Button(text=">>", state=tk.NORMAL,
                                                              command=self.__render_2_cmd))
                self.calc_buttons_second[0][-1].grid(column=3, columnspan=1, row=4, rowspan=1,
                                                padx=10, pady=10)
        else:
            for i in self.calc_buttons_second[0]:
                i.grid()
        self.__render_part()




    def __read_for_cmds(self) -> Optional[digit]:
        s = self.input.get()
        if s == ".":
            x = 0
        elif len(s) != 0:
            x = s
        else:
            if self.arg2 is not None:
                return None
            else:
                x = ""
                nab = [*set("0123456789.-e")]
                for i in self.input_lb["text"]:
                    if i in nab:
                        if i == '.' or i == '-' or i == 'e':
                            ind = nab.index(i)
                            nab.pop(ind)
                        x += i
                try:
                    x = float(x)
                except:
                    return digit(0)
        return digit(x)

    def __const_cmd(self, s: str):
        self.input.delete(0, tk.END)
        self.input.insert(0, digit(s))

    def __f2_x_cmd(self, operation: str, comment: str, comment2: Optional[str] = None):
        x = self.__read_for_cmds()
        if self.arg2 is None:
            self.calc.init_operation(f"{operation}({x},")
            self.arg2 = f"{operation}"
        elif x is not None:
            self.calc.add_to_operation(f"{x}")
            if self.calc.calculate():
                self.input_lb["text"] = "0"
                self.arg2 = None
                rs = self.calc.result
                self.calc.clear()
                mb.showerror(title="Ошибка вычисления", message=rs)
                return
            self.calc.init_operation(f"{operation}({self.calc.result},")
        else:
            self.calc.swap_operation_to(f"{operation}")
        self.input_lb["text"] = (f"{comment2} " if comment2 else "") + f"{self.calc.get_without_operation()} {comment} ..."
        self.input.delete(0, tk.END)

    def __cmd_f_x(self, f: str):
        x = self.__read_for_cmds()
        if x is not None:
            self.calc.init_operation(f"{f}({x})")
            s = repr(self.calc)
            if self.calc.calculate():
                rs = self.calc.result
                self.calc.clear()
                mb.showerror(title="Ошибка вычисления", message=rs)
                return
            self.input_lb["text"] = f"= {self.calc.result}"
            self.input.delete(0, tk.END)
            if s != "": self.history += s
        else:
            mb.showerror(title="Ошибка", message="Вы не закончили ввод операции.")

    def __div_cmd(self):
        x = self.__read_for_cmds()
        self.input.delete(0, tk.END)
        if self.arg2 is None:
            self.calc.init_operation(f"{x}/")
            self.arg2 = "/"
        elif x is not None:
            self.calc.add_to_operation(f"{x}")
            if self.calc.calculate():
                self.input_lb["text"] = "0"
                self.arg2 = None
                rs = self.calc.result
                self.calc.clear()
                mb.showerror(title="Ошибка вычисления", message=rs)
                return
            self.calc.init_operation(f"{self.calc.result}/")
        else:
            self.calc.swap_operation_to("/")
        self.input_lb["text"] = f"{self.calc.get_without_operation()} делить на ..."
        self.input.delete(0, tk.END)

    def __mul_cmd(self):
        x = self.__read_for_cmds()
        if self.arg2 is None:
            self.calc.init_operation(f"{x}*")
            self.arg2 = "*"
        elif x is not None:
            self.calc.add_to_operation(f"{x}")
            if self.calc.calculate():
                self.input_lb["text"] = "0"
                self.arg2 = None
                rs = self.calc.result
                self.calc.clear()
                mb.showerror(title="Ошибка вычисления", message=rs)
                return
            self.calc.init_operation(f"{self.calc.result}*")
        else:
            self.calc.swap_operation_to("*")
        self.input_lb["text"] = f"{self.calc.get_without_operation()} умножить на ..."
        self.input.delete(0, tk.END)

    def __sub_cmd(self):
        x = self.__read_for_cmds()
        if self.arg2 is None:
            self.calc.init_operation(f"{x}-")
            self.arg2 = "0"
        elif x is not None:
            self.calc.add_to_operation(f"{x}")
            if self.calc.calculate():
                self.input_lb["text"] = "0"
                self.arg2 = None
                rs = self.calc.result
                self.calc.clear()
                mb.showerror(title="Ошибка вычисления", message=rs)
                return
            self.calc.init_operation(f"{self.calc.result}-")
        else:
            self.calc.swap_operation_to("-")
        self.input_lb["text"] = f"{self.calc.get_without_operation()} уменьшить на ..."
        self.input.delete(0, tk.END)

    def __add_cmd(self):
        x = self.__read_for_cmds()
        if self.arg2 is None:
            self.calc.init_operation(f"{x}+")
            self.arg2 = "+"
        elif x is not None:
            self.calc.add_to_operation(f"{x}")
            if self.calc.calculate():
                self.input_lb["text"] = "0"
                self.arg2 = None
                rs = self.calc.result
                self.calc.clear()
                mb.showerror(title="Ошибка вычисления", message=rs)
                return
            self.calc.init_operation(f"{self.calc.result}+")
        else:
            self.calc.swap_operation_to("+")
        self.input_lb["text"] = f"{self.calc.get_without_operation()} увеличить на ..."
        self.input.delete(0, tk.END)

    def result_cmd(self):
        x = self.__read_for_cmds()
        if x is not None:
            self.calc.add_to_operation(f"{x}")
            self.arg2 = None
            s = repr(self.calc)
            if self.calc.calculate():
                rs = self.calc.result
                self.calc.clear()
                mb.showerror(title="Ошибка вычисления", message=rs)
                return
            self.input_lb["text"] = f"= {self.calc.result}"
            self.input.delete(0, tk.END)
            if s != "": self.history += s
        else:
            mb.showerror(title="Ошибка", message="Вы не закончили ввод операции.")

    def __posneg_cmd(self):
        x = self.__read_for_cmds()
        if x is not None:
            self.input.delete(0, tk.END)
            if x == 0:
                self.input.insert(0, "0")
            elif x > 0:
                self.input.insert(0, f"-{x}")
            else:
                self.input.insert(0, f"{x}"[1:])

    def __pow2_cmd(self):
        x = self.__read_for_cmds()
        if x is not None:
            self.calc.init_operation(f"pow2({x})")
            s = repr(self.calc)
            if self.calc.calculate():
                rs = self.calc.result
                self.calc.clear()
                mb.showerror(title="Ошибка вычисления", message=rs)
                return
            self.input_lb["text"] = f"= {self.calc.result}"
            self.input.delete(0, tk.END)
            if s != "": self.history += s
        else:
            mb.showerror(title="Ошибка", message="Вы не закончили ввод операции.")

    def __1dx_cmd(self):
        x = self.__read_for_cmds()
        if x is not None:
            self.calc.init_operation(f"1/{x}")
            s = repr(self.calc)
            if self.calc.calculate():
                rs = self.calc.result
                self.calc.clear()
                mb.showerror(title="Ошибка вычисления", message=rs)
                return
            self.input_lb["text"] = f"= {self.calc.result}"
            self.input.delete(0, tk.END)
            if s != "": self.history += s
        else:
            mb.showerror(title="Ошибка", message="Вы не закончили ввод операции.")

    def __point_cmd(self):
        s = self.input.get()
        self.input.delete(0, tk.END)
        if '.' in s:
            if s[-1] == '.': s = s[:-1]
            else: s = ''.join(x for x in s if x != '.') + '.'
        else:
            s += '.'
        self.input.insert(0, s)

    def __digit_cmd(self, x: str):
        self.input.insert(tk.END, x)

    def __C_cmd(self):
        self.calc.clear()
        self.input_lb["text"] = "0"
        self.input.delete(0, tk.END)

    def __CE_cmd(self):
        self.input.delete(0, tk.END)

    def __del_cmd(self):
        self.input.delete(tk.END)

    def __swap_cmd(self):
        if self.main:
            self.__render_second()
            self.main = False
        else:
            self.__render_first()
            self.main = True
        self.first_page = True
        self.first_page_buf = None

    def __finish(self):
        flag = mb.askyesno(title="Выход", message="Вы уверены, что хотите выйти?")
        if flag:
            self.destroy()
            if not self.history.empty():
                self.history.save_to_database()
