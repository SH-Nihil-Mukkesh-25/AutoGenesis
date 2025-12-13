"""
Project Templates for Autogenesis.
Pre-defined project structures for common use cases.
"""

TEMPLATES = [
    {
        "id": "portfolio",
        "name": "Personal Portfolio",
        "icon": "👤",
        "description": "Modern portfolio website with hero, projects, skills, and contact sections",
        "prompt": "Create a modern personal portfolio website with: hero section with name and tagline, about me section, projects grid with cards, skills section with icons, contact form, dark theme, smooth animations, responsive design. Use HTML, CSS, and JavaScript.",
        "tags": ["Web", "Frontend"]
    },
    {
        "id": "landing",
        "name": "Landing Page",
        "icon": "🚀",
        "description": "High-converting SaaS landing page with pricing and features",
        "prompt": "Create a professional SaaS landing page with: hero section with headline and CTA button, features grid, pricing table with 3 tiers, testimonials slider, FAQ accordion, footer with links. Modern gradient design, responsive. Use HTML, CSS, and JavaScript.",
        "tags": ["Web", "Frontend", "SaaS"]
    },
    {
        "id": "flask-api",
        "name": "Flask REST API",
        "icon": "🔥",
        "description": "Flask API with CRUD endpoints, authentication, and SQLite",
        "prompt": "Create a Flask REST API with: user authentication (register/login with JWT), CRUD endpoints for items, SQLite database, proper error handling, CORS enabled, Swagger documentation. Include requirements.txt and README.",
        "tags": ["Backend", "Python", "API"]
    },
    {
        "id": "chatbot",
        "name": "AI Chatbot",
        "icon": "🤖",
        "description": "Interactive chatbot interface with message history",
        "prompt": "Create an AI chatbot interface with: chat window with message bubbles, input field with send button, message history, typing indicator, dark theme, smooth scroll to bottom. Use HTML, CSS, JavaScript. Make it look like ChatGPT.",
        "tags": ["Web", "AI", "Frontend"]
    },
    {
        "id": "crud-app",
        "name": "CRUD Application",
        "icon": "📝",
        "description": "Full-stack CRUD app with table, forms, and API",
        "prompt": "Create a full CRUD application for managing tasks: table with data display, add/edit/delete buttons, modal forms, search and filter, Python Flask backend with SQLite, HTML/CSS/JS frontend. Include proper error handling and validation.",
        "tags": ["Full-Stack", "Python", "Database"]
    },
    {
        "id": "nextjs-saas",
        "name": "Next.js SaaS Starter",
        "icon": "⚡",
        "description": "Next.js starter with auth pages and dashboard layout",
        "prompt": "Create a Next.js SaaS starter with: login and signup pages, dashboard layout with sidebar, user profile page, settings page, responsive design, Tailwind CSS, dark mode support. Use TypeScript and Next.js App Router structure.",
        "tags": ["Next.js", "TypeScript", "SaaS"]
    }
]

def get_templates():
    """Get all available templates."""
    return TEMPLATES

def get_template_by_id(template_id: str):
    """Get a specific template by ID."""
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None

def get_template_prompt(template_id: str) -> str:
    """Get the prompt for a template."""
    template = get_template_by_id(template_id)
    return template["prompt"] if template else ""
