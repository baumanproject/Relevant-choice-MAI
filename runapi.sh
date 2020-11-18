docker build -t pdf_reader .; docker run -d -p 8080:8080 -v /home/ubuntu/PDF/Relevant-choice-MAI/logs:/opt/lib/logs pdf_reader "api.py" "--path" "/opt/lib/config/input_docker.json"
