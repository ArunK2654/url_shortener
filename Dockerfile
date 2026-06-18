FROM python:3.12-slim

WORKDIR /app

# copy only the required file for build
COPY /requirements.txt .

# RUN executes at build time
RUN pip install --no-cache-dir -r requirements.txt

# copy all the folders
COPY . .

# EXPOSE 8000

# CMD executes when container starts
# CMD ["executable", "arg1", "arg2"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]