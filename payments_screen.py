# -*- coding: utf-8 -*-
"""
Payments Screen - شاشة تسجيل المدفوعات
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

class PaymentItem(BoxLayout):
    """Payment history item"""

    def __init__(self, payment, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = dp(10)
        self.size_hint_y = None
        self.height = dp(50)

        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.add_widget(Label(
            text=payment.get('payment_date', ''),
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_x=0.3
        ))
        self.add_widget(Label(
            text=f"{payment.get('amount', 0):,.0f}",
            font_size='14sp',
            color=(0.2, 0.7, 0.3, 1),
            size_hint_x=0.3
        ))
        self.add_widget(Label(
            text=payment.get('payment_method', 'cash'),
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_x=0.4
        ))

    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

class PaymentsScreen(Screen):
    """Payments management screen"""

    customer_id = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """Build payments UI"""
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
            text='[b]تسجيل الدفع[/b]',
            markup=True,
            font_size='20sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.8
        )
        header.add_widget(title)

        main_layout.add_widget(header)

        # Customer info
        self.info_box = BoxLayout(orientation='vertical',
                                  size_hint_y=None,
                                  height=dp(80),
                                  padding=dp(15))
        self.info_box.add_widget(Label(
            text='اختر عميلاً',
            font_size='16sp',
            color=(0.5, 0.5, 0.5, 1)
        ))
        main_layout.add_widget(self.info_box)

        # Payment form
        form = BoxLayout(orientation='vertical',
                        padding=dp(20),
                        spacing=dp(15),
                        size_hint_y=None,
                        height=dp(200))

        form.add_widget(Label(
            text='مبلغ الدفع',
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25)
        ))

        self.amount_input = TextInput(
            hint_text='ادخل المبلغ',
            font_size='15sp',
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.amount_input)

        form.add_widget(Label(
            text='ملاحظات',
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(25)
        ))

        self.notes_input = TextInput(
            hint_text='ملاحظات اضافية',
            font_size='15sp',
            multiline=True,
            size_hint_y=None,
            height=dp(60),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        form.add_widget(self.notes_input)

        pay_btn = Button(
            text='[b]تسجيل الدفع[/b]',
            markup=True,
            font_size='16sp',
            size_hint_y=None,
            height=dp(55),
            background_color=(0.2, 0.7, 0.3, 1)
        )
        pay_btn.bind(on_release=self.record_payment)
        form.add_widget(pay_btn)

        main_layout.add_widget(form)

        # Payment history
        history_label = Label(
            text='[b]سجل المدفوعات[/b]',
            markup=True,
            font_size='16sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(history_label)

        scroll = ScrollView()
        self.payments_list = BoxLayout(orientation='vertical',
                                      spacing=dp(5),
                                      padding=dp(10),
                                      size_hint_y=None)
        self.payments_list.bind(minimum_height=self.payments_list.setter('height'))

        scroll.add_widget(self.payments_list)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def _update_header(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.35, 0.85, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[0])

    def receive_data(self, **kwargs):
        """Receive customer ID"""
        self.customer_id = kwargs.get('customer_id')
        Clock.schedule_once(self.load_customer, 0.1)

    def load_customer(self, dt):
        """Load customer info and payments"""
        if not self.customer_id:
            return

        app = self.manager.parent
        customer = app.db.get_customer(self.customer_id)

        if customer:
            self.info_box.clear_widgets()
            info_content = BoxLayout(orientation='vertical')
            info_content.add_widget(Label(
                text=f"[b]{customer['name']}[/b]",
                markup=True,
                font_size='18sp',
                color=(0.15, 0.35, 0.85, 1)
            ))
            remaining = customer.get('remaining_amount', 0)
            color = (0.2, 0.7, 0.3, 1) if remaining == 0 else (0.9, 0.3, 0.2, 1)
            info_content.add_widget(Label(
                text=f"المتبقي: {remaining:,.0f} {app.db.get_setting('currency', 'ريال')}",
                font_size='14sp',
                color=color
            ))
            self.info_box.add_widget(info_content)

            # Load payments history
            payments = app.db.get_customer_payments(self.customer_id)
            self.payments_list.clear_widgets()

            if payments:
                for payment in payments:
                    self.payments_list.add_widget(PaymentItem(payment))
            else:
                self.payments_list.add_widget(Label(
                    text='لا توجد مدفوعات سابقة',
                    font_size='14sp',
                    color=(0.5, 0.5, 0.5, 1),
                    size_hint_y=None,
                    height=dp(50)
                ))

    def record_payment(self, instance):
        """Record new payment"""
        if not self.customer_id:
            return

        try:
            amount = float(self.amount_input.text)
        except:
            app = self.manager.parent
            app.notifier.show_message('خطأ', 'الرجاء ادخال مبلغ صحيح', 'error')
            return

        if amount <= 0:
            app = self.manager.parent
            app.notifier.show_message('خطأ', 'المبلغ يجب ان يكون اكبر من صفر', 'error')
            return

        app = self.manager.parent
        app.db.add_payment(
            self.customer_id,
            amount,
            notes=self.notes_input.text.strip()
        )

        self.amount_input.text = ''
        self.notes_input.text = ''

        app.notifier.show_message('نجاح', 'تم تسجيل الدفع بنجاح', 'success')
        Clock.schedule_once(self.load_customer, 0.1)

    def go_back(self, instance):
        app = self.manager.parent
        app.go_back()
