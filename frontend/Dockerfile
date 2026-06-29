# Stage 1: Build the React Application
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first to leverage Docker layer caching
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the React application (outputs to /app/dist)
RUN npm run build

# Stage 2: Serve the Application
FROM nginxinc/nginx-unprivileged:alpine AS runner

# Copy custom Nginx config if needed (optional)
# COPY nginx.conf /etc/nginx/nginx.conf

# Copy static build output from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Run as non-root user for security
USER nginx

# Expose port 8080 (standard for unprivileged nginx)
EXPOSE 8080

# Start Nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]   