const ICONS = {
  search: "M9.5 3A6.5 6.5 0 0 1 16 9.5c0 1.61-.59 3.09-1.56 4.23l.27.27h.79l5 5-1.5 1.5-5-5v-.79l-.27-.27A6.52 6.52 0 0 1 9.5 16 6.5 6.5 0 0 1 3 9.5 6.5 6.5 0 0 1 9.5 3m0 2C7 5 5 7 5 9.5S7 14 9.5 14 14 12 14 9.5 12 5 9.5 5Z",
  star: "M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27Z",
  clock: "M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16m0-18a10 10 0 1 1 0 20 10 10 0 0 1 0-20m.5 5v5.25l4.5 2.67-.75 1.23L11 13V7h1.5Z",
  eye: "M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6m0 8a5 5 0 1 1 0-10 5 5 0 0 1 0 10m0-12.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5Z",
  thumb: "M23 10a2 2 0 0 0-2-2h-6.32l.96-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.58C7.22 7.95 7 8.45 7 9v10a2 2 0 0 0 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2M1 21h4V9H1v12Z",
  plus: "M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2Z",
  check: "M21 7 9 19l-5.5-5.5 1.41-1.41L9 16.17 19.59 5.59 21 7Z",
  open: "M14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7m5 16H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7h-2v7Z",
  back: "M20 11v2H8l5.5 5.5-1.42 1.42L4.16 12l7.92-7.92L13.5 5.5 8 11h12Z",
  web: "M16.36 14c.08-.66.14-1.32.14-2 0-.68-.06-1.34-.14-2h3.38c.16.64.26 1.31.26 2s-.1 1.36-.26 2m-5.15 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95a8.03 8.03 0 0 1-4.33 3.56M14.34 14H9.66c-.1-.66-.16-1.32-.16-2 0-.68.06-1.35.16-2h4.68c.09.65.16 1.32.16 2 0 .68-.07 1.34-.16 2M12 19.96c-.83-1.2-1.5-2.53-1.91-3.96h3.82c-.41 1.43-1.08 2.76-1.91 3.96M8 8H5.08A7.92 7.92 0 0 1 9.4 4.44C8.8 5.55 8.35 6.75 8 8m-2.92 8H8c.35 1.25.8 2.45 1.4 3.56A8 8 0 0 1 5.08 16m-.82-2C4.1 13.36 4 12.69 4 12s.1-1.36.26-2h3.38c-.08.66-.14 1.32-.14 2 0 .68.06 1.34.14 2M12 4.03c.83 1.2 1.5 2.54 1.91 3.97h-3.82c.41-1.43 1.08-2.77 1.91-3.97M18.92 8h-2.95a15.65 15.65 0 0 0-1.38-3.56c1.84.63 3.37 1.9 4.33 3.56M12 2C6.47 2 2 6.5 2 12a10 10 0 0 0 10 10 10 10 0 0 0 10-10A10 10 0 0 0 12 2Z",
  video: "M10 15l5.19-3L10 9v6m11.56-7.83c.13.47.22 1.1.28 1.9.07.8.1 1.49.1 2.09L22 12c0 2.19-.16 3.8-.44 4.83-.25.9-.83 1.48-1.73 1.73-.47.13-1.33.22-2.65.28-1.3.07-2.49.1-3.59.1L12 19c-4.19 0-6.8-.16-7.83-.44-.9-.25-1.48-.83-1.73-1.73-.13-.47-.22-1.1-.28-1.9-.07-.8-.1-1.49-.1-2.09L2 12c0-2.19.16-3.8.44-4.83.25-.9.83-1.48 1.73-1.73.47-.13 1.33-.22 2.65-.28 1.3-.07 2.49-.1 3.59-.1L12 5c4.19 0 6.8.16 7.83.44.9.25 1.48.83 1.73 1.73Z",
};
const SUGGESTIONS = ["Боб чорба", "Мусака", "Леща яхния", "Баница", "Таратор", "Pancakes"];
const LANGUAGES = [["all", "Всички езици"], ["bg", "Български"], ["en", "English"]];
const PROVIDERS = { web: ["web", "Сайтове"], youtube: ["video", "YouTube"] };

function icon(name, size = 18) {
  return `<svg viewBox="0 0 24 24" width="${size}" height="${size}" aria-hidden="true"><path fill="currentColor" d="${ICONS[name]}"/></svg>`;
}

function element(tag, className, html) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (html !== undefined) node.innerHTML = html;
  return node;
}

// Search result titles often end with " - Рецепта | Site"; the source is shown separately.
function cleanTitle(title) {
  let text = String(title || "").trim();
  const bar = text.lastIndexOf(" | ");
  if (bar > 10) text = text.slice(0, bar);
  return text.replace(/\s+[-–—]\s+(рецепта|recipe)\s*$/i, "").trim() || String(title || "");
}

function storage(key, value) {
  try {
    if (value === undefined) return localStorage.getItem(key);
    localStorage.setItem(key, value);
  } catch (error) { /* storage unavailable */ }
  return null;
}

class MealieDiscoverPanel extends HTMLElement {
  set hass(value) {
    this._hass = value;
    if (this._menu) this._menu.hass = value;
    if (!this._mounted) this._mount();
  }

  set narrow(value) {
    this._narrow = value;
    if (this._menu) this._menu.narrow = value;
  }

  disconnectedCallback() {
    clearInterval(this._keepAlive);
  }

  async _mount() {
    this._mounted = true;
    this._language = storage("mealie-discover-language") || "all";
    this._provider = storage("mealie-discover-provider");
    const root = this.attachShadow({ mode: "open" });
    root.innerHTML = `
      <style>
        :host {
          --md-accent: var(--primary-color, #03a9f4);
          --md-card: var(--card-background-color, #fff);
          --md-surface: var(--secondary-background-color, #f3f3f3);
          --md-text: var(--primary-text-color, #212121);
          --md-muted: var(--secondary-text-color, #727272);
          --md-line: var(--divider-color, rgba(0,0,0,.12));
          --md-success: var(--success-color, #43a047);
          display:block; min-height:100%; color:var(--md-text); background:var(--primary-background-color);
          font-family:var(--ha-font-family-body, var(--paper-font-body1_-_font-family, Roboto, system-ui, sans-serif));
          -webkit-tap-highlight-color:transparent;
        }
        * { box-sizing:border-box }
        [hidden] { display:none !important }
        button { font:inherit; cursor:pointer; border:0; background:none; color:inherit }
        svg { flex:none; display:block }
        .toolbar { display:flex; align-items:center; height:var(--header-height, 56px); padding:0 12px; gap:8px;
          background:var(--app-header-background-color, var(--md-accent)); color:var(--app-header-text-color, #fff);
          border-bottom:var(--app-header-border-bottom, none); font-size:20px }
        main { max-width:1180px; margin:0 auto; padding:20px 16px 96px }
        .hero { padding:12px 0 18px }
        .hero h1 { font-size:clamp(24px, 5vw, 32px); line-height:1.15; margin:0 0 6px; letter-spacing:-.01em }
        .hero p { margin:0; color:var(--md-muted); font-size:15px }
        .hero.compact h1, .hero.compact p { display:none }
        .hero.compact .searchbar { margin-top:0 }
        .searchbar { position:relative; display:flex; align-items:center; margin-top:18px; background:var(--md-card);
          border:1px solid var(--md-line); border-radius:28px; padding:6px 6px 6px 18px; gap:10px;
          box-shadow:0 6px 24px rgba(0,0,0,.08); transition:border-color .2s, box-shadow .2s }
        .searchbar:focus-within { border-color:var(--md-accent); box-shadow:0 0 0 3px color-mix(in srgb, var(--md-accent) 25%, transparent) }
        .searchbar > svg { color:var(--md-muted) }
        .searchbar input { flex:1; min-width:0; border:0; outline:0; background:none; color:var(--md-text); font:inherit; font-size:17px; padding:10px 0 }
        .searchbar input::placeholder { color:var(--md-muted) }
        .go { display:flex; align-items:center; gap:6px; background:var(--md-accent); color:var(--text-primary-color, #fff);
          border-radius:22px; padding:11px 18px; font-weight:500; transition:transform .1s, opacity .2s }
        .go:active { transform:scale(.97) }
        .go:disabled { opacity:.6; cursor:wait }
        .filters { display:flex; flex-wrap:wrap; gap:8px; margin-top:14px }
        .group { display:flex; gap:6px; flex-wrap:wrap }
        .group + .group { padding-left:8px; border-left:1px solid var(--md-line) }
        .chip { display:inline-flex; align-items:center; gap:6px; padding:7px 14px; border-radius:18px; font-size:14px;
          background:var(--md-surface); color:var(--md-text); border:1px solid transparent; transition:background .2s, color .2s }
        .chip[aria-pressed="true"] { background:color-mix(in srgb, var(--md-accent) 18%, transparent); color:var(--md-accent);
          border-color:color-mix(in srgb, var(--md-accent) 45%, transparent); font-weight:500 }
        .summary { margin:22px 2px 12px; color:var(--md-muted); font-size:14px; min-height:18px }
        .grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:18px }
        article { position:relative; display:flex; flex-direction:column; background:var(--md-card); border-radius:20px; overflow:hidden;
          border:1px solid var(--md-line); box-shadow:0 2px 10px rgba(0,0,0,.06); transition:transform .2s, box-shadow .2s;
          animation:rise .35s ease both }
        @media (hover:hover) { article:hover { transform:translateY(-3px); box-shadow:0 12px 30px rgba(0,0,0,.14) } }
        @keyframes rise { from { opacity:0; transform:translateY(8px) } }
        .media { position:relative; aspect-ratio:16/10; background:linear-gradient(135deg, var(--md-surface), color-mix(in srgb, var(--md-accent) 20%, var(--md-surface))) }
        .media img { width:100%; height:100%; object-fit:cover; display:block }
        .media .placeholder { position:absolute; inset:0; display:grid; place-items:center; font-size:48px; opacity:.6 }
        .badges { position:absolute; left:10px; right:10px; bottom:10px; display:flex; flex-wrap:wrap; gap:6px }
        .badge { display:inline-flex; align-items:center; gap:4px; padding:4px 9px; border-radius:12px; font-size:13px; font-weight:500;
          color:#fff; background:rgba(0,0,0,.58); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px) }
        .badge.star svg { color:#ffc107 }
        .body { display:flex; flex-direction:column; gap:8px; padding:14px 16px 16px; flex:1 }
        .source { display:flex; align-items:center; gap:6px; color:var(--md-muted); font-size:13px; overflow:hidden; white-space:nowrap }
        .source img { width:16px; height:16px; border-radius:4px }
        .source span { overflow:hidden; text-overflow:ellipsis }
        h2 { margin:0; font-size:17px; line-height:1.35; font-weight:600; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden }
        .note { font-size:12.5px; color:var(--md-muted); display:flex; gap:6px; align-items:flex-start }
        .note::before { content:"ⓘ" }
        .actions { display:flex; gap:8px; margin-top:auto; padding-top:6px }
        .primary { flex:1; display:flex; align-items:center; justify-content:center; gap:8px; padding:11px 14px; border-radius:14px;
          font-weight:500; background:var(--md-accent); color:var(--text-primary-color, #fff); transition:background .2s, transform .1s }
        .primary:active { transform:scale(.98) }
        .primary:disabled { cursor:wait; opacity:.75 }
        .primary.done { background:var(--md-success) }
        .icon-btn { display:grid; place-items:center; width:44px; border-radius:14px; background:var(--md-surface); color:var(--md-text); text-decoration:none }
        .spinner { width:16px; height:16px; border-radius:50%; border:2px solid currentColor; border-right-color:transparent; animation:spin .8s linear infinite }
        @keyframes spin { to { transform:rotate(360deg) } }
        .skeleton .media, .skeleton .line { background:linear-gradient(90deg, var(--md-surface) 25%, color-mix(in srgb, var(--md-text) 8%, var(--md-surface)) 50%, var(--md-surface) 75%);
          background-size:200% 100%; animation:shimmer 1.2s infinite linear }
        .skeleton .line { height:14px; border-radius:7px }
        @keyframes shimmer { to { background-position:-200% 0 } }
        .empty { text-align:center; padding:48px 16px; color:var(--md-muted) }
        .empty .big { font-size:56px; margin-bottom:8px }
        .empty h3 { margin:0 0 6px; color:var(--md-text); font-size:19px }
        .empty .group { justify-content:center; margin-top:16px }
        .toast { position:fixed; left:50%; bottom:24px; transform:translate(-50%, 20px); max-width:min(560px, calc(100% - 32px));
          padding:12px 18px; border-radius:14px; background:var(--md-text); color:var(--primary-background-color, #fff);
          box-shadow:0 10px 30px rgba(0,0,0,.25); font-size:14px; line-height:1.4; opacity:0; pointer-events:none; transition:opacity .25s, transform .25s; z-index:10 }
        .toast.show { opacity:1; transform:translate(-50%, 0) }
        #viewer { display:flex; flex-direction:column; height:calc(100vh - var(--header-height, 56px)) }
        .viewer-bar { display:flex; gap:8px; padding:8px 12px; background:var(--md-card); border-bottom:1px solid var(--md-line) }
        .viewer-bar .grow { flex:1 }
        .viewer-bar button { display:flex; align-items:center; gap:6px; padding:8px 14px; border-radius:18px; background:var(--md-surface) }
        .viewer-bar .accent { background:var(--md-accent); color:var(--text-primary-color, #fff) }
        #frame { flex:1; width:100%; border:0; background:var(--primary-background-color) }
        @media (max-width:600px) {
          main { padding:12px 12px 96px }
          .grid { grid-template-columns:1fr; gap:14px }
          .group + .group { padding-left:0; border-left:0 }
        }
      </style>
      <div class="toolbar"><ha-menu-button></ha-menu-button><div>Mealie Discover</div></div>
      <main>
        <section class="hero">
          <h1>Какво ще готвим днес?</h1>
          <p>Намери популярни рецепти и ги добави в Mealie с едно докосване.</p>
          <form id="form" class="searchbar" role="search">
            ${icon("search", 22)}
            <input id="query" type="search" enterkeyhint="search" autocomplete="off" placeholder="Боб, мусака, баница…" required minlength="2" maxlength="120" />
            <button id="submit" class="go" type="submit">${icon("search")}<span>Търси</span></button>
          </form>
          <div class="filters"><div class="group" id="providers"></div><div class="group" id="languages"></div></div>
        </section>
        <div class="summary" id="summary" role="status"></div>
        <div class="grid" id="results"></div>
        <div class="empty" id="empty">
          <div class="big">🍲</div>
          <h3>Потърси любимо ястие</h3>
          <div>При сайтовете най-отгоре са рецептите с най-много оценки, а при YouTube – най-гледаните.</div>
          <div class="group" id="suggestions"></div>
        </div>
      </main>
      <section id="viewer" hidden>
        <div class="viewer-bar">
          <button id="back" type="button">${icon("back")}Назад</button><span class="grow"></span>
          <button id="open-mealie" class="accent" type="button">${icon("open")}Отвори Mealie</button>
        </div>
        <iframe id="frame" title="Mealie"></iframe>
      </section>
      <div class="toast" id="toast" role="alert"></div>`;
    this.root = root;
    this._menu = root.querySelector("ha-menu-button");
    this._menu.hass = this._hass;
    this._menu.narrow = this._narrow;

    this._renderChips("#languages", LANGUAGES, () => this._language, (value) => {
      this._language = value;
      storage("mealie-discover-language", value);
    });
    const suggestions = root.querySelector("#suggestions");
    for (const text of SUGGESTIONS) {
      const chip = element("button", "chip", "");
      chip.type = "button";
      chip.textContent = text;
      chip.addEventListener("click", () => { root.querySelector("#query").value = text; this._search(); });
      suggestions.append(chip);
    }
    root.querySelector("#form").addEventListener("submit", (event) => { event.preventDefault(); this._search(); });
    root.querySelector("#back").addEventListener("click", () => this._closeRecipe());
    root.querySelector("#open-mealie").addEventListener("click", () => {
      this._closeRecipe();
      this._navigate(`/${this._mealiePanel.slug}`);
    });

    try {
      const state = await this._hass.callWS({ type: "mealie_discover/state" });
      this._mealiePanel = state.mealie_panel;
      if (!state.providers.includes(this._provider)) this._provider = state.providers[0];
      this._renderChips("#providers", state.providers.map((name) => [name, ...PROVIDERS[name]]), () => this._provider, (value) => {
        this._provider = value;
        storage("mealie-discover-provider", value);
      });
      if (!state.providers.length) this._toast("Настрой SearXNG или YouTube в настройките на интеграцията.");
    } catch (error) { this._toast(this._error(error)); }
  }

  _renderChips(selector, options, current, select) {
    const group = this.root.querySelector(selector);
    group.replaceChildren();
    for (const [value, first, second] of options) {
      const chip = element("button", "chip", second ? `${icon(first, 16)}${second}` : "");
      if (!second) chip.textContent = first;
      chip.type = "button";
      chip.setAttribute("aria-pressed", String(value === current()));
      chip.addEventListener("click", () => {
        select(value);
        for (const other of group.children) other.setAttribute("aria-pressed", String(other === chip));
      });
      group.append(chip);
    }
  }

  _navigate(path) {
    history.pushState(null, "", path);
    window.dispatchEvent(new CustomEvent("location-changed", { detail: { replace: false } }));
  }

  // Same session the add-on panels use, so Mealie opens inside Home Assistant.
  async _ingressSession() {
    const { session } = await this._hass.callWS({ type: "supervisor/api", endpoint: "/ingress/session", method: "post" });
    document.cookie = `ingress_session=${session};path=/api/hassio_ingress/;SameSite=Strict${location.protocol === "https:" ? ";Secure" : ""}`;
    this._session = session;
  }

  async _openRecipe(result) {
    try {
      await this._ingressSession();
    } catch (error) {
      // Only administrators may open add-on sessions; fall back to a browser tab.
      window.open(result.url, "_blank", "noopener");
      return;
    }
    clearInterval(this._keepAlive);
    this._keepAlive = setInterval(async () => {
      try {
        await this._hass.callWS({ type: "supervisor/api", endpoint: "/ingress/validate_session", method: "post", data: { session: this._session } });
      } catch (error) {
        try { await this._ingressSession(); } catch (retryError) { /* shown by Mealie on next request */ }
      }
    }, 60000);
    this.root.querySelector("#frame").src = this._mealiePanel.ingress_url.replace(/\/$/, "") + result.path;
    this.root.querySelector("main").hidden = true;
    this.root.querySelector("#viewer").hidden = false;
  }

  _closeRecipe() {
    clearInterval(this._keepAlive);
    this.root.querySelector("#frame").src = "about:blank";
    this.root.querySelector("#viewer").hidden = true;
    this.root.querySelector("main").hidden = false;
  }

  _error(error) { return error?.message || "Възникна грешка. Провери настройките и логовете на Home Assistant."; }

  _toast(message, duration = 5000) {
    const toast = this.root.querySelector("#toast");
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => toast.classList.remove("show"), duration);
  }

  async _search() {
    const query = this.root.querySelector("#query").value.trim();
    if (query.length < 2 || !this._provider) return;
    const button = this.root.querySelector("#submit");
    const grid = this.root.querySelector("#results");
    const summary = this.root.querySelector("#summary");
    this.root.querySelector("#query").blur();
    this.root.querySelector("#empty").hidden = true;
    this.root.querySelector(".hero").classList.add("compact");
    button.disabled = true;
    summary.textContent = "Търся рецепти…";
    grid.replaceChildren(...Array.from({ length: 6 }, () => this._skeleton()));
    try {
      const results = await this._hass.callWS({
        type: "mealie_discover/search", query, provider: this._provider, language: this._language,
      });
      summary.textContent = results.length ? `${results.length} резултата за „${query}“` : `Няма резултати за „${query}“. Опитай с друга дума или език.`;
      grid.replaceChildren(...results.map((recipe, index) => this._card(recipe, index)));
    } catch (error) {
      summary.textContent = "";
      grid.replaceChildren();
      this._toast(this._error(error));
    } finally { button.disabled = false; }
  }

  _skeleton() {
    const card = element("article", "skeleton", `<div class="media"></div><div class="body">
      <div class="line" style="width:40%"></div><div class="line" style="width:90%"></div><div class="line" style="width:70%"></div></div>`);
    card.setAttribute("aria-hidden", "true");
    return card;
  }

  _card(recipe, index) {
    const compact = new Intl.NumberFormat("bg-BG", { notation: "compact", maximumFractionDigits: 1 });
    const decimal = new Intl.NumberFormat("bg-BG", { maximumFractionDigits: 1 });
    const card = element("article");
    card.style.animationDelay = `${Math.min(index, 8) * 40}ms`;

    const media = element("div", "media");
    media.append(element("div", "placeholder", recipe.provider === "youtube" ? "🎬" : "🍽️"));
    if (/^https:\/\//.test(recipe.image || "")) {
      const image = element("img");
      image.src = recipe.image;
      image.alt = "";
      image.loading = "lazy";
      image.addEventListener("error", () => image.remove());
      media.append(image);
    }
    const badges = element("div", "badges");
    const badge = (name, text, extra = "") => {
      const node = element("span", `badge ${extra}`, icon(name, 14));
      node.append(text);
      badges.append(node);
    };
    if (recipe.rating) badge("star", `${decimal.format(recipe.rating)}${recipe.rating_count ? ` · ${compact.format(recipe.rating_count)}` : ""}`, "star");
    if (recipe.total_minutes) badge("clock", `${recipe.total_minutes} мин`);
    if (recipe.views) badge("eye", compact.format(recipe.views));
    if (recipe.likes) badge("thumb", compact.format(recipe.likes));
    media.append(badges);
    card.append(media);

    const body = element("div", "body");
    const source = element("div", "source");
    if (recipe.provider === "web" && recipe.source) {
      const favicon = element("img");
      favicon.src = `https://${recipe.source}/favicon.ico`;
      favicon.alt = "";
      favicon.addEventListener("error", () => favicon.replaceWith(element("span", "", icon("web", 16))));
      source.append(favicon);
    } else {
      source.append(element("span", "", icon(recipe.provider === "youtube" ? "video" : "web", 16)));
    }
    const sourceName = element("span");
    sourceName.textContent = String(recipe.source || "").replace(/^www\./, "");
    source.append(sourceName);
    const title = element("h2");
    title.textContent = cleanTitle(recipe.title);
    title.title = recipe.title || "";
    body.append(source, title);

    const warning = recipe.provider === "youtube"
      ? "Импортът на видео изисква AI в Mealie."
      : recipe.is_recipe ? "" : "Страницата няма структурирана рецепта – импортът може да не успее.";
    if (warning) {
      const note = element("div", "note");
      note.append(warning);
      body.append(note);
    }

    const actions = element("div", "actions");
    const add = element("button", "primary", `${icon("plus")}<span>Добави в Mealie</span>`);
    add.type = "button";
    const preview = element("a", "icon-btn", icon("open"));
    preview.href = recipe.url;
    preview.target = "_blank";
    preview.rel = "noopener noreferrer";
    preview.title = "Виж оригинала";
    preview.setAttribute("aria-label", "Виж оригинала");
    add.addEventListener("click", async () => {
      if (add._result) {
        if (this._mealiePanel) this._openRecipe(add._result);
        else window.open(add._result.url, "_blank", "noopener");
        return;
      }
      add.disabled = true;
      add.innerHTML = `<span class="spinner"></span><span>Импортиране…</span>`;
      try {
        const result = await this._hass.callWS({ type: "mealie_discover/import", url: recipe.url });
        add._result = result;
        add.classList.add("done");
        add.innerHTML = `${icon("check")}<span>Отвори в Mealie</span>`;
        this._toast(result.total
          ? `Добавена в Mealie ✓ Свързани съставки: ${result.linked} от ${result.total}.`
          : "Добавена в Mealie ✓");
      } catch (error) {
        add.innerHTML = `${icon("plus")}<span>Добави в Mealie</span>`;
        this._toast(this._error(error), 8000);
      } finally { add.disabled = false; }
    });
    actions.append(add, preview);
    body.append(actions);
    card.append(body);
    return card;
  }
}
customElements.define("mealie-discover-panel", MealieDiscoverPanel);
