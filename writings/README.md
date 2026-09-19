# Writings inbox

Put unfinished writing in this folder as numbered plain-text files:

```text
1.txt
2.txt
3.txt
```

The first non-empty line is the post title. Write the article underneath it using plain text or Markdown. The only required content is a title and article text.

Optional metadata can follow the title:

```text
Why I Invest
Tags: investing, learning
Description: A short summary shown in previews.

The article starts here.
```

Every push to `main` converts all numbered text files automatically before Jekyll builds the site. Updating `1.txt` updates its published post on the next successful deployment. The original publication date is taken from the commit that first added the text file.

Number files sequentially and do not reuse a number. This folder is excluded from the published website.

## Images

Put images for each draft in the matching numbered folder under `writings/images/`. For example, images belonging to `1.txt` go in `writings/images/1/`. See `writings/images/README.md` for naming and placement guidance.
