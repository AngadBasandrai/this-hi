# thishi.org

**Ever dream this hi?** A fan-made parody of [thisman.org](https://thisman.org/) about the cat that says hi
([@SillyPianist67](https://x.com/SillyPianist67)), inspired by [this post](https://x.com/azzyazide/status/2111359361851252860).

Static site served by GitHub Pages at https://thishi.org.

## Editing

- Page content lives in `_pages/*.html`. The shared header, nav and footer live in `_build.py`.
- After editing, rebuild and commit the generated files:

  ```sh
  python _build.py
  ```

- Styles: `assets/style.css` (layout mirrors thisman.org). Live entries: `assets/site.js`.
- Derived images (sketches, poster, icons) are generated from `assets/avatar.jpg` by `_make_images.py` (needs Pillow + numpy):

  ```sh
  python _make_images.py assets
  ```

## Live entries

Dreams, In the World, Fan Art and Guestbook entries come from this repo's GitHub issues. Any issue whose title starts with
`Dream:`, `Sighting:`, `Fan art:` or `Guestbook:` shows up on the matching page. The Contact and Guestbook forms open a prefilled issue. Close an issue to remove it from the site.

## Preview locally

```sh
python _build.py
python -m http.server 8000
```
