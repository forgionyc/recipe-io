# Use an official Node.js runtime as a base image
FROM node:20.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

RUN npm install -g @angular/cli

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the Angular app
CMD ["ng", "serve", "--host", "0.0.0.0", "--port", "8080"]


