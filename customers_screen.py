# -*- coding: utf-8 -*-
"""
Customers Screen - شاشة قائمة العملاء
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock

class CustomerItem(BoxLayout):
    """Customer list item widget"""

    def __init__(self, customer, on_edit, on_delete, on_pay, **kwargs):
        super().__init__(**kwargs)
        self.customer = customer
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(120)

        # Background
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Info row
        info_row = BoxLayout(orientation='horizontal', size_hint_y=0.5)

        name_phone = BoxLayout(orientation='vertical', size_hint_x=0.6)
        name_phone.add_widget(Label(
            text=f"[b]{customer['name']}[/b]",
            markup=True,
            font_size='16sp',
            color=(0.15, 0.35, 0.85, 1),
            halign='right'
        ))
        name_phone.add_widget(Label(
            text=customer['phone'],
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1),
            halign='right'
        ))
        info_row.add_widget(name_phone)

        amount_box = BoxLayout(orientation='vertical', size_hint_x=0.4)
        remaining = customer.get('remaining_amount', 0)
        amount_color = (0.2, 0.7, 0.3, 1) if remaining == 0 else (0.9, 0.3, 0.2, 1)
        amount_box.add_widget(Label(
            text=f"{remaining:,.0f} متبقي",
            font_size='13sp',
            color=amount_color,
            halign='left'
        ))
        info_row.add_widget(amount_box)

        self.add_widget(info_row)

        # Buttons row
        buttons_row = BoxLayout(orientation='horizontal', 
                               size_hint_y=0.5,
                               spacing=dp(5))

        edit_btn = Button(
            text='تعديل',
            font_size='12sp',
            background_color=(0.15, 0.35, 0.85, 1),
            size_hint_x=0.33
        )
        edit_btn.bind(on_release=lambda x: on_edit(customer['id']))

        pay_btn = Button(
            text='دفع',
            font_size='12sp',
            background_color=(0.2, 0.7, 0.3, 1),
            size_hint_x=0.33
        )
        pay_btn.bind(on_release=lambda x: on_pay(customer['id']))

        delete_btn = Button(
            text='حذف',
            font_size='12sp',
            background_color=(0.9, 0.2, 0.2, 1),
            size_hint_x=0.34
        )
        delete_btn.bind(on_release=lambda x: on_delete(customer['id']))

        buttons_row.add_widget(edit_btn)
        buttons_row.add_widget(pay_btn)
        buttons_row.add_widget(delete_btn)

        self.add_widget(buttons_row)

    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

class CustomersScreen(Screen):
    """Customers list screen"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """Build the customers screen UI"""
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
            text='[b]قائمة العملاء[/b]',
            markup=True,
            font_size='20sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.6
        )
        header.add_widget(title)

        add_btn = Button(
            text='+',
            font_size='24sp',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            size_hint_x=0.2
        )
        add_btn.bind(on_release=self.go_add)
        header.add_widget(add_btn)

        main_layout.add_widget(header)

        # Search bar
        search_box = BoxLayout(orientation='horizontal',
                              size_hint_y=None,
                              height=dp(50),
                              padding=dp(10),
                              spacing=dp(5))

        self.search_input = TextInput(
            hint_text='ابحث بالاسم او رقم الهاتف...',
            font_size='14sp',
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            size_hint_x=0.8
        )
        self.search_input.bind(text=self.on_search)

        search_btn = Button(
            text='🔍',
            font_size='18sp',
            background_color=(0.15, 0.35, 0.85, 1),
            size_hint_x=0.2
        )
        search_btn.bind(on_release=self.do_search)

        search_box.add_widget(self.search_input)
        search_box.add_widget(search_btn)
        main_layout.add_widget(search_box)

        # Customers list
        scroll = ScrollView()
        self.customers_list = BoxLayout(orientation='vertical',
                                       spacing=dp(10),
                                       padding=dp(10),
                                       size_hint_y=None)
        self.customers_list.bind(minimum_height=self.customers_list.setter('height'))

        scroll.add_widget(self.customers_list)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def _update_header(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.35, 0.85, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[0])

    def on_pre_enter(self):
        """Load customers when entering"""
        Clock.schedule_once(self.load_customers, 0.1)

    def load_customers(self, dt=None):
        """Load and display customers"""
        app = self.manager.parent
        customers = app.db.get_all_customers()
        self.display_customers(customers)

    def display_customers(self, customers):
        """Display customers in the list"""
        self.customers_list.clear_widgets()

        if not customers:
            self.customers_list.add_widget(Label(
                text='لا يوجد عملاء',
                font_size='16sp',
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(100)
            ))
            return

        for customer in customers:
            item = CustomerItem(
                customer,
                on_edit=self.edit_customer,
                on_delete=self.delete_customer,
                on_pay=self.add_payment
            )
            self.customers_list.add_widget(item)

    def on_search(self, instance, value):
        """Search as user types"""
        if len(value) >= 2:
            Clock.schedule_once(lambda dt: self.do_search(None), 0.3)

    def do_search(self, instance):
        """Perform search"""
        query = self.search_input.text.strip()
        if query:
            app = self.manager.parent
            results = app.db.search_customers(query)
            self.display_customers(results)
        else:
            self.load_customers()

    def edit_customer(self, customer_id):
        """Navigate to edit screen"""
        app = self.manager.parent
        app.switch_screen('edit_customer', customer_id=customer_id)

    def delete_customer(self, customer_id):
        """Delete customer with confirmation"""
        from kivy.uix.popup import Popup

        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        content.add_widget(Label(
            text='هل تريد حذف هذا العميل؟',
            font_size='16sp',
            color=(0.2, 0.2, 0.2, 1)
        ))

        buttons = BoxLayout(orientation='horizontal', spacing=dp(10))

        yes_btn = Button(
            text='نعم',
            background_color=(0.9, 0.2, 0.2, 1)
        )
        no_btn = Button(
            text='لا',
            background_color=(0.5, 0.5, 0.5, 1)
        )

        popup = Popup(title='تأكيد الحذف', 
                     content=content, 
                     size_hint=(0.8, 0.3))

        def confirm_delete(instance):
            app = self.manager.parent
            app.db.delete_customer(customer_id)
            popup.dismiss()
            self.load_customers()
            app.notifier.show_message('نجاح', 'تم حذف العميل بنجاح', 'success')

        yes_btn.bind(on_release=confirm_delete)
        no_btn.bind(on_release=lambda x: popup.dismiss())

        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        content.add_widget(buttons)

        popup.open()

    def add_payment(self, customer_id):
        """Navigate to payment screen"""
        app = self.manager.parent
        app.switch_screen('payments', customer_id=customer_id)

    def go_back(self, instance):
        """Go back to home"""
        app = self.manager.parent
        app.go_back()

    def go_add(self, instance):
        """Go to add customer screen"""
        app = self.manager.parent
        app.switch_screen('add_customer')
