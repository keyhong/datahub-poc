import datahub.emitter.mce_builder as builder
from datahub.emitter.rest_emitter import DatahubRestEmitter


# Create an emitter to the GMS REST API.
emitter = DatahubRestEmitter(
    gms_server="http://datahub-gms:8080",
    token="eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6ImFhNjE1ZWZmLWFmMDktNGM1OS05MjFiLTEzNjE0YjdiYmEwNSIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3MjY3MjYwNTksImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9._gn9ekfBkDk-j7adE0B4CGZ2brb_a1gHUGNZk7o9zy8",
)

# Test the connection
emitter.test_connection()

# Construct a lineage object.
lineage_mce = builder.make_lineage_mce(
    upstream_urns=[
        "urn:li:dataset:(urn:li:dataPlatform:postgres,dw.public.enrollments,PROD)",  # Upstream 1
        "urn:li:dataset:(urn:li:dataPlatform:hive,fct_users_deleted,PROD)",  # Upstream 2
    ],
    downstream_urn=builder.make_dataset_urn("hive", "logging_events"),  # Downstream
)

# Emit metadata!
emitter.emit_mce(lineage_mce)


# from typing import List


# upstream_table_1 = UpstreamClass(
#     dataset=builder.make_dataset_urn("bigquery", "upstream_table_1", "PROD"),
#     type=DatasetLineageTypeClass.TRANSFORMED,
# )
# upstream_tables: List[UpstreamClass] = [upstream_table_1]
# upstream_table_2 = UpstreamClass(
#     dataset=builder.make_dataset_urn("bigquery", "upstream_table_2", "PROD"),
#     type=DatasetLineageTypeClass.TRANSFORMED,
# )
# upstream_tables.append(upstream_table_2)

# # Construct a lineage object.
# upstream_lineage = UpstreamLineage(upstreams=upstream_tables)

# # Construct a MetadataChangeProposalWrapper object.
# lineage_mcp = MetadataChangeProposalWrapper(
#     entityUrn=builder.make_dataset_urn("bigquery", "downstream"),
#     aspect=upstream_lineage,
# )

# # Emit metadata!
# emitter.emit_mce(lineage_mcp)

# Emit metadata!
# curl --location --request POST 'datahub-gms:8080/api/graphql' \
# --header 'Authorization: Bearer ' \
# --header 'Content-Type: application/json'
# --data-raw '{ "query": "mutation updateLineage { updateLineage( input:{ edgesToAdd : { downstreamUrn: "urn:li:dataset:(urn:li:dataPlatform:postgres,dw.public.enrollments,PROD)", upstreamUrn : "urn:li:dataset:(urn:li:dataPlatform:postgres,dw.public.students,PROD)"}, edgesToRemove :{}", "variables":{}}'


# curl -X POST 'http://datahub-gms:8080/api/graphql' \
# --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6ImFhNjE1ZWZmLWFmMDktNGM1OS05MjFiLTEzNjE0YjdiYmEwNSIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3MjY3MjYwNTksImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9._gn9ekfBkDk-j7adE0B4CGZ2brb_a1gHUGNZk7o9zy8' \
# --header 'Content-Type: application/json' \
# --data-raw '{"query":"{\n  me {\n    corpUser {\n        username\n    }\n  }\n}","variables":{}}'


