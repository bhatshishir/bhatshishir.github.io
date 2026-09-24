---
layout: default
title: Topics
description: Browse writing by topic.
permalink: /tags/
---

{% include heading.html heading=page.title description=page.description %}

<main class="topic-page">
  {% for topic in site.data.topics %}
    {% assign tagged_posts = site.tags[topic] %}
    <section id="{{ topic | slugify }}" class="topic-section">
      <h2>{{ topic }}</h2>
      {% if tagged_posts.size > 0 %}
        <ul>
          {% for post in tagged_posts %}
            <li>
              <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %-d, %Y" }}</time>
              <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
            </li>
          {% endfor %}
        </ul>
      {% else %}
        <p>No articles yet.</p>
      {% endif %}
    </section>
  {% endfor %}
</main>
