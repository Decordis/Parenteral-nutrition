from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle


class NutritionCalculator:
    def __init__(self, mass, volume, Na, K,
                 Ca, Mg, protein, fat, soluvit, vitalipid, carbohydrates):
        self.mass = mass
        self.volume = volume
        self.Na = Na
        self.K = K
        self.Ca = Ca
        self.Mg = Mg
        self.protein = protein
        self.fat = fat
        self.soluvit = soluvit
        self.vitalipid = vitalipid
        self.carbohydrates = carbohydrates

    def res_prot(self):
        prot = (self.protein * self.mass * 100) / 10
        return prot

    def res_fat(self):
        fats = (self.fat * self.mass * 100) / 20
        return fats

    def res_soluvit(self):
        soluvit = float(self.soluvit * self.mass)
        return soluvit

    def res_vitalipid(self):
        vitalipid = min(float(self.vitalipid * self.mass), 10.0)
        return vitalipid

    def res_tot_fat(self):
        tot_fat = self.fat() + self.res_soluvit() + self.res_vitalipid()
        return tot_fat

    def res_tot_volume(self):
        tot_volume = self.mass * self.volume
        return tot_volume

    def res_volume(self):
        volume = self.res_tot_volume() - self.res_fat()
        return volume

    def res_carbohydrates(self):
        carbon = (self.carbohydrates * self.mass * 100) / 40
        return carbon

    def res_na(self):
        tot_na = self.Na * self.mass * 0.66
        return tot_na

    def res_k(self):
        tot_k = self.K * self.mass * 1.85
        return tot_k

    def res_ca(self):
        tot_ca = (self.Ca * self.mass) / 100
        return tot_ca

    def res_mg(self):
        tot_mg = (self.Mg * self.mass) / 250
        return tot_mg

    def res_h2O(self):
        tot_h20 = (
            self.res_volume() -
            (self.res_prot() - self.res_carbohydrates() -
                self.res_na() - self.res_k()
                - self.res_ca() - self.res_mg()))
        return tot_h20

    def res_concentration(self):
        concen = ((self.carbohydrates * self.mass) / self.res_volume()) * 100
        return concen

    def res_osmolarity(self):
        res = (((self.protein * self.mass) * 1000 / self.res_volume()) * 8)
        + (((self.carbohydrates * self.mass) * 1000 / self.res_volume()) * 7)
        + (((self.Na * self.mass) * 1000 / self.res_volume()) * 2) - 50
        return res

    def res_speed_volume(self):
        volume_speed = self.res_volume() / 24
        return volume_speed

    def res_speed_fat(self):
        fat_speed = self.res_fat() / 20
        return fat_speed

    def calculate(self):
        return {
            "Общий объем": self.res_tot_volume(),
            'Объем инфузии без жиров': self.res_volume(),
            "Белки": self.res_prot(),
            "Углеводы": self.res_carbohydrates(),
            'Вода для инъекций': self.res_h2O(),
            "Дотации Na": self.res_na(),
            "Дотация К": self.res_k(),
            "Дотация Ca": self.res_ca(),
            "Дотация Mg": self.res_mg(),
            "Жиры": self.res_fat(),
            "Солувит": self.res_soluvit(),
            "Виталипид": self.res_vitalipid(),
            "Концентрация": self.res_concentration(),
            "Осмолярность": self.res_osmolarity(),
            "Cкорость инфузии за 24 часа": self.res_speed_volume(),
            "Скорость жиров за 20 часов": self.res_speed_fat(),
        }


class InputScreen(Screen):
    def __init__(self, **kwargs):
        super(InputScreen, self).__init__(**kwargs)

        # Установка цвета фона
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Обновление фона при изменении размера
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = FloatLayout()

        self.inputs = {}
        fields = [
            'Масса',
            'Общий объем',
            'Белки',
            'Жиры',
            'Солувит - рекомендуемая доза 1 мг/кг/сут',
            'Виталипид - рекомендуемая доза 4 мг/кг/сут',
            'Углеводы',
            'Na',
            'K',
            'Ca',
            'Mg',
            ]

        # Установка позиции для меток и полей ввода
        for i, field in enumerate(fields):
            label = Label(
                text=field,
                font_size='20sp',
                size_hint=(0.5, None), height=50,
                pos_hint={'x': 0.05, 'y': 1 - (i + 1) * 0.08},
                color=(1, 1, 1, 1))
            self.layout.add_widget(label)

            text_input = TextInput(
                multiline=False, size_hint=(0.5, None), height=40,
                pos_hint={'x': 0.5, 'y': 1 - (i + 1) * 0.08},
                foreground_color=(0, 0, 0, 1),
                background_color=(1, 1, 1, 1))
            self.inputs[field] = text_input
            self.layout.add_widget(text_input)

        self.calculate_button = Button(text='Рассчитать',
                                       font_size='25sp',
                                       size_hint=(0.4, None), height=50,
                                       pos_hint={'center_x': 0.5, 'y': 0},
                                       on_press=self.calculate)
        self.layout.add_widget(self.calculate_button)

        self.add_widget(self.layout)

    def calculate(self, instance):
        mass = float(self.inputs['Масса'].text)
        volume = float(self.inputs['Общий объем'].text)
        protein = float(self.inputs['Белки'].text)
        fat = float(self.inputs['Жиры'].text)
        soluvit = float(
            self.inputs['Солувит - рекомендуемая доза 1 мг/кг/сут'].text)
        vitalipid = float(
            self.inputs['Виталипид - рекомендуемая доза 4 мг/кг/сут'].text)
        carbohydrates = float(self.inputs['Углеводы'].text)
        Na = float(self.inputs['Na'].text)
        K = float(self.inputs['K'].text)
        Ca = float(self.inputs['Ca'].text)
        Mg = float(self.inputs['Mg'].text)

        calculator = NutritionCalculator(mass, volume,
                                         Na, K, Ca, Mg,
                                         protein, fat,
                                         soluvit, vitalipid, carbohydrates)
        results = calculator.calculate()

        results_text = '\n'.join([f"{key}: {value:.2f}"
                                  for key, value in results.items()])
        self.manager.get_screen('result').show_results(results_text)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.result_label = Label(text='', size_hint=(0.9, None), height=80,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.layout.add_widget(self.result_label)

        back_button = Button(text='Назад', on_press=self.back,
                             size_hint=(0.5, None), height=50,
                             pos_hint={'center_x': 0.5, 'y': 0.1})
        self.layout.add_widget(back_button)
        self.add_widget(self.layout)

    def show_results(self, results_text):
        self.result_label.text = results_text
        self.manager.current = 'result'  # Switch to the ResultScreen

    def back(self, instance):
        self.manager.current = 'input'  # Switch back to the InputScreen


class NutritionApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input'))
        sm.add_widget(ResultScreen(name='result'))
        return sm


if __name__ == '__main__':
    NutritionApp().run()
