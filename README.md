# blog-engine

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

A fast, minimal static blog generator written in Python. Convert Markdown posts into a beautiful static website with zero database required.

## Features

- **Markdown Support** - Write posts in Markdown with YAML frontmatter
- **Template System** - Jinja2-based templates for full customization
- **Tag System** - Organize and filter posts by tags
- **RSS Feed** - Auto-generated RSS/Atom feed
- **Live Reload** - Watch mode rebuilds on file changes
- **CLI Interface** - Easy-to-use command line tools
- **Docker Support** - Build and serve with Docker

## Architecture

```
blog-engine/
├── cli.py                    # CLI entry point
├── config.yaml               # Site configuration
├── src/
│   ├── engine/
│   │   ├── core.py           # Markdown parser, Post/Site models
│   │   └── __init__.py
│   ├── builders/
│   │   ├── static_builder.py # Template renderer & output generator
│   │   └── __init__.py
│   └── templates/
│       └── default/
│           ├── index.html    # Home page template
│           ├── post.html     # Post page template
│           ├── tag.html      # Tag archive template
│           └── rss.xml       # RSS feed template
├── content/
│   ├── posts/                # Markdown blog posts
│   └── assets/               # Static assets
├── output/                   # Generated site (gitignored)
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Installation

### From Source

```bash
git clone https://github.com/janderik/blog-engine.git
cd blog-engine
pip install -r requirements.txt
```

### With Docker

```bash
docker-compose build
```

## Quick Start

1. **Configure your site** by editing `config.yaml`:

```yaml
title: "My Blog"
description: "My personal blog"
author: "Your Name"
base_url: "https://yourdomain.com"
```

2. **Create a new post**:

```bash
python cli.py new "My First Post" --tags "intro,blog"
```

3. **Build your site**:

```bash
python cli.py build
```

4. **Preview locally**:

```bash
python cli.py serve --port 8000
```

Visit `http://localhost:8000` to see your blog.

## CLI Commands

| Command | Description |
|---------|-------------|
| `build` | Build the static site from content |
| `serve` | Serve the built site locally |
| `watch` | Watch for changes and auto-rebuild |
| `new` | Create a new blog post |

### Build

```bash
python cli.py build
```

Generates the static site in the `output/` directory.

### Serve

```bash
python cli.py serve --port 8000 --host 0.0.0.0
```

Serves the built site on the specified port.

### Watch

```bash
python cli.py watch
```

Watches the `content/` directory and rebuilds automatically when files change.

### New Post

```bash
python cli.py new "Post Title" --tags "tag1,tag2"
```

Creates a new markdown file in `content/posts/` with frontmatter.

## Markdown Post Format

Posts use YAML frontmatter:

```markdown
---
title: "Post Title"
date: "2024-01-15"
tags: ["python", "tutorial"]
slug: "post-slug"
template: "post.html"
---

# Post Title

Your content here in Markdown format.

## Features

- Fenced code blocks with syntax highlighting
- Tables
- Tables of contents
- Blockquotes
```

## Template Options

### Available Templates

- **index.html** - Home page with paginated post listing
- **post.html** - Individual post display with metadata
- **tag.html** - Posts filtered by tag
- **rss.xml** - RSS feed for syndication

### Creating Custom Templates

Templates use Jinja2 syntax. Available variables:

```jinja2
{# Site-wide variables #}
{{ site.title }}
{{ site.description }}
{{ site.author }}
{{ site.base_url }}

{# Post variables (in post.html) #}
{{ post.title }}
{{ post.date }}
{{ post.html }}          {# Rendered HTML content #}
{{ post.excerpt }}
{{ post.tags }}
{{ post.slug }}

{# Post list (in index.html) #}
{% for post in posts %}
  {{ post.title }}
  {{ post.excerpt }}
{% endfor %}
```

### Template Location

Place custom templates in:
```
src/templates/your-theme-name/
```

Then update `config.yaml`:
```yaml
theme: "your-theme-name"
```

## Content Structure

```
content/
├── posts/           # Blog posts (Markdown files)
│   ├── my-post.md
│   └── another-post.md
├── pages/           # Static pages (optional)
│   └── about.md
└── assets/          # Images, CSS, JS
    ├── images/
    └── css/
```

## Development

### Setup

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Running Tests

```bash
pip install pytest
pytest tests/
```

## Docker Usage

### Build and Serve

```bash
docker-compose up
```

This starts:
- `blog` service - Builds the site
- `serve` service - Nginx serving the site on port 8080

### Single Container

```bash
docker build -t blog-engine .
docker run -v $(pwd)/content:/app/content -v $(pwd)/output:/app/output blog-engine build
```

## Performance

- Builds a 100-post site in under 1 second
- Incremental builds with watch mode
- No database required - pure file-based

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built with** Python, Jinja2, Markdown, Click
