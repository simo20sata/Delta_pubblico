import os
import sys
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


def crea_finestra():
    finestra = QMainWindow()
    finestra.setWindowTitle("Delta")
    finestra.resize(1450, 820)
    finestra.setMinimumSize(1050, 650)

    # ---------------------------------------------------------
    # DATI DIMOSTRATIVI
    # Per ora restano in memoria e non vengono inviati a un server.
    # ---------------------------------------------------------
    sezione_corrente = "Chat globale"
    conversazione_corrente = "Chat globale"

    conversazioni = {
        "Chat globale": ["Chat globale"],
        "Messaggi privati": ["Mario", "Luca", "Anna"],
        "Canali": ["Generale", "Progetti", "Off-topic"],
    }

    cronologia = {
        "Chat globale": [
            {
                "autore": "Sistema Delta",
                "ora": "09:30",
                "testo": "Benvenuto nella chat globale di Delta.",
            }
        ],
        "Mario": [
            {
                "autore": "Mario",
                "ora": "09:42",
                "testo": "Ciao! Questa è una conversazione privata di prova.",
            }
        ],
        "Luca": [],
        "Anna": [],
        "Generale": [
            {
                "autore": "Sistema Delta",
                "ora": "09:45",
                "testo": "Benvenuto nel canale Generale.",
            }
        ],
        "Progetti": [],
        "Off-topic": [],
    }

    # Ogni conversazione possiede la propria cronologia dei file.
    file_condivisi = {
        nome: [] for elenco in conversazioni.values() for nome in elenco
    }

    # ---------------------------------------------------------
    # FINESTRA E LAYOUT PRINCIPALE
    # ---------------------------------------------------------
    centrale = QWidget()
    finestra.setCentralWidget(centrale)

    layout_principale = QHBoxLayout(centrale)
    layout_principale.setContentsMargins(0, 0, 0, 0)
    layout_principale.setSpacing(0)

    # ---------------------------------------------------------
    # COLONNA 1: NAVIGAZIONE
    # ---------------------------------------------------------
    barra_nav = QFrame()
    barra_nav.setObjectName("barraNav")
    barra_nav.setFixedWidth(205)

    layout_nav = QVBoxLayout(barra_nav)
    layout_nav.setContentsMargins(15, 20, 15, 16)
    layout_nav.setSpacing(9)

    logo = QLabel("Delta")
    logo.setObjectName("logo")
    layout_nav.addWidget(logo)

    linea_nav = QFrame()
    linea_nav.setFrameShape(QFrame.Shape.HLine)
    linea_nav.setObjectName("linea")
    layout_nav.addWidget(linea_nav)

    etichetta_nav = QLabel("NAVIGAZIONE")
    etichetta_nav.setObjectName("etichetta")
    layout_nav.addWidget(etichetta_nav)

    btn_globale = QPushButton("  Chat globale")
    btn_privati = QPushButton("  Messaggi privati")
    btn_canali = QPushButton("  Canali")
    btn_impostazioni = QPushButton("  Impostazioni")

    pulsanti_nav = {
        "Chat globale": btn_globale,
        "Messaggi privati": btn_privati,
        "Canali": btn_canali,
    }

    for pulsante in pulsanti_nav.values():
        pulsante.setObjectName("pulsanteNav")
        pulsante.setCursor(Qt.CursorShape.PointingHandCursor)
        pulsante.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        layout_nav.addWidget(pulsante)

    layout_nav.addStretch()

    profilo = QFrame()
    profilo.setObjectName("profilo")
    layout_profilo = QVBoxLayout(profilo)
    layout_profilo.setContentsMargins(10, 10, 10, 10)

    nome_utente = QLabel("Utente Delta")
    nome_utente.setObjectName("nomeUtente")
    stato_utente = QLabel("Online • locale")
    stato_utente.setObjectName("statoUtente")

    layout_profilo.addWidget(nome_utente)
    layout_profilo.addWidget(stato_utente)
    layout_nav.addWidget(profilo)

    btn_impostazioni.setObjectName("pulsanteNav")
    btn_impostazioni.setCursor(Qt.CursorShape.PointingHandCursor)
    layout_nav.addWidget(btn_impostazioni)

    layout_principale.addWidget(barra_nav)

    # ---------------------------------------------------------
    # COLONNA 2: ELENCO CONVERSAZIONI / CANALI
    # ---------------------------------------------------------
    colonna_elenco = QFrame()
    colonna_elenco.setObjectName("colonnaElenco")
    colonna_elenco.setFixedWidth(245)

    layout_elenco = QVBoxLayout(colonna_elenco)
    layout_elenco.setContentsMargins(13, 20, 13, 15)
    layout_elenco.setSpacing(12)

    titolo_elenco = QLabel("Conversazioni")
    titolo_elenco.setObjectName("titoloColonna")
    layout_elenco.addWidget(titolo_elenco)

    ricerca = QLineEdit()
    ricerca.setObjectName("ricerca")
    ricerca.setPlaceholderText("Cerca...")
    layout_elenco.addWidget(ricerca)

    lista_conversazioni = QListWidget()
    lista_conversazioni.setObjectName("lista")
    lista_conversazioni.setSpacing(4)
    layout_elenco.addWidget(lista_conversazioni, 1)

    layout_principale.addWidget(colonna_elenco)

    # ---------------------------------------------------------
    # COLONNA 3: CHAT
    # ---------------------------------------------------------
    area_chat = QFrame()
    area_chat.setObjectName("areaChat")

    layout_chat = QVBoxLayout(area_chat)
    layout_chat.setContentsMargins(20, 18, 20, 18)
    layout_chat.setSpacing(13)

    intestazione_chat = QFrame()
    intestazione_chat.setObjectName("intestazioneChat")
    layout_intestazione = QVBoxLayout(intestazione_chat)
    layout_intestazione.setContentsMargins(14, 12, 14, 12)

    titolo_chat = QLabel()
    titolo_chat.setObjectName("titoloChat")
    descrizione_chat = QLabel()
    descrizione_chat.setObjectName("descrizioneChat")

    layout_intestazione.addWidget(titolo_chat)
    layout_intestazione.addWidget(descrizione_chat)
    layout_chat.addWidget(intestazione_chat)

    area_scorrimento = QScrollArea()
    area_scorrimento.setObjectName("areaScorrimento")
    area_scorrimento.setWidgetResizable(True)
    area_scorrimento.setHorizontalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    )

    contenuto_messaggi = QWidget()
    layout_messaggi = QVBoxLayout(contenuto_messaggi)
    layout_messaggi.setContentsMargins(12, 12, 12, 12)
    layout_messaggi.setSpacing(10)
    layout_messaggi.setAlignment(Qt.AlignmentFlag.AlignTop)

    area_scorrimento.setWidget(contenuto_messaggi)
    layout_chat.addWidget(area_scorrimento, 1)

    contenitore_input = QFrame()
    contenitore_input.setObjectName("contenitoreInput")
    layout_input = QHBoxLayout(contenitore_input)
    layout_input.setContentsMargins(10, 7, 10, 7)
    layout_input.setSpacing(8)

    btn_allega = QPushButton("＋")
    btn_allega.setObjectName("pulsanteAllega")
    btn_allega.setToolTip("Allega un file")
    btn_allega.setCursor(Qt.CursorShape.PointingHandCursor)

    campo_messaggio = QLineEdit()
    campo_messaggio.setObjectName("campoMessaggio")
    campo_messaggio.setPlaceholderText("Scrivi un messaggio...")

    btn_invia = QPushButton("Invia")
    btn_invia.setObjectName("pulsanteInvia")
    btn_invia.setCursor(Qt.CursorShape.PointingHandCursor)

    layout_input.addWidget(btn_allega)
    layout_input.addWidget(campo_messaggio, 1)
    layout_input.addWidget(btn_invia)
    layout_chat.addWidget(contenitore_input)

    layout_principale.addWidget(area_chat, 1)

    # ---------------------------------------------------------
    # COLONNA 4: FILE DELLA CONVERSAZIONE SELEZIONATA
    # ---------------------------------------------------------
    colonna_file = QFrame()
    colonna_file.setObjectName("colonnaFile")
    colonna_file.setFixedWidth(245)

    layout_file = QVBoxLayout(colonna_file)
    layout_file.setContentsMargins(13, 20, 13, 15)
    layout_file.setSpacing(12)

    titolo_file = QLabel("File condivisi")
    titolo_file.setObjectName("titoloColonna")
    layout_file.addWidget(titolo_file)

    sottotitolo_file = QLabel("Questa conversazione")
    sottotitolo_file.setObjectName("sottotitoloFile")
    sottotitolo_file.setWordWrap(True)
    layout_file.addWidget(sottotitolo_file)

    lista_file = QListWidget()
    lista_file.setObjectName("listaFile")
    lista_file.setSpacing(4)
    layout_file.addWidget(lista_file, 1)

    nota_file = QLabel(
        "Qui compariranno i file inviati e ricevuti nella chat selezionata."
    )
    nota_file.setObjectName("notaFile")
    nota_file.setWordWrap(True)
    layout_file.addWidget(nota_file)

    layout_principale.addWidget(colonna_file)

    # ---------------------------------------------------------
    # FUNZIONI DI AGGIORNAMENTO
    # ---------------------------------------------------------
    def pulisci_layout(layout):
        while layout.count():
            elemento = layout.takeAt(0)
            widget = elemento.widget()
            if widget is not None:
                widget.deleteLater()

    def mostra_messaggi():
        pulisci_layout(layout_messaggi)
        messaggi = cronologia.get(conversazione_corrente, [])

        if not messaggi:
            vuoto = QLabel(
                "Nessun messaggio in questa conversazione.\n"
                "Scrivi qui sotto per iniziare."
            )
            vuoto.setObjectName("testoBenvenuto")
            vuoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vuoto.setWordWrap(True)
            layout_messaggi.addStretch()
            layout_messaggi.addWidget(vuoto)
            layout_messaggi.addStretch()
            return

        for messaggio in messaggi:
            scheda = QFrame()
            scheda.setObjectName("schedaMessaggio")
            layout_scheda = QVBoxLayout(scheda)
            layout_scheda.setContentsMargins(12, 9, 12, 9)
            layout_scheda.setSpacing(5)

            autore = QLabel(
                f"{messaggio['autore']}  •  {messaggio['ora']}"
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
        barra = area_scorrimento.verticalScrollBar()
        barra.setValue(barra.maximum())

    def mostra_file():
        lista_file.clear()
        sottotitolo_file.setText(
            f"File della chat: {conversazione_corrente}"
        )

        elementi = file_condivisi.get(conversazione_corrente, [])

        if not elementi:
            vuoto = QListWidgetItem("Nessun file condiviso")
            vuoto.setFlags(Qt.ItemFlag.NoItemFlags)
            lista_file.addItem(vuoto)
            return

        for elemento in elementi:
            nome = elemento["nome"]
            ora = elemento["ora"]
            direzione = elemento["direzione"]
            icona = elemento["icona"]
            item = QListWidgetItem(f"{icona}  {nome}\n     {direzione} • {ora}")
            item.setToolTip(elemento["percorso"])
            lista_file.addItem(item)

    def aggiorna_elenco():
        lista_conversazioni.clear()

        if sezione_corrente == "Impostazioni":
            titolo_elenco.setText("Impostazioni")
            return

        if sezione_corrente == "Chat globale":
            titolo_elenco.setText("Chat")
        elif sezione_corrente == "Messaggi privati":
            titolo_elenco.setText("Conversazioni")
        else:
            titolo_elenco.setText("Canali")

        for nome in conversazioni[sezione_corrente]:
            item = QListWidgetItem(nome)
            item.setData(Qt.ItemDataRole.UserRole, nome)
            lista_conversazioni.addItem(item)

            if nome == conversazione_corrente:
                lista_conversazioni.setCurrentItem(item)

    def cambia_conversazione(nome):
        nonlocal conversazione_corrente
        if not nome:
            return

        conversazione_corrente = nome
        titolo_chat.setText(nome)

        if sezione_corrente == "Chat globale":
            descrizione_chat.setText("Conversazione comune a tutti gli utenti.")
        elif sezione_corrente == "Messaggi privati":
            descrizione_chat.setText(f"Conversazione privata con {nome}.")
        else:
            descrizione_chat.setText(f"Canale Delta: {nome}.")

        mostra_messaggi()
        mostra_file()

    def cambia_sezione(nome):
        nonlocal sezione_corrente
        sezione_corrente = nome

        for nome_pulsante, pulsante in pulsanti_nav.items():
            attivo = nome_pulsante == nome
            pulsante.setProperty("attivo", attivo)
            pulsante.style().unpolish(pulsante)
            pulsante.style().polish(pulsante)

        if nome == "Impostazioni":
            titolo_chat.setText("Impostazioni")
            descrizione_chat.setText("Configurazione iniziale di Delta.")
            titolo_elenco.setText("Impostazioni")
            lista_conversazioni.clear()
            pulisci_layout(layout_messaggi)

            info = QLabel(
                "Delta - Versione 1.1.0.0\n\n"
                "Stato: prototipo locale\n"
                "Utente: Utente Delta\n"
                "Messaggi: salvati solo in memoria\n"
                "File: registrati solo localmente\n"
                "Server: non collegato"
            )
            info.setObjectName("testoBenvenuto")
            info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info.setWordWrap(True)
            layout_messaggi.addStretch()
            layout_messaggi.addWidget(info)
            layout_messaggi.addStretch()

            contenitore_input.hide()
            colonna_file.hide()
            return

        contenitore_input.show()
        colonna_file.show()

        primo_nome = conversazioni[nome][0]
        aggiorna_elenco()
        cambia_conversazione(primo_nome)

    def invia_messaggio():
        testo = campo_messaggio.text().strip()
        if not testo or sezione_corrente == "Impostazioni":
            return

        ora = datetime.now().strftime("%H:%M")
        cronologia.setdefault(conversazione_corrente, []).append({
            "autore": "Utente Delta",
            "ora": ora,
            "testo": testo,
        })

        campo_messaggio.clear()
        mostra_messaggi()

    def icona_per_file(percorso):
        estensione = os.path.splitext(percorso)[1].lower()
        if estensione == ".pdf":
            return "📕"
        if estensione in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
            return "🖼️"
        if estensione in (".zip", ".rar", ".7z"):
            return "📦"
        if estensione in (".doc", ".docx", ".odt", ".txt"):
            return "📄"
        return "📎"

    def allega_file():
        if sezione_corrente == "Impostazioni":
            return

        percorsi, _ = QFileDialog.getOpenFileNames(
            finestra,
            "Seleziona uno o più file",
            "",
            "Tutti i file (*.*)",
        )

        if not percorsi:
            return

        ora = datetime.now().strftime("%H:%M")
        for percorso in percorsi:
            nome = os.path.basename(percorso)
            file_condivisi.setdefault(conversazione_corrente, []).append({
                "nome": nome,
                "percorso": percorso,
                "ora": ora,
                "direzione": "Inviato",
                "icona": icona_per_file(percorso),
            })

            cronologia.setdefault(conversazione_corrente, []).append({
                "autore": "Utente Delta",
                "ora": ora,
                "testo": f"📎 File allegato: {nome}",
            })

        mostra_messaggi()
        mostra_file()

    def filtra_conversazioni(testo):
        ricerca_testo = testo.casefold()
        for indice in range(lista_conversazioni.count()):
            item = lista_conversazioni.item(indice)
            item.setHidden(ricerca_testo not in item.text().casefold())

    # ---------------------------------------------------------
    # COLLEGAMENTI DEI PULSANTI
    # ---------------------------------------------------------
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

    lista_conversazioni.currentItemChanged.connect(
        lambda corrente, precedente: (
            cambia_conversazione(corrente.data(Qt.ItemDataRole.UserRole))
            if corrente is not None and sezione_corrente != "Impostazioni"
            else None
        )
    )

    btn_invia.clicked.connect(invia_messaggio)
    campo_messaggio.returnPressed.connect(invia_messaggio)
    btn_allega.clicked.connect(allega_file)
    ricerca.textChanged.connect(filtra_conversazioni)

    # ---------------------------------------------------------
    # STILE GRAFICO
    # ---------------------------------------------------------
    finestra.setStyleSheet("""
        QMainWindow {
            background-color: #191b24;
        }

        #barraNav {
            background-color: #222531;
            border-right: 1px solid #343746;
        }

        #logo {
            color: #ffffff;
            font-size: 28px;
            font-weight: bold;
            padding-bottom: 8px;
        }

        #linea {
            color: #383c4d;
        }

        #etichetta {
            color: #858ba3;
            font-size: 10px;
            font-weight: bold;
            padding-top: 8px;
        }

        #pulsanteNav {
            background-color: transparent;
            color: #c9ccda;
            border: none;
            border-radius: 6px;
            text-align: left;
            padding: 11px 8px;
            font-size: 13px;
        }

        #pulsanteNav:hover {
            background-color: #343746;
            color: #ffffff;
        }

        #pulsanteNav[attivo="true"] {
            background-color: #3b4160;
            color: #ffffff;
        }

        #profilo {
            background-color: #2b2f3d;
            border-radius: 8px;
        }

        #nomeUtente {
            color: #ffffff;
            font-weight: bold;
        }

        #statoUtente {
            color: #55d69e;
            font-size: 11px;
        }

        #colonnaElenco {
            background-color: #20232e;
            border-right: 1px solid #343746;
        }

        #colonnaFile {
            background-color: #20232e;
            border-left: 1px solid #343746;
        }

        #titoloColonna {
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
        }

        #sottotitoloFile, #notaFile {
            color: #9298ad;
            font-size: 11px;
        }

        #ricerca {
            background-color: #2a2e3b;
            color: #ffffff;
            border: 1px solid #3a3e50;
            border-radius: 6px;
            padding: 9px;
        }

        #lista, #listaFile {
            background-color: transparent;
            color: #d9dbea;
            border: none;
            outline: none;
        }

        #lista::item, #listaFile::item {
            padding: 11px 8px;
            border-radius: 6px;
        }

        #lista::item:hover, #listaFile::item:hover {
            background-color: #303545;
        }

        #lista::item:selected {
            background-color: #3b4160;
            color: #ffffff;
        }

        #areaChat {
            background-color: #191b24;
        }

        #intestazioneChat {
            background-color: #222531;
            border-radius: 8px;
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

        #pulsanteAllega {
            background-color: #3a3e50;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            min-width: 34px;
            min-height: 34px;
            font-size: 21px;
        }

        #pulsanteAllega:hover {
            background-color: #505873;
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
            width: 9px;
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    finestra = crea_finestra()
    finestra.show()
    sys.exit(app.exec())
