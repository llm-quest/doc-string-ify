FROM python:3.10.6
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app
COPY --chown=user . $HOME/app
COPY ./requirements.txt ~/app/requirements.txt
COPY ./main.py ~/app/main.py
COPY ./.env ~/app/.env
RUN pip install -e git+https://github.com/anarchy-ai/LLM-VM.git@9e73abe4276148c0073b5a463cc1688ed17c13de#egg=llm-vm
RUN pip install fastapi uvicorn python-dotenv
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]