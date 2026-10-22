#!/usr/bin/env bash
set -euo pipefail

mode="${1:-message}"
message="${2:-}"

valid_signoff() {
  printf '%s\n' "$1" | grep -Eq '^Signed-off-by: .+ <[^<>[:space:]]+@[^<>[:space:]]+>$'
}

if [[ "$mode" == "message" ]]; then
  valid_signoff "$message"
  exit $?
fi

if [[ "$mode" != "pr" ]]; then
  echo "usage: $0 message <commit-message> | pr" >&2
  exit 2
fi

: "${GITHUB_TOKEN:?GITHUB_TOKEN is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${PR_NUMBER:?PR_NUMBER is required}"

api="${GITHUB_API_URL:-https://api.github.com}"
page=1
failed=0
checked=0
skipped=0

while :; do
  response="$(curl --fail-with-body --silent --show-error \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${GITHUB_TOKEN}" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "${api}/repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}/commits?per_page=100&page=${page}")"

  count="$(jq 'length' <<<"$response")"
  [[ "$count" -eq 0 ]] && break

  while IFS=$'\t' read -r sha login author_type encoded_message; do
    message="$(printf '%s' "$encoded_message" | base64 --decode)"
    short="${sha:0:12}"

    # GitHub Apps/bots cannot make a human DCO certification. Their provenance
    # is the authenticated bot identity, so keep this exception explicit.
    if [[ "$author_type" == "Bot" || "$login" == *"[bot]" ]]; then
      echo "SKIP ${short}: automation commit by ${login:-unknown bot}"
      skipped=$((skipped + 1))
      continue
    fi

    checked=$((checked + 1))
    if valid_signoff "$message"; then
      echo "PASS ${short}: Signed-off-by trailer present"
    else
      echo "::error::Commit ${sha} is missing a valid Signed-off-by: Name <email> trailer."
      failed=1
    fi
  done < <(jq -r '.[] | [.sha, (.author.login // ""), (.author.type // ""), (.commit.message | @base64)] | @tsv' <<<"$response")

  [[ "$count" -lt 100 ]] && break
  page=$((page + 1))
done

echo "DCO summary: checked=${checked} automation_skipped=${skipped} failed=${failed}"
exit "$failed"
