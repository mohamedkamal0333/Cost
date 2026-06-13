# -*- coding: utf-8 -*-
"""
Search Screen - شاشة البحث المتقدم
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

class SearchResultItem(BoxLayout):
    """Search result item"""

    def __init__(self, customer, on_select, **kwargs):
        super().__init__(**kwargs)
        self.customer = customer
        self.orientation = 'vertical'
        self.padding = dp(12)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(90)

        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Name and phone
        info_row = BoxLayout(orientation='horizontal', size_hint_y=0.6)
        info_row.add_widget(Label(
            text=f"[b]{customer['name']}[/b]",
            markup=True,
            font_size='16sp',
            color=(0.15, 0.35, 0.85, 1),
            size_hint_x=0.6,
            halign='right'
        ))
        info_row.add_widget(Label(
            text=customer['phone'],
            font_size='13sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_x=0.4,
            halign='left'
        ))
        self.add_widget(info_row)

        # Amount and status
        status_row = BoxLayout(orientation='horizontal', size_hint_y=0.4)
        remaining = customer.get('remaining_amount', 0)
        color = (0.2, 0.7, 0.3, 1) if remaining == 0 else (0.9, 0.3, 0.2, 1)
        status_row.add_widget(Label(
            text=f"متبقي: {remaining:,.0f}",
            font_size='12sp',
            color=color,
            size_hint_x=0.5
        ))
        status_row.add_widget(Label(
            text=customer.get('service_type', ''),
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_x=0.5
        ))
        self.add_widget(status_row)

        self.bind(on_touch_down=lambda x, t: on_select(customer['id']) if self.collide_point(*t.pos) else None)

    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

class SearchScreen(Screen):
    """Advanced search screen"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """Build search UI"""
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
            text='[b]البحث[/b]',
            markup=True,
            font_size='20sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.8
        )
        header.add_widget(title)

        main_layout.add_widget(header)

        # Search input
        search_box = BoxLayout(orientation='horizontal',
                              size_hint_y=None,
                              height=dp(60),
                              padding=dp(15),
                              spacing=dp(10))

        self.search_input = TextInput(
            hint_text='ابحث بالاسم او رقم الهاتف...',
            font_size='15sp',
            multiline=False,
            size_hint_x=0.75,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        self.search_input.bind(on_text_validate=self.do_search)

        search_btn = Button(
            text='🔍',
            font_size='20sp',
            background_color=(0.15, 0.35, 0.85, 1),
            size_hint_x=0.25
        )
        search_btn.bind(on_release=self.do_search)

        search_box.add_widget(self.search_input)
        search_box.add_widget(search_btn)
        main_layout.add_widget(search_box)

        # Results
        scroll = ScrollView()
        self.results_list = BoxLayout(orientation='vertical',
                                     spacing=dp(10),
                                     padding=dp(15),
                                     size_hint_y=None)
        self.results_list.bind(minimum_height=self.results_list.setter('height'))

        self.results_list.add_widget(Label(
            text='ادخل كلمة البحث',
            font_size='16sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(100)
        ))

        scroll.add_widget(self.results_list)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def _update_header(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.35, 0.85, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[0])

    def do_search(self, instance):
        """Perform search"""
        query = self.search_input.text.strip()

        if len(query) < 2:
            self.results_list.clear_widgets()
            self.results_list.add_widget(Label(
                text='ادخل 2 احرف على الاقل',
                font_size='16sp',
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(100)
            ))
            return

        app = self.manager.parent
        results = app.db.search_customers(query)

        self.results_list.clear_widgets()

        if not results:
            self.results_list.add_widget(Label(
                text='لا توجد نتائج',
                font_size='16sp',
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(100)
            ))
            return

        for customer in results:
            item = SearchResultItem(customer, self.select_customer)
            self.results_list.add_widget(item)

    def select_customer(self, customer_id):
        """Select customer to edit"""
        app = self.manager.parent
        app.switch_screen('edit_customer', customer_id=customer_id)

    def go_back(self, instance):
        app = self.manager.parent
        app.go_back()
