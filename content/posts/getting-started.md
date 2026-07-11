---
title: "Getting Started with blog-engine"
date: "2024-01-15"
tags: ["tutorial", "markdown", "blogging"]
slug: "getting-started"
---

# Getting Started with blog-engine

blog-engine is a fast, minimal static blog generator written in Python. It converts your Markdown posts into a beautiful static website.

## Features

- **Markdown Support** - Write posts in Markdown with frontmatter metadata
- **Template System** - Customize your blog with Jinja2 templates
- **Tag Support** - Organize posts with tags
- **RSS Feed** - Automatically generated RSS feed
- **Live Reload** - Watch mode for development

## Installation

```bash
pip install -r requirements.txt
```

## Creating a Post

Create a new file in `content/posts/`:

```markdown
---
title: "My First Post"
date: "2024-01-15"
tags: ["intro", "blog"]
slug: "my-first-post"
---

# My First Post

Hello, world! This is my first blog post.
```

## Building Your Site

```bash
python cli.py build
```

This will generate your static site in the `output/` directory.

## Serving Locally

```bash
python cli.py serve --port 8000
```

## Template Options

blog-engine uses Jinja2 templates. The default template includes:

- `index.html` - Home page with post listing
- `post.html` - Individual post page
- `tag.html` - Tag archive page
- `rss.xml` - RSS feed

You can create custom templates by adding files to `src/templates/your-theme/`.

## Configuration

Edit `config.yaml` to customize your site:

```yaml
title: "My Awesome Blog"
description: "Thoughts on technology"
author: "Your Name"
base_url: "https://yourdomain.com"
theme: "default"
```
