from datahub.configuration.config_loader import load_config_file
from datahub.ingestion.run.pipeline import Pipeline

def datahub_recipe():
    # Note that this will also resolve environment variables in the recipe.
    config = load_config_file("./recipes.yaml")

    pipeline = Pipeline.create(config)
    pipeline.run()
    pipeline.raise_from_status()

datahub_recipe()