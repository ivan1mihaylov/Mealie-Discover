# Mealie Discover

Find recipes from the Home Assistant sidebar and import a selected URL into Mealie. This is a HACS custom integration; it does not modify Mealie's UI or database.

## What it shows

- **Recipe websites:** results from your [SearXNG](https://docs.searxng.org/) instance. Home Assistant opens each result and reads its schema.org `Recipe` data, so the rating, number of ratings and cooking time are shown when the site publishes them. Pages with a recipe come first, most rated on top; pages without one are marked because Mealie will likely fail to import them. Search position is **not** a view count.
- **YouTube:** videos sorted by actual YouTube view counts, with likes when available. Video import may require Mealie's AI import feature and is not guaranteed to work with every video.
- **Add to Mealie:** sends the selected URL to Mealie's `POST /api/recipes/create/url` API. The source must be supported by Mealie's scraper; Mealie's error message is shown when it is not.

Search is on demand. API keys and the Mealie token stay in Home Assistant's config entry and are not sent to the browser.

## Install from HACS

1. HACS → three-dot menu → **Custom repositories** → add `https://github.com/ivan1mihaylov/Mealie-Discover` as **Integration**.
2. Install Mealie Discover, then restart Home Assistant.
3. Settings → Devices & services → Add integration → **Mealie Discover**.
4. Supply the Mealie URL and a Mealie API token, plus at least one search provider below. Home Assistant checks the connection before saving.

   On Home Assistant OS, running SearXNG and Mealie add-ons are detected and their URLs are filled in for you; check them and add the token.
5. Open **Mealie Discover** from the Home Assistant sidebar.

To change the URLs, token or keys later: Settings → Devices & services → Mealie Discover → three-dot menu → **Reconfigure**.

### Mealie connection

Create a long-lived API token in your Mealie user profile. Enter a URL reachable **from Home Assistant Core**, for example `http://<mealie-host>:9000`. If Mealie is a Home Assistant app/add-on, use its internal address and port if it exposes one; its sidebar ingress URL may not be suitable for direct API access. The “Open recipe” link also uses this configured URL (with your Mealie group), so use a URL reachable by your browser if possible. Avoid putting the token in the URL.

### Recipe websites (optional)

Run a [SearXNG](https://docs.searxng.org/) instance reachable from Home Assistant (for example the SearXNG Docker image or a Home Assistant app/add-on) and enter its URL, for example `http://<searxng-host>:8080`. SearXNG disables JSON output by default; enable it in `settings.yml`:

```yaml
search:
  formats:
    - html
    - json
```

Search in any language. The panel has a language filter (all languages, Bulgarian or English, remembered per browser), and the integration adds “рецепта” or “recipe” to the query depending on its alphabet, unless you already wrote it. Public SearXNG instances usually block JSON requests, so use your own.

### YouTube (optional)

Enable YouTube Data API v3 in Google Cloud and enter an API key. YouTube search consumes API quota. The integration uses `search.list` and `videos.list` to retrieve the actual view counts.

## Releases

`manifest.json` carries the version. Update it, then run **Actions → Release** with the matching version. The workflow creates a `vX.Y.Z` GitHub Release for HACS. **Validate** runs HACS, hassfest, Python syntax and JavaScript syntax checks on pushes and pull requests.

## Limitations

- There is no universal view count for recipe websites. Ratings are only shown when the site publishes schema.org Recipe data.
- Some websites block Mealie scraping; an import error leaves the source untouched.
- No search provider credentials are bundled with this repository. YouTube search uses 100 units of the default 10,000 daily API quota per search.
- Tested structurally; live search/import requires the user's API keys and Mealie instance.

## License

MIT. See [LICENSE](LICENSE).
