import apache_beam as beam
from apache_beam.options.pipeline_options import StandardOptions, GoogleCloudOptions, SetupOptions
from apache_beam.io.gcp.pubsub import ReadFromPubSub
from apache_beam.io.gcp.bigquery import WriteToBigQuery

# Settings
PROJECT = 'GCP_PROJECT'
SUBSCRIPTION = 'PUBSUB_SUBSCRIPTION'
REGION = 'GCP_REGION'
BUCKET = 'GCS_BUCKET'
DATABASE = 'BQ_DATABASE'
TABLE = 'BQ_TABLE'

# Define options
opt = StandardOptions()
opt.streaming = True
opt.runner = 'DataflowRunner'

stp = opt.view_as(SetupOptions)
stp.requirements_file = "./requirements.txt"

gcp = opt.view_as(GoogleCloudOptions)
gcp.project = PROJECT
gcp.region = REGION
gcp.staging_location = 'gs://{bucket}/staging'.format(bucket=BUCKET)
gcp.temp_location = 'gs://{bucket}/temp'.format(bucket=BUCKET)


# Enrichment Function
def enrichment(text):
    import json, user_agents

    record = json.loads(text)

    # Add device information based on User-Agent.
    ua_obj = user_agents.parse(record['user_agent'])
    record.update({
        'er_ua_device_family': ua_obj.device.family,
        'er_ua_device_brand': ua_obj.device.brand,
        'er_ua_device_model': ua_obj.device.model,
        'er_ua_browser_family': ua_obj.browser.family,
        'er_ua_browser_version_string': ua_obj.browser.version_string,
        'er_ua_os_family': ua_obj.os.family,
        'er_ua_os_version_string': ua_obj.os.version_string,
        'er_ua_is_mobile': ua_obj.is_mobile,
        'er_ua_is_tablet': ua_obj.is_tablet,
        'er_ua_is_bot': ua_obj.is_bot,
    })

    return record


# Pipeline
pipeline = beam.Pipeline(options=opt)
(
        pipeline
        | 'subscribe' >> ReadFromPubSub(subscription='projects/{project}/subscriptions/{subscription}'.format(
            project=PROJECT, subscription=SUBSCRIPTION)
        )
        | 'modify' >> beam.Map(enrichment)
        | 'write_to_bq' >> WriteToBigQuery(
            '{project}:{database}.{table}'.format(project=PROJECT, database=DATABASE, table=TABLE)
        )
)
pipeline.run()
