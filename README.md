# CATO-Ping (`catoping.py`)

`catoping.py` ist ein leichtgewichtiges, kontinuierliches TCP-Ping-Skript in Python. Es misst die Netzwerklatenz auf spezifischen TCP-Ports (im Gegensatz zum herkömmlichen ICMP-Ping), führt automatische ASN- und rDNS-Abfragen durch und gibt die Ergebnisse farbig formatiert im Terminal aus.

## Features

* **Kontinuierlicher TCP-Ping:** Misst die Verbindungszeit in Millisekunden über beliebige TCP-Ports.
* **ASN- & rDNS-Lookup:** Erkennt bei IP-Adressen automatisch die Organisation, das Autonomous System (ASN) oder den Reverse-DNS-Namen.
* **Benutzerdefinierte Labels:** Erlaubt die Vergabe eigener Anzeigenamen für den Stream.
* **Live-Statistiken:** Zeigt beim Beenden (via `Ctrl+C`) eine detaillierte Zusammenfassung der gesendeten/verlorenen Pakete sowie Durchschnitts-, Min- und Max-Latenzen an.
* **Farbige Konsole:** Nutzt ANSI-Farbcodes mit dem Tag `[CATO-Ping]` für eine übersichtliche Darstellung unter Windows und Unix/Linux.

## Voraussetzungen

* Python 3.6 oder höher.
* Keine externen Python-Bibliotheken erforderlich (nutzt ausschließlich Standardmodule).
* System-Abhängigkeit: `nslookup` (wird standardmäßig für die ASN-Abfrage benötigt und ist auf den meisten Systemen vorinstalliert).

## Verwendung

Das Skript wird direkt über das Terminal ausgeführt:

```bash
python catoping.py <host> [Optionen]
```

### Befehlszeilen-Argumente & Flags

| Argument / Flag | Beschreibung | Standardwert |
| :--- | :--- | :--- |
| `<host>` | **[Erforderlich]** Ziel-Domain (z. B. `google.com`) oder IP-Adresse (z. B. `8.8.8.8`). | *Keiner* |
| `-p`, `--port <port>` | Der zu testende TCP-Port. | `80` |
| `-i`, `--interval <sec>` | Wartezeit in Sekunden zwischen den einzelnen Pings. | `1.0` |
| `-t`, `--timeout <sec>` | Verbindungs-Timeout in Sekunden. | `2.0` |
| `--no-lookup` | Überspringt die ASN- und rDNS-Abfrage (beschleunigt den Start). | `False` |
| `--label <name>` | Vergibt ein benutzerdefiniertes Anzeigelabel für den Stream. | *Keines* |

## Beispiele

1. **Standard-Ping (Port 80 / HTTP):**
   ```bash
   python catoping.py example.com
   ```

2. **SSH-Port prüfen (Port 22) alle 0.5 Sekunden:**
   ```bash
   python catoping.py 192.168.1.1 -p 22 -i 0.5
   ```

3. **Ping ohne DNS-/ASN-Lookups auf eine IP:**
   ```bash
   python catoping.py 8.8.8.8 --no-lookup
   ```

4. **Mit eigenem Label und erhöhtem Timeout:**
   ```bash
   python catoping.py 1.1.1.1 --label "Cloudflare-DNS" -t 5.0
   ```

## Tool beenden

Um die kontinuierliche Überprüfung zu stoppen und die Statistiken anzuzeigen, drücke im Terminal:

```text
Ctrl + C
```

## Gängige Ports für Dienste und Protokolle (Standard-Ports)

Hier ist eine Übersicht nützlicher Ports, die du mit dem Parameter `-p` ansprechen kannst:

| Dienst / Protokoll | Standard-Port | Beschreibung |
| :--- | :--- | :--- |
| **HTTP** | `80` | Unverschlüsselter Web-Traffic (Standard) |
| **HTTPS** | `443` | Verschlüsselter Web-Traffic (SSL/TLS) |
| **SSH** | `22` | Secure Shell für Remote-Server-Zugriff |
| **FTP** | `21` | File Transfer Protocol (Steuerungsverbindung) |
| **DNS** | `53` | Domain Name System |
| **SMTP** | `25` | E-Mail-Versand (Simple Mail Transfer Protocol) |
| **IMAP** | `143` | E-Mail-Abruf |
| **MySQL** | `3306` | MySQL-Datenbankserver |
| **PostgreSQL** | `5432` | PostgreSQL-Datenbankserver |
| **Minecraft (Java)** | `25565` | Standard-Port für Minecraft-Server |
| **FiveM (GTA V)** | `30120` | Standard-Port für FiveM Multiplayer-Server |