# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- import modules ----------------------------------------------------------

import sys, os
sys.path.insert(0, os.path.abspath('../../'))
import pyR2D2

# -- Project information -----------------------------------------------------

project = 'R2D2 Document'
copyright = '2020-2024, Hideyuki Hotta'
author = 'Hideyuki Hotta'

# The full version, including alpha/beta/rc tags
version = pyR2D2.__version__
release = pyR2D2.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',  # ソースコードのリンク 
    'sphinx.ext.intersphinx',  # 他のドキュメントへのリンク       
    'sphinx.ext.todo',
    'sphinx.ext.imgmath',
    'sphinx_automodapi.automodapi',
    'sphinx_multiversion',
]

# autodocsumm_member_order = 'bysource'
#autodoc_member_order = 'bysource'  # or 'alphabetical', 'groupwise'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),  # NumPy のドキュメントへのリンクを追加
    'gspread': ('https://docs.gspread.org/en/latest/', None),  # gspred のドキュメントへのリンクを追加
    # 他のプロジェクトのドキュメントへのリンクを追加する場合はここに記述
}

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bizstyle'
#html_theme = 'sphinx_book_theme'
#html_theme = 'alabaster'
#html_theme = 'sphinx_material'
html_theme = 'sphinx_rtd_theme'
#html_theme = "pydata_sphinx_theme"

autodoc_member_order = 'bysource'
autosummary_imported_members = True
autodoc_default_options = {
    # 'members': True,              # クラスやモジュールのメンバーを表示
    'undoc-members': True,        # ドキュメント化されていないメンバーも表示
    'private-members': True,      # アンダースコア(_)で始まるメンバーも表示
    'special-members': '__init__', # 特殊メソッドも表示 (__init__, __call__ など)
    'member-order': 'bysource',   # ソースコードの順に表示
    'show-inheritance': True,     # クラスの継承関係を表示
}

smv_tag_whitelist = r'^v.*$'  # タグ "v1.0" などを対象

automodsumm_sort = False  # ソートを無効化（ファイル順序を優先）

# napoleon_include_init_with_doc = True
napoleon_use_ivar = True

automodapi_inheritance_diagram = False
autosummary_generate = True  # autosummaryでファイルを生成

automodsumm_included_members = ['__init__']

graphviz_dot = 'dot'

##############################
# Logo setting
html_logo = '_static/figs/R2D2_logo_red.png'
html_theme_options = {
    'version_selector': True,
    "logo_only": False,  # サイドバーにロゴだけ表示
    "navigation_depth": 4,  # サイドバーの深さ
    "style_nav_header_background": "#30476E",  # ナビゲーションヘッダーの色を変更（任意）
}

##############################

html_context = {
  'current_version' : "v"+version,
}

##############################
todo_include_todos = True

#extensions += ['sphinx.ext.imgmath']
imgmath_image_format = 'svg'
pngmath_latex='platex'
imgmath_font_size = 12 # 数式のフォントサイズ
imgmath_latex_preamble = r'\usepackage{color}'

latex_elements = { \
'extraclassoptions': 'report', 
}

# Sphinx autodoc hook for adding alias information to methods of pyR2D2.Read and pyR2D2.Sync
# This hook modifies the docstrings of pyR2D2.Read and pyR2D2.Sync methods to include an alias 
# indicating how they are accessed through R2D2_data.read or R2D2_data.sync.
# Example: pyR2D2.Read.qq_select -> pyR2D2.Data.read.qq_select

import inspect

def autodoc_process_docstring(app, what, name, obj, options, lines):
    # Mapping of alias names (e.g., 'read', 'sync') to their respective classes
    target_classes = {
        "read": "pyR2D2.Read.",
        "sync": "pyR2D2.Sync."
    }

    for alias, target_class in target_classes.items():
        if name.startswith(target_class):
            # Add a note indicating how the method is accessed
            method_name = name.split(".")[-1]
            alias_name = f"pyR2D2.Data.{alias}.{method_name}"
            lines.append("")
            lines.append(f".. important:: This method is accessible as `{alias_name}`.")
            lines.append("")
            break  # No need to check further classes

def setup(app):
    # Connect the hook to the autodoc event in Sphinx
    app.connect("autodoc-process-docstring", autodoc_process_docstring)
    
    from sphinx.ext.autosummary import Autosummary