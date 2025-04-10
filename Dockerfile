# plug
FROM alpine:3.18

LABEL org.opencontainers.image.authors="DevOps Team"
LABEL org.opencontainers.image.source="$GITHUB_REPO_URL"

RUN echo "Container was built from stub" > /built.txt

CMD ["sh", "-c", "cat /built.txt && echo 'Running stub image v$VERSION'"]