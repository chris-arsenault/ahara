ARG PLAYWRIGHT_VERSION
FROM mcr.microsoft.com/playwright:v${PLAYWRIGHT_VERSION}-noble

ARG PNPM_VERSION=10.29.3
RUN npm install --global pnpm@${PNPM_VERSION}

ENV CI=1 HOME=/tmp
WORKDIR /workspace
