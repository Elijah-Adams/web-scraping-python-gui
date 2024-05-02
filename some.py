import sys
import random
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Word Occurrences Graph")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.generate_button = QPushButton("Generate Data")
        self.generate_button.clicked.connect(self.plot_data)
        self.layout.addWidget(self.generate_button)

    def plot_data(self):
        # Generate random data (word sizes and occurrences)
        word_sizes = [random.randint(1, 10) for _ in range(10)]
        occurrences = [random.randint(1, 50) for _ in range(10)]

        # Plot the data
        self.ax.clear()
        self.ax.bar(word_sizes, occurrences, width=0.5)
        self.ax.set_xlabel("Word Size")
        self.ax.set_ylabel("Occurrences")
        self.ax.set_title("Word Occurrences by Size")
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())