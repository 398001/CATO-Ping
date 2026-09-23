# Universal AI README Generator (`readme_generator.py`)

Der Universal AI README Generator ist ein leistungsstarkes Python-Skript, das mithilfe der Google Gemini API (Modell `gemini-3.5-flash-lite`) Code-Dateien oder ganze Projektverzeichnisse analysiert und automatisch eine extrem saubere, professionelle sowie vollständige `README.md`-Datei im Markdown-Format erstellt.

## Features

* **KI-gestützte Analyse**: Nutzt das fortschrittliche Gemini-Modell, um den Code semantisch zu verstehen und eine präzise Dokumentation zu verfassen.
* **Flexible Eingabequellen**: Unterstützt wahlweise die Analyse einzelner Dateien, ganzer Projektordner oder direktes Einfügen von Code im Terminal.
* **Intelligentes Filtern**: Ignoriert beim Scannen von Ordnern automatisch irrelevante Verzeichnisse (wie `.git`, `venv`, `node_modules`) sowie Binär- und Mediendateien.
* **Sichere API-Handhabung**: Liest den API-Key flexibel aus den Umgebungsvariablen (`GEMINI_API_KEY`) oder fragt diesen bei Bedarf interaktiv ab.
* **Standardisiertes Format**: Generiert strukturierte Dokumentationen inklusive Voraussetzungen, Befehlszeilen-Argumenten, Praxis-Beispielen und Port-Tabellen.

## Voraussetzungen

* **Python**: Version 3.8 oder höher
* **API-Key**: Ein gültiger Google Gemini API Key (`GEMINI_API_KEY`)
* **Abhängigkeiten**: Das Skript verwendet ausschließlich Standardbibliotheken (`os`, `sys`, `json`, `urllib`, `pathlib`), es ist keine externe Installation (wie `requests`) via `pip` erforderlich.

## Verwendung

Das Skript wird direkt über das Terminal gestartet:

```bash
python readme_generator.py
```

Beim Start werden Sie interaktiv gefragt, ob Sie einen ganzen Ordner, eine einzelne Datei oder Code direkt im Terminal einfügen möchten.

## Befehlszeilen-Argumente & Flags

Das Skript steuert den Ablauf über ein interaktives Terminal-Menü und benötigt im Standardaufruf keine direkten Kommandozeilen-Parameter.

| Argument / Flag | Beschreibung | Standardwert |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Umgebungsvariable für den Google Gemini API Key | `None` (wird interaktiv abgefragt) |

## Beispiele

### 1. Gesamten Projektordner analysieren
Wählen Sie im Menü Option `1`, um ein komplettes Verzeichnis einzulesen. Das Skript ignoriert dabei automatisch Cache- und Build-Ordner.
```bash
python readme_generator.py
# Wählen Sie: 1
# Pfad eingeben: /pfad/zu/ihrem/projekt
```

### 2. Einzelne Python-Datei dokumentieren
Wählen Sie Option `2`, um gezielt eine einzelne Quellcode-Datei zu analysieren. Die erstellte `README.md` wird im selben Verzeichnis gespeichert.
```bash
python readme_generator.py
# Wählen Sie: 2
# Pfad eingeben: main.py
```

### 3. Code direkt per Terminal übergeben
Wählen Sie Option `3`, fügen Sie Ihren Code ein und beenden Sie die Eingabe in einer neuen Zeile mit dem Wort `END`.
```bash
python readme_generator.py
# Wählen Sie: 3
# Code einfügen -> END tippen und Enter drücken
```

## Tool beenden

Das Skript kann jederzeit während der Eingabe oder Ausführung mit der Tastenkombination `Ctrl + C` abgebrochen werden.