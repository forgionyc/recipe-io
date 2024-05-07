# Use an official Node.js runtime as a base image
FROM node:20.9-alpine as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the Angular app
RUN npm run build --prod

# Use Nginx image as the final base image
FROM nginx:alpine

# Copy the built Angular app from the build stage to the NGINX public directory
COPY --from=build /app/dist/* /usr/share/nginx/html/

# Expose port 80
EXPOSE 9000

# Command to start NGINX server
CMD ["nginx", "-g", "daemon off;"]
