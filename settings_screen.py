# -*- coding: utf-8 -*-
"""
Settings Screen - شاشة الاعدادات
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock

class SettingsScreen(Screen):
    """Application settings screen"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """Build settings UI"""
        main_layout = BoxLayout(orientation='vertical')

        # Header
        header = BoxLayout(orientation='horizontal',
                          size_hint_y=None,
                          height=dp(60),
                          padding=[dp(15), dp(10)])
        header.canvas.before.clear()
        with header.canvas.before:
            Color(0.15, 0.35, 0.85, 1)
            RoundedRectangle(pos=header.pos, size=header.size, radius=[0])
        header.bind(pos=self._update_header, size=self._update_header)

        back_btn = Button(
            text='← رجوع',
            font_size='14sp',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            size_hint_x=0.2
        )
        back_btn.bind(on_release=self.go_back)
        header.add_widget(back_btn)

        title = Label(
            text='[b]الاعدادات[/b]',
            markup=True,
            font_size='20sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.8
        )
        header.add_widget(title)

        main_layout.add_widget(header)

        # Settings form
        scroll = ScrollView()
        form = BoxLayout(orientation='vertical',
                        padding=dp(20),
                        spacing=dp(15),
                        size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))

        # Company name
        form.add_widget(self._create_label('اسم الشركة'))
        self.company_input = TextInput(
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.company_input)

        # Currency
        form.add_widget(self._create_label('العملة'))
        self.currency_input = TextInput(
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.currency_input)

        # Renewal days
        form.add_widget(self._create_label('ايام التنبيه قبل التجديد'))
        self.renewal_days_input = TextInput(
            font_size='15sp',
            multiline=False,
            input_filter='int',
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.renewal_days_input)

        # Save button
        save_btn = Button(
            text='[b]حفظ الاعدادات[/b]',
            markup=True,
            font_size='16sp',
            size_hint_y=None,
            height=dp(55),
            background_color=(0.15, 0.35, 0.85, 1)
        )
        save_btn.bind(on_release=self.save_settings)
        form.add_widget(save_btn)

        # App info
        form.add_widget(Label(size_hint_y=None, height=dp(30)))

        info_box = BoxLayout(orientation='vertical',
                            size_hint_y=None,
                            height=dp(100),
                            padding=dp(15))
        info_box.canvas.before.clear()
        with info_box.canvas.before:
            Color(0.95, 0.96, 0.98, 1)
            RoundedRectangle(pos=info_box.pos, size=info_box.size, radius=[dp(10)])
        info_box.bind(pos=self._update_info_bg, size=self._update_info_bg)

        info_box.add_widget(Label(
            text='نظام ادارة العملاء',
            font_size='16sp',
            color=(0.15, 0.35, 0.85, 1)
        ))
        info_box.add_widget(Label(
            text='الاصدار 1.0.0',
            font_size='13sp',
            color=(0.5, 0.5, 0.5, 1)
        ))
        form.add_widget(info_box)

        form.add_widget(Label(size_hint_y=None, height=dp(30)))

        scroll.add_widget(form)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def _create_label(self, text):
        return Label(
            text=text,
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25),
            halign='right'
        )

    def _update_header(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.35, 0.85, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[0])

    def _update_info_bg(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.95, 0.96, 0.98, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[dp(10)])

    def on_pre_enter(self):
        """Load settings when entering"""
        Clock.schedule_once(self.load_settings, 0.1)

    def load_settings(self, dt):
        """Load current settings"""
        app = self.manager.parent
        self.company_input.text = app.db.get_setting('company_name', 'شركتي')
        self.currency_input.text = app.db.get_setting('currency', 'ريال')
        self.renewal_days_input.text = app.db.get_setting('renewal_days', '7')

    def save_settings(self, instance):
        """Save settings"""
        app = self.manager.parent

        app.db.set_setting('company_name', self.company_input.text.strip())
        app.db.set_setting('currency', self.currency_input.text.strip())
        app.db.set_setting('renewal_days', self.renewal_days_input.text.strip())

        app.notifier.show_message('نجاح', 'تم حفظ الاعدادات بنجاح', 'success')

    def go_back(self, instance):
        app = self.manager.parent
        app.go_back()
