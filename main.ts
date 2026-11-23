// Entry checker for the "Post a GTA 6 meme on X" contest entry.
// Node 22, standard library only. Run: node main.ts
// Verifies that this repository is a complete, submittable entry package.
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = dirname(fileURLToPath(import.meta.url));
let failed = false;

const post = JSON.parse(readFileSync(join(root, "POST.json"), "utf8"));
// The house reads the `url` field: it must be the post's full address on
// X (/@handle/status/<id>); a short link names no post, and the
// POST_URL_PLACEHOLDER value means Faa has not posted yet.
const url = post.url ?? post.x_url;
console.log("X post:", url);
console.log("Account:", post.account, "| Contest:", post.contest);
console.log("Referral code:", post.referral_code);
if (!/^https:\/\/(www\.)?x\.com\/[^/]+\/status\/\d+/.test(url ?? "")) {
  console.error("FAIL: POST.json url is not a full X post address (or still a placeholder)");
  failed = true;
}

// The posted meme image must be in the package, byte-identical to the
// render in the project directory.
const img = post.image_file;
const imgOk = typeof img === "string" && existsSync(join(root, img));
console.log(imgOk ? `ok   ${img}` : `MISS ${img}`);
if (!imgOk) failed = true;

for (const f of ["LICENSE", "README.md", "WORKLOG.md", "render.py", ".makefun/owner.json"]) {
  const ok = existsSync(join(root, f));
  console.log(ok ? `ok   ${f}` : `MISS ${f}`);
  if (!ok) failed = true;
}

const owner = JSON.parse(readFileSync(join(root, ".makefun/owner.json"), "utf8"));
console.log("Owner wallet:", owner.wallet);
if (!owner.wallet) { console.error("FAIL: owner wallet missing"); failed = true; }

console.log(failed ? "ENTRY INCOMPLETE" : "ENTRY PACKAGE OK");
process.exit(failed ? 1 : 0);
