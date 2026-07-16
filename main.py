from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.core.window import Window

# Для вебу Window.size не використовується, браузер сам підлаштує масштаб

class BankApp(App):
    # Картка та баланс
    card_last_digits = StringProperty("4504")
    card_date = StringProperty("15/15")
    main_balance = StringProperty("55 345.50")
    
    # СУМИ історії
    history_item_1 = StringProperty("- 150.00")
    history_item_2 = StringProperty("+ 1 200.00")
    history_item_3 = StringProperty("+ 2 400.00")
    
    # НАЗВИ транзакцій
    history_name_1 = StringProperty("Сільпо")
    history_name_2 = StringProperty("Богаткін Д.")
    history_name_3 = StringProperty("PAYSEND")
    
    # ДАТИ транзакцій
    history_date_1 = StringProperty("20 лютого, 23:49")
    history_date_2 = StringProperty("20 лютого, 23:48")
    history_date_3 = StringProperty("20 лютого, 23:26")

    def build(self):
        # Вказуємо назви файлів прямо (вони мають бути в тій же папці на GitHub)
        self.f_reg = "Manrope.ttf"
        self.f_bold = "Manrope-Bold.ttf"
        
        Window.clearcolor = (0, 0, 0, 1)
        self.main_layout = FloatLayout()
        
        # Фонове зображення
        self.background = Image(
            source='photo.png',
            allow_stretch=True, keep_ratio=False,
            size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.main_layout.add_widget(self.background)

        # --- КАРТКА ТА БАЛАНС ---
        self.btn_digits = self.create_edit_button(self.card_last_digits, {'center_x': 0.29, 'center_y': 0.647}, (60, 30), '14sp', 'card_last_digits', self.f_reg)
        self.btn_date = self.create_edit_button(self.card_date, {'center_x': 0.42, 'center_y': 0.647}, (60, 30), '14sp', 'card_date', self.f_reg)
        
        self.btn_balance = Button(
            text=self.format_balance_markup(self.main_balance),
            markup=True, font_size='21sp', font_name=self.f_reg,
            color=(1, 1, 1, 1), background_normal='', background_color=(0, 0, 0, 0),
            size_hint=(None, None), size=(250, 45), pos_hint={'center_x': 0.55, 'center_y': 0.574},
            halign='right', valign='middle'
        )
        self.btn_balance.text_size = self.btn_balance.size
        self.btn_balance.bind(on_release=lambda x: self.open_edit_popup('main_balance'))

        # --- ІСТОРІЯ (Координати змінено для кращого вигляду) ---
        self.btn_name1 = self.create_edit_button(self.history_name_1, {'center_x': 0.41, 'center_y': 0.289}, (180, 30), '12.5sp', 'history_name_1', self.f_bold, halign='left')
        self.btn_d1 = self.create_edit_button(self.history_date_1, {'center_x': 0.41, 'center_y': 0.270}, (180, 20), '11.5sp', 'history_date_1', self.f_bold, halign='left', color=(0.6, 0.6, 0.6, 1))
        self.btn_hist1 = self.create_edit_button(self.history_item_1, {'center_x': 0.71, 'center_y': 0.289}, (120, 40), '13.5sp', 'history_item_1', self.f_bold, halign='right', is_amount=True)

        self.btn_name2 = self.create_edit_button(self.history_name_2, {'center_x': 0.41, 'center_y': 0.222}, (180, 30), '12.5sp', 'history_name_2', self.f_bold, halign='left')
        self.btn_d2 = self.create_edit_button(self.history_date_2, {'center_x': 0.41, 'center_y': 0.203}, (180, 20), '11.5sp', 'history_date_2', self.f_bold, halign='left', color=(0.6, 0.6, 0.6, 1))
        self.btn_hist2 = self.create_edit_button(self.history_item_2, {'center_x': 0.71, 'center_y': 0.222}, (120, 40), '13.5sp', 'history_item_2', self.f_bold, halign='right', is_amount=True)

        self.btn_name3 = self.create_edit_button(self.history_name_3, {'center_x': 0.41, 'center_y': 0.155}, (180, 30), '12.5sp', 'history_name_3', self.f_bold, halign='left')
        self.btn_d3 = self.create_edit_button(self.history_date_3, {'center_x': 0.41, 'center_y': 0.136}, (180, 20), '11.5sp', 'history_date_3', self.f_bold, halign='left', color=(0.6, 0.6, 0.6, 1))
        self.btn_hist3 = self.create_edit_button(self.history_item_3, {'center_x': 0.71, 'center_y': 0.155}, (120, 40), '13.5sp', 'history_item_3', self.f_bold, halign='right', is_amount=True)

        widgets = [self.btn_digits, self.btn_date, self.btn_balance, 
                   self.btn_name1, self.btn_d1, self.btn_hist1,
                   self.btn_name2, self.btn_d2, self.btn_hist2,
                   self.btn_name3, self.btn_d3, self.btn_hist3]
        for w in widgets: self.main_layout.add_widget(w)
        
        return self.main_layout

    def get_text_color(self, text):
        clean = text.strip()
        if clean.startswith('-'): return (0.8, 0.8, 0.8, 1)
        if clean.startswith('+'): return (0.35, 0.75, 0.2, 1)
        return (1, 1, 1, 1)

    def format_balance_markup(self, value):
        try:
            clean_val = str(value).replace(' ', '').replace(',', '.')
            num = float(clean_val)
            formatted = "{:,.2f}".format(num).replace(',', ' ')
            parts = formatted.split('.')
            return f"{parts[0]}[size=17sp].{parts[1]}[/size]"
        except: return str(value)

    def create_edit_button(self, text, pos_hint, size, font_size, target_prop, font_name, halign='center', color=None, is_amount=False):
        btn_color = color if color else (self.get_text_color(text) if is_amount else (1, 1, 1, 1))
        btn = Button(
            text=text, font_size=font_size, font_name=font_name,
            color=btn_color,
            background_normal='', background_color=(0, 0, 0, 0),
            size_hint=(None, None), size=size, pos_hint=pos_hint,
            halign=halign, valign='middle'
        )
        btn.text_size = btn.size
        btn.bind(on_release=lambda x, p=target_prop: self.open_edit_popup(p))
        return btn

    def open_edit_popup(self, prop_name):
        self.current_editing_prop = prop_name
        current_val = getattr(self, prop_name)
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.input_field = TextInput(text=str(current_val), multiline=False, halign='center', font_size='22sp')
        content.add_widget(self.input_field)
        save_btn = Button(text="Оновити", size_hint=(1, 0.5))
        save_btn.bind(on_release=self.save_value)
        content.add_widget(save_btn)
        self.popup = Popup(title='Редагування', content=content, size_hint=(0.8, 0.3))
        self.popup.open()

    def save_value(self, instance):
        new_text = self.input_field.text
        setattr(self, self.current_editing_prop, new_text)
        self.popup.dismiss()
        # Для простоти у вебі ми просто перезавантажимо віджети, якщо треба, 
        # але StringProperty має спрацювати автоматично.

if __name__ == '__main__':
    BankApp().run()
