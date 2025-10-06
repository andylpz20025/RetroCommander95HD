# RetroCommander 95 HD

**GUI für DOSBox-Spiele mit Profilverwaltung, Grafik- und Audioeinstellungen**

---

## Projektbeschreibung

RetroCommander 95 HD ist ein modernes, aber nostalgisches Tool zur Verwaltung und Ausführung alter DOS-Spiele über **DOSBox**.  
Es ermöglicht die Erstellung individueller **Spielprofile** mit allen wichtigen Einstellungen wie Grafik, Fenster, Audio und optional Setup.  

Mit RetroCommander 95 HD kannst du:

- DOSBox-Spiele direkt aus der GUI starten  
- Profile für verschiedene Spiele anlegen, bearbeiten und löschen  
- Grafikeinstellungen wie Renderer, Skalierung, Auflösung und Vollbildmodus anpassen  
- Audioeinstellungen wie MIDI, OPL, Lautstärke und Latenz konfigurieren  
- Optional die Setup-Datei eines Spiels starten  
- Aktionen und Fehler in einem integrierten Log beobachten  
- Ein integriertes Tutorial und eine Hilfe jederzeit abrufen  

---

## Features

- **Profilverwaltung:** ➕ Neues Profil, ✏️ Bearbeiten, ❌ Löschen  
- **Grafik & Fenster:** Vollbild, Renderer (surface, overlay, OpenGL, D3D), Skalierung (HQ2X, HQ3X, AdvInterp2X), Auflösung, Seitenverhältnis, CPU-Zyklen, RAM  
- **Audio:** MIDI-Ausgabe, OPL-Modus, Lautstärke, Latenz  
- **Setup starten:** Optional, wenn ein Spiel ein Setup benötigt  
- **Log:** Zeigt Aktionen, Fehler und Hinweise  
- **Hilfe / Tutorial:** Immer abrufbar über die GUI  

---

## Systemanforderungen

- **Betriebssystem:** Windows 10 / 11  
- **Python:** Version 3.10+  
- **PyQt5:** GUI-Framework (Installieren mit `pip install PyQt5`)  
- **DOSBox:** Installiert auf dem System, Pfad in den Spieleinstellungen angeben  

---

## Installation

1. **Git installieren**  
   [Git herunterladen und installieren](https://git-scm.com/downloads)

2. **Python 3.10+ installieren**  
   [Python herunterladen](https://www.python.org/downloads/)

3. **PyQt5 installieren**  
   Öffne PowerShell oder CMD und tippe:

   ```powershell
   pip install PyQt5
