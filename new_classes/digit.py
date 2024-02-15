import math

from typing import Self, Callable, ParamSpec, TypeVar, Optional, overload
from functools import wraps

F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")

@overload
def rounding(
    func: Callable[F_Spec, F_Return],
    *,
    ndigits: None = None
) -> Callable[F_Spec, F_Return]:
    ...

@overload
def rounding(
    func: None = None,
    *,
    ndigits: Optional[int] = 12
) -> Callable[
    [Callable[F_Spec, F_Return]],
    Callable[F_Spec, F_Return]
]: ... 

def __rounding_wrapper__(ndigits: Optional[int]) -> Callable[[Callable[F_Spec, F_Return]], Callable[F_Spec, F_Return]]:
    if ndigits is None: ndigits = 12
    def decorator(func: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:
        @wraps(func)
        def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            x = func(*args, **kwargs)
            x_round = digit(round(digit(x * float(f"1e{ndigits}"))) / float(f"1e{ndigits}"))
            if abs(x_round - x) < float(f"1e{-ndigits}"):
                return x_round
            else:
                return x
        return wrapper
    return decorator

def rounding(func = None, *, ndigits = None):
    wrap_decorator = __rounding_wrapper__(ndigits)
    if func is None:
        return wrap_decorator
    return wrap_decorator(func)

class MathError(ArithmeticError): pass

class digit:
    def __new__(cls, x: int|float|str|Self) -> Self:
        if isinstance(x, digit):
            return x
        return super().__new__(cls)

    def __init__(self, x: int|float|str|Self) -> None:
        if isinstance(x, digit):
            self.__x = x.__x
        elif x == "PI":
            self.__x = math.pi
        elif x == "E":
            self.__x = math.e
        elif x == "TAU":
            self.__x = math.tau
        elif isinstance(x, (int, str)):
            self.__x = float(x)
        elif isinstance(x, float):
            self.__x = x
        elif isinstance(x, complex):
            raise MathError('Число не существует.')
        else:
            raise ValueError('Неверный тип данных. Поддерживаются только int, str и float.')

    def __bytes__(self, encoding, error) -> bytes:
        return bytes(self.__x, encoding, error)

    def __str__(self) -> str:
        if self.isint():
            return f"{int(self)}"
        else:
            return f"{self.__x}"

    def __int__(self) -> int:
        return int(self.__x)

    def __float__(self) -> float:
        return self.__x

    def isint(self) -> bool:
        return float(int(self)) == self

    def __bool__(self) -> bool:
        return True if self > 0 else False

    def __lt__(self, __value: int|float|Self) -> bool:
        if isinstance(__value, (int, float)):
            return self.__x < __value
        elif isinstance(__value, digit):
            return self.__x < __value.__x
        else:
            raise TypeError('Неверный тип данных для операции сравнения. Поддерживаются только int, float и объекты digit.')

    def __eq__(self, __value: int|float|Self) -> bool:
        if isinstance(__value, (int, float)):
            return self.__x == __value
        elif isinstance(__value, digit):
            return self.__x == __value.__x
        else:
            raise TypeError('Неверный тип данных для операции сравнения. Поддерживаются только int, float и объекты digit.')

    def __le__(self, __value: int|float|Self) -> bool:
        if isinstance(__value, (int, float, digit)):
            return self < __value or self == __value
        else:
            raise TypeError('Неверный тип данных для операции сравнения. Поддерживаются только int, float и объекты digit.')

    def __ne__(self, __value: int|float|Self) -> bool:
        if isinstance(__value, (int, float, digit)):
            return not self == __value
        else:
            raise TypeError('Неверный тип данных для операции сравнения. Поддерживаются только int, float и объекты digit.')

    def __gt__(self, __value: int|float|Self) -> bool:
        if isinstance(__value, (int, float, digit)):
            return not self < __value
        else:
            raise TypeError('Неверный тип данных для операции сравнения. Поддерживаются только int, float и объекты digit.')

    def __ge__(self, __value: int|float|Self) -> bool:
        if isinstance(__value, (int, float, digit)):
            return self > __value or self == __value
        else:
            raise TypeError('Неверный тип данных для операции сравнения. Поддерживаются только int, float и объекты digit.')

    def __add__(self, __value: int|float|Self) -> Self:
        if isinstance(__value, (int, float)):
            return digit(self.__x + __value)
        elif isinstance(__value, digit):
            return digit(self.__x + __value.__x)
        else:
            raise TypeError('Неверный тип данных для операции сложения. Поддерживаются только int, float и объекты digit.')

    def __iadd__(self, __value: int|float|Self) -> Self:
        return self + __value

    def __radd__(self, __value: int|float) -> Self:
        return self + __value

    def __sub__(self, __value: int|float|Self) -> Self:
        if isinstance(__value, (int, float)):
            return digit(self.__x - __value)
        elif isinstance(__value, digit):
            return digit(self.__x - __value.__x)
        else:
            raise TypeError('Неверный тип данных для операции вычитания. Поддерживаются только int, float и объекты digit.')

    def __isub__(self, __value: int|float|Self) -> Self:
        return self - __value

    def __rsub__(self, __value: int|float) -> Self:
        if isinstance(__value, (int, float)):
            return digit(__value - self.__x)
        else:
            raise TypeError('Неверный тип данных для операции вычитания. Поддерживаются только int, float и объекты digit.')

    def __mul__(self, __value: int|float|Self) -> Self:
        if isinstance(__value, (int, float)):
            return digit(self.__x * __value)
        elif isinstance(__value, digit):
            return digit(self.__x * __value.__x)
        else:
            raise TypeError('Неверный тип данных для операции умножения. Поддерживаются только int, float и объекты digit.')

    def __imul__(self, __value: int|float|Self) -> Self:
        return self * __value

    def __rmul__(self, __value: int|float) -> Self:
        return self * __value

    def __neg__(self) -> Self:
        return -1 * self

    def __pos__(self) -> Self:
        return self

    def __abs__(self) -> Self:
        return -self if self < 0 else self

    def __truediv__(self, __value: int|float|Self) -> Self:
        try:
            if isinstance(__value, (int, float)):
                return digit(self.__x / __value)
            elif isinstance(__value, digit):
                return digit(self.__x / __value.__x)
            else:
                raise TypeError('Неверный тип данных для операции деления. Поддерживаются только int, float и объекты digit.')
        except ZeroDivisionError:
            raise MathError('На ноль делить нельзя!')

    def __itruediv__(self, __value: int|float|Self) -> Self:
        return self / __value

    def __rtruediv__(self, __value: int|float) -> Self:
        try:
            if isinstance(__value, (int, float)):
                return digit(__value / self.__x)
            else:
                raise TypeError('Неверный тип данных для операции деления. Поддерживаются только int, float и объекты digit.')
        except ZeroDivisionError:
                raise MathError('На ноль делить нельзя!')

    def __floordiv__(self, __value: int|float|Self) -> Self:
        try:
            if isinstance(__value, (int, float)):
                return digit(self.__x // __value)
            elif isinstance(__value, digit):
                return digit(self.__x // __value.__x)
            else:
                raise TypeError('Неверный тип данных для операции целочисленного деления. Поддерживаются только int и целые объекты digit.')
        except ZeroDivisionError:
            raise MathError('На ноль делить нельзя!')

    def __ifloordiv__(self, __value: int|float|Self) -> Self:
        return self // __value

    def __rfloordiv__(self, __value: int|float) -> Self:
        try:
            if isinstance(__value, (int, float)):
                return digit(__value // self.__x)
            else:
                raise TypeError('Неверный тип данных для операции целочисленного деления. Поддерживаются только int и целые объекты digit.')
        except ZeroDivisionError:
            raise MathError('На ноль делить нельзя!')

    def __mod__(self, __value: int|float|Self) -> Self:
        if isinstance(__value, (int, float, digit)):
            return self - (self // __value) * __value
        else:
            raise TypeError('Неверный тип данных для операции нахождения остатка от деления. Поддерживаются только int, float и объекты digit.')

    def __imod__(self, __value: int|float|Self) -> Self:
        return self % __value

    def __rmod__(self, __value: int|float) -> Self:
        if isinstance(__value, (int, float)):
            return __value - (__value // self) * self
        else:
            raise TypeError('Неверный тип данных для операции нахождения остатка от деления. Поддерживаются только int, float и объекты digit.')

    def __divmod__(self, __value: int|float|Self) -> tuple[Self, Self]:
        if isinstance(__value, (int, float, digit)):
            tmp = self // __value
            return tmp, self - tmp * __value
        else:
            raise TypeError('Неверный тип данных для операции целочисленного деления и нахождения остатка от деления. Поддерживаются только int, float и объекты digit.')

    def __rdivmod__(self, __value: int|float) -> tuple[Self, Self]:
        if isinstance(__value, (int, float)):
            tmp = __value // self
            return tmp, __value - tmp * self 
        else:
            raise TypeError('Неверный тип данных для операции целочисленного деления и нахождения остатка от деления. Поддерживаются только int, float и объекты digit.')

    @rounding
    def __pow__(self, __value: int|float|Self) -> Self:
        if isinstance(__value, (int, float, digit)):
            try:
                return digit(self.__x ** float(__value))
            except ZeroDivisionError:
                raise MathError('0 нельзя возводить в отрицательную степень.')
        else:
            raise TypeError('Неверный тип данных для операции возведения в степень. Поддерживаются только int, float и объекты digit.')

    def __ipow__(self, __value: int|float|Self) -> Self:
        return self ** __value

    @rounding
    def __rpow__(self, __value: int|float) -> Self:
        if isinstance(__value, (int, float)):
            return digit(__value ** self.__x)
        else:
            raise TypeError('Неверный тип данных для операции возведения в степень. Поддерживаются только int, float и объекты digit.')

    def __lshift__(self, __value: int|Self) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if self.isint():
            if isinstance(__value, int):
                return digit(int(self) << __value)
            elif isinstance(__value, digit):
                if __value.isint():
                    return digit(int(self) << int(__value))
                else:
                    raise TypeError('Значение сдвига не может быть приведено к целому типу (int).')
            else:
                raise TypeError('Неверный тип данных для операции битового сдвига влево. Поддерживаются только int и целые объекты digit.')
        else:
            raise TypeError('Сдвигаемое число не может быть приведено к целому типу (int).')

    def __ilshift__(self, __value: int|Self) -> Self:
        return self << __value

    def __rlshift__(self, __value: int) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if isinstance(__value, int):
            if self.isint():
                return digit(__value << int(self))
            else:
                raise TypeError('Значение сдвига не может быть приведено к целому типу (int).')
        else:
            raise TypeError('Неверный тип данных для операции битового сдвига влево. Поддерживаются только int и целые объекты digit.')

    def __rshift__(self, __value: int|Self) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if self.isint():
            if isinstance(__value, int):
                return digit(int(self) >> __value)
            elif isinstance(__value, digit):
                if __value.isint():
                    return digit(int(self) >> int(__value))
                else:
                    raise TypeError('Значение сдвига не может быть приведено к целому типу (int).')
            else:
                raise TypeError('Неверный тип данных для операции битового сдвига влево. Поддерживаются только int и целые объекты digit.')
        else:
            raise TypeError('Сдвигаемое число не может быть приведено к целому типу (int).')

    def __irshift__(self, __value: int|Self) -> Self:
        return self >> __value

    def __rrshift__(self, __value: int) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if isinstance(__value, int):
            if self.isint():
                return digit(__value >> int(self))
            else:
                raise TypeError('Значение сдвига не может быть приведено к целому типу (int).')
        else:
            raise TypeError('Неверный тип данных для операции битового сдвига влево. Поддерживаются только int и целые объекты digit.')

    def __and__(self, __value: int|Self) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if self.isint():
            if isinstance(__value, int):
                return digit(int(self) & __value)
            elif isinstance(__value, digit):
                if __value.isint():
                    return digit(int(self) & int(__value))
                else:
                    raise TypeError('Объект digit не может быть приведён к целому типу (int).')
            else:
                raise TypeError('Неверный тип данных для операции битового И. Поддерживаются только int и целые объекты digit.')
        else:
            raise TypeError('Объект digit не может быть приведён к целому типу (int).')

    def __iand__(self, __value: int|Self) -> Self:
        return self & __value

    def __rand__(self, __value: int) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if isinstance(__value, int):
            if self.isint():
                return digit(int(self) & __value)
            else:
                raise TypeError('Объект digit не может быть приведён к целому типу (int).')
        else:
            raise TypeError('Неверный тип данных для операции битового И. Поддерживаются только int и целые объекты digit.')

    def __or__(self, __value: int|Self) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if self.isint():
            if isinstance(__value, int):
                return digit(int(self) | __value)
            elif isinstance(__value, digit):
                if __value.isint():
                    return digit(int(self) | int(__value))
                else:
                    raise TypeError('Объект digit не может быть приведён к целому типу (int).')
            else:
                raise TypeError('Неверный тип данных для операции битового И. Поддерживаются только int и целые объекты digit.')
        else:
            raise TypeError('Объект digit не может быть приведён к целому типу (int).')

    def __ior__(self, __value: int|Self) -> Self:
        return self | __value

    def __ror__(self, __value: int) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if isinstance(__value, int):
            if self.isint():
                return digit(int(self) | __value)
            else:
                raise TypeError('Объект digit не может быть приведён к целому типу (int).')
        else:
            raise TypeError('Неверный тип данных для операции битового И. Поддерживаются только int и целые объекты digit.')

    def __xor__(self, __value: int|Self) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if self.isint():
            if isinstance(__value, int):
                return digit(int(self) ^ __value)
            elif isinstance(__value, digit):
                if __value.isint():
                    return digit(int(self) ^ int(__value))
                else:
                    raise TypeError('Объект digit не может быть приведён к целому типу (int).')
            else:
                raise TypeError('Неверный тип данных для операции битового И. Поддерживаются только int и целые объекты digit.')
        else:
            raise TypeError('Объект digit не может быть приведён к целому типу (int).')

    def __ixor__(self, __value: int|Self) -> Self:
        return self ^ __value

    def __rxor__(self, __value: int) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if isinstance(__value, int):
            if self.isint():
                return digit(int(self) ^ __value)
            else:
                raise TypeError('Объект digit не может быть приведён к целому типу (int).')
        else:
            raise TypeError('Неверный тип данных для операции битового И. Поддерживаются только int и целые объекты digit.')

    def __invert__(self) -> Self:
        """
        Только для int и целых объектов digit.
        """
        if self.isint():
            return digit(~int(self))
        else:
            raise TypeError('Объект digit не может быть приведён к целому типу (int).')

    def __round__(self, ndigits: Optional[int] = 0) -> Self:
        if ndigits == 0:
            tmp = self - int(self)
            return digit(int(self) + (tmp >= 0.5))
        @rounding(ndigits=ndigits)
        def func() -> Self:
            return self
        return func()

    @rounding
    def sin(self) -> Self:
        return digit(math.sin(self.__x))

    @rounding
    def cos(self) -> Self:
        return digit(math.cos(self.__x))

    @rounding
    def sec(self) -> Self:
        try:
            return 1 / self.sin()
        except MathError:
            raise MathError("Секанс данного числа не существует!")

    @rounding
    def csc(self) -> Self:
        try:
            return 1 / self.cos()
        except MathError:
            raise MathError("Косеканс данного числа не существует!")

    @rounding
    def tg(self) -> Self:
        try:
            return self.sin() / self.cos()
        except MathError:
            raise MathError("Тангенс данного числа не существует!")

    @rounding
    def ctg(self) -> Self:
        try:
            return self.cos() / self.sin()
        except MathError:
            raise MathError("Котангенс данного числа не существует!")

    @rounding
    def asin(self) -> Self:
        try:
            return digit(math.asin(self.__x))
        except ValueError:
            raise MathError("Арксинус данного числа не существует!")

    @rounding
    def acos(self) -> Self:
        try:
            return digit(math.acos(self.__x))
        except ValueError:
            raise MathError("Арккосинус данного числа не существует!")

    def asec(self) -> Self:
        try:
            return (1 / self).acos()
        except:
            raise MathError("Арксеканс данного числа не существует!")

    def acsc(self) -> Self:
        try:
            return (1 / self).asin()
        except:
            raise MathError("Арккосеканс данного числа не существует!")

    @rounding
    def atg(self) -> Self:
        try:
            return digit(math.atan(self.__x))
        except ValueError:
            raise MathError("Арктангенс данного числа не существует!")

    @rounding
    def actg(self) -> Self:
        try:
            return digit("PI") / 2 - digit(math.atan(self.__x))
        except ValueError:
            raise MathError("Арккотангенс данного числа не существует!")

    @rounding
    def log(self, __value: Optional[int|float|Self] = math.e) -> Self:
        """
        __value - это основание логарифма.
        По-умолчанию считается натуральный логарифм.
        """
        try:
            if float(__value) == math.e:
                return digit(math.log(float(self)))
            elif float(__value) == 10.0:
                return digit(math.log10(float(self)))
            elif float(__value) == 2.0:
                return digit(math.log2(float(self)))
            return digit(math.log(float(self), float(__value)))
        except ZeroDivisionError:
            raise MathError("Основание логарифма положительное, не равное единице!")
        except ValueError:
            raise MathError("Основание и аргумент логарифма - положительные числа.")
        except TypeError:
            raise TypeError('Неверный тип данных для операции логарифма. Поддерживаются только int, float и объекты digit.')

    def ln(self) -> Self:
        return self.log(digit("E"))

    def lg(self) -> Self:
        return self.log(10)

    def log2(self) -> Self:
        return self.log(2)

    @rounding
    def exp(self) -> Self:
        """
        exp в степени данного числа.
        """
        try:
            return digit(math.exp(float(self)))
        except ZeroDivisionError:
            raise MathError("Основание логарифма положительное, не равное единице!")
        except ValueError:
            raise MathError("Основание и аргумент логарифма - положительные числа.")

    def sqrt(self) -> Self:
        return pow(self, 0.5)

    @rounding
    def radians(self) -> Self:
        return self * digit("PI") / 180

    @rounding
    def degrees(self) -> Self:
        return  self / digit("PI") * 180

    @rounding
    def sinh(self) -> Self:
        return digit(math.sinh(float(self)))

    @rounding
    def cosh(self) -> Self:
        return digit(math.cosh(float(self)))
    
    @rounding
    def sech(self) -> Self:
        try:
            return 1 / self.sinh()
        except MathError:
            raise MathError("Гиперболический секанс данного числа не существует!")

    @rounding
    def csch(self) -> Self:
        try:
            return 1 / self.cosh()
        except MathError:
            raise MathError("Гиперболический косеканс данного числа не существует!")

    @rounding
    def tgh(self) -> Self:
        try:
            return self.sinh() / self.cosh()
        except MathError:
            raise MathError("Гиперболический тангенс данного числа не существует!")

    @rounding
    def ctgh(self) -> Self:
        try:
            return self.cosh() / self.sinh()
        except MathError:
            raise MathError("Гиперболический котангенс данного числа не существует!")

    @rounding
    def asinh(self) -> Self:
        try:
            return digit(math.asinh(self.__x))
        except:
            raise MathError("Гиперболический арксинус данного числа не существует!")

    @rounding
    def acosh(self) -> Self:
        try:
            return digit(math.acosh(self.__x))
        except:
            raise MathError("Гиперболический арккосинус данного числа не существует!")

    def asech(self) -> Self:
        try:
            return (1 / self + (1 / pow(self, 2) - 1).sqrt()).ln()
        except:
            raise MathError("Гиперболический арксеканс данного числа не существует!")

    def acsch(self) -> Self:
        try:
            return (1 / self + (1 / pow(self, 2) + 1).sqrt()).ln()
        except:
            raise MathError("Гиперболический арккосеканс данного числа не существует!")

    @rounding
    def atgh(self) -> Self:
        try:
            return digit(math.atanh(self.__x))
        except:
            raise MathError("Гиперболический арктангенс данного числа не существует!")

    @rounding
    def actgh(self) -> Self:
        try:
            return 0.5 * ((self + 1) / (self - 1)).ln()
        except:
            raise MathError("Гиперболический арккотангенс данного числа не существует!")

    def factorial(self) -> Self:
        if self.isint():
            try:
                return digit(math.factorial(int(self.__x)))
            except ValueError:
                raise MathError("Число должно быть неотрицательным!")
        raise TypeError('Неверный тип данных для операции факториала. Поддерживаются только int и целые объекты digit.')

    def ceil(self):
        return digit(math.ceil(self.__x))

    def floor(self):
        return digit(math.floor(self.__x))

    def implication(self, __value: int|Self) -> Self:
        """
        self -> __value
        """
        return not (self) or __value
