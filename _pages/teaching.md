---
permalink: /teaching/
layout:    default
title:     Teaching
---

{% for research in site.pages reversed %}
{% if research.categories == 'teaching' %}
  <h3>{{ research.title }}</h3>
  {% if research.image %} ![JPG](/img/research/{{ research.image }})  {% endif %}
  {: style="text-align: left"}
  {{ research.content }}
  {% if research.paper %} [PDF](/img/pdfs/{{ research.paper }}) {% endif %}
  
  ----------
{% endif %}
{% endfor %}