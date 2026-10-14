class Converter:
    @staticmethod
    def do(x: float) -> int:
        if x >= 100.7:
            return 1000
        elif 0 < x < 100.7:
            return int(x)
        elif x == 0.0:
            raise ValueError("x не может быть равен 0")
        elif -30.5 <= x < 0:
            return int(x) - 5
        else:
            return -2000