#!/usr/bin/env python3
"""
Test-Skript für den MCP Server
Simuliert verschiedene Anfragen an die Webseite-Datenbank
"""

import asyncio
import json
from website_data import db

def test_database_operations():
    """Testet die Datenbankoperationen direkt"""
    print("=== Test der Datenbankoperationen ===\n")
    
    # Test 1: Alle Benutzer abrufen
    print("1. Alle Benutzer:")
    users = db.get_all_users()
    for user in users:
        print(f"   - {user.username} ({user.email}) - Aktiv: {user.is_active}")
    
    print("\n2. Aktive Benutzer:")
    active_users = db.get_active_users()
    for user in active_users:
        print(f"   - {user.username}")
    
    # Test 2: Artikel abrufen
    print("\n3. Alle Artikel:")
    articles = db.get_all_articles()
    for article in articles:
        author = db.get_user_by_id(article.author_id)
        print(f"   - {article.title} (von {author.username if author else 'Unbekannt'})")
        print(f"     Kategorie: {article.category}, Views: {article.views}, Likes: {article.likes}")
    
    # Test 3: Beliebte Artikel
    print("\n4. Beliebte Artikel (Top 3):")
    popular = db.get_popular_articles(3)
    for article in popular:
        print(f"   - {article.title} ({article.views} Views)")
    
    # Test 4: Artikel nach Kategorie
    print("\n5. Artikel nach Kategorie 'AI/ML':")
    ai_articles = db.get_articles_by_category("AI/ML")
    for article in ai_articles:
        print(f"   - {article.title}")
    
    # Test 5: Kommentare zu einem Artikel
    print("\n6. Kommentare zu Artikel 1:")
    comments = db.get_comments_by_article(1)
    for comment in comments:
        user = db.get_user_by_id(comment.user_id)
        print(f"   - {user.username if user else 'Unbekannt'}: {comment.content}")
        print(f"     Genehmigt: {comment.is_approved}")
    
    # Test 6: Webseite-Statistiken
    print("\n7. Webseite-Statistiken:")
    stats = db.get_website_stats()
    for key, value in stats.items():
        print(f"   - {key}: {value}")

def simulate_mcp_tool_calls():
    """Simuliert MCP Tool-Aufrufe"""
    print("\n=== Simulation von MCP Tool-Aufrufen ===\n")
    
    # Simuliere get_user_info
    print("1. get_user_info (user_id=1):")
    user = db.get_user_by_id(1)
    if user:
        result = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
            "is_active": user.is_active
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Simuliere get_all_articles mit Filter
    print("\n2. get_all_articles (category='Programming'):")
    articles = db.get_articles_by_category("Programming")
    result = []
    for article in articles:
        author = db.get_user_by_id(article.author_id)
        result.append({
            "id": article.id,
            "title": article.title,
            "content": article.content[:100] + "...",
            "author": author.username if author else "Unbekannt",
            "category": article.category,
            "views": article.views
        })
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Simuliere search_content
    print("\n3. search_content (query='Python'):")
    query = "python"
    results = []
    for article in db.get_all_articles():
        if (query in article.title.lower() or 
            query in article.content.lower()):
            author = db.get_user_by_id(article.author_id)
            results.append({
                "type": "article",
                "id": article.id,
                "title": article.title,
                "author": author.username if author else "Unbekannt",
                "category": article.category
            })
    print(json.dumps(results, indent=2, ensure_ascii=False))

def main():
    """Hauptfunktion"""
    print("MCP Server Test-Suite")
    print("=" * 50)
    
    test_database_operations()
    simulate_mcp_tool_calls()
    
    print("\n" + "=" * 50)
    print("Test abgeschlossen!")
    print("\nDer MCP Server ist bereit für die Verwendung mit Claude Desktop.")

if __name__ == "__main__":
    main()
