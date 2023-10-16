-- Create model_log table
CREATE TABLE model_log (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_name VARCHAR(255) NOT NULL,
    version_id VARCHAR(255) NOT NULL,
    metadata JSON
);

-- Create pending_models table
CREATE TABLE pending_models (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_name VARCHAR(255) NOT NULL,
    version_id VARCHAR(255) NOT NULL,
    metadata JSON
);

-- Create run log table
CREATE TABLE run_log (
    run_id VARCHAR(255) PRIMARY KEY,
    run_start_time TIMESTAMP,
    run_duration_ms INT,
    run_type VARCHAR(255),
    model_name VARCHAR(255),
    model_version_id VARCHAR(255),
    run_metadata JSONB NOT NULL
);

-- View to get the latest model version for each model
CREATE OR REPLACE VIEW current_production_model AS
WITH LatestEntries AS (
    SELECT model_name, MAX(created_at) as latest_created_at
    FROM model_log
    GROUP BY model_name
)
SELECT ml.*
FROM model_log ml
JOIN LatestEntries le ON ml.model_name = le.model_name AND ml.created_at = le.latest_created_at;