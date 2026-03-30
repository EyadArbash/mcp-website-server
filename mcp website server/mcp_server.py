#!/usr/bin/env python3
"""
Korrigierter MCP Server für eine fiktive Webseite
Funktioniert mit der aktuellen MCP-Version
"""

import asyncio
import json
import sys
from mcp.server.lowlevel.server import NotificationOptions
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from website_data import db

# MCP Server initialisieren
server = Server("website-mcp-server")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Liste alle verfügbaren Tools auf"""
    return [
        Tool(
            name="get_user_info",
            description="Holt Informationen über einen Benutzer anhand der ID oder des Benutzernamens",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "Die ID des Benutzers"
                    },
                    "username": {
                        "type": "string",
                        "description": "Der Benutzername"
                    }
                },
                "anyOf": [
                    {"required": ["user_id"]},
                    {"required": ["username"]}
                ]
            }
        ),
        Tool(
            name="get_all_users",
            description="Holt alle Benutzer der Webseite",
            inputSchema={
                "type": "object",
                "properties": {
                    "active_only": {
                        "type": "boolean",
                        "description": "Nur aktive Benutzer anzeigen",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="get_article_info",
            description="Holt Informationen über einen Artikel anhand der ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "article_id": {
                        "type": "integer",
                        "description": "Die ID des Artikels"
                    }
                },
                "required": ["article_id"]
            }
        ),
        Tool(
            name="get_all_articles",
            description="Holt alle Artikel der Webseite",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filtere nach Kategorie"
                    },
                    "author_id": {
                        "type": "integer",
                        "description": "Filtere nach Autor-ID"
                    },
                    "popular_only": {
                        "type": "boolean",
                        "description": "Nur beliebte Artikel anzeigen (nach Views sortiert)",
                        "default": False
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximale Anzahl der Artikel",
                        "default": 10
                    }
                }
            }
        ),
        Tool(
            name="get_article_comments",
            description="Holt Kommentare zu einem Artikel",
            inputSchema={
                "type": "object",
                "properties": {
                    "article_id": {
                        "type": "integer",
                        "description": "Die ID des Artikels"
                    },
                    "approved_only": {
                        "type": "boolean",
                        "description": "Nur genehmigte Kommentare anzeigen",
                        "default": True
                    }
                },
                "required": ["article_id"]
            }
        ),
        Tool(
            name="get_website_stats",
            description="Holt allgemeine Statistiken über die Webseite",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="search_content",
            description="Durchsucht Artikel und Kommentare nach einem Suchbegriff",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Der Suchbegriff"
                    },
                    "search_in": {
                        "type": "string",
                        "enum": ["articles", "comments", "both"],
                        "description": "Wo soll gesucht werden",
                        "default": "both"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Behandelt Tool-Aufrufe"""
    
    try:
        if name == "get_user_info":
            if "user_id" in arguments:
                user = db.get_user_by_id(arguments["user_id"])
            elif "username" in arguments:
                user = db.get_user_by_username(arguments["username"])
            else:
                return [TextContent(type="text", text="Fehler: user_id oder username erforderlich")]
            
            if user:
                result = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at,
                    "is_active": user.is_active
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
            else:
                return [TextContent(type="text", text="Benutzer nicht gefunden")]
        
        elif name == "get_all_users":
            active_only = arguments.get("active_only", False)
            users = db.get_active_users() if active_only else db.get_all_users()
            
            result = []
            for user in users:
                result.append({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at,
                    "is_active": user.is_active
                })
            
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_article_info":
            article = db.get_article_by_id(arguments["article_id"])
            if article:
                # Autor-Informationen hinzufügen
                author = db.get_user_by_id(article.author_id)
                result = {
                    "id": article.id,
                    "title": article.title,
                    "content": article.content,
                    "author": {
                        "id": author.id if author else None,
                        "username": author.username if author else "Unbekannt"
                    },
                    "created_at": article.created_at,
                    "updated_at": article.updated_at,
                    "views": article.views,
                    "likes": article.likes,
                    "category": article.category
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
            else:
                return [TextContent(type="text", text="Artikel nicht gefunden")]
        
        elif name == "get_all_articles":
            articles = db.get_all_articles()
            
            # Filter anwenden
            if "category" in arguments:
                articles = [a for a in articles if a.category == arguments["category"]]
            
            if "author_id" in arguments:
                articles = [a for a in articles if a.author_id == arguments["author_id"]]
            
            if arguments.get("popular_only", False):
                articles = sorted(articles, key=lambda x: x.views, reverse=True)
            
            # Limit anwenden
            limit = arguments.get("limit", 10)
            articles = articles[:limit]
            
            result = []
            for article in articles:
                author = db.get_user_by_id(article.author_id)
                result.append({
                    "id": article.id,
                    "title": article.title,
                    "content": article.content[:200] + "..." if len(article.content) > 200 else article.content,
                    "author": {
                        "id": author.id if author else None,
                        "username": author.username if author else "Unbekannt"
                    },
                    "created_at": article.created_at,
                    "views": article.views,
                    "likes": article.likes,
                    "category": article.category
                })
            
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_article_comments":
            article_id = arguments["article_id"]
            approved_only = arguments.get("approved_only", True)
            
            if approved_only:
                comments = db.get_approved_comments_by_article(article_id)
            else:
                comments = db.get_comments_by_article(article_id)
            
            result = []
            for comment in comments:
                user = db.get_user_by_id(comment.user_id)
                result.append({
                    "id": comment.id,
                    "content": comment.content,
                    "author": {
                        "id": user.id if user else None,
                        "username": user.username if user else "Unbekannt"
                    },
                    "created_at": comment.created_at,
                    "is_approved": comment.is_approved
                })
            
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
        
        elif name == "get_website_stats":
            stats = db.get_website_stats()
            return [TextContent(type="text", text=json.dumps(stats, indent=2, ensure_ascii=False))]
        
        elif name == "search_content":
            query = arguments["query"].lower()
            search_in = arguments.get("search_in", "both")
            results = []
            
            if search_in in ["articles", "both"]:
                for article in db.get_all_articles():
                    if (query in article.title.lower() or 
                        query in article.content.lower() or 
                        query in article.category.lower()):
                        author = db.get_user_by_id(article.author_id)
                        results.append({
                            "type": "article",
                            "id": article.id,
                            "title": article.title,
                            "content": article.content[:200] + "..." if len(article.content) > 200 else article.content,
                            "author": author.username if author else "Unbekannt",
                            "category": article.category
                        })
            
            if search_in in ["comments", "both"]:
                for comment in db.comments:
                    if query in comment.content.lower():
                        user = db.get_user_by_id(comment.user_id)
                        article = db.get_article_by_id(comment.article_id)
                        results.append({
                            "type": "comment",
                            "id": comment.id,
                            "content": comment.content,
                            "author": user.username if user else "Unbekannt",
                            "article_title": article.title if article else "Unbekannt",
                            "is_approved": comment.is_approved
                        })
            
            return [TextContent(type="text", text=json.dumps(results, indent=2, ensure_ascii=False))]
        
        else:
            return [TextContent(type="text", text=f"Unbekanntes Tool: {name}")]
    
    except Exception as e:
        print(f"Fehler in handle_call_tool: {e}", file=sys.stderr)
        return [TextContent(type="text", text=f"Fehler beim Ausführen des Tools: {str(e)}")]

async def main():
    """Hauptfunktion zum Starten des MCP Servers"""
    try:
        # Richtige NotificationOptions definieren
        notification_options = NotificationOptions(
            resources_changed=None,
            tools_changed=None
        )

        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="website-mcp-server",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=notification_options,
                        experimental_capabilities=None
                    )
                )
            )
    except Exception as e:
        print(f"Fehler im main: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    asyncio.run(main())
