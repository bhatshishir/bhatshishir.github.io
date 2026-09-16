# Investor, Antifragile and a Learning Machine

Shishir Bhat's Jekyll blog, using the Minima theme.

## Publish

1. In this repository on GitHub, open **Settings → Pages** and choose **GitHub Actions** as the source.
2. Commit and push these files to `main`.
3. Check the **Actions** tab for the deployment result.

After a successful deployment, the blog will be available at https://bhatshishir.github.io.
Every subsequent push to `main` builds and deploys the site automatically. No local Jekyll installation is required.

## Write a post

Create `_posts/YYYY-MM-DD-your-post-title.md` with front matter:

```markdown
---
layout: post
title: "Your post title"
date: 2026-09-16 00:00:00 +0530
tags: [learning]
---

Write your content here using Markdown.
```

Use the actual publication date in both the filename and front matter. Future-dated posts appear when a build runs after their publication time; the workflow does not schedule builds automatically.

## Add images

Upload images to `assets/images/` and reference them in a post:

```liquid
![Describe the image]({{ '/assets/images/my-photo.jpg' | relative_url }})
```

## Customize

- Edit `_config.yml` for the title, description, and author.
- Edit `index.md` for the homepage introduction. Minima's `home` layout lists posts automatically.
- Edit the sample welcome post or replace it with your own writing.
- Custom templates can go in `_layouts/` when needed. The theme currently supplies the layouts.

Other themes may require different layout names or additional configuration.
