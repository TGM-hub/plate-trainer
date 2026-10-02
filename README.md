# Plate Trainer

GeoGuessr licence-plate trainer: multiple choice (continent → country) or typed answer, plus a study gallery.

## Deploy on GitHub Pages
Push the contents of this folder (index.html, data/, images/) to a repo → Settings → Pages → Deploy from branch `main` / root.

## Adding plates
Drop the image in `images/` and add a line to `data/plates.js`:

```js
{"id": "any-unique-id", "img": "images/my-plate.jpg", "country": "Peru", "continent": "South America",
 "mustLearn": false, "tags": ["white-long"], "lookalikes": ["Bolivia", "Chile"], "note": "What to look for."}
```

- `country` must match a name in `data/countries.js` (add it there if missing).
- `tags` come from `TAG_LABELS` in `countries.js`; they drive the category filters and the "hard" distractors.
- `lookalikes` are always preferred as wrong answers.
