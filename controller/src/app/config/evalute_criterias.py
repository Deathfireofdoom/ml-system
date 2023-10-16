"""
This is a dict that contains the criterias that will be used to
determine if a new model should be promoted or not.

Due to time constraints I put it in a dict, which works but is not
ideal. Better solution could be a yaml file.

Maybe it should not even reside in this repo, since the code for the pipeline
is in "another" repo. 

But the idea is the same.
"""


EVALUATE_CRITERIAS = {
    "forecast_model": {
        "rmse": {
            "max": 12.0,
        },
    }
}
