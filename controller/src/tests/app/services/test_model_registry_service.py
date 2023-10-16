import pytest
from unittest import mock
from app.services.model_registry_service import ModelRegistryService

@pytest.fixture
def model_name():
    return "test_model"

@pytest.fixture
def evalute_criterias(model_name):
    return {
            model_name: {
                'accuracy': {'min': 0.8},
                'loss': {'max': 0.1}
            }
        }

@pytest.fixture
def setup_model_registry_service():
    model_registry_service = ModelRegistryService(mock.MagicMock(), mock.MagicMock())
    return ModelRegistryService(mock.MagicMock(), mock.MagicMock())


@pytest.fixture
def model_registry_service(setup_model_registry_service, evalute_criterias):
    setup_model_registry_service.evalute_criterias = evalute_criterias
    return setup_model_registry_service

def test_metrics_meet_criteria(model_registry_service, model_name):
    with mock.patch('app.services.model_registry_service.log', autospec=True) as _:
        model_metadata = {'model_metrics': {'accuracy': 0.85, 'loss': 0.05}}
        
        assert model_registry_service._evaluate_model(model_name, model_metadata) == True

def test_metrics_does_not_meet_criteria(model_registry_service, model_name):
    with mock.patch('app.services.model_registry_service.log', autospec=True) as mock_log: 
        model_metadata = {'model_metrics': {'accuracy': 0.75, 'loss': 0.2}}
        
        print(model_registry_service.evalute_criterias)
        print(model_name)
        assert model_registry_service._evaluate_model(model_name, model_metadata) == False
        mock_log.warning.assert_called_with("metric accuracy is 0.75 but should be above 0.8")
        mock_log.info.assert_called_with("Model is not promoted")

def test_one_metric_does_not_meet_criteria(model_registry_service, model_name):
    with mock.patch('app.services.model_registry_service.log', autospec=True) as mock_log:
        model_metadata = {'model_metrics': {'accuracy': 0.85, 'loss': 0.15}}
        
        assert model_registry_service._evaluate_model(model_name, model_metadata) == False
        mock_log.warning.assert_called_with("metric loss is 0.15 but should be below 0.1")
        mock_log.info.assert_called_with("Model is not promoted")

def test_metric_not_in_validation_results(model_registry_service, model_name):
    with mock.patch('app.services.model_registry_service.log', autospec=True) as mock_log:
        model_metadata = {'model_metrics': {'rmse': 0.15}}
        assert model_registry_service._evaluate_model(model_name, model_metadata) == False
        mock_log.info.assert_called_with("Model is not promoted")
