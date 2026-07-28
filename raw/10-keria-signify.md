# KERIA + Signify: Signing at the Edge — Doctrine Notes

Raw doctrine-mining notes from two source repos:
- **KERIA** (`/home/daniel/code/keria`) — the Python "KERI Agent in the cloud" (multi-tenant cloud agent).
- **signify-ts** (`/home/daniel/code/signify-ts`) — the TypeScript "edge signer" client library.

These are the two halves of the **Signify/KERIA architecture**: a custodial cloud agent that holds *no* private keys, paired with an edge client that holds *only* keys and does *all* signing. Together with keripy (Python reference) and SignifyPy, all four implementations must agree on wire formats.

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
- signify-ts `clienting.ts` `fetch()` enforces two checks on every response:
  1. `isSameAgent` — the `signify-resource` header on the response must equal the known Agent AID, else `throw new Error('message from a different remote agent')` (`signify-ts/src/keri/app/clienting.ts:240-244`).
  2. Signature verification of the response via `Authenticater.verify`, else `throw new Error('response verification failed')` (`clienting.ts:246-255`).
- On connect, the client verifies the delegation binding: the Agent's inception must anchor to the Client AID or it aborts: *"commitment to controller AID missing in agent inception event"* (`clienting.ts:166-170`).

### Pre-rotation as the firewall (post-quantum passcode recovery)
- The passcode-rotation design explicitly invokes pre-rotation as a **post-quantum-secure recovery firewall**: *"To provide post-quantum secure passcode recovery, a passcode recovery must be accompanied by partial rotation of the Client AID."* (`keria/docs/protocol.md` §Partial Client AID Rotation).
- The mechanism: the OLD rotation key (`R0`, regenerated from the old passcode) and a NEW signing key (`S0`, from the new passcode) co-sign a partial rotation; `S0` gets fractional weight `1` (full authority), `R0` gets weight `0` (no authority but proves possession) — a dual-indexed signature satisfies the prior next-key commitment (`protocol.md` §Partial Client AID Rotation, lines 209-250).
- This means recovering/changing a passcode is *cryptographically bound* to demonstrating control of the pre-committed rotation key — you cannot silently swap credentials.

### Aborted-rotation detection & lockout
- KERIA detects an interrupted passcode rotation and **locks out all other operations** until recovery completes: *"the Agent Worker will notify the client ... that a passcode rotation recovery is needed and lock out all other operations until it is completed successfully."* (`protocol.md` §Passcode Rotation Recovery). The old encrypted passcode is the recovery breadcrumb, deleted only on success.

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
- signify-ts `controller.ts` `Agent.parse` enforces, on connect:
  - inception type must be `dip` (delegated): `if (state['et'] !== Ilks.dip) throw ... 'invalid inception event type'` (`controller.ts:44-46`).
  - must have a delegator anchor: `if (!state['di']) throw new Error('no anchor to controller AID')` (`controller.ts:49-51`).
  - **exactly one** signing key, **exactly one** next key, threshold **exactly 1** for both current and next (`controller.ts:60-82`): agent inception *"can only have one key"*, *"can only have one next key"*, `invalid threshold ... must be 1`.
- KERIA side: multisig groups may **not** be an agent controller — *"multisig groups not supported as agent controller"* (`keria/src/keria/app/agenting.py:871`).

### Client AID is single-sig, transferable, one signing + one rotation key
- *"The Signify Client generates the client AID as a transferable AID with a single signing key and single rotation key"* (`protocol.md` Step One).

### Server rejects duplicate/unknown/invalid provisioning
- Boot: if `caid` already has an agent → HTTP 400 *"agent for controller {caid} already exists"* (`agenting.py:821-823`).
- Boot: the submitted `icp` must actually produce the claimed `caid`, else the agent is deleted and rejected: `if ctrlHab.pre != agent.caid: ... 'invalid icp event for caid'` (`agenting.py:834-837`).
- Identifier creation: unknown witness → 400 `'unknown witness'`; unknown delegator → 400 `'unknown delegator'` (`aiding.py:318-325`).
- Group inception: signing member must be a local AID and an actual participant, else 400 (`aiding.py:335-346`).

### Every Admin request/response must be signed (no unsigned admin traffic)
- `SignatureValidationComponent.process_request` short-circuits Falcon with **HTTP 401** if the signature fails: `resp.complete = True ... resp.status = falcon.HTTP_401` (`keria/src/keria/core/authing.py:187-189`). Only explicitly `allowed` paths (e.g. `/agent`) bypass.
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
- The Admin interface has no API keys or bearer tokens. Identity is the Client AID; proof is a fresh signature per request over `@method`, `@path`, `signify-resource`, `signify-timestamp` (`Authenticater.DefaultFields`, both languages). A stolen header set can't be replayed against a different method/path, and there is no long-lived secret to exfiltrate from the server.

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
- **Signify-Timestamp header** — signed freshness field (`httping.ts:16`).
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
- *"message from a different remote agent"* (client-side agent-impersonation guard) — `signify-ts/src/keri/app/clienting.ts:243`.
- *"commitment to controller AID missing in agent inception event"* — `clienting.ts:167-169`.
- *"multisig groups not supported as agent controller"* — `keria/src/keria/app/agenting.py:871`.
- *"This enpoint allows all KERI clients (not just Signify) to interact in a seamless way."* — `keria/README.md`, Message Router.

---

## 9. Deployment / operational doctrine (secondary but load-bearing)

- **HIO** (hierarchical async I/O) is the concurrency substrate: *"HIO is an efficient and scalable orchestration/processing mechanism that leverages queues, handlers, coroutines"* (`keria/README.md`, Agents). Each `Agent` is a `DoDoer` composed of ~15 doers (Witnesser, Delegator, ExchangeSender, Granter, Admitter, GroupRequester, Querier, Escrower, ParserDoer, etc.) (`agenting.py:362-378`).
- **All Agent DB access is through the associated Agent** (`keria/README.md`) — tenant isolation invariant; each caid gets its own `Keeper` + `Habery` + `Regery` keyed by caid.
- CORS exposes exactly the KERI/Signify headers: `cesr-attachment, cesr-date, content-type, signature, signature-input, signify-resource, signify-timestamp` (`agenting.py:57-59` and repeated).
- Agent worker modes: **dynamic** (Boot creates agents on demand) vs **static** (all workers configured at startup, Boot disabled) (`protocol.md` §KERIA Service Endpoint Interfaces).

---

## Gaps / not covered
- **protocol.md is unfinished**: several sections are stubs — "Reconnecting to Existing Agent Worker," "Salty Key Salt Rotations," "Sandy Keys," and the actual `Signify-Resource`/`Signify-Timestamp`/`Signature-Input`/`Signature` header wire-format sections all say "Document ... here." The authoritative header byte-format lives in code, not prose.
- **Default-field ORDER asymmetry** between `authing.ts` (`@method` first) and `authing.py` (`Signify-Resource` first) is unverified as harmless; I reasoned it's driven by the emitted `Signature-Input` header, but did not trace a full sign→verify round-trip to prove byte-identical `ser` across langs. Flag for a synthesizer/verifier.
- Did not deep-read **`end/ending.ts`** vs keripy `keri.end.ending` — the two independent message-signature implementations that most need line-level diffing for interop.
- Did not read **grouping/delegating/exchanging** modules in depth (multisig ceremony, IPEX state machine) — only the boundary touchpoints.
- **CESR core** (matter/counter/indexer/serder tables) not audited for code-table parity, which is the deepest interop layer (the qb64 derivation-code tables must be identical across all four impls).
- KERIA `specing.py` / the actual OpenAPI `spec.yaml` not read — it is the formal admin-API contract and would firm up every endpoint schema.
- No coverage of **witness/watcher** doctrine here (belongs to keripy sources); KERIA treats witnessing as async ops (`Witnesser`, `Receiptor`) but the threat-model doctrine of witnesses/watchers is upstream.
