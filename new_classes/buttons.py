from tkinter import ttk

class CalcButton(ttk.Button):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.styles = ttk.Style(self)
        self.styles.configure('Default.TButton',
                              background='#aaffaa',
                              foreground='#007700',
                              highlightbackground='#000000',
                              highlightcolor='#dd00dd',
                              borderwidth=1)
        self.styles.configure('Operational.TButton',
                              background='#ffaaaa',
                              foreground='#770000',
                              highlightbackground='#000000',
                              highlightcolor='#dd00dd',
                              borderwidth=1)
        self.styles.configure('Result.TButton',
                              background='#dd00dd',
                              foreground='#770077',
                              highlightbackground='#000000',
                              highlightcolor='#dd00dd',
                              borderwidth=1)
        self["style"] = 'Default.TButton'

class DigitButton(CalcButton):
    def __init__(self, x: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self["text"] = x

class OperationButton(CalcButton):
    def __init__(self, display: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self["style"] = 'Operational.TButton'
        self["text"] = display

class PointButton(CalcButton):
    def __init__(self, display: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self["style"] = 'Operational.TButton'
        self["text"] = display

class ResultButton(CalcButton):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self["text"] = '='
        self["style"] = 'Result.TButton'
