# -*- coding: utf-8 -*-
"""
Home Screen - الشاشة الرئيسية مع لوحة المعلومات
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

class StatCard(BoxLayout):
    """Statistics card widget"""

    def __init__(self, title, value, color, icon_text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(120)

        # Background
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color[:3], 0.1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            Color(*color)
            RoundedRectangle(pos=(self.x + dp(2), self.y + dp(2)), 
                           size=(self.width - dp(4), self.height - dp(4)), 
                           radius=[dp(10)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Icon
        icon = Label(
            text=icon_text,
            font_size='24sp',
            color=(1, 1, 1, 0.8),
            size_hint_y=0.3
        )
        self.add_widget(icon)

        # Value
        value_label = Label(
            text=str(value),
            font_size='28sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.4
        )
        self.add_widget(value_label)

        # Title
        title_label = Label(
            text=title,
            font_size='13sp',
            color=(1, 1, 1, 0.9),
            size_hint_y=0.3
        )
        self.add_widget(title_label)

    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.95, 0.96, 0.98, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])

class MenuButton(Button):
    """Custom menu button"""

    def __init__(self, text, icon, screen_name, **kwargs):
        super().__init__(**kwargs)
        self.text = f'{icon}\n{text}'
        self.screen_name = screen_name
        self.font_size = '14sp'
        self.background_color = (1, 1, 1, 1)
        self.background_normal = ''
        self.color = (0.2, 0.2, 0.2, 1)
        self.size_hint_y = None
        self.height = dp(90)

        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            Color(0.9, 0.92, 0.95, 1)
            RoundedRectangle(pos=(self.x + dp(1), self.y + dp(1)), 
                           size=(self.width - dp(2), self.height - dp(2)), 
                           radius=[dp(11)])
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            Color(0.9, 0.92, 0.95, 1)
            RoundedRectangle(pos=(self.x + dp(1), self.y + dp(1)), 
                           size=(self.width - dp(2), self.height - dp(2)), 
                           radius=[dp(11)])

class HomeScreen(Screen):
    """Main dashboard screen"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """Build the home screen UI"""
        main_layout = BoxLayout(orientation='vertical')

        # Header
        header = BoxLayout(orientation='horizontal', 
                          size_hint_y=None, 
                          height=dp(60),
                          padding=[dp(15), dp(10)])
        header.canvas.before.clear()
        with header.canvas.before:
            Color(0.15, 0.35, 0.85, 1)
            Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=self._update_header, size=self._update_header)

        title = Label(
            text='[b]نظام ادارة العملاء[/b]',
            markup=True,
            font_size='20sp',
            color=(1, 1, 1, 1),
            halign='right'
        )
        header.add_widget(title)

        main_layout.add_widget(header)

        # Scrollable content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', 
                           padding=dp(15), 
                           spacing=dp(15),
                           size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Statistics section
        stats_label = Label(
            text='[b]احصائيات سريعة[/b]',
            markup=True,
            font_size='18sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30),
            halign='right'
        )
        content.add_widget(stats_label)

        # Stats grid
        self.stats_grid = GridLayout(cols=2, 
                                     spacing=dp(10), 
                                     size_hint_y=None,
                                     height=dp(260))

        self.stat_cards = {
            'customers': StatCard('العملاء', '0', (0.15, 0.35, 0.85), '👥'),
            'amount': StatCard('اجمالي المبالغ', '0', (0.2, 0.7, 0.3), '💰'),
            'paid': StatCard('المدفوع', '0', (0.1, 0.6, 0.5), '✅'),
            'remaining': StatCard('المتبقي', '0', (0.9, 0.3, 0.2), '⚠️'),
        }

        for card in self.stat_cards.values():
            self.stats_grid.add_widget(card)

        content.add_widget(self.stats_grid)

        # Menu section
        menu_label = Label(
            text='[b]القائمة الرئيسية[/b]',
            markup=True,
            font_size='18sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30),
            halign='right'
        )
        content.add_widget(menu_label)

        # Menu grid
        menu_grid = GridLayout(cols=2, 
                              spacing=dp(10), 
                              size_hint_y=None,
                              height=dp(280))

        menu_items = [
            ('العملاء', '👥', 'customers'),
            ('اضافة عميل', '➕', 'add_customer'),
            ('البحث', '🔍', 'search'),
            ('المدفوعات', '💳', 'payments'),
            ('التقارير', '📊', 'reports'),
            ('الاعدادات', '⚙️', 'settings'),
        ]

        for text, icon, screen in menu_items:
            btn = MenuButton(text, icon, screen)
            btn.bind(on_release=self.on_menu_click)
            menu_grid.add_widget(btn)

        content.add_widget(menu_grid)

        # Renewals section
        renewals_label = Label(
            text='[b]تجديدات قادمة[/b]',
            markup=True,
            font_size='18sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30),
            halign='right'
        )
        content.add_widget(renewals_label)

        self.renewals_box = BoxLayout(orientation='vertical', 
                                     size_hint_y=None,
                                     height=dp(100))
        self.renewals_box.add_widget(Label(
            text='لا توجد تجديدات قادمة',
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1)
        ))
        content.add_widget(self.renewals_box)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def _update_header(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.35, 0.85, 1)
            Rectangle(pos=instance.pos, size=instance.size)

    def on_pre_enter(self):
        """Update statistics when entering screen"""
        Clock.schedule_once(self.load_statistics, 0.1)
        Clock.schedule_once(self.load_renewals, 0.2)

    def load_statistics(self, dt):
        """Load and display statistics"""
        app = self.manager.parent
        stats = app.db.get_statistics()

        currency = app.db.get_setting('currency', 'ريال')

        self.stat_cards['customers'].children[1].text = str(stats['total_customers'])
        self.stat_cards['amount'].children[1].text = f"{stats['total_amount']:,.0f} {currency}"
        self.stat_cards['paid'].children[1].text = f"{stats['total_paid']:,.0f} {currency}"
        self.stat_cards['remaining'].children[1].text = f"{stats['total_remaining']:,.0f} {currency}"

    def load_renewals(self, dt):
        """Load upcoming renewals"""
        app = self.manager.parent
        renewals = app.db.get_upcoming_renewals(days=7)

        self.renewals_box.clear_widgets()

        if renewals:
            self.renewals_box.height = dp(50) * len(renewals) + dp(20)
            for customer in renewals:
                item = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45))
                item.add_widget(Label(
                    text=customer['name'],
                    font_size='14sp',
                    color=(0.2, 0.2, 0.2, 1),
                    size_hint_x=0.7
                ))
                item.add_widget(Label(
                    text=customer['renewal_date'],
                    font_size='12sp',
                    color=(0.8, 0.2, 0.2, 1),
                    size_hint_x=0.3
                ))
                self.renewals_box.add_widget(item)
        else:
            self.renewals_box.height = dp(60)
            self.renewals_box.add_widget(Label(
                text='لا توجد تجديدات قادمة',
                font_size='14sp',
                color=(0.5, 0.5, 0.5, 1)
            ))

    def on_menu_click(self, instance):
        """Handle menu button click"""
        app = self.manager.parent
        app.switch_screen(instance.screen_name)
