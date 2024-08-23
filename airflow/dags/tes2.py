# Inlined from /metadata-ingestion/examples/library/lineage_emitter_dataset_finegrained_sample.py
import datahub.emitter.mce_builder as builder
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.com.linkedin.pegasus2avro.dataset import (
    DatasetLineageType,
    FineGrainedLineage,
    FineGrainedLineageDownstreamType,
    FineGrainedLineageUpstreamType,
    Upstream,
    UpstreamLineage,
)

from datahub_airflow_plugin.entities import Dataset, Urn


def datasetUrn(tbl):
    return builder.make_dataset_urn("hive", tbl)

def datasetUrn2(tbl):
    return builder.make_dataset_urn("postgres", tbl)


def fldUrn(tbl, fld):
    return builder.make_schema_field_urn(datasetUrn(tbl), fld)

def fldUrn2(tbl, fld):
    return builder.make_schema_field_urn(datasetUrn(tbl), fld)


fineGrainedLineages = [
    FineGrainedLineage(
        upstreamType=FineGrainedLineageUpstreamType.FIELD_SET,
        upstreams="urn:li:schemaField:(urn:li:dataset:(urn:li:dataPlatform:postgres,dw.public.enrollments,PROD),enrollment_id)",
        downstreamType=FineGrainedLineageDownstreamType.FIELD,
        downstreams=[fldUrn("logging_events", "browser")],
    ),
]


# this is just to check if any conflicts with existing Upstream, particularly the DownstreamOf relationship
upstream = Upstream(
    dataset="urn:li:dataset:(urn:li:dataPlatform:hive,fct_users_deleted,PROD)",
    type=DatasetLineageType.TRANSFORMED,
)

fieldLineages = UpstreamLineage(
    upstreams=[upstream], fineGrainedLineages=fineGrainedLineages
)

lineageMcp = MetadataChangeProposalWrapper(
    entityUrn=datasetUrn("logging_events"),
    aspect=fieldLineages,
)

# Create an emitter to the GMS REST API.
# Create an emitter to the GMS REST API.
emitter = DatahubRestEmitter(
    gms_server="http://datahub-gms:8080",
    token="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6ImFhNjE1ZWZmLWFmMDktNGM1OS05MjFiLTEzNjE0YjdiYmEwNSIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3MjY3MjYwNTksImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9._gn9ekfBkDk-j7adE0B4CGZ2brb_a1gHUGNZk7o9zy8",
)

# Emit metadata!
emitter.emit_mcp(lineageMcp)
