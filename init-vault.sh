#!/bin/sh

export VAULT_ADDR='http://vault:8200'
export VAULT_TOKEN='dev-root-token'

echo "================================================"
echo "  Medical AI Platform — Vault Setup"
echo "================================================"

echo "⏳ Checking Vault status at $VAULT_ADDR..."

# Use the 'vault' command which is already in the container
until vault status > /dev/null 2>&1; do
  echo "   ...Vault is still warming up, sleeping 2s..."
  sleep 2
done

echo "🚀 Vault is UP! Starting injection..."

# --- STEP 1: Enable KV ---
curl -s -X POST -H "X-Vault-Token: $VAULT_TOKEN" \
  -d '{"type":"kv","options":{"version":"2"}}' \
  $VAULT_ADDR/v1/sys/mounts/secret

# --- STEP 2: DATABASE_URL ---
curl -s -X POST -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data": {"value": "postgresql://postgres:svipl@db:5432/med_ai_db"}}' \
  $VAULT_ADDR/v1/secret/data/DATABASE_URL

echo "Step 2: Storing DB_ENCRYPTION_KEY..."


curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "value": "b30d1bbd99898af4eda8cd6eb67182637b886c70e584ab21026db1634077c0bf"
    }
  }' \
  $VAULT_ADDR/v1/secret/data/DB_ENCRYPTION_KEY

echo "================================"
echo "✓ DB_ENCRYPTION_KEY stored"
echo "  type:   AES-256"
echo "  size:   32 bytes / 256 bits"
echo "  format: hex (64 characters)"
echo "================================"



echo "Step 3: Storing EMAIL_HASH_KEY..."

curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "value": "eb4c18967b733d9d0a9e99e0a19fda95174777884140f608ec897e431e023160"
    }
  }' \
  $VAULT_ADDR/v1/secret/data/EMAIL_HASH_KEY

echo "================================"
echo "✓ EMAIL_HASH_KEY stored"
echo "  type:   HMAC-SHA256"
echo "  size:   32 bytes / 256 bits"
echo "  format: hex (64 characters)"
echo "================================"
echo "Step 4: Storing JWT_SECRET..."

curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "value": "5eb36eaddc7ba178c75ff3fd48e4a9b69326cc41157a156242049c520205137b"
    }
  }' \
  $VAULT_ADDR/v1/secret/data/JWT_SECRET

echo "================================"
echo "✓ JWT_SECRET stored"
echo "  type:   HMAC-SHA256"
echo "  size:   32 bytes / 256 bits"
echo "  format: base64 (44 characters)"

echo "================================"
echo "Step 5: Storing JWT_REFRESH..."

curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "value": "30ccc5def5af8933abf0c41db07ec832b90f64fe633de00f9e4d379c8b98290e"
    }
  }' \
  $VAULT_ADDR/v1/secret/data/JWT_REFRESH

echo "================================"
echo "✓ JWT_REFRESH stored"
echo "  type:   HMAC-SHA256"
echo "  size:   32 bytes / 256 bits"
echo "  format: base64 (44 characters)"
echo "================================"



echo "Step 6: Storing JWT_PRIVATE_KEY..."

curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "value": "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBd2M4OFE5eWR4TVFpSnVMeGVoNm43REVZU1RKOWs3ZVAyWHlGRnVvSlM1K2xMc1p6\nSVM1ZFpvVThRTlRHTjhVQ1p4bFRKempyWmhhNk41b0xZTnJuTktIaUpVT3VoenlzVGUzaEFEWnpnVy94UERN\ncW9YVTNJRTBFTUNQdzdxWWtJVFRvNmkyb1pkd3VyRkJXU1Mxa0dwWWNhVGk5MC9hVTgwa2JkNUwvMk1zeS8z\nWFlxVjFuWFd2MXhPN0NMZkhNSUdDNE1OWHJUVUFFc3I1c2hNM08yWVdPNmpjaExDSVhiQTdtQUNLZlpHY2Uw\najBlRFR6dXpCN3FqQ05LREIYJ37hmz7RACQ+TneJRRbs9yZQxmc+pfNqhui+ipiWLQynRUntYMpGnFJ63E++\nb7osA8FfvcoGktE26en9DMPf4jLS0tLS1FTkQgUlNBIFBSSVZBVEUgS0VZLS0tLS0="
    }
  }' \
  $VAULT_ADDR/v1/secret/data/JWT_PRIVATE_KEY

echo "================================"
echo "✓ JWT_PRIVATE_KEY stored"
echo "  type:   RSA"
echo "  size:   2048 bits"
echo "  format: PEM encoded as base64"
echo "================================"


echo "Step 7: Storing JWT_PUBLIC_KEY..."

curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "value": "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF3Yzg4UTl5ZHhNUWlKdUx4ZWg2bg03REVZU1RKOWs3ZVAyWHlGRnVvSlM1K2xMc1p6SVM1ZFpvVThRTlRHTjhVQ1p4bFRKempyWmhhNk41b0xZTnJu\nTktIaUpVT3VoenlzVGUzaEFEWnpnVy94UERNZ29YVTNJRTBFTUNQD3dxWWtJVFRvNmkyb1pkd3VyRkJXU1Mx\na0dwWWNhVGk5MC9hVTgwa2JkNUwvMk1zeS8zWFlxVjFuWFd2MXhPN0NMZkhNSUdDNE1OWHJUVUFFc3I1c2hN\nM08yWVdPNmpjaExDSVhiQTdtQUtmcFpHY2UwajBlRFR6dXpCN3FqQ05LREIYMQ==\nLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t"
    }
  }' \
  $VAULT_ADDR/v1/secret/data/JWT_PUBLIC_KEY

echo "================================"
echo "✓ JWT_PUBLIC_KEY stored"
echo "  type:   RSA"
echo "  size:   2048 bits"
echo "  format: PEM encoded as base64"
echo "================================"

echo "Step 8: Storing FIREBASE_CREDENTIALS..."

curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "service_account",
      "FIREBASE_PROJECT_ID": "mono-246c1",
      "FIREBASE_PRIVATE_KEY_ID": "b1c445ad507afe88623f3eb8c290b59f0ea65d5c",
      "FIREBASE_PRIVATE_KEY": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCl+z/rPBIoc6Fd\nbBP3ahvkXNVjdxC7ZfjCwRs8T7U7WpevGN7AUmsfzm3HkNyJqm8E/+bskeNwiM92\nzIRzLMcSsNmufiBNDdtcTyfOF8k4glMStC7LEgbPm1ZeG3n9EAbKtYmXhfWIuxoQ\nCaCUr4NRwUXCNN9j2JOSCHRgmj0I30ekMOrIR9XyL07ewx/YrttLNwU1Q/02GiZf\n2Y9qHMrtT0JUoF0ujj3Jf9+FdCeUbFc0HFgcW0bp2U406VABMqVb9N42o1zeUie4\nhrgxsd/fQENV5KoJvAD2u17S5jE+sfdEAd3cznV9/V2tolDKbDVzPQ0MHvdilzY3\n4h4y2P1DAgMBAAECggEAEksRrWRuf+TWmQxLWw5nypBsuEysHGtNsnFEBi6mw8bl\nRtgP3NR4mAXRVZhipg2RtNRbaCFgFswNSYOa6XK68hVpuHCQMM3hKlhTA8TdWYwL\nidkv+xOeio0NRMv0cu6sQPUnF/scp5gvdCsLdretWnpZrODU6hU5lnO2F9uH9I0x\n0NB31vyPjrdjm3V+AausG5a05MNEoEm5RTjjeBvLHvZthwxpBMI3tj30Fx2soTqi\n4Rd7Bh1txC6TMMSz5SfSGUhuxs+L4zOewHST21MI+K5oTsc5uLoFfwBOKne2y8T7\nFtyu31NZKdF+kdiVxvTPHvnniVkSgxNRJFIp/HpokQKBgQDPhNNF5rz4qjn3uInJ\nbYNBtOPiKyN+0mcFHMMbBqo86jlBdqOOKnxrDcHhKPob98hfUvxFTAZ59BMz0lII\ncp4dVDjqo6Z5p63UDZtt4aJ92F6LtFz3TERSnz1SOPbiUwIyzXo4kRtBuseNY0qi\nJE1/lagFrcsTExaAJZ5/RHtfWQKBgQDMwi2Gj8xXsGioh8H8mht7RlaFscNxnEnq\n0xWUW4jW/xjSR25B19RHUoaV3/DSVyoB4j8m/qx9OoUWr9voZjiw9mJQ0HgGYZR8\nWk/CHH7NmrvUcGNaIs5miOfx69imusi5TeK02sXc7EO6jVvFfXJjFHIruS4mlR4a\nWb2RKB9p+wKBgHptWld68TGi+9/xtxhmy3EQTwE3ghFn/+88ML7ZB8Y4SN8eJw/Q\ncOaXjzJPAn9Nh6D1TG91kryQCmQgSNVDCZU0AwAq3CQZkKvx+yiwXTTxWZYCKnab\nQBOebob7pGuRnVJrdxe4Q+RbVS9MzNMrp60FlcMD7TKrqDKh/wgGVuLBAoGAIJL7\nnx6dSY38+GKwj7kMii4Ecbx39UkB0WPHWRS+zkVC86D9f2gQk1AjrRA1RaEsQ6R0\nm4WEd1+p8JQFjhFFD5ICzgx8K7e2YZoUejMCUT8+hmtiwuIqp9E75Ra6Hrw0VpZ3\nbIIpXB4SIEmAwghU/EIyb5ZEK0spwNNp/v+9D6UCgYEAixO6LjGC//Tr+e2BwQ0j\nwEnGeAZJNkc3udgQYRuduWtjPtLERFn1152xrcTKWNqwYsl01apDFP1RnA6dstGV\nN79KgKyUBkOUoY8SgM1W2xGxz+2wbyUHlqKRGs0l/N4L2/bMBnGmncUXkHe9X7kR\n3gUojHzWvlvALKLmagA39uk=\n-----END PRIVATE KEY-----\n",
      "FIREBASE_CLIENT_EMAIL": "firebase-adminsdk-fbsvc@mono-246c1.iam.gserviceaccount.com",
      "client_id": "118098019665741603700",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token"
    }
  }' \
  $VAULT_ADDR/v1/secret/data/FIREBASE_CREDENTIALS

echo "================================"
echo "✓ FIREBASE_CREDENTIALS stored"
echo "  type:   JSON service account"
echo "  note:   replace with real Firebase credentials"
echo "================================"

echo "Step 9: Storing GCP config..."

curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "GOOGLE_CLOUD_PROJECT": "med-ai-project"
    }
  }' \
  $VAULT_ADDR/v1/secret/data/GOOGLE_CLOUD_PROJECT

curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "value": "med-ai-project"
    }
  }' \
  $VAULT_ADDR/v1/secret/data/GCP_PROJECT_ID

curl -s -X POST \
  -H "X-Vault-Token: $VAULT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "value": "med-ai-reports"
    }
  }' \
  $VAULT_ADDR/v1/secret/data/REPORTS_BUCKET_NAME

echo "✓ GCP config stored"

# ─── STEP 10: VERIFY ALL SECRETS ─────────────────────
echo ""
echo "================================================"
echo "  Verifying all secrets stored correctly..."
echo "================================================"



# ─── STEP 10: VERIFY ALL SECRETS ─────────────────────
echo ""
echo "================================================"
echo "  Verifying all secrets stored correctly..."
echo "================================================"

# Replace the array with this:
secrets="DB_ENCRYPTION_KEY EMAIL_HASH_KEY JWT_SECRET JWT_REFRESH JWT_PRIVATE_KEY JWT_PUBLIC_KEY FIREBASE_CREDENTIALS GCP_PROJECT_ID REPORTS_BUCKET_NAME"

for secret in $secrets; do
  response=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "X-Vault-Token: $VAULT_TOKEN" \
    $VAULT_ADDR/v1/secret/data/$secret)
  
  if [ "$response" = "200" ]; then
    echo "✓ $secret"
  else
    echo "✗ $secret FAILED (HTTP $response)"
  fi
done

echo ""
echo "================================================"
echo "  Setup complete"
echo "================================================"
echo ""
echo "IMPORTANT REMINDERS:"
echo "  1. Replace fake keys with real generated keys"
echo "  2. Replace Firebase credentials with real ones"
echo "  3. Never commit .env file to git"
echo "  4. These are LOCAL DEV keys only"
echo ""