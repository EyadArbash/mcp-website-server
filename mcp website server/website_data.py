"""
Fiktive Webseite-Datenbank für den MCP Server
Simuliert eine einfache Webseite mit Artikeln, Benutzern und Kommentaren
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class User:
    id: int
    username: str
    email: str
    created_at: str
    is_active: bool

@dataclass
class Article:
    id: int
    title: str
    content: str
    author_id: int
    created_at: str
    updated_at: str
    views: int
    likes: int
    category: str

@dataclass
class Comment:
    id: int
    article_id: int
    user_id: int
    content: str
    created_at: str
    is_approved: bool

class WebsiteDatabase:
    def __init__(self):
        self.users = [
            User(1, "alice_tech", "alice@example.com", "2024-01-15", True),
            User(2, "bob_dev", "bob@example.com", "2024-01-20", True),
            User(3, "charlie_ai", "charlie@example.com", "2024-02-01", True),
            User(4, "diana_ux", "diana@example.com", "2024-02-10", False),
        ]
        
        self.articles = [
            Article(1, "Einführung in Machine Learning", 
                   "Machine Learning ist ein faszinierendes Gebiet der künstlichen Intelligenz...", 
                   1, "2024-01-16", "2024-01-16", 1250, 45, "AI/ML"),
            Article(2, "Python für Anfänger", 
                   "Python ist eine der beliebtesten Programmiersprachen...", 
                   2, "2024-01-21", "2024-01-22", 2100, 78, "Programming"),
            Article(3, "Web Development Trends 2024", 
                   "Die Webentwicklung entwickelt sich rasant weiter...", 
                   1, "2024-02-02", "2024-02-02", 890, 32, "Web Development"),
            Article(4, "Datenbankdesign Best Practices", 
                   "Ein gutes Datenbankdesign ist die Grundlage für jede Anwendung...", 
                   2, "2024-02-11", "2024-02-12", 1560, 67, "Database"),
        ]
        
        self.comments = [
            Comment(1, 1, 2, "Sehr hilfreicher Artikel! Danke für die Erklärung.", "2024-01-17", True),
            Comment(2, 1, 3, "Könntest du mehr über Deep Learning schreiben?", "2024-01-18", True),
            Comment(3, 2, 1, "Python ist wirklich eine großartige Sprache für Anfänger.", "2024-01-22", True),
            Comment(4, 3, 2, "Interessante Trends! Was denkst du über WebAssembly?", "2024-02-03", False),
        ]
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return next((user for user in self.users if user.id == user_id), None)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return next((user for user in self.users if user.username == username), None)
    
    def get_all_users(self) -> List[User]:
        return self.users
    
    def get_active_users(self) -> List[User]:
        return [user for user in self.users if user.is_active]
    
    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        return next((article for article in self.articles if article.id == article_id), None)
    
    def get_all_articles(self) -> List[Article]:
        return self.articles
    
    def get_articles_by_category(self, category: str) -> List[Article]:
        return [article for article in self.articles if article.category == category]
    
    def get_articles_by_author(self, author_id: int) -> List[Article]:
        return [article for article in self.articles if article.author_id == author_id]
    
    def get_popular_articles(self, limit: int = 5) -> List[Article]:
        return sorted(self.articles, key=lambda x: x.views, reverse=True)[:limit]
    
    def get_comments_by_article(self, article_id: int) -> List[Comment]:
        return [comment for comment in self.comments if comment.article_id == article_id]
    
    def get_approved_comments_by_article(self, article_id: int) -> List[Comment]:
        return [comment for comment in self.comments 
                if comment.article_id == article_id and comment.is_approved]
    
    def get_website_stats(self) -> Dict:
        return {
            "total_users": len(self.users),
            "active_users": len(self.get_active_users()),
            "total_articles": len(self.articles),
            "total_comments": len(self.comments),
            "approved_comments": len([c for c in self.comments if c.is_approved]),
            "categories": list(set(article.category for article in self.articles)),
            "total_views": sum(article.views for article in self.articles),
            "total_likes": sum(article.likes for article in self.articles)
        }

# Globale Datenbankinstanz
db = WebsiteDatabase()
