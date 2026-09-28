Search recipe websites through your own SearXNG instance instead of Google Custom Search, which no longer accepts new customers. Replace a Google key with a SearXNG URL via **Reconfigure** after updating.

- Website results show the rating, number of ratings and cooking time from the page's schema.org Recipe data; recipe pages with the most ratings come first.
- On Home Assistant OS, setup detects running SearXNG and Mealie add-ons and fills in their URLs.
- Setup checks the Mealie URL, the token and SearXNG before saving, and a **Reconfigure** option changes them later.
- Mealie's own error message is shown when an import fails.
- “Open recipe” links use your Mealie group instead of assuming `home`.
- Reloading the integration no longer fails; results from several searches or tabs can all be imported.
- The panel has the sidebar menu button on phones, and updates are no longer hidden by the browser cache.
- Search is no longer limited to Bulgarian: the panel has a language filter (all languages, Bulgarian, English), and “рецепта” or “recipe” is added to the query based on its alphabet.
