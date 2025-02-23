import pytest

@pytest.fixture
def list_creator(incoming_list):
    for index in range(len(incoming_list)):
        incoming_list[index] = int(incoming_list[index])
    return incoming_list