# Use an official Node.js runtime as a base image
FROM node:20-alpine as builder
FROM node:20-alpine as builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install Angular CLI globally
# Install Angular CLI globally
RUN npm install -g @angular/cli

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the Angular app
RUN ng build

# Use a lightweight Node.js image for the final stage
FROM nginx:alpine

# copy the custom nginx configuration file to the container in the
# default location
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the built Angular app to the nginx server directory
COPY --from=builder /app/dist/ia-frontp/browser /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Command to start nginx server
CMD ["nginx", "-g", "daemon off;"]
