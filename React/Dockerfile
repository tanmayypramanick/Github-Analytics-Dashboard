# Specify platform explicitly
FROM node:16 as builder

# Set the working directory
WORKDIR /app

# Copy only package.json and package-lock.json for dependency installation
COPY package.json package-lock.json ./

# Install dependencies efficiently
RUN npm install --production && npm cache clean --force

# Copy the application source code
COPY ./public ./public
COPY ./src ./src

# Expose the application port
EXPOSE 3000

# Command to start the application
CMD ["npm", "start"]

