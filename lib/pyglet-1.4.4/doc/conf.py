# -*- coding: utf-8 -*-
#
# Nabla Lab documentation build configuration file, created by
# Txema Vicente <txema@nabla.net>
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# pyglet base path.
sys.path.insert(0, os.path.abspath('..'))

# patched extensions base path.
sys.path.insert(0, os.path.abspath('.'))

sys.is_epydoc = True
try:
    import pyglet
except:
    print "ERROR: pyglet not found"
    sys.exit(1)

print "Generating pyglet %s Documentation" % (pyglet.version)

implementations = ["carbon", "cocoa", "win32", "xlib"]

# Do not try to import these modules
skip_modules = {"pyglet": {
                     "pyglet.app": implementations,
                     "pyglet.canvas": implementations + ["xlib_vidmoderestore"],
                     "pyglet.font": ["carbon",
                                     "quartz",
                                     "win32",
                                     "freetype", "freetype_lib"],
                     "pyglet.input": ["carbon_hid", "carbon_tablet",
                                      "darwin_hid",
                                      "directinput",
                                      "evdev",
                                      "wintab",
                                      "x11_xinput", "x11_xinput_tablet"],
                     "pyglet.image.codecs": ["gdiplus",
                                             "gdkpixbuf2",
                                             "pil",
                                             "quartz",
                                             "quicktime"],
                     "pyglet.gl": implementations + ["agl",
                                  "glext_arb", "glext_nv",
                                  "glx", "glx_info",
                                  "glxext_arb", "glxext_mesa", "glxext_nv",
                                  "lib_agl", "lib_glx", "lib_wgl",
                                  "wgl", "wgl_info", "wglext_arb", "wglext_nv"],
                     "pyglet.libs": ["darwin",
                                     "win32",
                                     "x11"],
                     "pyglet.media.drivers": ["directsound",
                                              "openal",
                                              "pulse"],
                     "pyglet.window": implementations,
                     },
                "tests": {}
               }


# Skip members
def skip_member(member, obj):
    module = obj.__name__

    if ".win32" in module: return True
    if ".carbon" in module: return True
    if ".cocoa" in module: return True
    if ".xlib" in module: return True

    if member.startswith("PFN"): return True

    if module.startswith("pyglet.gl.glext_"): return True
    if module.startswith("pyglet.gl.gl_ext_"): return True
    if module.startswith("pyglet.gl.glxext_"): return True
    if module.startswith("pyglet.image.codecs."): return True

    if module=="pyglet.gl.gl" or module=="pyglet.gl.gl_info":
        if member=="pointer": return True
    else:
        if member.upper().startswith("GL"):
            if member.endswith("Info"): return False
            if member.upper().startswith("GLU"):
                if (".glu" in module):
                    if member.startswith("GLU") and \
                       not member.startswith("GLU_") : return True
                    return False
            if not member.startswith("gl_"): return True

    if module in ["pyglet.gl.gl_info",
                  "pyglet.gl.glu",
                  "pyglet.gl.glu_info"]  \
       or module.startswith("pyglet.image"):
        if member in ["FormatError",
                      "POINTER",
                      "addressof",
                      "alignment",
                      "byref",
                      "get_errno",
                      "get_last_error",
                      "pointer",
                      "resize",
                      "set_conversion_mode",
                      "set_last_error",
                      "set_errno",
                      "sizeof"]:
            return True

    return False

autosummary_generate = True

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc',
              'ext.autosummary',
              'sphinx.ext.inheritance_diagram',
              'sphinx.ext.todo']

inheritance_graph_attrs = dict(rankdir="LR", size='""')

autodoc_member_order='groupwise'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.txt'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'pyglet'
copyright = u'2006, Alex Holkner'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '1.2'
# The full version, including alpha/beta/rc tags.
release = pyglet.version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '_templates']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['pyglet.']


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'nature'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "pyglet v%s documentation" % (pyglet.version)

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "pyglet"

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/logo.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = True

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'pygletdoc'


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'pyglet.tex', u'pyglet Documentation',
   u'Alex Holkner', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'pyglet', u'pyglet Documentation',
     [u'Alex Holkner'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'pyglet', u'pyglet Documentation',
   u'Alex Holkner', 'pyglet', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'


# pyglet documentation --------------------------------------------------

import inspect
import time
import datetime

# Search all submodules
def _get_submodules(rootpath, skip):
    """
    Look for every file in the directory tree and return a dict
    Hacked from sphinx.autodoc
    """

    INITPY = '__init__.py'

    rootpath = os.path.normpath(os.path.abspath(rootpath))
    if INITPY in os.listdir(rootpath):
        root_package = rootpath.split(os.path.sep)[-1]
        print "Searching modules in", rootpath
    else:
        print "No modules in", rootpath
        return

    def makename(package, module):
        """Join package and module with a dot."""
        if package:
            name = package
            if module:
                name += '.' + module
        else:
            name = module
        return name

    tree = {}
    saved = 0
    found = 0
    def save(module, submodule):
        if skip.has_key(module):
            if submodule in skip[module]:
                return False
        if not tree.has_key(module):
            tree[module] = []
        tree[module].append(submodule)
        return True

    for root, subs, files in os.walk(rootpath):
        py_files = sorted([f for f in files if os.path.splitext(f)[1] == '.py'])

        if INITPY in py_files:
            subpackage = root[len(rootpath):].lstrip(os.path.sep).\
                replace(os.path.sep, '.')
            full = makename(root_package, subpackage)
            part = full.rpartition('.')
            base_package, submodule = part[0], part[2]
            found += 1
            if save(base_package, submodule): saved += 1

            py_files.remove(INITPY)
            for py_file in py_files:
                found += 1
                module = os.path.splitext(py_file)[0]
                if save(full, module): saved += 1

    for item in tree.keys():
        tree[item].sort()
    print "%s contains %i submodules, %i skipped" % \
          (root_package, found, found-saved)
    return tree

for mod in skip_modules.keys():
    sys.all_submodules = _get_submodules(os.path.join('..', mod),
                                         skip_modules[mod])
sys.skip_member = skip_member


# Events
from sphinx.ext.autodoc import MethodDocumenter, ModuleDocumenter

class EventDocumenter(MethodDocumenter):
    objtype = "event"
    member_order = 45
    priority = 5

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        if member.__doc__ is not None:
            if ":event:" in member.__doc__:
                return inspect.isroutine(member) and \
                       not isinstance(parent, ModuleDocumenter)
        return False

def setup(app):
    app.add_autodocumenter(EventDocumenter)


# Generated contents
with open('internal/blacklist.rst', 'w') as f:
    pack = skip_modules["pyglet"]
    modules = pack.keys()
    modules.sort()
    for mod in modules:
        pack[mod].sort()
        for sub in pack[mod]:
            f.write("* ``"+mod+"."+sub+"``\n")

now = datetime.datetime.fromtimestamp(time.time())
with open('internal/build.rst', 'w') as f:
    f.write(".. list-table::\n")
    f.write("   :widths: 50 50\n")
    f.write("\n")
    for var, val in (("Date", now.strftime("%Y/%m/%d %H:%M:%S")),
                     ("pyglet version", pyglet.version)):
        f.write("   * - "+var+"\n     - "+val+"\n")


