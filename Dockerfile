# Use the official PostgreSQL image from the Docker Hub
FROM postgres:13

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=autograb_user
ENV POSTGRES_PASSWORD=autograb_password
ENV POSTGRES_DB=autograb_db

# Copy the initialization script and SQL script to the Docker image
COPY init-db.sh /docker-entrypoint-initdb.d/init-db.sh
COPY data.sql /docker-entrypoint-initdb.d/data.sql

# Ensure the initialization script is executable
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

# Expose the PostgreSQL port
EXPOSE 5432
