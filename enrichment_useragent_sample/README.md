# Ingestly Enrichment (User-Agent)

## Preparation

1. Create a database and a table in BigQuery. You can use `table_schema` in this repository.
2. Create a GCS bucket dedicated to this Dataflow job.
3. Create a pair of Topic & Subscription in Cloud Pub/Sub.
4. Create a Notebook within Dataflow.

## Deployment

1. Go to the Notebook in Dataflow.
2. Create `ingestly_enrichment.py` and `requirements.txt` by copy-and-paste from this repository.
3. Open a Console within Notebook then execute the following command to install required modules:

    ```sh
    !pip install PyYAML ua-parser user-agents
    ```

4. Define some variables in `ingestly_enrichment.py`:

    ```python
    # Settings
    PROJECT = 'GCP_PROJECT'
    SUBSCRIPTION = 'PUBSUB_SUBSCRIPTION'
    REGION = 'GCP_REGION'
    BUCKET = 'GCS_BUCKET'
    DATABASE = 'BQ_DATABASE'
    TABLE = 'BQ_TABLE'
    ```
5. Then, run the script and make a Dataflow job by:

    ```sh
    python ingestly_enrichment.py --machine_type n1-standard-1 --job_name ingestly_enrichment
    ```
