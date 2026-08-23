# Start here (no coder required)

You're getting a **front desk** for your AI providers. One address that stands
between you and OpenRouter, Gemini, DashScope, bynara, and any provider you
sign up for next. It does three things:

1. Holds all your provider keys in one place.
2. Gives you a **budget card** per project, so no project can overspend.
3. Keeps a **receipt** for every single request.

The page you'll do all your work in: **http://localhost:4000/ui**

---

## Step 1 — Turn it on (you do this once)

1. Double-click **`setup.cmd`** (it's in this folder).
2. A black window opens and does the work by itself. It might take a few
   minutes the first time.
3. Your web browser opens the dashboard page for you. That page is where you
   live from now on.

The black window will also tell you your **username and password** for that
page. Write them down. (Username is always `admin`. The password is the long
`sk-...` thing — that's your master key.)

---

## Step 2 — The one idea you actually need

There are **two kinds of keys**. That's the whole secret.

- **Provider keys** = your credit cards. Each provider gave you one when you
  signed up (OpenRouter key, Gemini key, etc.). You enter them once and never
  look at them again. We already made space for them in the `.env` file.
- **Virtual keys** = budget cards. You make one of these for each app or test,
  with a dollar limit on it. Hand *these* out, never your credit cards.

If a budget card runs out of money, it just **stops working** — politely, with
a "no more budget" error. Nothing can silently eat your balance ever again.

---

## Step 3 — Everyday stuff

**"I want to see where my money went."**
Log into the dashboard page → click **Logs** (left menu, under Observability).
That's every receipt.
There's also a way to see it without the page: double-click **`keys.cmd`** and
type `list`.

**"I want to give a new project $5."**
Double-click **`keys.cmd`** and type:

```
create myproject 5
```

(Change `myproject` and `5` to whatever you want.) It gives you a card number
— copy it and paste it into the app. That's it. The card is good for $5 and
no more, forever.

**"That thing is spending too fast. Stop it."**
Double-click **`keys.cmd`** and type:

```
block sk-the-card-number
```

The card is dead instantly. You can also just delete it.

---

## Step 4 — When you sign up for a new provider

1. Sign up, get your key. Note any free credit they gave you.
2. Add the key to the `.env` file (open it in Notepad, add the line, save).
3. Restart: double-click **`setup.cmd`** again.
4. Write it in the **`providers.md`** file — that's your ledger: which
   providers you have, their budgets, and how much free credit is still
   sitting there waiting to be used up on purpose.

---

## Your first five minutes on the dashboard page

The page has a menu down the left side. You only ever need **four** items from
it: **Virtual Keys**, **Playground**, **Models + Endpoints**, and **Logs**.
That's the whole app. (Labels checked against LiteLLM v1.97.0.)

**Minute 1 — get in.**
Double-click `setup.cmd` if you haven't. Your browser opens the page and asks
for a login. Username: `admin`. Password: the long `sk-...` thing the black
window printed (it's also in the `.env` file, on the `LITELLM_MASTER_KEY` line).

**Minute 2 — look at your providers.**
Click **Models + Endpoints** in the left menu. You should already see your
four providers (openrouter, gemini, dashscope, bynara) — they came pre-loaded,
no work needed.

**When you sign up for a NEW provider later**, this is where you add it:

1. Click **Models + Endpoints**, then the **Add Model** tab at the top.
2. Give it a name (the provider's name, e.g. `myprovider/gpt-4o`).
3. In the API key field, paste the key the provider gave you.
   (If you put the key in `.env` instead, type `os.environ/NAME` in that field.)
4. Weird provider that isn't standard? There's a field for its web address
   (base URL) — that's where `BYNARA_API_BASE` goes.
5. Save. It exists forever now, even after restarts.

**Minute 3 — make your first budget card.**

1. Click **Virtual Keys** in the left menu.
2. Click the **+ Create New Key** button (top right).
3. Give it a name (e.g. `test`).
4. Set the **budget**: type `5` (that's $5).
5. Leave models empty (= allowed to use everything), click create.
6. It shows you the card number **once** — a long `sk-...` string. Copy it.
   You can't see it again later, so this is the moment.

The card now sits in the **Virtual Keys** list with its budget, spend ($0.00),
and what's left ($5.00). Hand this number to apps — never your own keys.

**Minute 4 — see it actually work.**
Click **Playground** in the left menu, pick a model from the dropdown, type
`hi`, hit send. It goes through your front desk: one request, one receipt.

**Minute 5 — see the receipt.**
Click **Logs** in the left menu (under Observability). That request is there
with its cost (a fraction of a cent). This is where "where did my money go"
gets answered forever.

**The whole app in one line:** Models + Endpoints = add providers, Virtual
Keys = make budget cards, Logs = receipts, Playground = try stuff. Four menu
items, nothing else.

Button names can differ slightly between LiteLLM versions. If something in
this list isn't where I said, tell me what you see instead and I'll adjust.

---

## If something goes wrong

- Black window says Docker isn't running → open **Docker Desktop**, wait until
  it says it's running, then double-click `setup.cmd` again.
- Page won't load → same fix, plus be patient: the first start downloads a
  lot.
- Anything else, or any red text in the black window → copy it and send it.
  That's what I'm for.
