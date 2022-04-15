sphinx-better-subsection
========================

Better your Sphinx_ section IDs.

This extension helps keep your permalinks permanent by allowing you to specify
a section's ID. As an example:

.. code-block:: rest

    .. _v1.2.3:

    v1.2.3 (2022-03-19)
    -------------------

The permalink on the title will be ``#v1-2-3`` instead of
``#v1-2-3-2022-03-19``. When you change the section title later on, the
permalink will still work.

.. _Sphinx: https://www.sphinx-doc.org/en/master/

Installation
------------

Download and install this extension using pip:

.. code-block:: bash

    $ pip install sphinx-better-subsection

Then add this extension in your ``conf.py``:

.. code-block:: python

    extensions += ["sphinx_better_subsection"]

Usage
-----

Add a `reST internal hyperlink target`_ (the ``.. _name:`` syntax) before your
section. This extension moves that ID to the front of the IDs list, making the
permalink the target's ID instead of the generated ID from the title. When
multiple are found, the **last** one is used.

This enhances existing reST to `do the expected thing`_ and also degrades
gracefully when this extension isn't used (such as in GitHub or online
renderers).

.. _reST internal hyperlink target: https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#inline-internal-targets
.. _do the expected thing: https://github.com/sphinx-doc/sphinx/issues/1961

Docutils
--------

This package provides a docutils_ transformer called `PreferSectionTarget`
(subclass of ``docutils.transforms.Transform``) usable via:

.. code-block:: python

    from sphinx_better_subsection import PreferSectionTarget
    document.transformer.add_transform(PreferSectionTarget)

.. _docutils: https://docutils.sourceforge.io/

MyST
----

As far as I can tell, this extension is compatible with MyST_ using its
`header target syntax`_ (the ``(name)=`` syntax). The first example in
MyST would be:

.. code-block:: markdown

    (v1.2.3)=
    ## v1.2.3 (2022-03-19)

.. _MyST: https://myst-parser.readthedocs.io/en/latest/
.. _header target syntax: https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html#targets-and-cross-referencing
