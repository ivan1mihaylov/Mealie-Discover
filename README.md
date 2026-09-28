# Mealie Discover

Find recipes from the Home Assistant sidebar and import a selected URL into Mealie. This is a HACS custom integration; it does not modify Mealie's UI or database.

## What it shows

- **Recipe websites:** results from Google Programmable Search. Where Google exposes structured rating metadata, the rating and count are shown. Search position is **not** a view count.
- **YouTube:** videos sorted by actual YouTube view counts, with likes when available. Video import may require Mealie's AI import feature and is not guaranteed to work with every video.
- **Add to Mealie:** sends the selected URL to Mealie's `POST /api/recipes/create/url` API. The source must be supported by Mealie's scraper.

Search is on demand. API keys and the Mealie token stay in Home Assistant's config entry and are not sent to the browser.

## Install from HACS

1. HACS → three-dot menu → **Custom repositories** → add `https://github.com/ivan1mihaylov/Mealie-Discover` as **Integration**.
2. Install Mealie Discover, then restart Home Assistant.
3. Settings → Devices & services → Add integration → **Mealie Discover**.
4. Supply the Mealie URL and a Mealie API token, plus at least one search provider below.
5. Open **Mealie Discover** from the Home Assistant sidebar.

### Mealie connection

Create a long-lived API token in your Mealie user profile. Enter a URL reachable **from Home Assistant Core**, for example `http://<mealie-host>:9000`. If Mealie is a Home Assistant app/add-on, use its internal address and port if it exposes one; its sidebar ingress URL may not be suitable for direct API access. The “Open recipe” link also uses this configured URL, so use a URL reachable by your browser if possible. Avoid putting the token in the URL.

### Recipe websites (optional)

Create a Google Programmable Search Engine that searches the web and enable the Custom Search JSON API in Google Cloud. Enter its **API key** and **Search engine ID (cx)** together. The engine's scope and API quota determine the available results. A Bulgarian search term works; the integration adds “рецепта” and prefers Bulgarian results.

### YouTube (optional)

Enable YouTube Data API v3 in Google Cloud and enter an API key. This can be a different key from Custom Search. YouTube search consumes API quota. The integration uses `search.list` and `videos.list` to retrieve the actual view counts.

## Releases

`manifest.json` carries the version. Update it, then run **Actions → Release** with the matching version. The workflow creates a `vX.Y.Z` GitHub Release for HACS. **Validate** runs HACS, hassfest, Python syntax and JavaScript syntax checks on pushes and pull requests.

## Limitations

- There is no universal view count for recipe websites. Ratings are only shown when Google returns structured metadata.
- Some websites block Mealie scraping; an import error leaves the source untouched.
- No search provider credentials are bundled with this repository. Google may apply usage limits or charges according to your account and plan.
- Tested structurally; live search/import requires the user's API keys and Mealie instance.

## License

MIT. See [LICENSE](LICENSE).
