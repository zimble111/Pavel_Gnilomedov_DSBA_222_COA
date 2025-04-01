#!/bin/bash

API=http://localhost:8000

echo "=== Register user ==="
curl -s -X POST "$API/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"login":"curluser","password":"123456","email":"curluser@example.com"}' \
  | jq

echo "=== Login ==="
TOKEN=$(curl -s -X POST "$API/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"login":"curluser","password":"123456"}' \
  | jq -r .access_token)

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
  echo "❌ Failed to log in"
  exit 1
fi

echo "✅ Got token: $TOKEN"

echo "=== Create post ==="
POST=$(curl -s -X POST "$API/api/v1/posts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Curl Post",
    "description": "Generated via curl",
    "is_private": false,
    "tags": ["curl", "script"]
}' | jq)

POST_ID=$(echo "$POST" | jq -r .id)
echo "✅ Created post with ID: $POST_ID"

echo "=== Get post by ID ==="
curl -s -X GET "$API/api/v1/posts/$POST_ID" \
  -H "Authorization: Bearer $TOKEN" | jq

echo "=== List posts ==="
curl -s -X GET "$API/api/v1/posts?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN" | jq

echo "=== Update post ==="
curl -s -X PUT "$API/api/v1/posts/$POST_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Curl Post",
    "description": "Now updated!",
    "is_private": true,
    "tags": ["updated"]
}' | jq

echo "=== Delete post ==="
curl -s -X DELETE "$API/api/v1/posts/$POST_ID" \
  -H "Authorization: Bearer $TOKEN"

echo "✅ Done."
