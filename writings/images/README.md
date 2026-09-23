# Images inbox

Create one numbered folder for each writing and place its images inside:

```text
writings/
├── 1.txt
├── 2.txt
└── images/
    ├── 1/
    │   ├── cover.jpg
    │   └── chart.png
    └── 2/
        └── photo.webp
```

Use descriptive filenames when possible. If there is only one image, it becomes the post's cover and homepage thumbnail automatically. When there are multiple images, name the cover `cover.jpg`, `cover.png`, or `cover.webp`. Other images will be placed where markers such as `[place chart.png here]` appear in the text.

During conversion, images will be copied to `assets/images/posts/<number>/`, given useful alternative text, and linked using Jekyll-safe paths. Files in this inbox are not published directly.
