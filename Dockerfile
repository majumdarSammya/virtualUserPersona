# Initialises a new build stage and sets the base image for subsequent instructions.
FROM python:3.10-slim

# Sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions.
WORKDIR /app

# Copy the entire app to the container
COPY . .

# Executes commands in a new layer on top of the current image and commits the results.
# Installs all Python dependencies from requirements file in the container.
RUN pip install -r requirements.txt

# Informs Docker that the container listens on the specified network ports at runtime. This is Streamlit's default port.
EXPOSE 8501

# Tells Docker how to test a container to check that it is still working. 
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
# Configures a container that will run as an executable.
# Contains streamlit run command so it does not need to be called from command line.
ENTRYPOINT ["streamlit", "run", "dataModeller.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]