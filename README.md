# MCP Server für Fiktive Webseite

Dieses Projekt implementiert einen Model Context Protocol (MCP) Server, der eine fiktive Webseite mit Benutzern, Artikeln und Kommentaren simuliert. Der Server kann in Claude Desktop integriert werden, um KI-Anfragen mit echten Daten zu beantworten.

## 🚀 Features

- **Benutzerverwaltung**: Abrufen von Benutzerinformationen und -statistiken
- **Artikelverwaltung**: Durchsuchen und Filtern von Artikeln nach Kategorie, Autor oder Beliebtheit
- **Kommentarsystem**: Anzeigen von Kommentaren zu Artikeln
- **Suchfunktion**: Volltextsuche in Artikeln und Kommentaren
- **Statistiken**: Webseite-weite Statistiken und Metriken

## 📁 Projektstruktur

```
├── mcp_server.py          # Haupt-MCP Server
├── website_data.py        # Fiktive Webseite-Datenbank
├── test_mcp_server.py     # Test-Suite
├── requirements.txt       # Python-Abhängigkeiten
├── claude_desktop_config.json  # Claude Desktop Konfiguration
├── setup_instructions.md  # Detaillierte Setup-Anleitung
└── README.md             # Diese Datei
```

## 🛠️ Installation

1. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Claude Desktop konfigurieren:**
   - Befolge die Anweisungen in `setup_instructions.md`
   - Füge die MCP Server-Konfiguration zu Claude Desktop hinzu

3. **Server testen:**
   ```bash
   python test_mcp_server.py
   ```

## 🔧 Verfügbare MCP Tools

### Benutzer-Tools
- `get_user_info` - Benutzerinformationen anhand ID oder Benutzername
- `get_all_users` - Alle Benutzer mit optionalem Filter für aktive Benutzer

### Artikel-Tools
- `get_article_info` - Vollständige Artikelinformationen
- `get_all_articles` - Artikel mit Filtern (Kategorie, Autor, Beliebtheit)
- `get_article_comments` - Kommentare zu einem Artikel

### Allgemeine Tools
- `get_website_stats` - Webseite-Statistiken
- `search_content` - Volltextsuche in Artikeln und Kommentaren

## 📊 Beispiel-Daten

Die fiktive Webseite enthält:

- **4 Benutzer** (3 aktiv, 1 inaktiv)
- **4 Artikel** in verschiedenen Kategorien (AI/ML, Programming, Web Development, Database)
- **4 Kommentare** zu den Artikeln
- **Realistische Metriken** (Views, Likes, etc.)

## 🧪 Test-Szenarien

### 1. Benutzeranalyse
```
"Zeige mir alle aktiven Benutzer und ihre Beiträge"
```

### 2. Content-Discovery
```
"Welche Artikel über Python gibt es und wie beliebt sind sie?"
```

### 3. Community-Engagement
```
"Zeige mir die Kommentare zu dem beliebtesten Artikel"
```

### 4. Webseite-Insights
```
"Gib mir eine Übersicht über die Webseite-Statistiken"
```

### 5. Suchfunktion
```
"Suche nach Inhalten über Machine Learning"
```

## 🔗 Integration mit LLM-APIs

Der MCP Server kann zusätzlich zu Claude Desktop mit anderen LLM-APIs verbunden werden:

1. **OpenAI API**: Für erweiterte Analysefunktionen
2. **Anthropic API**: Für Claude-spezifische Features
3. **Lokale LLMs**: Für datenschutzfreundliche Lösungen

## 🐛 Fehlerbehebung

### Häufige Probleme:

1. **MCP Server wird nicht erkannt:**
   - Überprüfe die Pfade in der Claude Desktop Konfiguration
   - Stelle sicher, dass Python im PATH verfügbar ist

2. **Tools funktionieren nicht:**
   - Teste den Server mit `python test_mcp_server.py`
   - Überprüfe die Claude Desktop Logs

3. **JSON-Fehler:**
   - Validiere die Konfigurationsdatei mit einem JSON-Validator

## 📈 Erweiterungsmöglichkeiten

- **Datenbank-Integration**: SQLite oder PostgreSQL für persistente Daten
- **Authentifizierung**: Benutzer-Login und Session-Management
- **Content-Management**: Artikel erstellen, bearbeiten und löschen
- **Analytics**: Erweiterte Statistiken und Berichte
- **API-Endpoints**: REST-API für externe Anwendungen

## 📝 Lizenz

Dieses Projekt ist für Bildungszwecke erstellt und kann frei verwendet und modifiziert werden.

## 🤝 Beitragen

Verbesserungen und Erweiterungen sind willkommen! Erstelle einfach einen Pull Request oder öffne ein Issue.

---

**Hinweis**: Dies ist ein Prototyp für Demonstrationszwecke. Für Produktionsumgebungen sollten zusätzliche Sicherheits- und Performance-Überlegungen berücksichtigt werden.
