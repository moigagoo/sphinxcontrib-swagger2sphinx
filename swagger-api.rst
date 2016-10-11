{% macro render_item(item, item_data) %}
  {% if item == "$ref" %}
- {{ render_ref(item_data) }}
  {% else %}
- {{ item }}: {{ item_data }}
  {% endif %}
{% endmacro %}

{% macro render_items(items, indent = 0) %}
  {% for item, item_data in items | dictsort %}
{{ render_item(item, item_data) | indent(indent, True) }}
  {% endfor %}
{% endmacro %}

{% macro render_property(property, property_data, is_required = False) %}
  {% if property == "$ref" %}
- {{ render_ref(property_data) }}
  {% elif "$ref" in property_data and property_data | length == 1 %}
- {{ render_ref(property_data["$ref"]) }}{% if is_required %}\*{% endif %}
  {% elif "allOf" in property_data and property_data | length == 1 %}
- {{ render_ref(property_data["allOf"][0]["$ref"]) }}{% if is_required %}\*{% endif %}
  {% else %}
- {{ property }}{% if is_required %}\*{% endif %}{% if property_data.type%} *({{ property_data.type }})*{% endif %}{% if property_data.description %}: {{ property_data.description }}{% endif %}
  {% endif %}
{% endmacro %}

{% macro render_properties(properties, required = [], indent = 0) %}
  {% for property, property_data in properties | dictsort %}
{{ render_property(property, property_data, property in required) | indent(indent, True)}}

    {% if "properties" in property_data %}
{{ render_properties(property_data.properties) | indent(indent+2, True) }}

    {% elif "items" in property_data %}
{{ render_items(property_data["items"]) | indent(indent+2, True) }}

    {% endif %}
  {% endfor %}
{% endmacro %}

{% macro render_definitions(definitions, indent = 0) %}
  {% for ref, definition in definitions | dictsort %}
{{ ref | indent(indent, True) }}

{{ render_properties(definition.properties, definition.required, indent+2) }}
  {% endfor %}
{% endmacro %}


#############################
{{ swagger_data.info.title }}
#############################

{{ swagger_data.info.description }}

:Version: {{ swagger_data.info.version }}

{% if swagger_data.schemes | length > 1 %}
:Schemes:

  {% for scheme in swagger_data.schemes %}
  - {{ scheme }}
  {% endfor %}
{% elif swagger_data.schemes | length == 1 %}
:Scheme:

  {{ swagger_data.schemes[0] }}
{% endif %}

{% if swagger_data.consumes | length > 1 %}
:Consumes:

  {% for consume in swagger_data.consumes %}
  - {{ consume }}
  {% endfor %}
{% elif swagger_data.consumes | length == 1 %}
:Consumes:

  {{ swagger_data.consumes[0] }}
{% endif %}

{% if swagger_data.produces | length > 1 %}
:Produces:

  {% for produce in swagger_data.produces %}
  - {{ produce }}
  {% endfor %}
{% elif swagger_data.produces | length == 1 %}
:Produces:

  {{ swagger_data.produces[0] }}
{% endif %}

:Swagger File:

  {% if swagger_file %}
  :download:`swagger.json <{{ swagger_file }}>`
  {% elif swagger_uri %}
  `swagger.json <{{ swagger_uri }}>`__
  {% endif %}


*****
Paths
*****

{% macro render_ref(ref) %}:term:`{{ ref.replace("#/definitions/", "") }}`{% endmacro %}

{% for path, methods in swagger_data.paths | dictsort %}
  {% for method, method_data in methods | dictsort %}

.. http:{{ method }}:: {{ path }}

  {{ method_data.summary }}

    {% for param in method_data.parameters %}
      {% if param.in == "query" %}

  :query {{ param.type }} {{ param.name }}: {{ param.description }}

      {% elif param.in == "path" %}

  :param {{ param.type }} {{ param.name }}: {{ param.description }}

      {% elif param.in == "body"  %}

  :Body: {{ render_ref(param.schema["$ref"]) }}

      {% endif %}
    {% endfor %}

    {% for response_code, response_data in method_data.responses | dictsort %}
  :status {{ response_code }}:
    {{ response_data.description }}
      {% if "schema" in response_data %}
    Response: {{ render_ref(response_data.schema["$ref"]) }}
      {% endif %}
    {% endfor %}

  {% endfor %}
{% endfor %}


***********
Definitions
***********

.. glossary::

{{ render_definitions(swagger_data.definitions, 2) }}
