import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QSplitter, QSizePolicy
from PyQt5.QtCore import Qt
import requests 
from bs4 import BeautifulSoup 
from dataclasses import dataclass
import json
import re
import copy

class ParentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # Create a horizontal layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Set contents margins to zero

        # Create four buttons and add them to the layout
        buttons = ['HTML', 'Text', 'Keywords', 'hrefs']
        for i in range(4):
            button = QPushButton(buttons[i])
            button.setObjectName(buttons[i])
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy
            button.setCheckable(True)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                    border: none;
                    padding: 8px 16px;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                }
                QPushButton:checked {
                    background-color: #404040;
                    border-bottom: 2px solid #FFD700;
                }
            """)
            layout.addWidget(button, stretch=1)

        # Set the layout for the widget
        self.setLayout(layout)

class WordDisplayWidget(QWidget):
    def __init__(self):
        self.main_html = 'HTML'
        self.main_text = 'Text'
        self.main_keywords = 'Keywords'
        self.main_hrefs = 'hrefs'
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle('Web Scraper')
        self.setGeometry(1000, 250, 1000, 1000)

        # Set dark mode stylesheet
        self.setStyleSheet("QWidget { background-color: #222; color: #eee; }")

        # Create layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Splitter
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)

        # Text box
        self.textbox = QTextEdit(self)
        self.textbox.setPlaceholderText("Enter a URL")  # Placeholder text
        self.textbox.setText("https://omscs.gatech.edu/current-courses")
        self.textbox.textChanged.connect(self.on_text_changed)  # Connect textChanged signal
        self.textbox.setMinimumHeight(100)
        self.textbox.setStyleSheet("QTextEdit { background-color: #333; color: #eee; border-style: none; }")
        splitter.addWidget(self.textbox)

        # Button
        self.display_button = QPushButton('Scrape URL', self)
        self.display_button.clicked.connect(self.display_words)
        self.display_button.setStyleSheet(
            '''
            QPushButton {
                background-color: #333;
                color: #eee;
                border-width: 1px;
                border-radius: 10px;
                border-color: #bbb;
                padding: 6px;
                margin: 6px 0px 6px 0px;
                font: bold 12px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #777;
            }
            '''
        )
        splitter.addWidget(self.display_button)

        self.display_area = QTextEdit(self)
        # Buttons
        self.parent_widget = ParentWidget()
        splitter.addWidget(self.parent_widget)
        self.current_button = self.parent_widget.findChildren(QWidget)[0]
        self.on_clicked(self.current_button)
        # HTML
        self.parent_widget.findChildren(QWidget)[0].clicked.connect(self.set_html)
        self.parent_widget.findChildren(QWidget)[0].clicked.connect(lambda: self.on_clicked(self.parent_widget.findChildren(QWidget)[0]))
        # Text
        self.parent_widget.findChildren(QWidget)[1].clicked.connect(self.set_text)
        self.parent_widget.findChildren(QWidget)[1].clicked.connect(lambda: self.on_clicked(self.parent_widget.findChildren(QWidget)[1]))
        # Keywords
        self.parent_widget.findChildren(QWidget)[2].clicked.connect(self.set_keywords)
        self.parent_widget.findChildren(QWidget)[2].clicked.connect(lambda: self.on_clicked(self.parent_widget.findChildren(QWidget)[2]))
        # hrefs
        self.parent_widget.findChildren(QWidget)[3].clicked.connect(self.set_hrefs)
        self.parent_widget.findChildren(QWidget)[3].clicked.connect(lambda: self.on_clicked(self.parent_widget.findChildren(QWidget)[3]))

        # Display area
        self.display_area.setLineWrapMode(QTextEdit.NoWrap)
        self.display_area.setStyleSheet("QTextEdit { background-color: #333; color: #eee; border-style: none; }")
                # Apply style sheet to the scroll bar
        self.display_area.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                background: #2E2E2E;
                width: 15px;
                margin: 15px 0 15px 0;
            }
            QScrollBar::handle:vertical {
                background: #404040;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical {
                background: none;
                height: 15px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background: none;
                height: 15px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar::up-arrow:vertical {
                background: #404040;
                width: 15px;
                height: 15px;
            }
            QScrollBar::down-arrow:vertical {
                background: #404040;
                width: 15px;
                height: 15px;
            }
            """)
        # Apply style sheet to the scroll bar
        self.display_area.horizontalScrollBar().setStyleSheet("""
            QScrollBar:horizontal {
                background: #2E2E2E;
                height: 15px;
                margin: 0 15px 0 15px;
            }
            QScrollBar::handle:horizontal {
                background: #404040;
                min-width: 30px;
                border-radius: 7px;
            }
            QScrollBar::add-line:horizontal {
                background: none;
                width: 15px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal {
                background: none;
                width: 15px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
            QScrollBar::left-arrow:horizontal {
                background: #404040;
                width: 15px;
                height: 15px;
            }
            QScrollBar::right-arrow:horizontal {
                background: #404040;
                width: 15px;
                height: 15px;
            }
        """)
        splitter.addWidget(self.display_area)


        # Fix splitter collapsibility and spawn location
        for index in range(splitter.count()):
            splitter.setCollapsible(index, False)
        splitter.setSizes([0, 0, 0, 10000]) # Push the last splitter widget to the top as high as it can go.

        # Get the handle for the second-to-last widget
        splitter.setHandleWidth(0)

    def on_clicked(self, button):
        if button == self.current_button:
            button.setChecked(True)
            return
        self.current_button.setChecked(False)
        button.setChecked(True)
        self.current_button = button

    def set_html(self):
        self.display_area.setPlainText(self.main_html)

    def set_text(self):
        self.display_area.setPlainText(self.main_text)
    
    def set_keywords(self):
        self.display_area.setPlainText(self.main_keywords)

    def set_hrefs(self):
        self.display_area.setPlainText(self.main_hrefs)

    def on_text_changed(self):
        # Check if the text is empty
        if self.textbox.toPlainText():
            self.textbox.setPlaceholderText("")  # Clear placeholder text
        else:
            self.textbox.setPlaceholderText("Enter a URL")  # Set placeholder text

    def clean_text(self, text=''):
        # Remove extra spaces while preserving newlines
        text = '\n'.join(' '.join(line.split()) for line in text.split('\n'))
        
        # Reduce consecutive newlines to just one newline
        text = re.sub(r'\n+', '\n', text)

        # Remove leading newlines
        while text.startswith('\n'):
            text = text[1:]

        # Remove trailing newlines
        while text.endswith('\n'):
            text = text[:-1]

        return text

    def parse_html_for_keywords(self, soup):
        # Extract text content
        text = soup.get_text(separator=' ', strip=True)

        # Tokenize the text into words keeping hyphens and apostrophes
        words = re.findall(r'\b[a-zA-Z0-9\-\'’]+\b', text.lower())

        # Get unique keywords
        unique_keywords = set(words)

        return unique_keywords

    def is_valid_href(self, href):
        try:
            # Check if href is a well-formed URL
            response = requests.head(href)
            if response.status_code == 200:
                return True  # URL is valid and accessible
            else:
                return False  # URL is valid but not accessible
        except Exception as e:
            print("Error:", e)
            return False  # URL is not valid

    def get_href_links(self, soup):

        # Find all anchor tags (a) with href attributes
        href_links = list(set([link.get('href') for link in soup.find_all('a', href=True)]))

        # Remove newlines, single backslashes, and empty strings
        for href in href_links:
            if href == '/':
                href_links.remove('/')
            if href == '':
                href_links.remove('')
            if href == '\n':
                href_links.remove('\n')

        temp_href_links = []

        for href in href_links:
            url = self.textbox.toPlainText() + href if href[0] == '/' else href
            print(url)
            # if self.is_valid_href(url):
            temp_href_links.append(url)

        return set(temp_href_links)

    def scrape_website(self, url=''):
        # Making a GET request 
        try:
            r = requests.get(url) 

            # Parsing the HTML 
            s = BeautifulSoup(r.content, 'html.parser') 
            self.main_html = s.prettify()
            self.main_text = self.clean_text(s.get_text())
            # self.main_keywords = '\n'.join(set(re.sub(' +', ' ', re.sub(r"[^\w\d'\s\-]+", '', s.get_text()).lower().strip()).split()))
            self.main_keywords = '\n'.join(self.parse_html_for_keywords(s))
            self.main_hrefs = '\n'.join(sorted([item for item in self.get_href_links(s) if self.textbox.toPlainText() in item]))

        except Exception as e:
            return str(e)

        return self.main_html

    def display_words(self):
        # Disable button and textbox while loading
        self.display_button.setEnabled(False)
        self.textbox.setEnabled(False)

        # Clear previous content
        self.display_area.clear()

        # Get URL from textbox
        url = self.textbox.toPlainText()
        words = self.scrape_website(url)

        # Display words in the display area
        self.display_area.setPlainText(words)

        # Enable button and textbox after loading
        self.display_button.setEnabled(True)
        self.textbox.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application-wide dark mode stylesheet
    app.setStyleSheet("QApplication { background-color: #222; color: #eee; }")

    window = WordDisplayWidget()
    window.show()
    sys.exit(app.exec_())
