from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
)


def crea_finestra():
    finestra = QMainWindow()

    finestra.setWindowTitle("Delta")
    finestra.resize(1000, 650)

    pannello_centrale = QWidget()
    finestra.setCentralWidget(pannello_centrale)

    layout = QVBoxLayout()
    pannello_centrale.setLayout(layout)

    testo = QLabel("Benvenuto in Delta, le auguriamo una buona esperienza di utilizzo :)")
    layout.addWidget(testo)

    return finestra