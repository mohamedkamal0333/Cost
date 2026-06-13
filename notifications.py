# -*- coding: utf-8 -*-
"""
Notification Manager - ادارة التنبيهات والاشعارات
"""

from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle

class NotificationManager:
    """Handle app notifications and alerts"""

    def __init__(self):
        self.popup = None

    def show_renewal_notification(self, customers):
        """Show renewal notification popup"""
        if not customers:
            return

        content = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Title
        title_label = Label(
            text='[b]تنبيهات التجديد[/b]',
            markup=True,
            font_size='20sp',
            color=(0.2, 0.4, 0.8, 1),
            size_hint_y=None,
            height=40
        )
        content.add_widget(title_label)

        # Customers list
        scroll = ScrollView(size_hint=(1, 1))
        list_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))

        for customer in customers:
            item = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            item.canvas.before.clear()
            with item.canvas.before:
                Color(0.95, 0.97, 1, 1)
                RoundedRectangle(pos=item.pos, size=item.size, radius=[8])
            item.bind(pos=self._update_rect, size=self._update_rect)

            name_label = Label(
                text=customer['name'],
                font_size='14sp',
                color=(0.2, 0.2, 0.2, 1),
                size_hint_x=0.6
            )
            date_label = Label(
                text=customer['renewal_date'],
                font_size='12sp',
                color=(0.8, 0.2, 0.2, 1),
                size_hint_x=0.4
            )

            item.add_widget(name_label)
            item.add_widget(date_label)
            list_layout.add_widget(item)

        scroll.add_widget(list_layout)
        content.add_widget(scroll)

        # Close button
        close_btn = Button(
            text='اغلاق',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.5, 0.9, 1)
        )
        close_btn.bind(on_release=lambda x: self.popup.dismiss())
        content.add_widget(close_btn)

        self.popup = Popup(
            title='',
            content=content,
            size_hint=(0.9, 0.7),
            auto_dismiss=False,
            background='',
            background_color=(1, 1, 1, 1)
        )
        self.popup.open()

    def _update_rect(self, instance, value):
        """Update rectangle position"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.95, 0.97, 1, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[8])

    def show_message(self, title, message, message_type='info'):
        """Show a message popup"""
        colors = {
            'info': (0.2, 0.5, 0.9, 1),
            'success': (0.2, 0.7, 0.3, 1),
            'warning': (0.9, 0.7, 0.1, 1),
            'error': (0.9, 0.2, 0.2, 1)
        }

        content = BoxLayout(orientation='vertical', padding=20, spacing=15)

        msg_label = Label(
            text=message,
            font_size='16sp',
            color=(0.2, 0.2, 0.2, 1),
            text_size=(300, None),
            halign='center'
        )
        content.add_widget(msg_label)

        ok_btn = Button(
            text='موافق',
            size_hint_y=None,
            height=45,
            background_color=colors.get(message_type, colors['info'])
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        ok_btn.bind(on_release=lambda x: popup.dismiss())
        content.add_widget(ok_btn)

        popup.open()
