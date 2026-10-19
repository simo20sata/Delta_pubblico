
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFrame,
    QScrollArea,
)
from PySide6.QtCore import Qt
from datetime import datetime


def crea_finestra():
    finestra = QMainWindow()
    finestra.setWindowTitle("Delta")
    finestra.resize(1200, 750)
    finestra.setMinimumSize(900, 600)

    # Stato locale dell'interfaccia
    sezione_corrente = "Chat globale"
    cronologia = {
        "Chat globale": [],
        "Messaggi privati": [],
        "Canali": [],
    }

    # Widget centrale
    centrale = QWidget()
    finestra.setCentralWidget(centrale)

    layout_principale = QHBoxLayout(centrale)
    layout_principale.setContentsMargins(0, 0, 0, 0)
    layout_principale.setSpacing(0)

    # Barra laterale
    barra = QFrame()
    barra.setObjectName("barraLaterale")
    barra.setFixedWidth(230)

    layout_barra = QVBoxLayout(barra)
    layout_barra.setContentsMargins(16, 20, 16, 16)
    layout_barra.setSpacing(10)

    logo = QLabel("Delta")
    logo.setObjectName("logo")
    layout_barra.addWidget(logo)

    separatore = QFrame()
    separatore.setFrameShape(QFrame.Shape.HLine)
    layout_barra.addWidget(separatore)

    titolo_navigazione = QLabel("NAVIGAZIONE")
    titolo_navigazione.setObjectName("titoloSezione")
    layout_barra.addWidget(titolo_navigazione)

    btn_globale = QPushButton("Chat globale")
    btn_privati = QPushButton("Messaggi privati")
    btn_canali = QPushButton("Canali")
    btn_impostazioni = QPushButton("Impostazioni")

    pulsanti_nav = {
        "Chat globale": btn_globale,
        "Messaggi privati": btn_privati,
        "Canali": btn_canali,
    }

    for pulsante in pulsanti_nav.values():
        pulsante.setObjectName("pulsanteNavigazione")
        pulsante.setCursor(Qt.CursorShape.PointingHandCursor)
        layout_barra.addWidget(pulsante)

    layout_barra.addStretch()

    profilo = QFrame()
    profilo.setObjectName("profilo")
    layout_profilo = QVBoxLayout(profilo)

    nome_utente = QLabel("Utente Delta")
    nome_utente.setObjectName("nomeUtente")

    stato_utente = QLabel("Online • locale")
    stato_utente.setObjectName("statoUtente")

    layout_profilo.addWidget(nome_utente)
    layout_profilo.addWidget(stato_utente)
    layout_barra.addWidget(profilo)

    btn_impostazioni.setObjectName("pulsanteNavigazione")
    btn_impostazioni.setCursor(
        Qt.CursorShape.PointingHandCursor
    )
    layout_barra.addWidget(btn_impostazioni)

    layout_principale.addWidget(barra)

    # Area principale
    area = QWidget()
    area.setObjectName("areaPrincipale")

    layout_area = QVBoxLayout(area)
    layout_area.setContentsMargins(24, 20, 24, 20)
    layout_area.setSpacing(16)

    # Intestazione
    intestazione = QFrame()
    intestazione.setObjectName("intestazione")
    layout_intestazione = QVBoxLayout(intestazione)

    titolo_chat = QLabel()
    titolo_chat.setObjectName("titoloChat")

    descrizione_chat = QLabel()
    descrizione_chat.setObjectName("descrizioneChat")

    layout_intestazione.addWidget(titolo_chat)
    layout_intestazione.addWidget(descrizione_chat)
    layout_area.addWidget(intestazione)

    # Area scorrevole dei messaggi
    area_scorrimento = QScrollArea()
    area_scorrimento.setWidgetResizable(True)
    area_scorrimento.setObjectName("areaScorrimento")
    area_scorrimento.setHorizontalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    )

    contenuto_messaggi = QWidget()
    layout_messaggi = QVBoxLayout(contenuto_messaggi)
    layout_messaggi.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout_messaggi.setSpacing(10)

    area_scorrimento.setWidget(contenuto_messaggi)
    layout_area.addWidget(area_scorrimento, 1)

    # Campo di scrittura
    contenitore_input = QFrame()
    contenitore_input.setObjectName("contenitoreInput")
    layout_input = QHBoxLayout(contenitore_input)
    layout_input.setContentsMargins(12, 8, 12, 8)

    campo_messaggio = QLineEdit()
    campo_messaggio.setPlaceholderText(
        "Scrivi un messaggio..."
    )
    campo_messaggio.setObjectName("campoMessaggio")

    btn_invia = QPushButton("Invia")
    btn_invia.setObjectName("pulsanteInvia")
    btn_invia.setCursor(Qt.CursorShape.PointingHandCursor)

    layout_input.addWidget(campo_messaggio, 1)
    layout_input.addWidget(btn_invia)

    layout_area.addWidget(contenitore_input)
    layout_principale.addWidget(area, 1)

    def mostra_messaggi():
        # Elimina i messaggi visibili, non la cronologia salvata
        while layout_messaggi.count():
            elemento = layout_messaggi.takeAt(0)
            widget = elemento.widget()
            if widget is not None:
                widget.deleteLater()

        messaggi = cronologia.get(sezione_corrente, [])

        if not messaggi:
            testo = QLabel(
                "Nessun messaggio in questa sezione.\n"
                "Scrivi qui sotto per aggiungerne uno."
            )
            testo.setObjectName("testoBenvenuto")
            testo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            testo.setWordWrap(True)
            layout_messaggi.addStretch()
            layout_messaggi.addWidget(testo)
            layout_messaggi.addStretch()
            return

        for messaggio in messaggi:
            scheda = QFrame()
            scheda.setObjectName("schedaMessaggio")
            layout_scheda = QVBoxLayout(scheda)

            autore = QLabel(
                f"{messaggio['autore']}  •  "
                f"{messaggio['ora']}"
            )
            autore.setObjectName("autoreMessaggio")

            testo = QLabel(messaggio["testo"])
            testo.setObjectName("testoMessaggio")
            testo.setWordWrap(True)
            testo.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )

            layout_scheda.addWidget(autore)
            layout_scheda.addWidget(testo)
            layout_messaggi.addWidget(scheda)

        layout_messaggi.addStretch()

        barra_verticale = area_scorrimento.verticalScrollBar()
        barra_verticale.setValue(barra_verticale.maximum())

    def cambia_sezione(nome):
        nonlocal sezione_corrente
        sezione_corrente = nome

        titoli = {
            "Chat globale": (
                "Chat globale",
                "Area locale di prova della chat globale."
            ),
            "Messaggi privati": (
                "Messaggi privati",
                "Spazio dimostrativo per le conversazioni private."
            ),
            "Canali": (
                "Canali",
                "Area dimostrativa per i canali di Delta."
            ),
            "Impostazioni": (
                "Impostazioni",
                "Configurazione iniziale dell'interfaccia."
            ),
        }

        titolo, descrizione = titoli[nome]
        titolo_chat.setText(titolo)
        descrizione_chat.setText(descrizione)

        for nome_pulsante, pulsante in pulsanti_nav.items():
            attivo = nome_pulsante == nome
            pulsante.setProperty("attivo", attivo)
            pulsante.style().unpolish(pulsante)
            pulsante.style().polish(pulsante)

        # Nasconde la scrittura nelle impostazioni
        scrittura_attiva = nome != "Impostazioni"
        contenitore_input.setVisible(scrittura_attiva)

        if nome == "Impostazioni":
            while layout_messaggi.count():
                elemento = layout_messaggi.takeAt(0)
                widget = elemento.widget()
                if widget is not None:
                    widget.deleteLater()

            info = QLabel(
                "Delta - Versione 1.1.0.0\n\n"
                "Stato: prototipo locale\n"
                "Utente: Utente Delta\n"
                "Messaggi: salvati solo in memoria\n"
                "Server: non collegato"
            )
            info.setObjectName("testoBenvenuto")
            info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info.setWordWrap(True)
            layout_messaggi.addWidget(info)
        else:
            mostra_messaggi()

    def invia_messaggio():
        testo = campo_messaggio.text().strip()

        if not testo or sezione_corrente == "Impostazioni":
            return

        ora = datetime.now().strftime("%H:%M")

        cronologia[sezione_corrente].append({
            "autore": "Utente Delta",
            "ora": ora,
            "testo": testo,
        })

        campo_messaggio.clear()
        mostra_messaggi()

    # Collega i pulsanti alle funzioni
    btn_globale.clicked.connect(
        lambda: cambia_sezione("Chat globale")
    )
    btn_privati.clicked.connect(
        lambda: cambia_sezione("Messaggi privati")
    )
    btn_canali.clicked.connect(
        lambda: cambia_sezione("Canali")
    )
    btn_impostazioni.clicked.connect(
        lambda: cambia_sezione("Impostazioni")
    )

    btn_invia.clicked.connect(invia_messaggio)
    campo_messaggio.returnPressed.connect(invia_messaggio)

    # Stile grafico
    finestra.setStyleSheet("""
        QMainWindow {
            background-color: #191b24;
        }

        #barraLaterale {
            background-color: #222531;
            border-right: 1px solid #343746;
        }

        #logo {
            color: #ffffff;
            font-size: 28px;
            font-weight: bold;
            padding-bottom: 8px;
        }

        #titoloSezione {
            color: #858ba3;
            font-size: 11px;
            font-weight: bold;
            padding-top: 8px;
        }

        #pulsanteNavigazione {
            background-color: transparent;
            color: #c9ccda;
            border: none;
            border-radius: 6px;
            text-align: left;
            padding: 11px 8px;
            font-size: 13px;
        }

        #pulsanteNavigazione:hover {
            background-color: #343746;
            color: #ffffff;
        }

        #pulsanteNavigazione[attivo="true"] {
            background-color: #3b4160;
            color: #ffffff;
        }

        #profilo {
            background-color: #2b2f3d;
            border-radius: 8px;
            padding: 5px;
        }

        #nomeUtente {
            color: #ffffff;
            font-weight: bold;
        }

        #statoUtente {
            color: #55d69e;
            font-size: 11px;
        }

        #areaPrincipale {
            background-color: #191b24;
        }

        #intestazione {
            background-color: #222531;
            border-radius: 8px;
            padding: 4px;
        }

        #titoloChat {
            color: #ffffff;
            font-size: 21px;
            font-weight: bold;
        }

        #descrizioneChat {
            color: #9298ad;
            font-size: 12px;
        }

        #areaScorrimento {
            background-color: #1e202b;
            border: 1px solid #303342;
            border-radius: 8px;
        }

        #areaScorrimento QWidget {
            background-color: transparent;
        }

        #schedaMessaggio {
            background-color: #292c39;
            border: 1px solid #383c4d;
            border-radius: 8px;
        }

        #autoreMessaggio {
            color: #9da8ff;
            font-size: 11px;
            font-weight: bold;
        }

        #testoMessaggio {
            color: #f0f1f7;
            font-size: 14px;
        }

        #testoBenvenuto {
            color: #9298ad;
            font-size: 14px;
            padding: 18px;
        }

        #contenitoreInput {
            background-color: #292c39;
            border: 1px solid #3a3e50;
            border-radius: 8px;
        }

        #campoMessaggio {
            background-color: transparent;
            color: #ffffff;
            border: none;
            padding: 8px;
            font-size: 13px;
        }

        #pulsanteInvia {
            background-color: #6575e8;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: bold;
        }

        #pulsanteInvia:hover {
            background-color: #7887f2;
        }

        QScrollBar:vertical {
            background-color: #1e202b;
            width: 10px;
        }

        QScrollBar::handle:vertical {
            background-color: #454a60;
            border-radius: 4px;
            min-height: 25px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)

    cambia_sezione("Chat globale")
    return finestra
