FROM --platform=linux/amd64 node:20-alpine as builder
WORKDIR /RiskVision/frontend
COPY package*.json ./
RUN npm i
COPY . ./
RUN npm run build

FROM node:20-alpine
WORKDIR /RiskVision/frontend
COPY --from=builder /RiskVision/frontend/.next /RiskVision/frontend/.next
COPY --from=builder /RiskVision/frontend/node_modules /RiskVision/frontend/node_modules
COPY next.config.ts /RiskVision/frontend/next.config.ts
COPY package.json /RiskVision/frontend/package.json
COPY public /RiskVision/frontend/public

EXPOSE 3000
CMD ["npm", "start"]