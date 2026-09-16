# Investor, Antifragile and a Learning Machine

shiihsr's blog using [Jekyll Atlantic](https://github.com/zerostaticthemes/jekyll-atlantic-theme) by Zerostatic. The original MIT license is included in LICENSE.

## Publishing

Set GitHub repository Settings > Pages > Source to GitHub Actions, then push to main. The workflow builds Tailwind CSS and Jekyll before deploying to https://bhatshishir.github.io.

## Writing

Add posts in `_posts/YYYY-MM-DD-title.md` with `layout: post`, `title`, `date`, and optional `tags` in YAML front matter. Optional `thumbnail` displays an image in the homepage card; `image` and `image_alt` add an article cover. Keep assets in `assets/images/` and use the Liquid `relative_url` filter for links.

Future-dated posts require a build after their publication time.

## Design

Edit `index.md` for the headline and introduction, `_config.yml` for site settings, and `_data/authors.yml` for author information. The title appears once on the homepage; the header uses the author's name.

Edit `assets/css/custom.css` for colors and spacing. `npm ci` followed by `npm run build:css` compiles the stylesheet. With Ruby installed, use `bundle install` and `bundle exec jekyll serve` to preview locally.

The demo thumbnail is provided by the Atlantic template (Unsplash).
