# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: {{ ', '.join(description.files) }}
# plugin: python-betterproto
from dataclasses import dataclass
{% if description.datetime_imports %}
from datetime import {% for i in description.datetime_imports %}{{ i }}{% if not loop.last %}, {% endif %}{% endfor %}

{% endif%}
{% if description.typing_imports %}
from typing import {% for i in description.typing_imports %}{{ i }}{% if not loop.last %}, {% endif %}{% endfor %}

{% endif %}

import betterproto
{% if description.services %}
import grpclib
{% endif %}

{% for i in description.imports %}
{{ i }}
{% endfor %}


{% if description.enums %}{% for enum in description.enums %}
class {{ enum.py_name }}(betterproto.Enum):
    {% if enum.comment %}
{{ enum.comment }}

    {% endif %}
    {% for entry in enum.entries %}
        {% if entry.comment %}
{{ entry.comment }}
        {% endif %}
    {{ entry.name }} = {{ entry.value }}
    {% endfor %}


{% endfor %}
{% endif %}
{% for message in description.messages %}
@dataclass
class {{ message.py_name }}(betterproto.Message):
    {% if message.comment %}
{{ message.comment }}

    {% endif %}
    {% for field in message.properties %}
        {% if field.comment %}
{{ field.comment }}
        {% endif %}
    {{ field.py_name }}: {{ field.type }} = betterproto.{{ field.field_type }}_field({{ field.number }}{% if field.field_type == 'map'%}, betterproto.{{ field.map_types[0] }}, betterproto.{{ field.map_types[1] }}{% endif %}{% if field.one_of %}, group="{{ field.one_of }}"{% endif %}{% if field.field_wraps %}, wraps={{ field.field_wraps }}{% endif %})
    {% endfor %}
    {% if not message.properties %}
    pass
    {% endif %}


{% endfor %}
{% for service in description.services %}
class {{ service.py_name }}Stub(betterproto.ServiceStub):
    {% if service.comment %}
{{ service.comment }}

    {% endif %}
    {% for method in service.methods %}
    async def {{ method.py_name }}(self
        {%- if not method.client_streaming -%}
            {%- if method.input_message and method.input_message.properties -%}, *,
                {%- for field in method.input_message.properties -%}
                    {{ field.name }}: {% if field.zero == "None" and not field.type.startswith("Optional[") -%}
                                        Optional[{{ field.type }}]
                                      {%- else -%}
                                        {{ field.type }}
                                      {%- endif -%} = {{ field.zero }}
                    {%- if not loop.last %}, {% endif -%}
                {%- endfor -%}
            {%- endif -%}
        {%- else -%}
            {# Client streaming: need a request iterator instead #}
            , request_iterator: Iterator["{{ method.input }}"]
        {%- endif -%}
            ) -> {% if method.server_streaming %}AsyncGenerator[{{ method.output }}, None]{% else %}{{ method.output }}{% endif %}:
        {% if method.comment %}
{{ method.comment }}

        {% endif %}
        {% if not method.client_streaming %}
        request = {{ method.input }}()
        {% for field in method.input_message.properties %}
            {% if field.field_type == 'message' %}
        if {{ field.name }} is not None:
            request.{{ field.name }} = {{ field.name }}
            {% else %}
        request.{{ field.name }} = {{ field.name }}
            {% endif %}
        {% endfor %}
        {% endif %}

        {% if method.server_streaming %}
        {% if method.client_streaming %}
        async for response in self._stream_stream(
            "{{ method.route }}",
            request_iterator,
            {{ method.input }},
            {{ method.output }},
        ):
            yield response
        {% else %}{# i.e. not client streaming #}
        async for response in self._unary_stream(
            "{{ method.route }}",
            request,
            {{ method.output }},
        ):
            yield response

        {% endif %}{# if client streaming #}
        {% else %}{# i.e. not server streaming #}
        {% if method.client_streaming %}
        return await self._stream_unary(
            "{{ method.route }}",
            request_iterator,
            {{ method.input }},
            {{ method.output }}
        )
        {% else %}{# i.e. not client streaming #}
        return await self._unary_unary(
            "{{ method.route }}",
            request,
            {{ method.output }}
        )
        {% endif %}{# client streaming #}
        {% endif %}

    {% endfor %}
{% endfor %}
