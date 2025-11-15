FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Expose port
EXPOSE 5173

# Serve the app (for development, use preview)
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]