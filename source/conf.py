# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from sphinx.writers.html import HTMLTranslator
from docutils import nodes
from docutils.nodes import Element
import os
import sys

sys.path.insert(0, os.path.abspath("_themes"))

project = 'Vicharak'
copyright = '2023, Vicharak Computers LLP'
author = 'Vicharak'
version = "0.1"

html_theme = 'sphinxawesome_theme'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['breathe', 'myst_parser']
# extensions += ["sphinxawesome_theme.docsearch", "sphinxawesome.highlighting"]
source_suffix = ['.rst', '.md']

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# -- Documentation for adding theme to local directory
# https://sphinxawesome.xyz/how-to/add/


html_static_path = ['_static']
html_title = "Vicharak"
# html_theme_path = ["_themes"]
# exclude_patterns = ["_themes"]






class PatchedHTMLTranslator(HTMLTranslator):

    def visit_reference(self, node: Element) -> None:
        atts = {'class': 'reference'}
        if node.get('internal') or 'refuri' not in node:
            atts['class'] += ' internal'
        else:
            atts['class'] += ' external'
            # ---------------------------------------------------------
            # Customize behavior (open in new tab, secure linking site)
            atts['target'] = '_blank'
            atts['rel'] = 'noopener noreferrer'
            # ---------------------------------------------------------
        if 'refuri' in node:
            atts['href'] = node['refuri'] or '#'
            if self.settings.cloak_email_addresses and atts['href'].startswith('mailto:'):
                atts['href'] = self.cloak_mailto(atts['href'])
                self.in_mailto = True
        else:
            assert 'refid' in node, \
                   'References must have "refuri" or "refid" attribute.'
            atts['href'] = '#' + node['refid']
        if not isinstance(node.parent, nodes.TextElement):
            assert len(node) == 1 and isinstance(node[0], nodes.image)
            atts['class'] += ' image-reference'
        if 'reftitle' in node:
            atts['title'] = node['reftitle']
        if 'target' in node:
            atts['target'] = node['target']
        self.body.append(self.starttag(node, 'a', '', **atts))

        if node.get('secnumber'):
            self.body.append(('%s' + self.secnumber_suffix) %
                             '.'.join(map(str, node['secnumber'])))


def setup(app):
    app.set_translator('html', PatchedHTMLTranslator)


html_theme_options = {
    "logo_light": "_static/vicharak-logo-light.svg",
    "logo_dark": "_static/vicharak-logo-dark.svg"
}

breathe_projects = {"drm_fpga_write": os.getcwd() + "/../xml/"}
breathe_default_project = "drm_fpga_write"