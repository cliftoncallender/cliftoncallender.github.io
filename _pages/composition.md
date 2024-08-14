---
permalink: /composition/
layout: default
title: Composition
---
### Selected Compositions
Contact me for complete list, parts, click tracks, etc.

{% for composition in site.pages reversed %}
{% if composition.categories == 'composition' %}
 __________
 
 *{{ composition.title }}*
 {% if composition.instrumentation %} for {{ composition.instrumentation }} {% endif %}
 {% if composition.score %} [PDF](/img/pdfs/{{ composition.score }}) {% endif %}<br>
 {% if composition.performance %} {{ composition.performance }} {% endif %}
 
 {% if composition.soundcloud-id %} <iframe width="100%" height="100" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F{{ composition.soundcloud-id }}&amp;show_artwork=true&amp;color=FFA640"></iframe> {% endif %}
 {% if composition.soundcloud-playlist-id %} <iframe width="100%" height="350" scrolling="yes" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/{{ composition.soundcloud-playlist-id }}&amp;show_artwork=true&amp;color=FFA640"></iframe> {% endif %}
 {% if composition.youtube-id %}
  <div class="videoWrapper">
   <iframe width="560" height="315" src='http://www.youtube.com/embed/{{ composition.youtube-id }}' frameborder='0' allowfullscreen></iframe>
  </div>
 {% endif %}

 {{ composition.content }}

{% endif %}
{% endfor %}