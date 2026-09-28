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
    const root = this.attachShadow({ mode: "open" });
    root.innerHTML = `
      <style>
        :host { display:block; min-height:100%; color:var(--primary-text-color); background:var(--primary-background-color); font-family:var(--paper-font-body1_-_font-family,Arial,sans-serif) }
        .toolbar { display:flex; align-items:center; height:56px; padding:0 12px; background:var(--app-header-background-color,var(--primary-color)); color:var(--app-header-text-color,#fff); font-size:20px }
        .toolbar .title { margin-left:12px }
        main { max-width:1100px; margin:auto; padding:24px 16px 70px }
        .hint { color:var(--secondary-text-color); line-height:1.5; margin:0 0 22px }
        form { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:14px }
        input,select,button { font:inherit; border-radius:10px; padding:12px; border:1px solid var(--divider-color,#ddd) }
        input { flex:1 1 260px; color:var(--primary-text-color); background:var(--card-background-color,#fff) }
        select { color:var(--primary-text-color); background:var(--card-background-color,#fff) }
        button { background:var(--primary-color,#347c62); color:#fff; cursor:pointer; border:0 }
        button:disabled { opacity:.6; cursor:wait }
        a { color:var(--primary-color,#347c62) }
        #status { min-height:24px; margin:10px 0 16px }
        .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:16px }
        article { background:var(--card-background-color,#fff); border:1px solid var(--divider-color,#ddd); border-radius:16px; overflow:hidden; display:flex; flex-direction:column }
        article img { width:100%; aspect-ratio:16/9; object-fit:cover; background:#d8e0d9 }
        .body { padding:16px; display:flex; flex-direction:column; gap:10px; flex:1 }
        h2 { font-size:18px; line-height:1.3; margin:0 }
        .meta { color:var(--secondary-text-color); font-size:14px }
        .actions { display:flex; gap:10px; align-items:center; margin-top:auto }
        .actions button { padding:9px 12px }
        .notice { font-size:13px; color:var(--secondary-text-color) }
        [hidden] { display:none !important }
        #viewer { display:flex; flex-direction:column; height:calc(100vh - 56px) }
        .viewer-bar { display:flex; gap:10px; padding:8px 12px; border-bottom:1px solid var(--divider-color,#ddd) }
        .viewer-bar button { padding:8px 12px }
        .viewer-bar .grow { flex:1 }
        #frame { flex:1; width:100%; border:0; background:var(--primary-background-color) }
      </style>
      <div class="toolbar"><ha-menu-button></ha-menu-button><div class="title">🍲 Mealie Discover</div></div>
      <main>
      <p class="hint">Потърси рецепта онлайн. Гледанията са само за видеоклипове. При сайтовете най-отгоре са рецептите с най-много оценки; оценки има само когато сайтът ги публикува.</p>
      <form id="form"><input id="query" placeholder="Например: боб яхния" required minlength="2" maxlength="120" />
      <select id="provider"></select>
      <select id="language" aria-label="Език"><option value="all">Всички езици</option><option value="bg">Български</option><option value="en">English</option></select><button id="submit" type="submit">Търси</button></form>
      <div id="status" role="status"></div><div class="grid" id="results"></div></main>
      <section id="viewer" hidden><div class="viewer-bar"><button id="back" type="button">← Назад към търсенето</button><span class="grow"></span>
      <button id="open-mealie" type="button">Отвори Mealie</button></div><iframe id="frame" title="Mealie"></iframe></section>`;
    this.root = root;
    this._menu = root.querySelector("ha-menu-button");
    this._menu.hass = this._hass;
    this._menu.narrow = this._narrow;
    const language = root.querySelector("#language");
    try { language.value = localStorage.getItem("mealie-discover-language") || "all"; } catch (error) { /* storage unavailable */ }
    language.addEventListener("change", () => {
      try { localStorage.setItem("mealie-discover-language", language.value); } catch (error) { /* storage unavailable */ }
    });
    root.querySelector("#form").addEventListener("submit", (event) => { event.preventDefault(); this._search(); });
    root.querySelector("#back").addEventListener("click", () => this._closeRecipe());
    root.querySelector("#open-mealie").addEventListener("click", () => {
      this._closeRecipe();
      this._navigate(`/${this._mealiePanel.slug}`);
    });
    try {
      const state = await this._hass.callWS({ type: "mealie_discover/state" });
      this._mealiePanel = state.mealie_panel;
      const select = root.querySelector("#provider");
      for (const name of state.providers) {
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name === "youtube" ? "YouTube · най-гледани" : "Сайтове с рецепти (SearXNG)";
        select.append(option);
      }
      if (!state.providers.length) this._status("Настрой източник за търсене в интеграцията.");
    } catch (error) { this._status(this._error(error)); }
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
  _status(message) { this.root.querySelector("#status").textContent = message; }

  async _search() {
    const button = this.root.querySelector("#submit");
    const grid = this.root.querySelector("#results");
    button.disabled = true;
    grid.replaceChildren();
    this._status("Търся рецепти…");
    try {
      const provider = this.root.querySelector("#provider").value;
      const results = await this._hass.callWS({
        type: "mealie_discover/search",
        query: this.root.querySelector("#query").value.trim(),
        provider,
        language: this.root.querySelector("#language").value,
      });
      this._status(results.length ? `${results.length} резултата` : "Няма намерени резултати.");
      for (const recipe of results) grid.append(this._card(recipe));
    } catch (error) { this._status(this._error(error)); }
    finally { button.disabled = false; }
  }

  _card(recipe) {
    const card = document.createElement("article");
    if (recipe.image && /^https:\/\//.test(recipe.image)) {
      const image = document.createElement("img");
      image.src = recipe.image;
      image.alt = "";
      image.loading = "lazy";
      card.append(image);
    }
    const body = document.createElement("div");
    body.className = "body";
    const title = document.createElement("h2");
    title.textContent = recipe.title;
    body.append(title);
    const meta = document.createElement("div");
    meta.className = "meta";
    const parts = [recipe.source];
    if (recipe.views !== undefined) parts.push(`${new Intl.NumberFormat("bg-BG").format(recipe.views)} гледания`);
    if (recipe.likes) parts.push(`${new Intl.NumberFormat("bg-BG").format(recipe.likes)} харесвания`);
    const number = new Intl.NumberFormat("bg-BG");
    if (recipe.rating) parts.push(`⭐ ${recipe.rating}${recipe.rating_count ? ` (${number.format(recipe.rating_count)} оценки)` : ""}`);
    if (recipe.total_minutes) parts.push(`⏱ ${recipe.total_minutes} мин`);
    meta.textContent = parts.filter(Boolean).join(" · ");
    body.append(meta);
    const actions = document.createElement("div");
    actions.className = "actions";
    const link = document.createElement("a");
    link.href = recipe.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = "Преглед";
    const add = document.createElement("button");
    add.type = "button";
    add.textContent = "+ Добави в Mealie";
    add.addEventListener("click", async () => {
      add.disabled = true;
      this._status("Mealie импортира рецептата…");
      try {
        const result = await this._hass.callWS({ type: "mealie_discover/import", url: recipe.url });
        add.textContent = "Добавена ✓";
        this._status(result.total
          ? `Рецептата е добавена в Mealie. Свързани съставки: ${result.linked} от ${result.total}; останалите са като текст.`
          : "Рецептата е добавена в Mealie.");
        let created;
        if (this._mealiePanel) {
          created = document.createElement("button");
          created.type = "button";
          created.addEventListener("click", () => this._openRecipe(result));
        } else {
          created = document.createElement("a");
          created.href = result.url;
          created.target = "_blank";
          created.rel = "noopener noreferrer";
        }
        created.textContent = "Отвори рецептата";
        actions.append(created);
      } catch (error) { this._status(this._error(error)); add.disabled = false; }
    });
    actions.append(link, add);
    body.append(actions);
    const warning = recipe.provider === "youtube"
      ? "За видео импортът зависи от настройките и версията на Mealie."
      : recipe.is_recipe ? "" : "Страницата няма структурирана рецепта; импортът може да не успее.";
    if (warning) {
      const notice = document.createElement("div");
      notice.className = "notice";
      notice.textContent = warning;
      body.append(notice);
    }
    card.append(body);
    return card;
  }
}
customElements.define("mealie-discover-panel", MealieDiscoverPanel);
