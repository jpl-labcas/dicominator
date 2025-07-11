# The Dicominator

A census (and other details) of the [Early Detection Research Network](https://edrn.nci.nih.gov/)'s usage of [DICOM](https://www.dicomstandard.org/) tags throughout its flagship data search and archive product, [LabCAS](https://edrn-labcas.jpl.nasa.gov/).



## 👷 Local Building and Running

TBD.


### 🛠️ Required Tools

A Unix-like (macOS included) environment is expected. The following are required in order to run locally:

- [PostgreSQL](https://www.postgresql.org/) 17
- [Taskfile](https://taskfile.dev/) 3
- [Python](https://www.python.org/) 3.11 (later versions not supported)



### 💽 Database Setup

Use PostgreSQL 17. Run

    createdb dicominator

For the suggested schema, see: https://chatgpt.com/share/6807cd23-5f48-8003-8f25-7d7efe7d7dc3

Make any necessary database migrations with

    task manage command=makemigrations

Then apply them with

    task manage command=migrate

Finally populate the server with

    task manage command=dicominator_bloom
    task manage command=autopopulate_main_menus

And load DICOM data with

    task manage command=dicominator_load -- FOLDER [SLUG]

where `FOLDER` is a top-level folder containing DICOM files. The extension `.dcm` of the file doesn't matter; it will try to read _every_ file as a DICOM file. The `SLUG` is the slug of the `PatientIndex` that should contain everything. By default it's `patients`.

Add DICOM tag frequency data with a similar command:

    task manage command=scan_tag_frequencies -- FOLDER


### 🏃 Run the Serveer

To start the server, run

    task run

This will build the Python virtual environment if it doesn't already exist and start things up. You'll be able to visit it at http://localhost:6468

If you ever need to rebuild the Python environment, you can destory the old one with

    task clean

The next time it's needed it'll be rebuilt.


### ☑️ Other Tasks

Just type

    task --list

to see what's possible.


## 🌱 Environment Variables and Secrets

The variables are:

| Variable                 | Purpose                                  | Default                        |
|:-------------------------|:-----------------------------------------|:-------------------------------|
| `DICOMINATOR_VERSION`    | Image version                            | `latest`                       |
| `CERT_CN`                | Common name in generated TLS certificate | `edrn-docker.jpl.nasa.gov`     |
| `HTTPS_PORT`             | Listening port for `https`               | `2371`                         |
| `LDAP_URI`               | Where to find the LDAP server            | `ldaps://edrn-ds.jpl.nasa.gov` |
| `LDAP_BIND_DN`           | Distinguished name of service account    | `uid=service,dc=edrn,…`        |
| `LDAP_BIND_PASSWORD`     | Credential for service account           | (unset)                        |
| `POSTGRES_PASSWORD`      | Password to Postgres DB                  | `dicominator` on CLI or unset  |
| `SIGNING_KEY`            | Secures Django data                      | `s3cr3t` or set via `.env`     |
| `DATA_DIR`               | Persistent Docker data                   | See `docker-compose.yaml`      |

Secrets may be set in `~/.secrets/passwords.sh` or as environment variables.

| Secret               | Purpose                        | Place                             |
|:---------------------|:-------------------------------|:----------------------------------|
| `DOCKERHUB_USERNAME` | User ID in DockerHub           | `jpl-labcas` organization secrets |
| `DOCKERHUB_TOKEN`    | Token for `DOCKERHUB_USERNAME` | `jpl-labcas` organization secrets |


## 🚢 Docker

GitHub Actions takes care of automatically creating the Docker image for this.

To do it by hand:

    support/build-wheels.sh
    docker image build --tag edrndocker/dicominator:latest --file docker/Dockerfile .

Spot check:

    docker container run --env LDAP_BIND_PASSWORD=x --env SIGNING_KEY=x --rm --publish 8000:8000 edrndocker/dicominator:latest

And visiting http://localhost:8000/ should give you "Bad Request (400)".

You can then launch the composition with

    task comp-up

Populate with

    docker compose --project-name dicominator --file docker/docker-compose.yaml exec db createdb --username=postgres --encoding=UTF8 --owner=postgres dicominator
    task comp-app-exec -- /app/bin/django-admin migrate
    task comp-app-exec -- /app/bin/django-admin dicominator_bloom
    task comp-app-exec -- /app/bin/django-admin autopopulate_main_menus

You can then visit https://localhost:9999/dicominator/ (ignore the certificate warning).

## 🔎 Additional Project Details

The following details pertinent to this project are described in the remaining sections.


### 👥 Contributing

TBD.


### 🔢 Versioning

We use the [SemVer](https://semver.org/) philosophy for versioning this software. More TBD.


### 👩‍🎨 Creators

You can contact

- [Ashish Mahabal](https://github.com/AshishMahabal)
- [Sean Kelly](https://github.com/nutjob4life)


### 📃 License

The project is licensed under the [Apache version 2](LICENSE.md) license.


### 🎨 Art Credits

None at this time.
