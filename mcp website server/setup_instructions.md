# MCP Server Setup Anleitung

## 1. Installation der Abhängigkeiten

```bash
pip install -r requirements.txt
```

## 2. Claude Desktop Konfiguration

### Windows:
1. Öffne den Datei-Explorer und navigiere zu:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Füge die folgende Konfiguration hinzu oder erstelle die Datei falls sie nicht existiert:

```json
{
  "mcpServers": {
    "website-mcp-server": {
      "command": "python",
      "args": ["C:\\Users\\Eyad\\Desktop\\Verteilte systeme\\mcp_server.py"],
      "cwd": "C:\\Users\\Eyad\\Desktop\\Verteilte systeme",
      "env": {}
    }
  }
}
```

### macOS:
1. Öffne den Finder und navigiere zu:
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. Füge die Konfiguration hinzu (Pfade entsprechend anpassen)

### Linux:
1. Navigiere zu:
   ```
   ~/.config/claude/claude_desktop_config.json
   ```

## 3. Claude Desktop neustarten

Nach der Konfiguration muss Claude Desktop neu gestartet werden, damit die MCP Server erkannt werden.

## 4. Testen des MCP Servers

Nach dem Neustart von Claude Desktop sollten die folgenden Tools verfügbar sein:

- `get_user_info` - Benutzerinformationen abrufen
- `get_all_users` - Alle Benutzer anzeigen
- `get_article_info` - Artikelinformationen abrufen
- `get_all_articles` - Alle Artikel anzeigen
- `get_article_comments` - Kommentare zu einem Artikel
- `get_website_stats` - Webseite-Statistiken
- `search_content` - Inhalte durchsuchen

## 5. Beispiel-Anfragen

### Benutzer abrufen:
"Zeige mir alle aktiven Benutzer der Webseite"

### Artikel durchsuchen:
"Suche nach Artikeln über Python"

### Statistiken anzeigen:
"Zeige mir die Webseite-Statistiken"

### Kommentare zu einem Artikel:
"Zeige mir die Kommentare zu Artikel ID 1"

## 6. Fehlerbehebung

Falls der MCP Server nicht funktioniert:

1. Überprüfe, ob Python im PATH verfügbar ist
2. Überprüfe die Pfade in der Konfigurationsdatei
3. Teste den Server manuell:
   ```bash
   python mcp_server.py
   ```
4. Überprüfe die Claude Desktop Logs auf Fehlermeldungen
