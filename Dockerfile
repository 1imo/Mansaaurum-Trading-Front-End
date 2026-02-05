FROM nginx:alpine

# Copy static files to nginx html directory
COPY index.html /usr/share/nginx/html/
COPY scripts.js /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY sitemap.xml /usr/share/nginx/html/
COPY robots.txt /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/

# Create custom nginx config to run on port 4003
RUN echo 'server { \
    listen 4003; \
    server_name _; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Expose port 4003
EXPOSE 4003

CMD ["nginx", "-g", "daemon off;"]
