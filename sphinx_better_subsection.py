"""Better your Sphinx section IDs

Specify the ID of a section with normal `reST internal hyperlink targets`_:

.. code-block:: rest

    .. _v1.2.3:

    v1.2.3 (2022-03-19)
    -------------------

The permalink is ``#v1-2-3`` instead of ``#v1-2-3-2022-03-19``. Both target
IDs work however, so old docs will still point to the correct section.

.. _reST internal hyperlink targets:
    https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#hyperlink-targets

"""
from docutils import nodes
from docutils.transforms import Transform

class PreferSectionTarget(Transform):
    """Prefer target IDs over the section's own

    Given this input text:

    .. code-block:: rest

        .. _a:
        .. _b:
        .. _c:

        Section Title
        -------------

        A paragraph.

    This parses into:

    .. code-block:: xml

        ...
            <target refid="a">
            <target refid="b">
            <target refid="c">
            <section ids="section-title a b c">
                ...

    Transforming it gives:

    .. code-block:: xml

        ...
            <target refid="a">
            <target refid="b">
            <target refid="c">
            <section ids="c section-title a b">
                ...

    Note that the other IDs are all preserved; only the order is modified.
    Nested subsections are also checked.

    """
    # Post processing priority from
    # https://www.sphinx-doc.org/en/master/extdev/appapi.html?highlight=transform#sphinx.application.Sphinx.add_transform
    default_priority = 700

    def apply(self):
        """Docutils transform entry point"""
        for node in self.document.findall(nodes.section):
            # Get node directly preceding the section
            index = node.parent.index(node)
            if index == 0:
                continue
            last = node.parent[index - 1]
            # Targets are part of the previous section so we should look deeper
            while isinstance(last, nodes.Node) and last.children:
                last = last[-1]
            # Filter away nodes that aren't targets
            if not isinstance(last, nodes.target):
                continue
            # Internal hyperlink targets have refid (external ones have refuri)
            if "refid" not in last:
                continue
            refid = last["refid"]
            assert refid in node["ids"]
            # Prefer the target's ID
            node["ids"].remove(refid)
            node["ids"].insert(0, refid)

def setup(app):
    """Sphinx extension entry point"""
    app.add_transform(PreferSectionTarget)
    return {
        # Probably parallel-read safe (though I'm not sure)
        "parallel_read_safe": True,
    }