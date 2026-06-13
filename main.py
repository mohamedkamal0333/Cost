# -*- coding: utf-8 -*-
"""
Customer Manager App - تطبيق ادارة العملاء
Created with Kivy for Android
"""

from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
import os
import sys

# Add src to path
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from screens.home_screen import HomeScreen
from screens.customers_screen import CustomersScreen
from screens.add_customer_screen import AddCustomerScreen
from screens.edit_customer_screen import EditCustomerScreen
from screens.payments_screen import PaymentsScreen
from screens.reports_screen import ReportsScreen
from screens.settings_screen import SettingsScreen
from screens.search_screen import SearchScreen
from utils.database import DatabaseManager
from utils.notifications import NotificationManager

# Register fonts
fonts_dir = os.path.join(base_dir, 'src', 'assets', 'fonts')
os.makedirs(fonts_dir, exist_ok=True)

# Try to register Cairo font, fallback to system font
try:
    cairo_font = os.path.join(fonts_dir, 'Cairo-Regular.ttf')
    if os.path.exists(cairo_font):
        LabelBase.register(name='Cairo', fn_regular=cairo_font)
    else:
        # Use system fallback
        LabelBase.register(name='Cairo', fn_regular='DroidSansFallback.ttf')
except:
    pass

# Set default font for RTL support
import kivy.uix.label
kivy.uix.label.Label.font_name = 'Cairo'

class CustomerManagerApp(App):
    """Main Application Class"""

    db = ObjectProperty(None)
    notifier = ObjectProperty(None)
    current_screen = StringProperty('home')

    def build(self):
        """Build the application"""
        # Window settings
        Window.clearcolor = (0.95, 0.96, 0.98, 1)

        # Initialize database
        self.db = DatabaseManager()
        self.db.init_database()

        # Initialize notifications
        self.notifier = NotificationManager()

        # Create Screen Manager
        self.sm = ScreenManager(transition=SlideTransition())

        # Add screens
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(CustomersScreen(name='customers'))
        self.sm.add_widget(AddCustomerScreen(name='add_customer'))
        self.sm.add_widget(EditCustomerScreen(name='edit_customer'))
        self.sm.add_widget(PaymentsScreen(name='payments'))
        self.sm.add_widget(ReportsScreen(name='reports'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(SearchScreen(name='search'))

        # Check for renewal reminders
        Clock.schedule_once(self.check_renewals, 3)

        # Schedule periodic renewal checks
        Clock.schedule_interval(self.check_renewals, 3600)  # Every hour

        return self.sm

    def check_renewals(self, dt):
        """Check for upcoming renewals"""
        try:
            days = int(self.db.get_setting('renewal_days', '7'))
            upcoming = self.db.get_upcoming_renewals(days=days)
            if upcoming:
                self.notifier.show_renewal_notification(upcoming)
        except:
            pass

    def switch_screen(self, screen_name, **kwargs):
        """Switch to another screen"""
        try:
            screen = self.sm.get_screen(screen_name)
            if hasattr(screen, 'on_pre_enter'):
                screen.on_pre_enter()
            if kwargs and hasattr(screen, 'receive_data'):
                screen.receive_data(**kwargs)
            self.sm.current = screen_name
            self.current_screen = screen_name
        except Exception as e:
            print(f"Error switching screen: {e}")

    def go_back(self):
        """Go back to previous screen"""
        if self.sm.current != 'home':
            self.sm.transition.direction = 'right'
            self.sm.current = 'home'
            self.sm.transition.direction = 'left'

    def on_pause(self):
        """Handle app pause"""
        return True

    def on_resume(self):
        """Handle app resume"""
        pass

if __name__ == '__main__':
    CustomerManagerApp().run()
