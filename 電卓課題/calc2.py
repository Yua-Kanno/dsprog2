import flet as ft
# mathは三角関数・大数・πなどの数学計算用
import math

#Fletの普通のボタンを電卓用にカスタマイズすルための土台
class CalcButton(ft.ElevatedButton):
    # text:ボタンに表示する文字（例："7","+","sin"）button_clicked:ボタンがクリックされたときに呼び出される関数expand:ボタンの横幅の拡張率
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    # 親クラスの設定（文字・クリック処理・幅）をそのまま利用
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE

# +, -, *, /などの操作ボタン用
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE

# AC, +/-, %などの追加操作ボタン用
class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK

# containerを使って背景・角丸を設定
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()
        #　計算結果・入力中の数字を表示
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=28)

        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        # 縦方向に並べる
        self.content = ft.Column(
            controls=[
            
                ft.Row(controls=[self.result], alignment="end"),

                # --- 科学計算ボタン ---
                ft.Row(
                    controls=[
                        ExtraActionButton("sin", self.button_clicked),
                        ExtraActionButton("cos", self.button_clicked),
                        ExtraActionButton("tan", self.button_clicked),
                        ExtraActionButton("log", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton("√", self.button_clicked),
                        ExtraActionButton("π", self.button_clicked),
                    ]
                ),

                # --- 通常電卓 ---
                ft.Row(
                    controls=[
                        ExtraActionButton("AC", self.button_clicked),
                        ExtraActionButton("+/-", self.button_clicked),
                        ExtraActionButton("%", self.button_clicked),
                        ActionButton("/", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("7", self.button_clicked),
                        DigitButton("8", self.button_clicked),
                        DigitButton("9", self.button_clicked),
                        ActionButton("*", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("4", self.button_clicked),
                        DigitButton("5", self.button_clicked),
                        DigitButton("6", self.button_clicked),
                        ActionButton("-", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("1", self.button_clicked),
                        DigitButton("2", self.button_clicked),
                        DigitButton("3", self.button_clicked),
                        ActionButton("+", self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton("0", self.button_clicked, expand=2),
                        DigitButton(".", self.button_clicked),
                        ActionButton("=", self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data

        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."):
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                # 「次の数字は新しい入力か？」を判断するフラグ
                self.new_operand = False
            else:
                self.result.value += data

        elif data in ("+", "-", "*", "/"):
            # 連続計算ができる理由はここにある
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            self.operand1 = 0 if self.result.value == "Error" else float(self.result.value)
            self.new_operand = True

        elif data == "=":
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data == "%":
            self.result.value = self.format_number(float(self.result.value) / 100)
            self.reset()

        # 正、負を切り替える。表示だけ変更
        elif data == "+/-":
            value = float(self.result.value)
            self.result.value = self.format_number(-value)

        # --- 科学計算 ---
        # 入力値は度数方
        # radiana()でラジアンに変換
        elif data == "sin":
            self.result.value = self.format_number(
                math.sin(math.radians(float(self.result.value)))
            )
            self.reset()

        elif data == "cos":
            self.result.value = self.format_number(
                math.cos(math.radians(float(self.result.value)))
            )
            self.reset()

        elif data == "tan":
            self.result.value = self.format_number(
                math.tan(math.radians(float(self.result.value)))
            )
            self.reset()

        elif data == "log":
            value = float(self.result.value)
            self.result.value = "Error" if value <= 0 else self.format_number(math.log10(value))
            self.reset()

        elif data == "√":
            value = float(self.result.value)
            self.result.value = "Error" if value < 0 else self.format_number(math.sqrt(value))
            self.reset()

        elif data == "π":
            self.result.value = self.format_number(math.pi)
            self.reset()

        self.update()

    def calculate(self, operand1, operand2, operator):
        try:
            if operator == "+":
                return self.format_number(operand1 + operand2)
            elif operator == "-":
                return self.format_number(operand1 - operand2)
            elif operator == "*":
                return self.format_number(operand1 * operand2)
            elif operator == "/":
                return "Error" if operand2 == 0 else self.format_number(operand1 / operand2)
        except:
            return "Error"

    def format_number(self, num):
        return int(num) if num % 1 == 0 else num

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Scientific Calculator"
    page.add(CalculatorApp())


ft.app(main)
