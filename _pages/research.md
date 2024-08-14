---
permalink: /research/
layout:    default
title:     Research
---

{% for research in site.pages reversed %}
{% if research.categories == 'research' %}
  <h3>{{ research.title }}</h3>
  {% if research.image %} ![JPG](/img/research/{{ research.image }})  {% endif %}
  {: style="text-align: center"}
  {{ research.content }}
  {% if research.paper %} [PDF](/img/pdfs/{{ research.paper }}) {% endif %}
  {% if research.presentation %} [presentation](/resources/{{ research.presentation }}) {% endif %}
  
  ----------
{% endif %}
{% endfor %}