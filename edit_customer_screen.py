# -*- coding: utf-8 -*-
"""
Edit Customer Screen - شاشة تعديل بيانات العميل
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

class EditCustomerScreen(Screen):
    """Edit customer screen"""

    customer_id = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """Build the edit customer UI"""
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
            text='[b]تعديل بيانات العميل[/b]',
            markup=True,
            font_size='20sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.8
        )
        header.add_widget(title)

        main_layout.add_widget(header)

        # Form
        scroll = ScrollView()
        form = BoxLayout(orientation='vertical',
                        padding=dp(20),
                        spacing=dp(15),
                        size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))

        # Name
        form.add_widget(self._create_label('الاسم'))
        self.name_input = TextInput(
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.name_input)

        # Phone
        form.add_widget(self._create_label('رقم الهاتف'))
        self.phone_input = TextInput(
            font_size='15sp',
            multiline=False,
            input_filter='int',
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.phone_input)

        # Email
        form.add_widget(self._create_label('البريد الالكتروني'))
        self.email_input = TextInput(
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.email_input)

        # Address
        form.add_widget(self._create_label('العنوان'))
        self.address_input = TextInput(
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.address_input)

        # Service Type
        form.add_widget(self._create_label('نوع الخدمة'))
        self.service_input = TextInput(
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.service_input)

        # Amount
        form.add_widget(self._create_label('المبلغ'))
        self.amount_input = TextInput(
            font_size='15sp',
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.amount_input)

        # Dates
        form.add_widget(self._create_label('تاريخ البدء'))
        self.start_date_input = TextInput(
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.start_date_input)

        form.add_widget(self._create_label('تاريخ الانتهاء'))
        self.end_date_input = TextInput(
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.end_date_input)

        form.add_widget(self._create_label('تاريخ التجديد'))
        self.renewal_date_input = TextInput(
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.renewal_date_input)

        # Notes
        form.add_widget(self._create_label('ملاحظات'))
        self.notes_input = TextInput(
            font_size='15sp',
            multiline=True,
            size_hint_y=None,
            height=dp(80),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.notes_input)

        # Status
        form.add_widget(self._create_label('الحالة'))
        self.status_input = TextInput(
            hint_text='active / inactive',
            font_size='15sp',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.status_input)

        # Submit button
        submit_btn = Button(
            text='[b]تحديث البيانات[/b]',
            markup=True,
            font_size='16sp',
            size_hint_y=None,
            height=dp(55),
            background_color=(0.2, 0.7, 0.3, 1)
        )
        submit_btn.bind(on_release=self.update_customer)
        form.add_widget(submit_btn)

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

    def receive_data(self, **kwargs):
        """Receive customer data"""
        self.customer_id = kwargs.get('customer_id')
        Clock.schedule_once(self.load_customer_data, 0.1)

    def load_customer_data(self, dt):
        """Load customer data into form"""
        if not self.customer_id:
            return

        app = self.manager.parent
        customer = app.db.get_customer(self.customer_id)

        if customer:
            self.name_input.text = customer.get('name', '')
            self.phone_input.text = customer.get('phone', '')
            self.email_input.text = customer.get('email', '')
            self.address_input.text = customer.get('address', '')
            self.service_input.text = customer.get('service_type', '')
            self.amount_input.text = str(customer.get('amount', ''))
            self.start_date_input.text = customer.get('start_date', '')
            self.end_date_input.text = customer.get('end_date', '')
            self.renewal_date_input.text = customer.get('renewal_date', '')
            self.notes_input.text = customer.get('notes', '')
            self.status_input.text = customer.get('status', 'active')

    def update_customer(self, instance):
        """Update customer data"""
        if not self.customer_id:
            return

        name = self.name_input.text.strip()
        phone = self.phone_input.text.strip()

        if not name or not phone:
            app = self.manager.parent
            app.notifier.show_message('خطأ', 'الرجاء ادخال الاسم ورقم الهاتف', 'error')
            return

        try:
            amount = float(self.amount_input.text or 0)
        except:
            amount = 0

        app = self.manager.parent
        app.db.update_customer(
            self.customer_id,
            name=name,
            phone=phone,
            email=self.email_input.text.strip(),
            address=self.address_input.text.strip(),
            service_type=self.service_input.text.strip(),
            amount=amount,
            start_date=self.start_date_input.text.strip(),
            end_date=self.end_date_input.text.strip(),
            renewal_date=self.renewal_date_input.text.strip(),
            notes=self.notes_input.text.strip(),
            status=self.status_input.text.strip() or 'active'
        )

        app.notifier.show_message('نجاح', 'تم تحديث البيانات بنجاح', 'success')
        app.go_back()

    def go_back(self, instance):
        app = self.manager.parent
        app.go_back()
