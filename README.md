# mini-rag-app

Minimal RAG Application.

## Setup

This environment is setup to work on a Linux platform. Make sure to use WSL2 on windows.

- Clone this repository.

```bash
git clone https://github.com/e-hossam96/mini-rag-app.git
```

- Install developer tools for C++ package building.

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install build-essential
```

- Download and install Miniconda

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ./miniconda
```

- Activate conda `base` environment.

```bash
source ./miniconda/bin/activate
```

- Create **mini-rag** env from [YAML](./environment.yml) file

```bash
cd mini-rag-app/src
conda env create -f environment.yml
conda activate mini-rag
```

- Fill [.env.example](./.env.example) file and save it into a `.env` file.

```bash
cp .env.example .env
```

- Configure **Docker** setups to run **MongoDB** container.

  - Install `docker`. [details for linux to be added later]
  - Add your `user` to `docker` group.

  ```bash
  user@DEVICE:~$ usermod -aG docker user
  ```

  - Fill [.env.example](./docker/.env.example) file using desired `mongodb` credentials and save it into a `.env` file.

  ```bash
  cp ../docker/.env.example ../docker/.env
  ```

  - Compose the docker services. You may need to use `sudo` if it is the first time.

  ```bash
  docker compose up -d
  ```

  - You may need to reset the `mongodb` container while development. [details to be added later]

- Run the `FastAPI` server. Use the `--reload` argument only for development. A **Postman** collection is available in the [assets](./assets/mini-rag-app.postman_collection.json) directory for your help.

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
