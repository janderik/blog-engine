"""Core engine for parsing markdown posts and managing site configuration."""

import os
import frontmatter
import markdown
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Post:
    """Represents a single blog post."""
    title: str
    slug: str
    date: str
    content: str
    html: str = ""
    tags: list = field(default_factory=list)
    excerpt: str = ""
    template: str = "post.html"
    metadata: dict = field(default_factory=dict)


@dataclass
class SiteConfig:
    """Site-wide configuration."""
    title: str = "My Blog"
    description: str = "A static blog generated with blog-engine"
    author: str = "Author"
    base_url: str = "https://example.com"
    posts_per_page: int = 10
    theme: str = "default"
    content_dir: str = "content"
    output_dir: str = "output"
    template_dir: str = "src/templates"


class MarkdownProcessor:
    """Processes markdown content with extensions."""

    EXTENSIONS = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.toc',
        'markdown.extensions.meta',
    ]

    EXTENSION_CONFIGS = {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'linenums': False,
        },
        'markdown.extensions.toc': {
            'permalink': True,
            'toc_depth': 3,
        },
    }

    def __init__(self):
        self.md = markdown.Markdown(
            extensions=self.EXTENSIONS,
            extension_configs=self.EXTENSION_CONFIGS,
        )

    def convert(self, text: str) -> str:
        """Convert markdown text to HTML."""
        self.md.reset()
        return self.md.convert(text)

    def extract_toc(self, html: str) -> str:
        """Extract table of contents from converted HTML."""
        import re
        toc_match = re.search(r'<div class="toc">.*?</div>', html, re.DOTALL)
        return toc_match.group(0) if toc_match else ""


class PostParser:
    """Parses markdown files into Post objects."""

    def __init__(self, processor: MarkdownProcessor):
        self.processor = processor

    def parse_file(self, filepath: Path) -> Optional[Post]:
        """Parse a markdown file into a Post."""
        if not filepath.exists() or filepath.suffix != '.md':
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            post_data = frontmatter.load(f)

        metadata = dict(post_data.metadata)
        content = post_data.content
        html = self.processor.convert(content)

        slug = metadata.get('slug', filepath.stem)
        tags = metadata.get('tags', [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',')]

        excerpt = self._generate_excerpt(content)

        return Post(
            title=metadata.get('title', filepath.stem),
            slug=slug,
            date=metadata.get('date', ''),
            content=content,
            html=html,
            tags=tags,
            excerpt=excerpt,
            template=metadata.get('template', 'post.html'),
            metadata=metadata,
        )

    def _generate_excerpt(self, content: str, max_length: int = 200) -> str:
        """Generate an excerpt from markdown content."""
        plain_text = content.replace('#', '').replace('*', '').replace('_', '')
        plain_text = ' '.join(plain_text.split())
        if len(plain_text) > max_length:
            return plain_text[:max_length].rsplit(' ', 1)[0] + '...'
        return plain_text


class Site:
    """Main site object that holds all parsed content."""

    def __init__(self, config: SiteConfig):
        self.config = config
        self.posts: list = []
        self.pages: list = []
        self.tags: dict = {}

    def load(self):
        """Load all content from the content directory."""
        processor = MarkdownProcessor()
        parser = PostParser(processor)
        content_path = Path(self.config.content_dir)

        posts_dir = content_path / 'posts'
        if posts_dir.exists():
            for md_file in sorted(posts_dir.glob('*.md')):
                post = parser.parse_file(md_file)
                if post:
                    self.posts.append(post)
                    for tag in post.tags:
                        self.tags.setdefault(tag, []).append(post)

        self.posts.sort(key=lambda p: p.date, reverse=True)

        pages_dir = content_path / 'pages'
        if pages_dir.exists():
            for md_file in sorted(pages_dir.glob('*.md')):
                page = parser.parse_file(md_file)
                if page:
                    self.pages.append(page)

    def get_posts_by_tag(self, tag: str) -> list:
        return self.tags.get(tag, [])

    def get_recent_posts(self, count: int = None) -> list:
        n = count or self.config.posts_per_page
        return self.posts[:n]
