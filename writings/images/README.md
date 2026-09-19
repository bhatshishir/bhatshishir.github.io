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

Use descriptive filenames when possible. `cover.jpg` or `cover.png` will be treated as the post's cover and homepage thumbnail. Other images will be placed in the article where they fit the text. If placement matters, write a note in the text such as `[place chart.png here]`.

During conversion, images will be copied to `assets/images/posts/<number>/`, given useful alternative text, and linked using Jekyll-safe paths. Files in this inbox are not published directly.
