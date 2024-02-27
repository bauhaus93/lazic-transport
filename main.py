#!/usr/bin/env python3
import logging
import os
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from context import CONTEXT

logging.basicConfig(
    format="%(asctime)s - %(levelname)s:  %(message)s",
    encoding="utf-8",
    level=logging.INFO,
)
_logger = logging.getLogger(__name__)


def _render_templates(input_dir: Path, output_dir: Path) -> None:
    env = Environment(
        loader=FileSystemLoader(str(input_dir)), autoescape=select_autoescape()
    )
    pages_dir = input_dir.joinpath("pages")

    for template_name in env.list_templates():
        template_path = input_dir.joinpath(template_name)
        if template_path.is_relative_to(pages_dir):
            page_path = template_path.relative_to(pages_dir)
            output_path = (
                output_dir.joinpath(page_path)
                .with_name(template_path.name)
                .with_suffix("")
            )
            _logger.info("Render template: %s -> %s", template_path, output_path)
            template = env.get_template(template_name)
            data = template.render(CONTEXT)
            with open(str(output_path), "w", encoding="utf-8") as f:
                f.write(data)


def main(input_dir: Path, output_dir: Path):
    _logger.info("Input directory: %s", input_dir)
    _logger.info("Output directory: %s", output_dir)
    _render_templates(input_dir, output_dir)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: main.py INPUT_DIR OUTPUT_DIR")
        sys.exit(1)
    main(Path(sys.argv[1]).absolute(), Path(sys.argv[2]).absolute())
