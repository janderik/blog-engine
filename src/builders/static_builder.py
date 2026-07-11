"""Static site builder that renders templates and writes output files."""

import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.engine.core import Site, SiteConfig


class StaticBuilder:
    """Builds the static site from templates and content."""

    def __init__(self, site: Site):
        self.site = site
        self.config = site.config
        self.env = self._create_jinja_env()

    def _create_jinja_env(self) -> Environment:
        template_path = Path(self.config.template_dir) / self.config.theme
        if not template_path.exists():
            template_path = Path(self.config.template_dir) / 'default'

        return Environment(
            loader=FileSystemLoader(str(template_path)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def build(self):
        """Build the entire site."""
        output_path = Path(self.config.output_dir)
        self._clean_output(output_path)
        self._ensure_dirs(output_path)
        self._copy_assets()
        self._render_index(output_path)
        self._render_posts(output_path)
        self._render_tags(output_path)
        self._render_rss(output_path)
        print(f"Site built successfully in {output_path}/")

    def _clean_output(self, output_path: Path):
        if output_path.exists():
            shutil.rmtree(output_path)

    def _ensure_dirs(self, output_path: Path):
        (output_path / 'posts').mkdir(parents=True)
        (output_path / 'tags').mkdir(parents=True)
        (output_path / 'assets').mkdir(parents=True)

    def _copy_assets(self):
        assets_src = Path(self.config.content_dir) / 'assets'
        assets_dst = Path(self.config.output_dir) / 'assets'
        if assets_src.exists():
            shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)

    def _render_index(self, output_path: Path):
        template = self.env.get_template('index.html')
        recent_posts = self.site.get_recent_posts()
        html = template.render(
            site=self.site.config,
            posts=recent_posts,
            total_posts=len(self.site.posts),
        )
        (output_path / 'index.html').write_text(html, encoding='utf-8')

    def _render_posts(self, output_path: Path):
        template = self.env.get_template('post.html')
        for post in self.site.posts:
            post_html = template.render(
                site=self.site.config,
                post=post,
            )
            post_dir = output_path / 'posts' / post.slug
            post_dir.mkdir(parents=True)
            (post_dir / 'index.html').write_text(post_html, encoding='utf-8')

    def _render_tags(self, output_path: Path):
        tag_template = self.env.get_template('tag.html')
        for tag, posts in self.site.tags.items():
            tag_html = tag_template.render(
                site=self.site.config,
                tag=tag,
                posts=posts,
            )
            tag_dir = output_path / 'tags' / tag
            tag_dir.mkdir(parents=True)
            (tag_dir / 'index.html').write_text(tag_html, encoding='utf-8')

    def _render_rss(self, output_path: Path):
        template = self.env.get_template('rss.xml')
        rss = template.render(
            site=self.site.config,
            posts=self.site.posts[:20],
        )
        (output_path / 'rss.xml').write_text(rss, encoding='utf-8')
