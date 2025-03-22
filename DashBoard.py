import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QHBoxLayout


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurazione finestra principale
        self.setWindowTitle("Formula 1")
        self.setGeometry(100, 100, 800, 600)

        # Layout principale
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout verticale
        self.layout = QVBoxLayout()


        # Aggiungere widget
        self.label = QLabel("Menu")
        self.label.setStyleSheet("font-size: 30px; font-weight: bold; color: red")

        # Layout orizzontale per centrare il widget in alto
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addStretch()  # Aggiungi uno spazio flessibile a sinistra
        self.horizontal_layout.addWidget(self.label)  # Aggiungi il widget al centro
        self.horizontal_layout.addStretch()  # Aggiungi uno spazio flessibile a sinistra

        # Aggiungi il layout orizzontale (centrato) al layout verticale
        self.layout.addLayout(self.horizontal_layout)

        # Aggiungi uno spazio flessibile prima del widget per posizionarlo in alto
        self.layout.addStretch()  # Spazio flessibile sopra il widget
        self.layout.addLayout(self.horizontal_layout)  # Aggiungi il layout orizzontale con il widget
        #self.layout.addStretch()  # Spazio flessibile sotto il widget (non necessario)

        # Pulsante
        self.button = QPushButton("Cliccami!")
        self.button.resize(20, 60)
        self.button.clicked.connect(self.open_second_window)
        self.layout.addWidget(self.button)

        # Pulsante
        self.button = QPushButton("Cliccami!")
        self.button.resize(20, 60)
        self.button.clicked.connect(self.button_clicked)
        self.layout.addWidget(self.button)

        # Pulsante
        self.button = QPushButton("Cliccami!")
        self.button.resize(20, 60)
        self.button.clicked.connect(self.button_clicked)
        self.layout.addWidget(self.button)

        self.layout.addStretch()  # Spazio flessibile sotto il widget (non necessario)

        # Imposta layout al central widget
        self.central_widget.setLayout(self.layout)

    def button_clicked(self):
        self.label.setText("Classifica Costruttori.")

    def open_second_window(self):
        # Crea e mostra la seconda finestra
        self.second_window = SecondPage()  # Crea la seconda finestra
        self.second_window.show()  # Mostra la seconda finestra

class SecondPage(QWidget):
    def __init__(self):
        super().__init__()

        # Configurazione della seconda finestra
        self.setWindowTitle("Seconda Finestra")
        self.setGeometry(200, 200, 400, 300)

        # Aggiungi un'etichetta o altri widget per questa finestra
        self.label = QPushButton("Questa è la seconda finestra!")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

# Avvio dell'applicazione
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())

