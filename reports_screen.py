# -*- coding: utf-8 -*-
"""
Reports Screen - شاشة التقارير والاحصائيات
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock

class ReportCard(BoxLayout):
    """Report statistics card"""

    def __init__(self, title, value, color, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(100)

        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color[:3], 0.1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            Color(*color)
            RoundedRectangle(pos=(self.x + dp(2), self.y + dp(2)),
                           size=(self.width - dp(4), self.height - dp(4)),
                           radius=[dp(10)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.add_widget(Label(
            text=str(value),
            font_size='24sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=0.5
        ))
        self.add_widget(Label(
            text=title,
            font_size='13sp',
            color=(1, 1, 1, 0.9),
            size_hint_y=0.5
        ))

    def _update_bg(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.95, 0.96, 0.98, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])

class ReportsScreen(Screen):
    """Reports and statistics screen"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """Build reports UI"""
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
            text='[b]التقارير والاحصائيات[/b]',
            markup=True,
            font_size='20sp',
            color=(1, 1, 1, 1),
            size_hint_x=0.8
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

        # Statistics cards
        stats_label = Label(
            text='[b]احصائيات عامة[/b]',
            markup=True,
            font_size='18sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        content.add_widget(stats_label)

        self.stats_grid = GridLayout(cols=2,
                                     spacing=dp(10),
                                     size_hint_y=None,
                                     height=dp(220))

        self.stat_cards = {
            'customers': ReportCard('اجمالي العملاء', '0', (0.15, 0.35, 0.85)),
            'amount': ReportCard('اجمالي المبالغ', '0', (0.2, 0.7, 0.3)),
            'paid': ReportCard('المدفوع', '0', (0.1, 0.6, 0.5)),
            'remaining': ReportCard('المتبقي', '0', (0.9, 0.3, 0.2)),
        }

        for card in self.stat_cards.values():
            self.stats_grid.add_widget(card)

        content.add_widget(self.stats_grid)

        # Export section
        export_label = Label(
            text='[b]تصدير البيانات[/b]',
            markup=True,
            font_size='18sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        content.add_widget(export_label)

        export_box = BoxLayout(orientation='horizontal',
                              spacing=dp(10),
                              size_hint_y=None,
                              height=dp(60))

        csv_btn = Button(
            text='تصدير CSV',
            font_size='14sp',
            background_color=(0.15, 0.35, 0.85, 1)
        )
        csv_btn.bind(on_release=self.export_csv)

        excel_btn = Button(
            text='تصدير Excel',
            font_size='14sp',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        excel_btn.bind(on_release=self.export_excel)

        export_box.add_widget(csv_btn)
        export_box.add_widget(excel_btn)
        content.add_widget(export_box)

        # Export status
        self.export_status = Label(
            text='',
            font_size='14sp',
            color=(0.2, 0.7, 0.3, 1),
            size_hint_y=None,
            height=dp(30)
        )
        content.add_widget(self.export_status)

        # Overdue customers
        overdue_label = Label(
            text='[b]العملاء المتأخرين[/b]',
            markup=True,
            font_size='18sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        content.add_widget(overdue_label)

        self.overdue_box = BoxLayout(orientation='vertical',
                                    size_hint_y=None,
                                    height=dp(100))
        self.overdue_box.add_widget(Label(
            text='جاري التحميل...',
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1)
        ))
        content.add_widget(self.overdue_box)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def _update_header(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.35, 0.85, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[0])

    def on_pre_enter(self):
        """Load data when entering"""
        Clock.schedule_once(self.load_statistics, 0.1)
        Clock.schedule_once(self.load_overdue, 0.2)

    def load_statistics(self, dt):
        """Load and display statistics"""
        app = self.manager.parent
        stats = app.db.get_statistics()
        currency = app.db.get_setting('currency', 'ريال')

        self.stat_cards['customers'].children[1].text = str(stats['total_customers'])
        self.stat_cards['amount'].children[1].text = f"{stats['total_amount']:,.0f}"
        self.stat_cards['paid'].children[1].text = f"{stats['total_paid']:,.0f}"
        self.stat_cards['remaining'].children[1].text = f"{stats['total_remaining']:,.0f}"

    def load_overdue(self, dt):
        """Load overdue customers"""
        app = self.manager.parent
        overdue = app.db.get_overdue_customers()

        self.overdue_box.clear_widgets()

        if overdue:
            self.overdue_box.height = dp(50) * len(overdue) + dp(20)
            for customer in overdue:
                item = BoxLayout(orientation='horizontal',
                                size_hint_y=None,
                                height=dp(45))
                item.add_widget(Label(
                    text=customer['name'],
                    font_size='14sp',
                    color=(0.2, 0.2, 0.2, 1),
                    size_hint_x=0.6
                ))
                item.add_widget(Label(
                    text=f"{customer['remaining_amount']:,.0f}",
                    font_size='14sp',
                    color=(0.9, 0.2, 0.2, 1),
                    size_hint_x=0.4
                ))
                self.overdue_box.add_widget(item)
        else:
            self.overdue_box.height = dp(60)
            self.overdue_box.add_widget(Label(
                text='لا يوجد عملاء متأخرين',
                font_size='14sp',
                color=(0.5, 0.5, 0.5, 1)
            ))

    def export_csv(self, instance):
        """Export to CSV"""
        from utils.export_manager import ExportManager

        app = self.manager.parent
        data = app.db.get_all_data_for_export()

        exporter = ExportManager()
        filepath = exporter.export_to_csv(data)

        self.export_status.text = f'تم التصدير: {filepath}'
        app.notifier.show_message('نجاح', 'تم تصدير البيانات الى CSV', 'success')

    def export_excel(self, instance):
        """Export to Excel"""
        from utils.export_manager import ExportManager

        app = self.manager.parent
        data = app.db.get_all_data_for_export()

        exporter = ExportManager()
        filepath = exporter.export_to_excel(data)

        self.export_status.text = f'تم التصدير: {filepath}'
        app.notifier.show_message('نجاح', 'تم تصدير البيانات الى Excel', 'success')

    def go_back(self, instance):
        app = self.manager.parent
        app.go_back()
