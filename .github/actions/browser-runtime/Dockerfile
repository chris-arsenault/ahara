ARG PLAYWRIGHT_VERSION
FROM mcr.microsoft.com/playwright:v${PLAYWRIGHT_VERSION}-noble

ARG PNPM_VERSION
RUN npm install --global pnpm@${PNPM_VERSION}

ENV CI=1 HOME=/tmp
WORKDIR /workspace
