# -*- coding: utf-8 -*-
#
# NWCSAF/MSG PP documentation build configuration file, created by
# sphinx-quickstart on Fri Sep 25 16:58:28 2009.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
"""Sphinx documentation configuration and setup."""

from __future__ import annotations

import datetime as dt
import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.append(os.path.abspath("../../"))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from pyresample.area_config import _read_yaml_area_file_content, generate_area_def_rst_list  # noqa: E402
from reader_table import generate_reader_table, rst_table_header, rst_table_row  # noqa: E402

import satpy  # noqa: E402
from satpy.resample import get_area_file  # noqa: E402

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# get version using setuptools-scm
release = satpy.__version__
# The full version, including alpha/beta/rc tags.
# for example take major/minor
version = ".".join(release.split(".")[:2])


class Mock(object):  # noqa
    """Mock class for mocking module instances."""

    def __init__(self, *args, **kwargs):
        """Mask any arguments to mock object."""
        self.__version__ = "0.0.0"

    def __call__(self, *args, **kwargs):
        """Mock a function and class object when accessed from mocked module."""
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        """Mock common module attributes used in documentation."""
        if name in ("__file__", "__path__"):
            return "/dev/null"
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        elif name == "inf":
            return 0
        else:
            return Mock()


# https://github.com/sphinx-doc/sphinx/issues/3920
MOCK_MODULES = ["h5py"]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()  # type: ignore

autodoc_mock_imports = ["cf", "glymur", "h5netcdf", "holoviews", "imageio", "mipp", "netCDF4",
                        "pygac", "pygrib", "pyhdf", "pyninjotiff",
                        "pyorbital", "pyspectral", "rasterio", "trollimage",
                        "zarr"]
autoclass_content = "both"  # append class __init__ docstring to the class docstring

# auto generate reader table from reader config files
with open("reader_table.rst", mode="w") as f:
    f.write(generate_reader_table())

# create table from area definition yaml file
area_file = get_area_file()[0]

area_dict = _read_yaml_area_file_content(area_file)
area_table = [rst_table_header("Area Definitions", header=["Name", "Description", "Projection"],
                               widths=[45, 60, 10], class_name="area-table")]

for aname, params in area_dict.items():
    area_table.append(rst_table_row([f"`{aname}`_", params.get("description", ""),
                                     params.get("projection").get("proj")]))

with open("area_def_list.rst", mode="w") as f:
    f.write("".join(area_table))
    f.write("\n\n")
    f.write(generate_area_def_rst_list(area_file))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx", "sphinx.ext.todo", "sphinx.ext.coverage",
              "sphinx.ext.doctest", "sphinx.ext.napoleon", "sphinx.ext.autosummary", "doi_role",
              "sphinx.ext.viewcode", "sphinxcontrib.apidoc",
              "sphinx.ext.mathjax"]

# API docs
apidoc_module_dir = "../../satpy"
apidoc_output_dir = "api"
apidoc_excluded_paths = [
    "readers/caliop_l2_cloud.py",
    "readers/ghrsst_l3c_sst.py",
    "readers/li_l2.py",
    "readers/scatsat1_l2b.py",
]
apidoc_separate_modules = True
apidoc_extra_args = [
    "--private",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = u"Satpy"
copyright = u"2009-{}, The PyTroll Team".format(dt.datetime.utcnow().strftime("%Y"))  # noqa: A001

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
# unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees: list[str] = []

# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "theme_overrides.css",  # override wide tables in RTD theme
    "https://cdn.datatables.net/v/dt/dt-2.0.0/datatables.min.css",
]

html_js_files = [
    "https://cdn.datatables.net/v/dt/dt-2.0.0/datatables.min.js",
    "main.js",
]


# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_use_modindex = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = "NWCSAFMSGPPdoc"


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
# latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ("index", "satpy.tex", "Satpy Documentation",
   "Satpy Developers", "manual"),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_use_modindex = True


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "dask": ("https://docs.dask.org/en/latest", None),
    "geoviews": ("https://geoviews.org", None),
    "jobqueue": ("https://jobqueue.dask.org/en/latest", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pydecorate": ("https://pydecorate.readthedocs.io/en/stable", None),
    "pyorbital": ("https://pyorbital.readthedocs.io/en/stable", None),
    "pyproj": ("https://pyproj4.github.io/pyproj/dev", None),
    "pyresample": ("https://pyresample.readthedocs.io/en/stable", None),
    "pytest": ("https://docs.pytest.org/en/stable/", None),
    "python": ("https://docs.python.org/3", None),
    "scipy": ("https://scipy.github.io/devdocs", None),
    "trollimage": ("https://trollimage.readthedocs.io/en/stable", None),
    "trollsift": ("https://trollsift.readthedocs.io/en/stable", None),
    "xarray": ("https://xarray.pydata.org/en/stable", None),
    "rasterio": ("https://rasterio.readthedocs.io/en/latest", None),
    "donfig": ("https://donfig.readthedocs.io/en/latest", None),
    "pooch": ("https://www.fatiando.org/pooch/latest/", None),
    "fsspec": ("https://filesystem-spec.readthedocs.io/en/latest/", None),
}
