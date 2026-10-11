# Claim-Link Generator — signing reference

## Sign (Python)
```python
import hashlib, hmac, time

def make_claim_token(email: str, secret: str, ttl_days: int = 30) -> str:
    exp = int(time.time()) + ttl_days * 24 * 3600
    payload = f"{email.strip().lower()}|{exp}"
    sig = hmac.new(secret.encode(), f"claim.{payload}".encode(),
                   hashlib.sha256).hexdigest()
    # token carries email|expiry|sig so verification needs no DB lookup
    return f"{payload}|{sig}"

def claim_url(email: str, secret: str, base: str) -> str:
    return f"{base}/claim?token={make_claim_token(email, secret)}"
```

## Verify (worker / server)
```js
async function verifyClaim(token, secret) {
  const [email, exp, sig] = String(token || '').split('|');
  if (!email || !exp || !sig) return null;
  if (Number(exp) * 1000 < Date.now()) return null; // expired
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const mac = await crypto.subtle.sign(
    'HMAC', key, new TextEncoder().encode(`claim.${email}|${exp}`));
  const hex = [...new Uint8Array(mac)].map(b => b.toString(16).padStart(2, '0')).join('');
  // constant-time compare
  if (hex.length !== sig.length) return null;
  let diff = 0;
  for (let i = 0; i < hex.length; i++) diff |= hex.charCodeAt(i) ^ sig.charCodeAt(i);
  return diff === 0 ? email : null;
}
```

## Notes
- The `"claim."` domain-separation prefix prevents cross-use if you sign
  other token types with the same secret.
- Keep tokens out of logs and analytics. Email clients are fine; server
  access logs are not — strip query strings there if you log URLs.
- On expiry, offer a one-click "resend my link" that re-sends to the same
  address (proves ownership again without an account).
