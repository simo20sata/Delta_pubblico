import sys
from PySide6.QtWidgets import QApplication
from interfaccia import crea_finestra

app = QApplication(sys.argv)

finestra = crea_finestra()
finestra.show()

sys.exit(app.exec())