import sys
import os
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QListWidget, QMessageBox, QCheckBox,
    QComboBox, QSpinBox, QGroupBox, QTextEdit, QScrollArea, QFormLayout
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# ---------------- Theme ----------------
THEME_BG = "#85abd4"
THEME_PANEL = "#1b2838"
THEME_ACCENT = "#66c0f4"
THEME_TEXT = "#ff6600"
THEME_LOG = "#66c0f4"
FONT = QFont("Segoe UI", 11)
PROFILES_FILE = "profiles.json"

# ---------------- Main Class ----------------
class RetroCommander(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Retro Commander 95 HD v2.2 (Dark Stable)")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(1000, 750)
        self.setFont(FONT)

        # Dark Theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(THEME_BG))
        palette.setColor(QPalette.Base, QColor(THEME_PANEL))
        palette.setColor(QPalette.Text, QColor(THEME_TEXT))
        palette.setColor(QPalette.ButtonText, QColor(THEME_TEXT))
        palette.setColor(QPalette.Button, QColor(THEME_ACCENT))
        palette.setColor(QPalette.Highlight, QColor(THEME_ACCENT))
        palette.setColor(QPalette.HighlightedText, QColor("#ff6600"))
        self.setPalette(palette)

        # Main Layout
        main_layout = QHBoxLayout(self)

        # Left: Profile List
        left_layout = QVBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔎 Suche nach Spiel...")
        self.search_field.textChanged.connect(self.filter_profiles)
        left_layout.addWidget(self.search_field)

        self.profile_list = QListWidget()
        self.profile_list.itemSelectionChanged.connect(self.load_selected_profile)
        left_layout.addWidget(self.profile_list)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_new_profile = QPushButton("➕ Neues Profil")
        self.btn_edit_profile = QPushButton("✏️ Bearbeiten")
        self.btn_delete_profile = QPushButton("❌ Löschen")
        btn_layout.addWidget(self.btn_new_profile)
        btn_layout.addWidget(self.btn_edit_profile)
        btn_layout.addWidget(self.btn_delete_profile)
        left_layout.addLayout(btn_layout)

        self.btn_new_profile.clicked.connect(self.new_profile)
        self.btn_edit_profile.clicked.connect(self.edit_profile)
        self.btn_delete_profile.clicked.connect(self.delete_profile)

        main_layout.addLayout(left_layout, 2)

        # Right: Scroll Area for Details
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        right_widget = QWidget()
        self.scroll.setWidget(right_widget)
        main_layout.addWidget(self.scroll, 5)
        self.detail_layout = QVBoxLayout(right_widget)

        # Sections
        self.setup_general_section()
        self.setup_graphics_section()
        self.setup_audio_section()
        self.setup_action_buttons()
        self.setup_log_section()

        # Load profiles
        self.load_profiles()
        self.update_profile_list()

    # ---------------- Sections ----------------
    def setup_general_section(self):
        self.grp_general = QGroupBox("🎮 Allgemein")
        layout = QFormLayout()
        self.name_input = QLineEdit()
        self.path_input = QLineEdit()
        self.exe_input = QLineEdit()
        self.dosbox_input = QLineEdit()
        self.setup_input = QLineEdit()
        self.btn_path = QPushButton("Ordner...")
        self.btn_dosbox = QPushButton("DOSBox...")
        self.btn_setup = QPushButton("Setup...")
        self.btn_path.clicked.connect(self.select_game_path)
        self.btn_dosbox.clicked.connect(self.select_dosbox_path)
        self.btn_setup.clicked.connect(self.select_setup_path)
        layout.addRow("🎮 Spielname:", self.name_input)
        layout.addRow("📂 Spielpfad:", self._combine_line(self.path_input, self.btn_path))
        layout.addRow("▶️ Startdatei (.EXE):", self.exe_input)
        layout.addRow("🧰 DOSBox Pfad:", self._combine_line(self.dosbox_input, self.btn_dosbox))
        layout.addRow("⚙️ Setup (optional):", self._combine_line(self.setup_input, self.btn_setup))
        self.grp_general.setLayout(layout)
        self.detail_layout.addWidget(self.grp_general)

    def setup_graphics_section(self):
        self.grp_graphics = QGroupBox("🖥️ Grafik & Fenster")
        layout = QFormLayout()
        self.fullscreen_check = QCheckBox("Vollbild")
        self.renderer_combo = QComboBox()
        self.renderer_combo.addItems(["surface","overlay","opengl","openglnb","d3d"])
        self.scaler_combo = QComboBox()
        self.scaler_combo.addItems(["none","normal2x","hq2x","hq3x","advinterp2x"])
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["original","640x480","800x600","1024x768","1920x1080"])
        self.keep_aspect = QCheckBox("Seitenverhältnis beibehalten")
        self.cpu_combo = QComboBox()
        self.cpu_combo.addItems(["auto","max","benutzerdefiniert"])
        self.custom_cycles = QSpinBox(); self.custom_cycles.setRange(1000,1000000); self.custom_cycles.setValue(30000)
        self.mem_spin = QSpinBox(); self.mem_spin.setRange(1,128); self.mem_spin.setValue(16)
        layout.addRow("🖥️ Vollbild:", self.fullscreen_check)
        layout.addRow("🎨 Renderer:", self.renderer_combo)
        layout.addRow("🔍 Skalierung:", self.scaler_combo)
        layout.addRow("🖼️ Auflösung:", self.resolution_combo)
        layout.addRow("📐 Seitenverhältnis:", self.keep_aspect)
        layout.addRow("🧮 CPU:", self._combine_line(self.cpu_combo, self.custom_cycles))
        layout.addRow("💾 RAM (MB):", self.mem_spin)
        self.grp_graphics.setLayout(layout)
        self.detail_layout.addWidget(self.grp_graphics)

    def setup_audio_section(self):
        self.grp_audio = QGroupBox("🔊 Audio")
        layout = QFormLayout()
        self.midi_combo = QComboBox(); self.midi_combo.addItems(["default","mt32","fluidsynth","none"])
        self.opl_combo = QComboBox(); self.opl_combo.addItems(["auto","fast","accurate"])
        self.mixer_spin = QSpinBox(); self.mixer_spin.setRange(0,100); self.mixer_spin.setValue(80)
        self.latency_spin = QSpinBox(); self.latency_spin.setRange(10,200); self.latency_spin.setValue(50)
        layout.addRow("🎵 MIDI:",self.midi_combo)
        layout.addRow("🎹 OPL:",self.opl_combo)
        layout.addRow("🔊 Lautstärke (%):",self.mixer_spin)
        layout.addRow("🎧 Latenz (ms):",self.latency_spin)
        self.grp_audio.setLayout(layout)
        self.detail_layout.addWidget(self.grp_audio)

    # ---------------- Action Buttons ----------------
    def setup_action_buttons(self):
        btn_layout = QHBoxLayout()
        self.btn_save_profile = QPushButton("💾 Profil speichern")
        self.btn_start_game = QPushButton("🚀 Spiel starten")
        self.btn_start_setup = QPushButton("🧩 Setup starten")
        self.btn_help = QPushButton("❓ Hilfe / Tutorial")  # Neuer Button
        btn_layout.addWidget(self.btn_save_profile)
        btn_layout.addWidget(self.btn_start_game)
        btn_layout.addWidget(self.btn_start_setup)
        btn_layout.addWidget(self.btn_help)  # Hinzufügen
        self.btn_save_profile.clicked.connect(self.save_profile)
        self.btn_start_game.clicked.connect(self.start_game)
        self.btn_start_setup.clicked.connect(self.start_setup)
        self.btn_help.clicked.connect(self.show_help)  # Verbindung zum Help-Fenster
        self.detail_layout.addLayout(btn_layout)

    # ---------------- Log Section ----------------
    def setup_log_section(self):
        self.log = QTextEdit(); self.log.setReadOnly(True)
        self.log.setStyleSheet(f"background-color:{THEME_PANEL}; color:{THEME_LOG};")
        self.log.setFixedHeight(120)
        self.detail_layout.addWidget(QLabel("📜 Log:")); self.detail_layout.addWidget(self.log)

    # ---------------- Helpers ----------------
    def _combine_line(self, widget1, widget2):
        layout = QHBoxLayout(); layout.addWidget(widget1); layout.addWidget(widget2)
        wrapper = QWidget(); wrapper.setLayout(layout); return wrapper
    def select_game_path(self): path = QFileDialog.getExistingDirectory(self,"Spielverzeichnis wählen"); self.path_input.setText(path) if path else None
    def select_dosbox_path(self): path,_=QFileDialog.getOpenFileName(self,"DOSBox auswählen","","DOSBox (*.exe)"); self.dosbox_input.setText(path) if path else None
    def select_setup_path(self): path,_=QFileDialog.getOpenFileName(self,"Setup auswählen","","EXE Dateien (*.exe)"); self.setup_input.setText(path) if path else None

    # ---------------- Profile ----------------
    def new_profile(self):
        for w in [self.name_input,self.path_input,self.exe_input,self.dosbox_input,self.setup_input]:
            w.clear()
        self.fullscreen_check.setChecked(False)
        self.cpu_combo.setCurrentIndex(0)
        self.custom_cycles.setValue(30000)
        self.mem_spin.setValue(16)
        self.renderer_combo.setCurrentIndex(0)
        self.scaler_combo.setCurrentIndex(0)
        self.resolution_combo.setCurrentIndex(0)
        self.keep_aspect.setChecked(True)
        self.midi_combo.setCurrentIndex(0)
        self.opl_combo.setCurrentIndex(0)
        self.mixer_spin.setValue(80)
        self.latency_spin.setValue(50)
        self.log.append("🆕 Neues Profil erstellen, bitte Daten eingeben.")

    def edit_profile(self): self.load_selected_profile()

    def load_profiles(self):
        if os.path.exists(PROFILES_FILE):
            with open(PROFILES_FILE,"r",encoding="utf-8") as f: self.profiles=json.load(f)
        else: self.profiles=[]

    def update_profile_list(self):
        self.profile_list.clear()
        for p in self.profiles: self.profile_list.addItem(p["name"])

    def filter_profiles(self,text):
        self.profile_list.clear()
        for p in self.profiles:
            if text.lower() in p["name"].lower(): self.profile_list.addItem(p["name"])

    # ---------------- Profile Aktionen ----------------
    def load_selected_profile(self):
        if not self.profile_list.currentItem():
            return
        name = self.profile_list.currentItem().text()
        profile = next((p for p in self.profiles if p["name"] == name), None)
        if not profile:
            self.log.append("⚠️ Profil nicht gefunden!")
            return
        # Allgemein
        self.name_input.setText(profile.get("name",""))
        self.path_input.setText(profile.get("pfad",""))
        self.exe_input.setText(profile.get("exe",""))
        self.dosbox_input.setText(profile.get("dosbox",""))
        self.setup_input.setText(profile.get("setup_exe",""))
        # Grafik
        self.fullscreen_check.setChecked(profile.get("fullscreen",False))
        self.cpu_combo.setCurrentText(profile.get("cpu","auto"))
        self.custom_cycles.setValue(profile.get("custom_cycles",30000))
        self.mem_spin.setValue(profile.get("mem",16))
        self.renderer_combo.setCurrentText(profile.get("renderer","surface"))
        self.scaler_combo.setCurrentText(profile.get("scaler","none"))
        self.resolution_combo.setCurrentText(profile.get("resolution","original"))
        self.keep_aspect.setChecked(profile.get("keep_aspect",True))
        # Audio
        self.midi_combo.setCurrentText(profile.get("midi","default"))
        self.opl_combo.setCurrentText(profile.get("opl","auto"))
        self.mixer_spin.setValue(profile.get("mixer",80))
        self.latency_spin.setValue(profile.get("latency",50))
        self.log.append(f"📂 Profil '{name}' geladen.")

    def save_profile(self):
        name = self.name_input.text().strip()
        if not name:
            self.log.append("⚠️ Profilname darf nicht leer sein!")
            return
        profile = {
            "name": name,
            "pfad": self.path_input.text().strip(),
            "exe": self.exe_input.text().strip(),
            "dosbox": self.dosbox_input.text().strip(),
            "setup_exe": self.setup_input.text().strip(),
            "fullscreen": self.fullscreen_check.isChecked(),
            "cpu": self.cpu_combo.currentText(),
            "custom_cycles": self.custom_cycles.value(),
            "mem": self.mem_spin.value(),
            "renderer": self.renderer_combo.currentText(),
            "scaler": self.scaler_combo.currentText(),
            "resolution": self.resolution_combo.currentText(),
            "keep_aspect": self.keep_aspect.isChecked(),
            "midi": self.midi_combo.currentText(),
            "opl": self.opl_combo.currentText(),
            "mixer": self.mixer_spin.value(),
            "latency": self.latency_spin.value()
        }
        existing = next((p for p in self.profiles if p["name"] == name), None)
        if existing: self.profiles.remove(existing)
        self.profiles.append(profile)
        with open(PROFILES_FILE,"w",encoding="utf-8") as f: json.dump(self.profiles,f,indent=4)
        self.update_profile_list()
        self.log.append(f"💾 Profil '{name}' gespeichert.")

    def delete_profile(self):
        if not self.profile_list.currentItem():
            return
        name = self.profile_list.currentItem().text()
        reply = QMessageBox.question(self,"Löschen bestätigen",
                                     f"Soll das Profil '{name}' wirklich gelöscht werden?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.profiles = [p for p in self.profiles if p["name"] != name]
            with open(PROFILES_FILE,"w",encoding="utf-8") as f: json.dump(self.profiles,f,indent=4)
            self.update_profile_list()
            self.log.append(f"❌ Profil '{name}' gelöscht.")

    # ---------------- Spiel Start ----------------
    def start_game(self):
        if not self.profile_list.currentItem():
            self.log.append("⚠️ Kein Profil ausgewählt!")
            return
        name = self.profile_list.currentItem().text()
        profile = next((p for p in self.profiles if p["name"]==name),None)
        if not profile:
            self.log.append("⚠️ Profil nicht gefunden!")
            return
        if not profile.get("exe") or not profile.get("pfad") or not profile.get("dosbox"):
            self.log.append("⚠️ Fehlende Pfade oder EXE!")
            return
        conf_path = os.path.join(profile["pfad"],f"{profile['name']}.conf")
        self.create_dosbox_conf(profile,conf_path)
        self.log.append(f"🚀 Starte Spiel '{name}'...")
        subprocess.Popen([profile["dosbox"],"-conf",conf_path])

    def start_setup(self):
        setup_path = self.setup_input.text().strip()
        if not setup_path:
            self.log.append("⚠️ Kein Setup definiert!")
            return
        if not os.path.exists(setup_path):
            self.log.append("⚠️ Setup-Datei existiert nicht!")
            return
        self.log.append(f"🧩 Starte Setup '{setup_path}'...")
        subprocess.Popen([setup_path])

    # ---------------- DOSBox Config ----------------
    def create_dosbox_conf(self,profile,conf_path):
        exe_name = profile.get("exe","")
        conf = [
            "[sdl]",
            f"fullscreen={'true' if profile['fullscreen'] else 'false'}",
            f"windowresolution={profile['resolution']}",
            f"output={profile['renderer']}",
            "",
            "[dosbox]",
            f"memsize={profile['mem']}",
            "",
            "[cpu]",
            f"cycles={profile['custom_cycles']}",
            "",
            "[render]",
            f"scaler={profile['scaler']}",
            "",
            "[mixer]",
            f"rate=44100",
            f"oplmode={profile['opl']}",
            "",
            "[midi]",
            f"mpu401={profile['midi']}",
            "",
            "[autoexec]",
            f"mount c \"{profile['pfad']}\"",
            "c:",
            f"{exe_name}",
            "exit"
        ]
        with open(conf_path,"w",encoding="utf-8") as f: f.write("\n".join(conf))
        self.log.append(f"🧩 Config-Datei '{conf_path}' erstellt.")

    # ---------------- Hilfe / Tutorial ----------------
    def show_help(self):
        help_text = """
Retro Commander 95 HD - Hilfe & Tutorial

1️⃣ Neues Profil erstellen:
   - Klick auf ➕ Neues Profil
   - Gib Spielname, Spielpfad, Startdatei (.EXE) und optional Setup ein
   - Wähle Grafik-, Fenster- und Audioeinstellungen nach Wunsch
   - Klick auf 💾 Profil speichern

2️⃣ Spiel starten:
   - Wähle ein Profil aus der Liste
   - Klick auf 🚀 Spiel starten
   - DOSBox wird mit den gewählten Einstellungen gestartet

3️⃣ Setup starten:
   - Falls dein Spiel ein Setup benötigt, gib den Pfad an
   - Klick auf 🧩 Setup starten

4️⃣ Profile verwalten:
   - ✏️ Bearbeiten: lädt das Profil in die Eingabefelder
   - ❌ Löschen: entfernt das Profil dauerhaft

5️⃣ Einstellungen:
   - Vollbild, Renderer, Skalierung, Auflösung, Seitenverhältnis, CPU, RAM
   - Audio: MIDI, OPL, Lautstärke, Latenz

💡 Tipp:
   - Du kannst jederzeit ein Profil auswählen und anpassen
   - Die Log-Sektion unten zeigt Aktionen und Fehler
   - Alle Dateien (profiles.json) liegen im gleichen Ordner wie die Python-Datei
"""
        msg = QMessageBox(self)
        msg.setWindowTitle("📖 Hilfe / Tutorial")
        msg.setText(help_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setMinimumWidth(600)
        msg.exec_()

# ---------------- Main ----------------
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = RetroCommander()
    window.show()
    sys.exit(app.exec_())
