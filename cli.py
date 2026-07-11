#!/usr/bin/env python3
"""Command-line interface for blog-engine."""

import os
import sys
import time
import yaml
import click
from pathlib import Path

from src.engine.core import SiteConfig, Site
from src.builders.static_builder import StaticBuilder


def load_config(config_path: str = "config.yaml") -> SiteConfig:
    """Load site configuration from YAML file."""
    path = Path(config_path)
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return SiteConfig(**{k: v for k, v in data.items() if hasattr(SiteConfig, k)})
    return SiteConfig()


@click.group()
@click.option('--config', default='config.yaml', help='Path to config file')
@click.pass_context
def cli(ctx, config):
    """blog-engine - A fast static blog generator."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(config)


@cli.command()
@click.pass_context
def build(ctx):
    """Build the static site."""
    config = ctx.obj['config']
    site = Site(config)
    click.echo("Loading content...")
    site.load()
    click.echo(f"Found {len(site.posts)} posts, {len(site.pages)} pages")
    builder = StaticBuilder(site)
    click.echo("Building site...")
    builder.build()
    click.echo("Done!")


@cli.command()
@click.option('--port', default=8000, help='Port to serve on')
@click.option('--host', default='127.0.0.1', help='Host to serve on')
@click.pass_context
def serve(ctx, port, host):
    """Serve the built site locally."""
    import http.server
    import functools

    config = ctx.obj['config']
    output_dir = Path(config.output_dir)
    if not output_dir.exists():
        click.echo("No built site found. Running build first...")
        ctx.invoke(build)

    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(output_dir)
    )

    with http.server.HTTPServer((host, port), handler) as httpd:
        click.echo(f"Serving site at http://{host}:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            click.echo("\nShutting down.")


@cli.command()
@click.pass_context
def watch(ctx):
    """Watch for changes and rebuild automatically."""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        click.echo("Install watchdog: pip install watchdog")
        sys.exit(1)

    config = ctx.obj['config']

    class RebuildHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if not event.is_directory:
                click.echo(f"Change detected: {event.src_path}")
                site = Site(config)
                site.load()
                builder = StaticBuilder(site)
                builder.build()
                click.echo("Rebuilt!")

    site = Site(config)
    site.load()
    builder = StaticBuilder(site)
    builder.build()

    observer = Observer()
    observer.schedule(RebuildHandler(), config.content_dir, recursive=True)
    observer.start()
    click.echo(f"Watching {config.content_dir} for changes... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@cli.command()
@click.argument('title')
@click.option('--tags', default='', help='Comma-separated tags')
@click.pass_context
def new(ctx, title, tags):
    """Create a new blog post."""
    config = ctx.obj['config']
    slug = title.lower().replace(' ', '-').replace("'", '')
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')

    from datetime import date
    today = date.today().isoformat()

    tags_yaml = f'[{", ".join(t.strip() for t in tags.split(",") if t.strip())}]' if tags else '[]'

    content = f"""---
title: "{title}"
date: "{today}"
tags: {tags_yaml}
slug: "{slug}"
---

# {title}

Write your post content here.
"""

    posts_dir = Path(config.content_dir) / 'posts'
    posts_dir.mkdir(parents=True, exist_ok=True)
    filepath = posts_dir / f"{slug}.md"
    filepath.write_text(content, encoding='utf-8')
    click.echo(f"Created new post: {filepath}")


if __name__ == '__main__':
    cli()
