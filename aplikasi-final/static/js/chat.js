// =====================================================================
// Logika antarmuka chat: kirim pesan ke /api/chat dengan fetch()
// lalu tampilkan balasan tanpa memuat ulang halaman.
// =====================================================================
const messagesEl = document.getElementById("messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const btnClear = document.getElementById("btn-clear");
const learnMode = document.getElementById("learn-mode");

/** Tambahkan satu gelembung pesan ke layar. */
function addMessage(sender, text, meta) {
  const row = document.createElement("div");
  row.className = `msg msg-${sender}`;

  if (sender === "bot") {
    const avatar = document.createElement("span");
    avatar.className = "msg-avatar";
    avatar.textContent = THEME.avatar;
    row.appendChild(avatar);
  }

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;            // textContent, BUKAN innerHTML -> aman dari XSS

  if (meta) {
    const small = document.createElement("small");
    small.className = "meta";
    small.textContent = meta;
    bubble.appendChild(small);
  }

  row.appendChild(bubble);
  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return bubble;
}

/** Tampilkan indikator mengetik dengan tiga titik animasi. */
function addTyping() {
  const row = document.createElement("div");
  row.className = "msg msg-bot typing-row";
  const avatar = document.createElement("span");
  avatar.className = "msg-avatar";
  avatar.textContent = THEME.avatar;
  const bubble = document.createElement("div");
  bubble.className = "bubble typing-bubble";
  bubble.setAttribute("aria-label", "WargaBot sedang mengetik");
  for (let i = 0; i < 3; i += 1) {
    const dot = document.createElement("span");
    dot.className = "typing-dot";
    bubble.appendChild(dot);
  }
  row.append(avatar, bubble);
  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return row;
}

/** Intent berkonteks: tombol pertanyaan lanjutan di bawah jawaban bot. */
function clearNext() {
  document.querySelectorAll(".next-chips").forEach((el) => el.remove());
}

function addNext(items) {
  const wrap = document.createElement("div");
  wrap.className = "next-chips";
  items.forEach((text) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chip";
    btn.textContent = text;             // textContent -> aman dari XSS
    btn.addEventListener("click", () => sendMessage(text));
    wrap.appendChild(btn);
  });
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

/** Mode belajar: tampilkan 3 kandidat intent teratas di bawah jawaban. */
async function showCandidates(bubble, text) {
  const res = await fetch("/api/explain", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text, theme: THEME.id }),
  });
  const data = await res.json();
  const list = document.createElement("ol");
  list.className = "candidates";
  data.candidates.forEach((c) => {
    const li = document.createElement("li");
    const lolos = c.score >= data.threshold ? "lolos ambang" : "di bawah ambang";
    li.textContent = `${c.intent} · ${c.score.toFixed(2)} (${lolos}) — pola “${c.pattern}”`;
    list.appendChild(li);
  });
  bubble.appendChild(list);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

/** Kirim pesan ke server. */
async function sendMessage(text) {
  clearNext();                            // hapus tombol lanjutan lama
  addMessage("user", text);
  const typing = addTyping();
  input.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, theme: THEME.id }),
    });
    const data = await res.json();
    typing.remove();

    if (!res.ok) {
      addMessage("bot", `⚠️ ${data.error}`);
      return;
    }
    const meta = data.intent
      ? `intent: ${data.intent} · skor ${data.score.toFixed(2)}`
      : `tidak dikenali · skor ${data.score.toFixed(2)}`;
    const bubble = addMessage("bot", data.reply, meta);
    if (data.next && data.next.length) addNext(data.next);
    if (learnMode.checked) await showCandidates(bubble, text);
  } catch (err) {
    typing.remove();
    addMessage("bot", "⚠️ Gagal terhubung ke server.");
    console.error(err);
  } finally {
    input.disabled = false;
    input.focus();
  }
}

/** Muat riwayat percakapan saat halaman dibuka. */
async function loadHistory() {
  const res = await fetch(`/api/history/${THEME.id}`);
  const rows = await res.json();
  if (rows.length === 0) {
    addMessage("bot", THEME.greeting);
    return;
  }
  rows.forEach((r) => addMessage(r.sender, r.text));
}

// ---- Event listener ------------------------------------------------
form.addEventListener("submit", (e) => {
  e.preventDefault();                     // cegah form memuat ulang halaman
  const text = input.value.trim();
  if (!text) return;                      // pesan kosong diabaikan
  input.value = "";
  sendMessage(text);
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => sendMessage(chip.textContent));
});

btnClear.addEventListener("click", async () => {
  await fetch(`/api/history/${THEME.id}`, { method: "DELETE" });
  messagesEl.innerHTML = "";
  addMessage("bot", THEME.greeting);
});

loadHistory();
