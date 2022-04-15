{{ fullname | escape | underline }}

.. automodule:: {{ fullname }}
	:members:
	:undoc-members:
	:show-inheritance:
	:member-order: bysource

	{# The ordering of auto-summaries is from
	https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_member_order #}

	{% block modules %}
	{% if modules %}
	{{ _("Modules") | escape }}
	{{ "-" * (_("Modules") | escape | length) }}

	.. autosummary::
		:toctree:
		:recursive:

		{% for item in modules %}
		{{ item }}
		{%- endfor %}

	{% endif %}
	{% endblock %}

	{% block attributes %}
	{% if attributes %}
	{{ _("Module Attributes") | escape }}
	{{ "-" * (_("Module Attributes") | escape | length) }}

	.. autosummary::
		:nosignatures:

		{% for item in attributes %}
		{{ item }}
		{%- endfor %}

	{% endif %}
	{% endblock %}

	{% block exceptions %}
	{% if exceptions %}
	{{ _("Exceptions") | escape }}
	{{ "-" * (_("Exceptions") | escape | length) }}

	.. autosummary::
		:nosignatures:

		{% for item in exceptions %}
		{{ item }}
		{%- endfor %}

	{% endif %}
	{% endblock %}

	{% block classes %}
	{% if classes %}
	{{ _("Classes") | escape }}
	{{ "-" * (_("Classes") | escape | length) }}

	.. autosummary::
		:nosignatures:

		{% for item in classes %}
		{{ item }}
		{%- endfor %}

	{% endif %}
	{% endblock %}

	{% block functions %}
	{% if functions %}
	{{ _("Functions") | escape }}
	{{ "-" * (_("Functions") | escape | length) }}

	.. autosummary::
		:nosignatures:

		{% for item in functions %}
		{{ item }}
		{%- endfor %}

	{% endif %}
	{% endblock %}

	{# This adds separation between the auto-summaries and the auto-docs. #}
	{% if members %}
	{{ _("Documentation") | escape }}
	{{ "-" * (_("Documentation") | escape | length) }}
	{% endif %}
