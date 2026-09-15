# KERIA + Signify: Signing at the Edge — Doctrine Notes

Raw doctrine-mining notes from two source repos:
- **KERIA** (`/home/daniel/code/wot/keria`) — the Python "KERI Agent in the cloud" (multi-tenant cloud agent).
- **signify-ts** (`/home/daniel/code/wot/signify-ts`) — the TypeScript "edge signer" client library.

These are the two halves of the **Signify/KERIA architecture**: a custodial cloud agent that holds *no* private keys, paired with an edge client that holds *only* keys and does *all* signing. Together with keripy (Python reference) and SignifyPy, all four implementations must agree on wire formats.

## Pins and mining status

| Source | Branch | Commit | Date | Status |
|---|---|---|---|---|
| KERIA | `upstream/main` (WebOfTrust/keria) | `7e685edaaeca408919f9adf6789a6626d9c5cf79` | 2026-09-11 | mined 2026-09-15 |
| signify-ts | `upstream/development` (WebOfTrust/signify-ts) | `4c0072f62ede449d44136e8db87972ceb90bc760` | **2024-04-12** | **stale branch — see warning below** |
| signify-ts | `upstream/main` (WebOfTrust/signify-ts) | `ffba8406ef5d0c148decefd6ecfb2f31c480a0ef` | 2026-09-10 | spot-checked 2026-09-15 |

**Mining date: 2026-09-15.** Both sources previously carried `unknown` pins; this pass is the first anchoring, so every `[K]` claim below either gained a commit or is flagged as not re-read. What this pass covered: the KERIA auth path end-to-end (`core/authing.py`), the `endrole`/`locscheme` establishment-event sealing fix, the ESSR tunnel changes, the untargeted-ACDC fix, the custody claims at code level rather than README level, and a set of deliberate negative checks. What it did **not** cover is listed under "Not re-read in the 2026-09 pass".

### WARNING: the signify-ts pin names a branch that has been dormant since April 2024

`4c0072f62` is a real commit and it is genuinely the head of `WebOfTrust/signify-ts`'s `development` branch — but that branch has not moved since **2024-04-12**. The branch the project actually develops on is `main`, at `ffba8406e` (2026-09-10). A pin on `development` is therefore a pin on a two-and-a-half-year-old tree, and any `[K]` claim anchored there is a claim about signify-ts as it stood in April 2024. The manifest field is a reviewed field and this note does not change it; the retarget is proposed in the PR body.

### WARNING: the CESR post-quantum and stream-parser work is NOT upstream signify-ts

Seven commits — `4c9aab4`, `6caf3be`, `ff79077`, `43e1be6`, `b5385b4`, `6e70dd0`, `4ed767b` — sit on the branches `feat/cesr-pq-codes` and `feat/cesr-stream-parser*`. `git branch -a --contains 4ed767b` returns **only** `feat/cesr-pq-codes` and `origin/feat/cesr-pq-codes`, where `origin` is `git@github.com:dhh1128/signify-ts.git`. Every one of the seven is authored by `Daniel Hardman <daniel.hardman@gmail.com>`, and none is contained in any `upstream/*` branch. A search of `upstream/main` for `ML-DSA|MLDSA|FN-DSA|SLH-DSA|Dilithium|Falcon|SPHINCS|Kyber` across `src` returns **nothing**.

So the sentence "signify-ts has implemented the post-quantum codes" is **false** as a statement about the project. What is true is that *an unmerged branch on Daniel's personal fork* has implemented them. These are notes about our own work-in-progress, not evidence about the ecosystem, and the distinction is exactly the kind this corpus exists to keep straight. They are recorded in §10 under a tier marker that says so.

---

## 1. What the KERIA/Signify split fundamentally IS (worldview / design intent)

The central doctrine: **the cloud agent never holds the controller's private keys; the edge signs everything.** This is "signing at the edge."

- KERIA README frames the whole point as key custody: *"This architecture protects the host and the holder private keys. All client tasks/calls are signed 'at the edge', not in the hosted KERIA instance."* (`keria/README.md`, "KERIA Service Architecture"). Therefore *"KERIA relies on the Signify protocol for all calls."*
- signify-ts enumerates the **five functions of a KERI agent** and states exactly which two are split off to the edge (`signify-ts/README.md`, "Signify - KERI Signing at the Edge"):
  1. Key generation
  2. Encrypted key storage
  3. Event generation
  4. Event signing
  5. Event Validation
  > *"Signify-TS splits off two, key generation and event signing into a TypeScript library to provide 'signing at the edge'."*
- The remaining three functions (encrypted key *storage*, event *generation*, event *validation*) live in the cloud agent — but storage is only ever of **encrypted** material the agent can't decrypt.
- Agent role (KERIA README, "Agents"): *"Agents act on behalf of their Signify clients. They don't have the secrets of the client. Instead, they handle all actions for the clients, other than secret/encryption/signing."*
- The private protocol name is **SKRAP** — "Signify/KERIA Request Authentication Protocol" (`keria/docs/protocol.md`, title).

### The two-AID delegation spine
The architecture is built on a **pair of AIDs in a delegation relationship**:
- **Client AID** ("caid") — the controller's own AID, keys derived at the edge from a passcode. It is the *delegator*.
- **Agent AID** — the cloud agent's own AID, created by KERIA as a **delegated** (`dip`) AID whose delegator (`di`) is the Client AID (`keria/docs/protocol.md`, Steps One–Three).
- The Agent AID has its own keys and **signs all responses back to the client** so the client can verify messages genuinely came from its agent (KERIA README, "Agents": *"Agents do have their own keys and do sign all of their messages BACK to the Signify client"*).
- Mutual authentication is thus asymmetric-by-role but symmetric-in-mechanism: **client signs every request with the Client AID; agent signs every response with the Agent AID.**

---

## 2. Security & threat-model positions

### Zero-trust custodian / malicious-host stance
- The cloud agent is treated as **untrusted with secrets**. Even though it is "custodial," it is custodial only of *encrypted* blobs whose decryption keys it never possesses. signify-ts: *"The encrypted private key and salts are then stored on a remote cloud agent that never has access to the decryption keys."* (`signify-ts/README.md`).
- Only **public keys and the blake3 hash of the next keys** are ever made available to the agent in cleartext: *"only the public keys and blake3 hash of the next keys made available to the agent."* (`signify-ts/README.md`).
- Doctrine restated across all "Key Generate Methods" (`keria/docs/protocol.md` §Key Generate Methods): *"the Signify Client creates and signs all KERI events, credentials, etc. ensuring that unencrypted private key material never leaves the client."*

### End-verifiability preserved across the boundary
- Because the edge produces real KEL/TEL events with real signatures, the agent is a *relay and store*, not a trust anchor. Everything the agent emits to the world is edge-signed and independently verifiable — the agent adds no authority of its own to the controller's events.
- The KERI Protocol Interface (http port, default 3902) speaks **CESR-over-HTTP** to the rest of the world and *"allows all KERI clients (not just Signify) to interact in a seamless way"* (KERIA README, "Message Router") — i.e. the agent is a normal KERI participant externally; the Signify split is an internal implementation detail invisible to verifiers.

### Response verification is mandatory (client defends against agent impersonation)
- The client enforces two checks on every response. **Re-anchored 2026-09-15 at `ffba8406e`; both survive, but they MOVED from `clienting.ts` into `authing.ts` during the authenticator refactor (§10a), so the original line hints are dead:**
  1. The `signify-resource` header on the response must equal the known Agent AID, else `throw new Error('message from a different remote agent');` (`signify-ts/src/keri/core/authing.ts:83` — was `clienting.ts:240-244`).
  2. Signature verification of the response, else `throw new Error('response verification failed');` (`authing.ts:93` — was `clienting.ts:246-255`).
  3. **NEW**: a second impersonation guard now exists on the ESSR path — `throw new Error('Message from a different remote agent');` (`authing.ts:331`, note the capitalized `Message`). The check is applied in both transport modes rather than only the signed-header one.
- On connect, the client verifies the delegation binding: the Agent's inception must anchor to the Client AID or it aborts: *"commitment to controller AID missing in agent inception event"* (`clienting.ts:202` at `ffba8406e`; was `clienting.ts:166-170`).

### Pre-rotation as the firewall (post-quantum passcode recovery)
- The passcode-rotation design explicitly invokes pre-rotation as a **post-quantum-secure recovery firewall**: *"To provide post-quantum secure passcode recovery, a passcode recovery must be accompanied by partial rotation of the Client AID."* (`keria/docs/protocol.md` §Partial Client AID Rotation).
- The mechanism: the OLD rotation key (`R0`, regenerated from the old passcode) and a NEW signing key (`S0`, from the new passcode) co-sign a partial rotation; `S0` gets fractional weight `1` (full authority), `R0` gets weight `0` (no authority but proves possession) — a dual-indexed signature satisfies the prior next-key commitment (`protocol.md` §Partial Client AID Rotation, lines 209-250).
- This means recovering/changing a passcode is *cryptographically bound* to demonstrating control of the pre-committed rotation key — you cannot silently swap credentials.

### Aborted-rotation detection & lockout
- KERIA detects an interrupted passcode rotation and **locks out all other operations** until recovery completes: *"the Agent Worker will notify the client ... that a passcode rotation recovery is needed and lock out all other operations until it is completed successfully."* (`protocol.md` §Passcode Rotation Recovery). The old encrypted passcode is the recovery breadcrumb, deleted only on success.

### The signature BINDS a timestamp; nothing ENFORCES freshness (re-confirmed, and now symmetric)

This is the corpus's sharpest negative result — `bible/09 §9` and the bearer-token shibboleth row in `keri-doctrine.md` both rest on it. **Re-checked at `7e685edaa` on 2026-09-15: it still holds, and it is stronger than previously recorded.**

- **[K]** `Signify-Timestamp` is a *covered field* of the signature and nothing more. In `SignedHeaderAuthenticator.inbound` the header is folded into the signed byte string alongside every other covered field — `items.append(f'"{field}": {value}')` (`keria/src/keria/core/authing.py:SignedHeaderAuthenticator.inbound`, L140, at `7e685edaa`) — and is never parsed into a datetime or compared to anything.
- **[K]** The negative is exhaustive, not a sampling. A search of all of `src/keria` at `7e685edaa` for `nowIso8601|fromIso8601|toIso8601|datetime\.now|timedelta|skew` returns no hit inside any inbound authentication path. **`fromIso8601` does not appear in `authing.py` at all.** The only two time calls in the file are outbound stamps: `response.set_header("Signify-Timestamp", helping.nowIso8601())` (`authing.py:180`) and `dt = helping.nowIso8601()` (`authing.py:302`). Every other `timedelta` in the codebase is an agent-cache eviction (`agenting.py:1576`) or a long-running-operation timeout (`longrunning.py:301,573`) — neither is auth.
- **[K]** The ESSR path is the same. `ESSRAuthenticator.inbound` reads the timestamp with `dt = self.getRequiredHeader(request, "SIGNIFY-TIMESTAMP")` (`authing.py:233`) and places it in the signed payload as `dt=dt` (`authing.py:253`). It is verified as *bytes inside a signature* and never as a *time*.
- **[K]** Two further fields that could carry freshness are parsed and left unenforced. `inputage.expires` and `inputage.nonce` are appended to the signature-params string (`authing.py:143,145`) so they are cryptographically bound — but `expires` is never compared to the clock, and there is **no replay cache**: a search of `src/keria` for `replay|nonce` at `7e685edaa` turns up no store of seen nonces, only unrelated KEL-replay machinery and a test fixture. An RFC-9421 `expires` that the verifier does not check is decoration.
- **[K] The client half does not enforce it either.** In signify-ts at `ffba8406e`, `authing.ts` folds `input.expires` into the params string at L136-137 and never compares it; the only `new Date()` is `const dt = new Date().toISOString().replace('Z', '000+00:00')` (`authing.ts:219`), an outbound stamp. The `EssrAuthenticator` checks the timestamp is *present* — *"Timestamp is missing from ESSR payload"* (`authing.ts:342`) — which is a presence check, not a freshness check.

**Statement of the finding.** Neither side of the Signify/KERIA channel enforces timestamp freshness at the pinned commits. Both bind a timestamp into the signature; neither reads it as a time. The security property this buys is **request integrity and origin authentication, not replay protection**: a captured request replays indefinitely against the same method and path, and the signature verifies every time, because the verifier's only question is whether the bytes are signed by the current key. The note previously stated this one-sidedly for KERIA; it is symmetric.

**What it is not.** This is not evidence that replay is unconsidered — the fields to enforce it are present and signed, so enforcement is a verifier change with no wire change. It is evidence that at these commits nothing enforces it. Do not upgrade "the fields exist" into "the protocol resists replay"; the shibboleth in `keri-doctrine.md` turns on precisely that gap and should be restated with these pins rather than softened.

### Network-interface isolation (defense-in-depth deployment)
- Three HTTP endpoints on **three separate network interfaces** (`protocol.md` §KERIA Service Endpoint Interfaces):
  1. **Boot Interface** (default 3903) — agent worker initialization; *"can be expose[d] to internal infrastructure only (or disabled all together)"*; if launched in static worker mode, Boot can be disabled entirely.
  2. **Admin Interface** (default 3901) — the signed REST API for command & control from the Signify client.
  3. **KERI Protocol Interface** (default 3902) — CESR-over-HTTP to the world.

---

## 3. Invariants and "never do X" rules

### Never leaves the edge
- **INVARIANT: unencrypted private key material never leaves the client** (`protocol.md` §Key Generate Methods, restated per algorithm). Salts/keys sent to the server are always X25519-encrypted; the server stores CESR-encoded `Cipher` blobs.

### Agent AID must be a single-key delegated AID anchored to the client
- signify-ts `controller.ts` `Agent.parse` enforces, on connect. **All four re-anchored 2026-09-15 at `ffba8406e`; unchanged in substance, line hints refreshed:**
  - inception type must be `dip` (delegated): `throw new Error(\`invalid inception event type ${state['et']}\`);` (`controller.ts:45`).
  - must have a delegator anchor: `throw new Error('no anchor to controller AID');` (`controller.ts:50`).
  - **exactly one** signing key and **exactly one** next key: `throw new Error(\`agent inception event can only have one key\`);` (`controller.ts:61`) and `throw new Error(\`agent inception event can only have one next key\`);` (`controller.ts:67`); thresholds must be 1 for both current and next.
- KERIA side: multisig groups may **not** be an agent controller — *"multisig groups not supported as agent controller"* (`keria/src/keria/app/agenting.py:871`).

### Client AID is single-sig, transferable, one signing + one rotation key
- *"The Signify Client generates the client AID as a transferable AID with a single signing key and single rotation key"* (`protocol.md` Step One).

### Server rejects duplicate/unknown/invalid provisioning
- Boot: if `caid` already has an agent → HTTP 400 *"agent for controller {caid} already exists"* (`agenting.py:821-823`).
- Boot: the submitted `icp` must actually produce the claimed `caid`, else the agent is deleted and rejected: `if ctrlHab.pre != agent.caid: ... 'invalid icp event for caid'` (`agenting.py:834-837`).
- Identifier creation: unknown witness → 400 `'unknown witness'`; unknown delegator → 400 `'unknown delegator'` (`aiding.py:318-325`).
- Group inception: signing member must be a local AID and an actual participant, else 400 (`aiding.py:335-346`).

### Every Admin request/response must be signed (no unsigned admin traffic)
- ~~`SignatureValidationComponent.process_request` short-circuits Falcon with **HTTP 401** if the signature fails: `resp.complete = True ... resp.status = falcon.HTTP_401` (`keria/src/keria/core/authing.py:187-189`).~~ **SUPERSEDED 2026-09-15** — the class no longer exists. `core/authing.py` was restructured into an abstract `Authenticator` with two concrete subclasses and a middleware; see §10a. The *behavior* survives the rename, re-anchored below.
- **[K]** `AuthenticationMiddleware.process_request` short-circuits Falcon with **HTTP 401** on any authentication failure: *"This short-circuits Falcon, skipping all further processing"* (`keria/src/keria/core/authing.py:AuthenticationMiddleware.process_request`, L458, at `7e685edaa`). The failure funnel is one `except` clause — `except (kering.AuthNError, ValueError, UnicodeDecodeError):` — so a bad signature, a malformed header and a non-UTF-8 ESSR payload are indistinguishable to the caller, all returning a bare 401 with no body.
- **[K]** Only explicitly `allowed` paths bypass, and at `7e685edaa` that list has exactly one entry: `authing.AuthenticationMiddleware(agency=agency, authn=authn, allowed=["/agent"])` (`keria/src/keria/app/agenting.py:952`).
- **[K]** Which authenticator runs is decided purely by path: `authenticator = self.essrAuthn if req.path == "/" else self.authn` (`authing.py:AuthenticationMiddleware.process_request`, L449). `POST /` is the ESSR tunnel; everything else is signed-header. Correspondingly `ESSRAuthenticator.inbound` opens with `if request.path != "/": raise kering.AuthNError("Request should not expose endpoint in the clear")` (`authing.py:229-230`) — the tunnel exists so the *endpoint* is confidential, not just the body.
- Client rotation over the admin interface is itself gated on a valid current-key signature: on `/agent/{caid}` PUT rotation, `if not self.authn.verify(req): raise falcon.HTTPForbidden` (`aiding.py:160-161`).

### Rotation-recryption integrity check (never accept keys that don't match state)
- On client rotation, the edge **re-derives and validates** each managed AID's keys against its published key state before re-encrypting: Salty path throws `'Invalid Salty AID'` if `pubs.join(',') != _signers.join(',')` (`controller.ts:372-374`); Randy path throws `'unable to rotate, validation of encrypted public keys ... failed'` (`controller.ts:399-403`).

---

## 4. Anti-patterns / outsider-tells this material corrects

### "The cloud holds my keys" (custodial-wallet / KMS mental model) — WRONG
- Outsider prior: a cloud agent or HSM-as-a-service holds and uses your private keys (à la AWS KMS, cloud HSM, custodial crypto wallet). KERIA-correct: the agent holds only **encrypted** key material it *cannot decrypt* and **never signs on the controller's behalf**. The custodian is a blind store + relay, not a signer. (`signify-ts/README.md`; `keria/README.md` "Agents").

### "The server is trusted infrastructure" (client-server / IAM prior) — WRONG
- Outsider prior (OAuth/OIDC/session tokens): the server issues you a bearer token and is the authority. KERIA-correct: **the client is the authority (delegator); the agent is the delegate.** Auth is not a bearer token but a per-request Ed25519 signature over HTTP message-signature fields (RFC httpbis message signatures), keyed to the AID's *current* signing key. Responses are likewise signed — the client authenticates the *server*, inverting the usual trust asymmetry. (`authing.ts`, `authing.py`).

### "Rotating a passcode is just changing a password" — WRONG
- Password-manager prior: change the secret, re-encrypt the vault, done. KERIA-correct: a passcode rotation **is a KEL rotation event** with a dual-key partial rotation binding old rotation authority to new signing authority — an on-ledger, cryptographically-committed operation with post-quantum recovery semantics, not a cleartext vault re-key. (`protocol.md` §Partial Client AID Rotation).

### "Use a bearer credential / API key to call the agent" — WRONG
- The Admin interface has no API keys or bearer tokens. Identity is the Client AID; proof is a fresh signature per request over `@method`, `@path`, `signify-resource`, `signify-timestamp` (`DefaultFields`, both languages — the class is `SignedHeaderAuthenticator` as of 2026-09, not `Authenticater`). A stolen header set can't be replayed against a different method/path, and there is no long-lived secret to exfiltrate from the server.
- **BOUNDARY, added 2026-09-15 — state it whenever this row is used.** "Can't be replayed against a *different* method/path" is the whole of the protection, and the corpus has been sloppy about the other half. A stolen header set **can** be replayed against the *same* method and path, indefinitely, because neither implementation checks the timestamp against a clock and neither keeps a nonce cache (§2). The honest comparison to a bearer token is therefore narrower than it looks: the signature is scoped to one method+path pair and to one key state, where a bearer token is scoped to neither — but on that one pair it is as replayable as the token is, and it does not expire. What removes the stolen credential is key rotation, not time.

### "The agent adds trust / vouches for the controller" (CA/federation prior) — WRONG
- The agent contributes *no* authority to the controller's events. Externally it's just another KERI node relaying edge-signed CESR. Verifiers never trust the agent; they verify the KEL/TEL. (KERIA README "Message Router": all KERI clients interact the same way.)

---

## 5. Precise terminology / definitions (as used in these repos)

- **Client AID / caid** — the controller's own transferable AID; delegator of the Agent AID; single signing + single rotation key; keys derived at the edge from the passcode (`protocol.md` Step One).
- **Agent AID** — KERIA-created **delegated** (`dip`) AID with `di` = Client AID; single-key, threshold-1; signs all agent→client responses (`protocol.md` Step Two; `controller.ts` Agent).
- **Agency** — the boot service and *"central repository for initializing agents"*; persists the caid→agent mapping for recovery on restart; the `Agency` class holds `agents` dict + `AgencyBaser` DB with `agnt` (caid→agentPre), `ctrl` (agentPre→caid), and `aids` (managedPre→caid) sub-DBs (`agenting.py:149-273`).
- **Agent (worker)** — a `DoDoer` Habery bundle per controller; runs HIO coroutines/queues/handlers for all async work (multisig, delegation, witnessing, IPEX grant/admit, escrows) (`agenting.py:276-378`). KERIA README "Agents": uses **KERI HIO** for orchestration.
- **bran / passcode** — 21-char user secret. The **bran** = `'0A'` (Salt_128 code) + `'A'` (pad) + first 21 chars of passcode, interpreted as qb64 salt for key stretching (`controller.ts:159`, `protocol.md` Step One item 1).
- **Salty keys** — HDK chain: one random salt per AID, stretched via **Argon2** with a `path` computed from the AID's prefix index (`pidx`) and key index (`kidx`); salt stored server-side encrypted (`sxlt`) (`protocol.md` §Salty Keys; `keeping.py` `SaltyPrm`).
- **Randy keys** — fully random signing/rotation keys, each encrypted with X25519 and stored as indexed CESR `Cipher` in separate LMDB sub-DBs (`prxs.`, `nxts.`) (`protocol.md` §Randy Keys; `keeping.py` `RandyManager`).
- **Sandy keys** — keys from a *different* salt per inception and each rotation (`protocol.md` §Sandy Keys — documented as a listed method).
- **Group keys** — special algo that manages **no keys at all**; designates one of the other-typed AIDs as the "local" participant in a distributed multisig; all signing done at the edge for that local member (`protocol.md` §Group Keys; `keeping.py` `GroupManager`).
- **HSM keys / SHIM** — experimental "Signify HSM Integration Module" letting all keygen + signing happen in an external HSM (Google KSM, Trezor samples) (`protocol.md` §HSM Keys).
- **sxlt** — the qualified-b64 **encrypted AID salt** (`SaltyPrm.sxlt`); also a global (`RemoteManager.sxlt` in `gbls.`) holding the encrypted passcode-salt during rotation (`keeping.py:27,161-169`).
- **pidx / kidx / ridx** — prefix index (which managed AID), key index (cumulative signing+rotation key count over lifetime), rotation index (`controller.ts:110-169`, `keeping.py`).
- **RemoteKeeper / RemoteManager** — server-side encrypted key store; `TailDirPath = "keri/rks"`; sub-DBs must end in `.` to avoid Base64 prefix collisions (`keeping.py:41-131`).
- **Signify-Resource header** — carries the AID whose signature authenticates the request/response (`authing.py:34-40`).
- **Signify-Timestamp header** — ~~signed freshness field~~ **CORRECTED 2026-09-15**: a signed *timestamp* field. Calling it a "freshness field" overstates it — it is bound by the signature and never checked against a clock by either implementation (see §2, "The signature BINDS a timestamp"). It establishes *when the signer says the request was made*, not that the request is recent (`httping.ts:16`).
- **Signage / Signature-Input** — the RFC-httpbis structured-header signature envelope produced by `siginput`/`signature` and parsed by `desiginput`/`designature` (`httping.ts`, `end/ending.ts`).
- **OpTypes / long-running operation** — async server-side operations the client polls: `delegation`, `witness`, `group`, `credential`, `done` (`aiding.py`, `credentialing.py`, `longrunning`).

---

## 6. Worked flows across the edge/cloud boundary (interop-critical)

### 6a. Agent provisioning (bootstrap) — the delegation handshake
Three steps (`protocol.md` §Agent Worker Initialization):
1. **Client generates Client AID** at the edge (transferable, single sig + single rot). Keys: prepend `0A` + `A` to 21-char passcode → Argon2-stretch with paths `signify:controller00` (signing) and `signify:controller01` (rotation). POST signed `icp` to Boot interface `/boot`.
   - Wire body (signify-ts `boot()`): `{ icp: evt.sad, sig: sign.qb64, stem, pidx: 1, tier }` (`clienting.ts:110-117`).
   - KERIA `BootEnd.on_post`: validates `icp` + `sig`, derives `caid = icp.pre`, creates the agent, and (if `salt`/`randy` in body) stores the encrypted params (`agenting.py:796-874`).
2. **KERIA creates the Agent Worker** and a **delegated** `dip` Agent AID with `di = Client AID`; returns the Agent AID inception in a signed HTTP response (`protocol.md` Step Two). `Agency.create` makes a per-caid `Keeper`, `Habery`, `agent-{caid}` Hab (`ns="agent"`, `delpre=caid`), and `Regery` (`agenting.py:176-220`).
3. **Client approves the delegation** with an **interaction event** anchoring the agent's inception seal, sent to the Admin interface: `PUT /agent/{caid}?type=ixn` with `{ ixn: serder.sad, sigs }` (`clienting.ts:307-325`; `controller.approveDelegation` builds anchor `{i: agentPre, s: agentSn, d: agentSaid}` at `controller.ts:228-241`). KERIA `AgentResourceEnd.interact` applies the ixn to the ctrlHab and processes it in the agent's Kevery; `anchorSeals` writes the delegator authorizing-event seal (`agenting.py`/`aiding.py:200-239`).
   - INVARIANT: *"all HTTP requests against the Admin Interface must be signed by the Client AID and expect all responses to be signed by the Agent AID."* (`protocol.md` Step Three).

### 6b. Connect / reconnect
- `SignifyClient.state()` → `GET /agent/{caid}` returns `{agent, controller, ridx, pidx}`; 404 if no agent (`clienting.ts:133-148`).
- `connect()` rebuilds the `Controller` from stored `state.controller`, builds the `Agent`, **verifies the anchor matches**, approves delegation if the controller is still at sn 0, then builds the `Authenticater` from the controller's current signer + the agent's verfer (`clienting.ts:153-182`).

### 6c. Creating a managed identifier (edge generates event, cloud stores encrypted params)
- Edge: manager creates keys, builds `icp` (or delegated `icp`), signs with keeper; POST `/identifiers` with `{ name, icp: serder.sad, sigs, proxy, smids, rmids, <algo>: keeper.params() }` (`aiding.ts:161-281`).
- Cloud `IdentifierCollectionEnd.on_post`: makes a **SignifyHab** (a Hab with no local keys — keys live at the edge) via `makeSignifyHab(name, serder=serder, sigers=sigers)`, then `inceptSalty/inceptRandy/inceptExtern` stores the encrypted params; returns a long-running op keyed to whether the AID is delegated / has witnesses / is plain (`aiding.py:296-425`).
- **Salty params on the wire** (`keeping.py` `SaltyPrm` / `params()`): `{sxlt, pidx, kidx, stem, tier, dcode, icodes, ncodes, transferable}` — signing/next **codes**, never seeds.
- **Randy params on the wire**: `{prxs: [encrypted signing keys], nxts: [encrypted next keys]}` — CESR `Cipher` blobs (`keeping.py:307-331`).

### 6d. Signing (indexed vs unindexed)
- Edge `SaltyKeeper.sign` re-derives signers deterministically from the salt and produces **indexed** `Siger`s (for KEL events) or **unindexed** `Cigar`s (`keeping.ts:428-490`). Dual-index (`ondex`) support mirrors keripy for rotation events that satisfy prior next-key commitments.
- CHANGELOG note: `rotated=true` flag on signing added to **match KERIpy `BaseHab.sign` behaviour** (`signify-ts/CHANGELOG.md` 0.4.0) — explicit cross-impl parity.
- CHANGELOG: `ondex` must be computed from the **prior** establishment event, not the proposed one (issue #378) — a subtle interop correctness rule.

### 6e. Client (passcode) rotation + managed-AID recryption
- Edge `Controller.rotate(nbran, aids)`: partial-rotates the Client AID (dual key, weights `['1','0']`), re-encrypts the passcode salt to `sxlt`, and for **every managed AID** decrypts→validates-against-key-state→re-encrypts its salt/keys under the new passcode's X25519 key; returns `{rot, sigs, sxlt, keys}` (`controller.ts:272-426`).
- Cloud `AgentResourceEnd.on_put` (rotation branch): applies the rot to the ctrlHab, **re-verifies the request signature**, swaps in the new global `sxlt`, updates each managed AID's `sxlt`/`prxs`/`nxts`, then `delete_sxlt()` clears the transient global (`aiding.py:140-198`). The transient `sxlt` global is the aborted-rotation breadcrumb.

### 6f. Credential issuance (ACDC) across the boundary
- Edge builds `acdc`, `iss` (TEL issuance), and the anchoring `ixn`/`rot`, signs, and POSTs to `/identifiers/{name}/credentials`.
- Cloud `CredentialCollectionEnd.on_post`: parses `acdc` (SerderACDC), `iss` (SerderKERI), and anchor (`ixn` or `rot`); rejects issuance against an unknown registry SAID (`ri`); anchors via rotate (if estOnly) or interact; then `validate` → `registrar.issue` → `credentialer.issue`; returns a `credential` long-running op (`credentialing.py:404-505`).
- Body schema fields (`credentialing.py:440-458`): `acdc`, `iss`, `rules` (Ricardian contract), `source` (ACDC edge/edge-group with `d`+`s` SAIDs for chaining), `credentialData`, `private` (privacy-preserving presentation flag).
- IPEX grant/admit are driven server-side by the `Granter`/`Admitter` HIO doers that forward artifacts to recipients via `StreamPoster` and parse inbound acdc/iss/anc (`agenting.py:504-595`).

---

## 7. Cross-language / cross-implementation interop invariants (keripy ↔ KERIA ↔ signify-ts ↔ SignifyPy)

These are the contracts two implementations **must** agree on byte-for-byte.

### 7a. HTTP message-signature construction (the highest-risk interop surface)
The signed byte string `ser` is assembled identically in TS and Python; any divergence breaks auth silently.
- **Default signed fields** must match:
  - signify-ts `Authenticater.DefaultFields = ['@method', '@path', 'signify-resource', 'signify-timestamp']` (`authing.ts:14-19`).
  - KERIA `Authenticater.DefaultFields = ["Signify-Resource", "@method", "@path", "Signify-Timestamp"]` (`authing.py:17-20`).
  - NOTE (potential ordering subtlety worth flagging): the two default lists are in **different order**. Because the actual signed order is driven by the `Signature-Input` header the *signer* emits (parsed back by `desiginput` and iterated in that order on verify), order agreement is enforced by the wire header, not the constant. Still, this asymmetry is a landmine — see Gaps.
- **Field serialization**: each covered field is emitted as `"<field>": <value>` lines joined by `\n`; `@method` → HTTP method, `@path` → request path; header values are `normalize()`-d (trim). Final line is `"@signature-params: (<fields>);created=...;[expires=;][nonce=;][keyid=;][context=;][alg=]"`. Identical in `httping.ts:56-114` (TS sign), `authing.ts:42-85` (TS verify), and `authing.py:60-93` (Py verify).
- **alg** is `ed25519`; **keyid** is the signer's `qb64` public key (`authing.ts:106-108`, `authing.py:130-131`).
- Signature envelope name is the literal string **`"signify"`**: `inputs.filter(input => input.name == 'signify')` (TS) / `[i for i in inputs if i.name == "signify"]` (Py). Both drop non-`signify` inputs.
- **Timestamp format quirk**: signify-ts writes the time header as ISO with `Z` replaced by `000+00:00`: `new Date().toISOString().replace('Z', '000+00:00')` (`clienting.ts:205-207`, `clienting.ts:288-290`). KERIA uses `helping.nowIso8601()`. Both must parse each other's format — a real cross-impl constraint.
- **Path percent-encoding**: KERIA quotes the path before verify and unquotes after (`authing.py:170-186`), and re-quotes for response signing; the edge signs over `path.split('?')[0]` (query string excluded) (`clienting.ts:216-217,246-249`). Query params are NOT covered by the signature.

### 7b. CESR primitive encoding
- signify-ts README: *"The communication protocol ... will encode all cryptographic primitives as CESR base64 encoded strings for the initial implementation. Support for binary CESR can be added in the future."* — so the JSON-over-HTTP wire uses **qb64 text CESR**, while the external KERI Protocol interface is CESR-over-HTTP (may be binary). All `k`, `n`, `d`, `i`, signatures, ciphers are qb64.

### 7c. Key derivation must be deterministic & identical
- **bran construction**: `Salt_128 ('0A') + 'A' + passcode[0:21]` — identical in `controller.ts:159` and `protocol.md` Step One. A mismatch here means the edge and any other edge impl derive different keys from the same passcode.
- **Controller stem** is the literal `'signify:controller'` (`controller.ts:180`); Salty AID stems are per-AID. Argon2 + `tier` (low/medium/high) + path determines the key. keripy's `SaltyCreator` must produce identical output to signify-ts `SaltyCreator` for the same inputs.
- Blake3-256 digest of the next public key is the next-key commitment (`controller.ts:208-211`).

### 7d. Event/threshold semantics parity
- CHANGELOG parity fixes prove these are live interop constraints:
  - `rotate` defaults to **next** threshold, not current (#208).
  - `rotate` must use proper `adds` and `cuts` (#359).
  - `serder` must correctly parse **string/hex** sequence numbers (`s` may be hex string) — both impls must agree (`CHANGELOG.md`).
  - `rotated=true` flag added to match keripy `BaseHab.sign` (0.4.0).
- Rotation ilk switches to `drt` (delegated rotation) when the AID is delegated: `const ilk = delegated ? Ilks.drt : Ilks.rot` (`aiding.ts:392`).
- Default rotation thresholds computed as `max(1, ceil(count/2))` in hex (`aiding.ts:364-369`) — must match keripy's default.

### 7e. Types are generated FROM the KERIA OpenAPI spec
- signify-ts generates its request/response types directly from KERIA's OpenAPI (`npm run generate:types`, `SPEC_URL=.../spec.yaml`) (`signify-ts/README.md`). CHANGELOG 0.3.0: *"Auto-generated credential types from KERIA OpenAPI spec (#337)."* → KERIA's `specing.py`/`spec.yaml` is the **source of truth** for the admin API contract; the TS client is a downstream consumer. `src/types/keria-api-schema.ts` is the generated artifact.

### 7f. Where keripy and signify-ts must agree (explicit)
- **Signing behavior**: `BaseHab.sign` (keripy) ↔ `SaltyKeeper.sign` (TS) — indexed/unindexed, dual-index ondex from prior est event.
- **Key stretching**: keripy `SaltyCreator`/Argon2 ↔ TS `SaltyCreator` — same salt/tier/path → same keypair.
- **Serder/CESR (de)serialization**: version string, field order, hex `s`, SAID computation — must be byte-identical for signatures to verify.
- **HTTP message-signature bytes**: keripy `keri.end.ending` (`siginput`/`designature`) is imported directly by KERIA (`from keri.end import ending`), and re-implemented independently in TS (`end/ending.ts`, `httping.ts`). These two independent implementations are the true interop risk.
- **Delegation seal format**: `couple = seqner.qb64b + saider.qb64b` authorizing-event seal (`aiding.py:237`) must match keripy's delegation-approval expectation.

---

## 8. Notable exact short quotes (with citations)

- *"This architecture protects the host and the holder private keys. All client tasks/calls are signed 'at the edge'."* — `keria/README.md`, KERIA Service Architecture.
- *"They don't have the secrets of the client."* — `keria/README.md`, Agents.
- *"Agents do have their own keys and do sign all of their messages BACK to the Signify client."* — `keria/README.md`, Agents.
- *"splits off two, key generation and event signing ... to provide 'signing at the edge'."* — `signify-ts/README.md`.
- *"a remote cloud agent that never has access to the decryption keys."* — `signify-ts/README.md`.
- *"only the public keys and blake3 hash of the next keys made available to the agent."* — `signify-ts/README.md`.
- *"unencrypted private key material never leaves the client."* — `keria/docs/protocol.md`, Key Generate Methods.
- *"the Signify Client AID (called the 'Client AID') being the delegator for the KERIA agent worker AID (called the 'Agent AID')."* — `protocol.md`, Agent Worker Initialization.
- *"all HTTP requests against the Admin Interface must be signed by the Client AID and expect all responses to be signed by the Agent AID."* — `protocol.md`, Step Three.
- *"To provide post-quantum secure passcode recovery, a passcode recovery must be accompanied by partial rotation of the Client AID."* — `protocol.md`, Partial Client AID Rotation.
- *"lock out all other operations until it is completed successfully."* — `protocol.md`, Passcode Rotation Recovery.
- *"message from a different remote agent"* (client-side agent-impersonation guard) — ~~`clienting.ts:243`~~ → `signify-ts/src/keri/core/authing.ts:83` at `ffba8406e` (moved 2026-09).
- *"commitment to controller AID missing in agent inception event"* — ~~`clienting.ts:167-169`~~ → `clienting.ts:202` at `ffba8406e`.
- *"multisig groups not supported as agent controller"* — `keria/src/keria/app/agenting.py:871`. **Line hint not re-verified in the 2026-09 pass.**
- ~~*"This enpoint allows all KERI clients (not just Signify) to interact in a seamless way."*~~ **CUT 2026-09-15 — the quote does not match the source.** At `7e685edaa` the line reads *"This endpoint allows all KERI clients (not just Signify) to interact in a seamless way."* (`keria/README.md:17`) — `endpoint`, correctly spelled. Whether the note mistranscribed it or the typo was fixed upstream is not determinable from here, and per the rule a quote that cannot be found at its commit is cut rather than reworded. The replacement is the verbatim line above, re-read at `7e685edaa`, and it supports the same claim (§2, §4: externally the agent is a normal KERI participant).

### Added in the 2026-09 pass (all re-read at the stated commit)

KERIA, all at `7e685edaa`:
- *"This short-circuits Falcon, skipping all further processing"* — `core/authing.py:AuthenticationMiddleware.process_request`, L458.
- *"Request should not expose endpoint in the clear"* — `core/authing.py:ESSRAuthenticator.inbound`, L230.
- *"ESSR payload missing or incorrect encrypted sender"* — `core/authing.py:ESSRAuthenticator.inbound`, L270.
- *"The body is carried through as raw bytes so the tunnel is byte transparent."* — `core/authing.py:buildEnviron` docstring, L340-341 (the sentence wraps across the two lines).
- `coring.Seqner(sn=hab.kever.lastEst.s),` — `app/aiding.py:1665` (and `:1766` for locschemes).
- *"Include the issuee KEL and delegation parents only when the issuee is disclosed and differs from the recipient."* — `app/ipexing.py:871-872`.
- `response.set_header("Signify-Timestamp", helping.nowIso8601())` — `core/authing.py:180`. The *only* outbound-stamp site; no inbound counterpart exists, which is the freshness negative in one line.

signify-ts, at `ffba8406e` unless marked:
- `export class EssrAuthenticator extends Authenticator {` — `src/keri/core/authing.ts:192`.
- *"Timestamp is missing from ESSR payload"* — `src/keri/core/authing.ts:342` (a presence check, not a freshness check).
- `if (typeof fs !== 'number' || fs < 0) return { fail: 'bad' }; // variable-size: unsupported` — `src/keri/core/parsing.ts:263` **at `4ed767b` (fork branch)**.
- `return avail < fs ? { fail: 'short' } : { node: fs };` — `src/keri/core/parsing.ts:264` **at `4ed767b` (fork branch)**.
- `if (genus === 2) return frameGroupV2(bytes, at);` — `src/keri/core/parsing.ts:429` **at `4ed767b` (fork branch)**.
- `| 'incomplete'; // the stream ends inside an element — RECOVERABLE, more bytes may complete it` — `src/keri/core/parsing.ts:101` **at `4ed767b` (fork branch)**.
- `ver.proto === 'KERI' && sad && typeof sad.s === 'string'` — `src/keri/core/parsing.ts:725` **at `4ed767b` (fork branch)**.
- `'1AAR': new Sizage(4, 0, 892, 0), // FN-DSA-512 signature, 666 B` — `src/keri/core/matter.ts:174` **at `4ed767b` (fork branch)**.

---

## 9. Deployment / operational doctrine (secondary but load-bearing)

- **HIO** (hierarchical async I/O) is the concurrency substrate: *"HIO is an efficient and scalable orchestration/processing mechanism that leverages queues, handlers, coroutines"* (`keria/README.md`, Agents). Each `Agent` is a `DoDoer` composed of ~15 doers (Witnesser, Delegator, ExchangeSender, Granter, Admitter, GroupRequester, Querier, Escrower, ParserDoer, etc.) (`agenting.py:362-378`).
- **All Agent DB access is through the associated Agent** (`keria/README.md`) — tenant isolation invariant; each caid gets its own `Keeper` + `Habery` + `Regery` keyed by caid.
- CORS exposes exactly the KERI/Signify headers: `cesr-attachment, cesr-date, content-type, signature, signature-input, signify-resource, signify-timestamp` (`agenting.py:57-59` and repeated).
- Agent worker modes: **dynamic** (Boot creates agents on demand) vs **static** (all workers configured at startup, Boot disabled) (`protocol.md` §KERIA Service Endpoint Interfaces).

---

## 10. The 2026-09 pass — what changed at the new pins

### 10a. Both implementations refactored their authenticator in lockstep, and grew an ESSR tunnel

The single largest structural change since this note was written. KERIA's `core/authing.py` no longer has a `SignatureValidationComponent` or an `Authenticater`; it has an abstract `Authenticator(ABC)` with `inbound`/`outbound` abstract methods (`authing.py:47,72,76`), two concrete subclasses `SignedHeaderAuthenticator` (`authing.py:80`) and `ESSRAuthenticator` (`authing.py:208`), an `AuthMode` enum (`authing.py:37`), and an `AuthenticationMiddleware` (`authing.py:413`) that picks between them.

**[K]** signify-ts has the mirror image of the same shape: `export abstract class Authenticator` (`authing.ts:21`), `export class SignedHeaderAuthenticator extends Authenticator` (`authing.ts:43`), `export class EssrAuthenticator extends Authenticator` (`authing.ts:192`) — all at `ffba8406e`. Two independently-maintained codebases converging on the same class decomposition, in the same period, is evidence that the ESSR mode is a designed protocol addition rather than one side's implementation detail.

**What ESSR is, in one line.** "Encrypt Sender, Sign Receiver": the client POSTs to `/` with an opaque ciphertext body, so the *endpoint path itself* is confidential — the signed-header mode leaks `@path` to anyone watching, because the path is a covered field emitted in the clear. The agent decrypts, reconstitutes a real WSGI request from the plaintext, and re-dispatches it internally.

- **[K]** The reconstitution is literal HTTP-over-HTTP: `buildEnviron` splits the plaintext `head, _, body = raw.partition(b"\r\n\r\n")` and builds a WSGI `environ`, then `request.reinit(environ)` (`authing.py:273`) re-initializes the Falcon request in place — which is what the custom `class ModifiableRequest(falcon.Request)` with its `reinit` method (`authing.py:42-44`) exists for.
- **[K]** `f43a294` "make the ESSR tunnel byte-transparent" is documented in the source itself: *"The body is carried through as raw bytes so the tunnel is byte transparent."* (`authing.py:buildEnviron` docstring, L340-341, at `7e685edaa`). The commit that preceded it had `rstrip`ped the body; `bd1fe46` removed that. **Doctrinal point:** a tunnel that normalizes bytes breaks every signature carried inside it, because a KERI signature is over exact bytes. Byte-transparency is not a nicety here, it is the precondition for the tunnel being usable at all.
- **[K]** `9ed58e4` is why `UnicodeDecodeError` appears in the middleware's `except` tuple: a body that is not valid UTF-8 is an authentication failure returning 401, not a 500. The decision to catch it at the auth boundary means a malformed ESSR payload is indistinguishable from a bad signature to the caller.
- **[K]** ESSR responses are sealed to the client's *KEL key*, converted to a box key: `pubkey = pysodium.crypto_sign_pk_to_box_pk(ckever.verfers[0].raw)` then `raw = pysodium.crypto_box_seal(inner, pubkey)` (`authing.py:ESSRAuthenticator.outbound`, L309-310). No key exchange and no session: the Ed25519 verification key already in the KEL is birationally mapped to X25519 and used as a sealed-box recipient. This is the same trick the edge uses to encrypt salts to the agent, run in the other direction.
- **[K]** The ESSR inbound path re-checks sender identity *inside* the ciphertext, not just outside it: `if "HTTP_SIGNIFY_RESOURCE" not in environ or environ["HTTP_SIGNIFY_RESOURCE"] != resource: raise kering.AuthNError("ESSR payload missing or incorrect encrypted sender")` (`authing.py:265-270`). The outer header and the inner header must agree, so an attacker cannot wrap someone else's ciphertext in their own envelope.

### 10b. KERIA seals `endrole`/`locscheme` reply signatures to the last ESTABLISHMENT event — matching keripy the same month

**[K]** At `7e685edaa`, both `EndRoleCollectionEnd.on_post` and `LocSchemeCollectionEnd.on_post` build the transferable-signature-group with `coring.Seqner(sn=hab.kever.lastEst.s),` / `coring.Saider(qb64=hab.kever.lastEst.d),` (`keria/src/keria/app/aiding.py:1665-1666` and `:1766-1767`). Before `b57780a` (Patrick Vu, 2026-09-07, contained in `upstream/main`) these two sites used `hab.kever.sn` and `hab.kever.serder.said` — the last event of *any* kind.

**Why this is design evidence and not just a bug.** A `tsg` (transferable signature group) tells a verifier *which key state* to validate the reply's signature against. Key state only changes at establishment events, so citing the latest event — which is usually an interaction event — names an event that establishes nothing. The correct referent is the last establishment event.

Two things make this more than a one-line fix. First, **the rest of KERIA already did it correctly**: `lastEst.s`/`lastEst.d` appears at fourteen sites across `ipexing.py`, `grouping.py` and `peer/exchanging.py` (e.g. `ipexing.py:107`, `grouping.py:104`, `exchanging.py:148`), all in `SealEvent` construction. The `endrole`/`locscheme` handlers were the two stragglers. Second, **keripy made the same correction in the same month** in `kraming.py` (PRs #1658, #1662 — cross-reference; `raw/15` owns that half and this note does not re-mine it). Two implementations independently converging on "decide `tsg` currency against last establishment event, not last event" is evidence about the *design rule*, not about either codebase's carelessness. It belongs with the establishment-event material in chapter 03/06 rather than in a bug list.

### 10c. The "blind store, not a signer" claim is now supported by CODE, not only by READMEs

`keri-doctrine.md`'s cloud-agent shibboleth row previously rested on README prose. All three README quotes re-verify verbatim — KERIA's at `7e685edaa` (`README.md:11,17,31`), signify-ts's at *both* `4c0072f62` and `ffba8406e` (`README.md:20,23,24`), so they are stable across two and a half years. But the pass found direct code-level support, which is a stronger footing:

**[K]** The string `decrypt` occurs exactly **three** times in all of `src/keria` at `7e685edaa`, and all three are in `authing.py`: two in docstrings, and one real call — `environ = self.buildEnviron(agent.agentHab.decrypt(ser=cipher))` (`authing.py:262`), which decrypts the **ESSR transport envelope** using the *agent's own* AID key. **`core/keeping.py` contains zero `decrypt` calls and zero `.sign(` calls.** That module is the one that stores the controller's encrypted salts and keys (`sxlt`, `prxs`, `nxts`). So KERIA stores the controller's cipher blobs and never, anywhere in its source, calls decrypt on them — and the only decryption it performs at all is of material sealed *to itself*.

That is the difference between "we promise not to look" and "there is no code that could look", and it is the sharper form of the claim. State it with the scope named: it is a statement about `src/keria` at `7e685edaa`, not a proof about deployments.

### 10d. Untargeted ACDCs: the issuee is optional and the attribute section may not be a dict

**[K]** `b5d8e64` (Kent Bull, 2026-07-21, "Fixes #452 crash on untargeted ACDC or missing issuee", in `upstream/main`). At `7e685edaa` the artifact-gathering helper reads the issuee defensively: `isse = attrib.get("i") if isinstance(attrib, dict) else None` (`keria/src/keria/app/ipexing.py:855`), and gates the issuee's KEL on `if isse is not None and isse != recp:` (`ipexing.py:873`), documented in-source as *"Include the issuee KEL and delegation parents only when the issuee is disclosed and differs from the recipient."* (`ipexing.py:871-872`).

Two doctrinal facts are encoded in that one line, and both are easy to get wrong from outside. An ACDC **need not have an issuee at all** — an untargeted ACDC is an attestation about the world rather than a credential about a subject, so `a.i` is absent and code that assumes a subject crashes. And the attribute section **need not be a dict** — when it is compacted or blinded it is a SAID string, so `attrib.get` is not even a valid operation. The `isinstance` check is doing selective-disclosure work, not defensive-programming work.

### 10e. Post-quantum codes — implemented, but on a personal fork, not in signify-ts

Read the second warning at the top of this note before using anything in this subsection. Tier marker for everything here is **`[K-fork]`** — a marker this note coins for "code exists at a named commit on an unmerged personal fork". It is deliberately *weaker* than `[K]`, because `[K]` means an implementation behaves this way and this is not yet an implementation anyone else runs. Do not promote it to `[K]` without a merge into `WebOfTrust/signify-ts`.

**[K-fork]** At `4ed767b` (`dhh1128/signify-ts`, branch `feat/cesr-pq-codes`), `Matter.Sizes` carries **33 post-quantum rows** across the four-character `1`, `2` and `3` fixed tables — 14 in `1AAQ`–`1AAd`, 15 in `2AAA`–`2AAO`, 4 in `3AAA`–`3AAD` (`src/keri/core/matter.ts:173-205`). They are sizes only. Examples, verbatim: `'1AAR': new Sizage(4, 0, 892, 0), // FN-DSA-512 signature, 666 B` (`matter.ts:174`) and `'2AAN': new Sizage(4, 0, 39728, 1), // SLH-DSA-SHA2-256s signature, 29792 B` (`matter.ts:200`).

**[K-fork]** No named `MatterCodex` constants were added, deliberately. The commit touches exactly two files (`src/keri/core/matter.ts` +40/−2, `test/core/pq.test.ts` +212) and a search of `src` for `FNDSA|MLDSA|SLHDSA|PostQuantum` returns nothing. The stated reason is parity discipline: names should follow the reference implementation so the two do not diverge, and adding them later is additive.

**[K-fork]** Two existing rows changed meaning. `2AAA` and `3AAA` previously held `Sizage(4, 0, 8, 1)` and `Sizage(4, 0, 8, 2)` — placeholder rows nothing in the repository referenced — and now hold FN-DSA-1024 and ML-DSA-44 public keys. A code table row changing meaning is exactly the class of change that breaks byte-for-byte parity silently, which is why it was called out rather than left to ride in as a diff line.

**Cross-implementation state, as of this pass.** Three findings, from three agents, at three pins:
- CESR `v1.1` at `65fd7518b` defines these codes; CESR `main` at `bad6edd84` has **zero** post-quantum codes (cross-reference, `raw/02` agent — not re-verified here).
- keripy at `b8f60166b` has **no** post-quantum codes; a search for FN-DSA/ML-DSA/SLH-DSA/Dilithium/Falcon/SPHINCS/Kyber/ML-KEM found only the `falcon` web framework (cross-reference, `raw/09` agent — not re-verified here).
- `WebOfTrust/signify-ts` at `ffba8406e` has **zero** post-quantum codes — **verified in this pass**, by searching `upstream/main -- src` for `ML-DSA|MLDSA|FN-DSA|SLH-DSA|Dilithium|Falcon|SPHINCS|Kyber` and getting no match.

So the correct statement is: **no shipped implementation carries the CESR 1.1 post-quantum code table.** The codes are `[N1.1]` — spec-side only, in the v1.1 branch and not the standardizing line. The earlier framing of this as "the reference implementation and the TypeScript client disagree about the post-quantum code table" does not survive checking: they agree, in that neither has them. What exists is a fork branch ahead of both. That is a much less interesting finding about interop and a much more honest one, and it does **not** move `keri-doctrine.md` claim 9.

### 10f. The CESR stream parser (same fork caveat — `[K-fork]`, all at `4ed767b`)

A stream parser in `src/keri/core/parsing.ts` (746 lines), with `test/core/parsing.test.ts` (897 lines). It bears directly on chapter 04's "sizing is a pure function of the code" territory, and it is worth mining precisely because an independent implementation is where that doctrine either holds or breaks.

**Sizing is arithmetic on the code, never on the value.** `probePrimitive` selects a table by class (`const hards = part === 'sig' ? Indexer.Hards : Matter.Hards;`, `parsing.ts:248`), looks up the hard code (`const sizage = sizes.get(head.slice(0, hs));`, `parsing.ts:256`), and returns the table's full size as the length: `return avail < fs ? { fail: 'short' } : { node: fs };` (`parsing.ts:264`). The payload is never decoded before its length is decided. Group sizing is the same shape — `const innerEnd = innerStart + count * 4; // self-framing: count is quadlets` (`parsing.ts:frameGroupV2`, L385). **This is the doctrine holding under independent implementation**, and it is why the 33 post-quantum rows needed no parser change at all: `4ed767b` does not touch `parsing.ts`, and a 21 KB SLH-DSA signature frames correctly the moment the table knows its size.

**Genus dispatch decides the counter table, and the genus comes from the version string.** `if (genus === 2) return frameGroupV2(bytes, at);` (`parsing.ts:frameGroup`, L429). The genus is read from the version string — base64 for v2, hardcoded `genus: 1` for v1 — not sniffed from the counters. **Terminology warning worth carrying into any chapter that uses this:** "genus" names two different things here, the CESR genus *major version* (1 or 2, which selects the table) and the `-_AAA` genus-version *counter* primitive (a bodyless in-stream declaration). At this commit the counter is framed and reported but does not switch tables; the version string does. Conflating them would produce a false claim about how a stream announces its own encoding.

**Variable-size codes are rejected by runtime value, not declared type**: `if (typeof fs !== 'number' || fs < 0) return { fail: 'bad' }; // variable-size: unsupported` (`parsing.ts:263`). The prior form was `fs === undefined || fs < 0`, which trusts TypeScript's declared `fs?: number`. The hazard it guards is a table value the declared type does not admit — `null` passes both arms of the old check, since `null === undefined` is false and `null < 0` is false, and the function would then hand back `null` as a byte length. **Flagged as unresolved:** the in-source comment claims "the Sizes tables store that as null", but this repo's tables store `undefined` (e.g. `'4A': new Sizage(2, 2, undefined, 0)`, `matter.ts:206`); keripy's use `None`. The code change is real; its stated justification does not describe this repo. Listed in open questions.

**Truncation is recoverable and is not an error class.** The parser never throws — errors are returned as data. The distinction is a boolean field, `permanent: boolean;` (`parsing.ts:ParseError`, L112), plus a reserved code: `| 'incomplete'; // the stream ends inside an element — RECOVERABLE, more bytes may complete it` (`parsing.ts:ParseErrorCode`, L101). The declared-length bounds check is `if (bodyEnd > n) {` (`parsing.ts:parse`, L673), yielding `permanent: false`. Without it, `subarray` clamps silently and **a truncated message decodes as a whole one** — which is the failure mode that matters, because a silently-truncated KERI event is a different event. On `incomplete`, `consumed` stays at the message's first byte so a caller can append and re-parse.

**`s` means different things in different protocols, and the guard is on `proto`, not genus.** `ver.proto === 'KERI' && sad && typeof sad.s === 'string'` (`parsing.ts:parse`, L725), else `sn` is `null`. `s` is the sequence number under KERI and the **schema SAID** under ACDC — the same field name with unrelated meanings. Gating on the protocol field of the version string covers both v1 and v2 KERI and excludes ACDC under either. **This is a genuine interop hazard worth a chapter mention:** a parser that reads `s` as a sequence number unconditionally will report an ACDC's schema SAID as a sequence number, and will do so without erroring.

---

## Negative results from the 2026-09 pass (searched for, not found — recorded as findings)

A negative at a named commit is a finding. Each of these is a search that returned nothing, stated so that a future pass can tell a genuine absence from an unexamined question.

- **Neither implementation serves a `/.well-known/` OOBI endpoint, in either the old or the new path shape.** The KERI spec repathed `/.well-known/keri/oobi/{aid}` to `/.well-known/oobi/{aid}` this month, dropping the `keri/` segment, and an implementation still serving the old path would be a real parity gap. It is not KERIA's gap: enumerating every `add_route` call in `src/keria` at `7e685edaa` (41 routes across `agenting.py`, `aiding.py`, `credentialing.py`) turns up no `/.well-known/` route of any kind. KERIA's OOBI surface is `/oobis` and `/oobis/{alias}` (`agenting.py:1593,1595`) plus `/identifiers/{name}/oobis` (`aiding.py:45`). The `WellKnown` class at `aiding.py:2153` is unrelated — it is a *contact annotation* recording well-known URLs observed for a contact, not an endpoint served. signify-ts's only `WellKnown` is the generated mirror of that type. **So the repathing question is live for keripy and witness hosts, and moot for KERIA.**
- **Neither implementation reads `wurls`.** KERIA reads `iurls` (introduction OOBIs) and `durls` (data OOBIs) — both are config fields, env-settable as `KERIA_IURLS` (`agenting.py:145,147,310-319`, `cli/commands/start.py:159`) and merged into each agent's config at startup. There is **no `wurls`** anywhere in `src/keria` at `7e685edaa`. signify-ts at `ffba8406e` has no bootstrap-bucket implementation at all: its single `iurls` occurrence is `iurls?: string[];` in `src/types/keria-api-schema.ts:651`, which is *generated from KERIA's OpenAPI spec* and is a type reflection of the server's config shape, not client behavior. That is a small independent confirmation of §7e — the TS client is a downstream consumer of KERIA's contract.
- **Neither implementation implements `dp` disclosure paths.** Searching `src/keria` at `7e685edaa` and signify-ts `src` at `ffba8406e` for `'dp'`/`"dp"` returns zero occurrences in both. Whatever `dp` is specified to do, no part of the Signify/KERIA pair does it at these commits.
- **No replay protection of any kind in KERIA's auth path.** No nonce cache, no seen-request store, no timestamp window. Detailed with its evidence in §2; repeated here because it is a negative and belongs in the list where a reader will look for negatives.
- **KERIA never decrypts stored controller key material.** Three `decrypt` occurrences in all of `src/keria`, all in `authing.py`, only one a live call, and it decrypts the ESSR envelope sealed to the agent's own key. `core/keeping.py` — the store for `sxlt`/`prxs`/`nxts` — has zero. Detailed in §10c.

## Not re-read in the 2026-09 pass (do not treat these as re-anchored)

Under-claiming deliberately. The following were carried forward from the original note without being re-read at the new pins, so their line hints and their continued accuracy are **unverified as of 2026-09-15**:

- All of `keria/docs/protocol.md` — every §1, §2, §3 and §6 claim sourced to `protocol.md` (the SKRAP protocol, the three-step provisioning handshake, Salty/Randy/Sandy/Group/HSM key methods, partial client-AID rotation, passcode-rotation recovery, the three network interfaces). This is a large fraction of the note and none of it was re-opened.
- `keria/src/keria/core/keeping.py` beyond the `decrypt`/`sign` search in §10c — `SaltyPrm`, `RandyManager`, `GroupManager`, the `params()` wire shapes in §6c, the `TailDirPath`/sub-DB details in §5.
- `keria/src/keria/app/agenting.py` beyond the route enumeration, the middleware wiring and the `iurls`/`durls` config — the `Agency`/`Agent` internals in §5 and §9, the boot-rejection paths in §3, the IPEX `Granter`/`Admitter` doers in §6f.
- `keria/src/keria/app/credentialing.py` entirely — all of §6f's body-schema and issuance-flow detail.
- signify-ts `keeping.ts`, `aiding.ts`, `httping.ts`, `end/ending.ts` — §6c, §6d, §7a's field-serialization detail, §7d's threshold arithmetic. Only the README, `authing.ts` and `controller.ts` guard strings were checked.
- **§7a in particular has NOT been re-verified and is the most likely to have drifted**, because the code it describes has moved: the response-verification logic it cites at `clienting.ts:240-255` now lives in `authing.ts:83,93`. The `DefaultFields` order asymmetry it flags was not re-examined. Treat §7a's line hints as stale and its substance as unconfirmed at the new pins.

**Claims that WERE re-read and re-anchored:** the three KERIA README custody quotes (`7e685edaa`); the three signify-ts README custody quotes (at both `4c0072f62` and `ffba8406e`); the four `controller.ts` agent-inception guards and the three client-side impersonation/verification guards (at `ffba8406e`, locations moved); the whole of `keria/src/keria/core/authing.py`; the `endrole`/`locscheme` handlers in `aiding.py`; the artifact-gathering helper in `ipexing.py`; the route table; `matter.ts` and `parsing.ts` at `4ed767b`.

## Open questions and unresolved tensions

1. **The signify-ts pin names a dormant branch.** `upstream/development` has not moved since 2024-04-12 while `upstream/main` is current. Any `[K]` claim anchored at `4c0072f62` is a claim about April 2024. `refresh/sources.yaml` is a reviewed field and this pass did not change it; the retarget is proposed in the PR body. **Until it is retargeted, this note's signify-ts claims are pinned to `ffba8406e` and say so, which is a divergence between the note and the manifest that a reader should know about.**
2. **What tier do fork-branch implementations get?** §10e and §10f coin `[K-fork]` for "code at a named commit on an unmerged personal fork". The existing ladder has no rung for it: it is not `[K]` (no implementation anyone runs behaves this way), not `[P]` (it is code, not a proposal), and not `[N1.1]` (it is not a spec). The marker is provisional and needs a decision — either adopt it corpus-wide with a definition in the tier key, or rule that fork branches are not citable at all and cut §10e and §10f. **They must not be silently read as `[K]`.**
3. **The variable-size rejection comment does not describe its own repo.** `parsing.ts:258-261` justifies the fix by asserting the Sizes tables "store that as null", but signify-ts's tables store `undefined` (`matter.ts:206`, `indexer.ts:202`); keripy's use `None`. Either the comment was written against keripy's tables and carried over, or there is a table entry not found. The code is defensible as defense-in-depth; the stated reason is not accurate for this codebase. Unresolved.
4. **Does anything downstream depend on freshness that the protocol does not provide?** The timestamp is signed, carried, and never checked. A deployment that assumes the agent rejects stale requests would be wrong, but nothing in either codebase documents the assumption either way. Whether any deployed system relies on it is outside what code reading can settle.
5. **Are the `endrole`/`locscheme` `tsg` sites the last stragglers?** Fourteen sites already used `lastEst`; two did not and were fixed. No systematic audit was done to confirm no third class of site still seals to the latest event rather than the latest establishment event. Worth a sweep on the next pass.
6. **§7a's default-field order asymmetry remains unverified**, as it was in the original note, and the code has since moved. The original gap statement stands unresolved and is now additionally stale.

## Gaps / not covered
- **protocol.md is unfinished**: several sections are stubs — "Reconnecting to Existing Agent Worker," "Salty Key Salt Rotations," "Sandy Keys," and the actual `Signify-Resource`/`Signify-Timestamp`/`Signature-Input`/`Signature` header wire-format sections all say "Document ... here." The authoritative header byte-format lives in code, not prose.
- **Default-field ORDER asymmetry** between `authing.ts` (`@method` first) and `authing.py` (`Signify-Resource` first) is unverified as harmless; I reasoned it's driven by the emitted `Signature-Input` header, but did not trace a full sign→verify round-trip to prove byte-identical `ser` across langs. Flag for a synthesizer/verifier.
- Did not deep-read **`end/ending.ts`** vs keripy `keri.end.ending` — the two independent message-signature implementations that most need line-level diffing for interop.
- Did not read **grouping/delegating/exchanging** modules in depth (multisig ceremony, IPEX state machine) — only the boundary touchpoints.
- **CESR core** (matter/counter/indexer/serder tables) not audited for code-table parity, which is the deepest interop layer (the qb64 derivation-code tables must be identical across all four impls).
- KERIA `specing.py` / the actual OpenAPI `spec.yaml` not read — it is the formal admin-API contract and would firm up every endpoint schema.
- No coverage of **witness/watcher** doctrine here (belongs to keripy sources); KERIA treats witnessing as async ops (`Witnesser`, `Receiptor`) but the threat-model doctrine of witnesses/watchers is upstream.
