# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
import sphinxcontrib_django
import django

sys.path.insert(0, os.path.abspath('../back-end/'))
#print(sys.path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'revs_backend.settings' 
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Rev's Restaurant POS System"
copyright = '2024, Rushil Jayant, Riley Wenckens, Rahul Rajendran, Elvis Chen, Diego Martinez, Laith Bohsali'
author = 'Rushil Jayant, Riley Wenckens, Rahul Rajendran, Elvis Chen, Diego Martinez, Laith Bohsali'
release = '3.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinxcontrib_django']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']