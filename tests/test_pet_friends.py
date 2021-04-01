from api import PetFriends
from settings import account_email, account_password


pf = PetFriends()

def test_get_api_key_for_valid_user(email=account_email, password=account_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

def test_get_api_key_with_wrong_creds(email='fake_email', password='fake_password'):
    status, result = pf.get_api_key(email, password)

    assert status == 403

def test_get_all_pets_with_valid_key(filter='', ):
    _, auth_key = pf.get_api_key(account_email, account_password)

    status, result = pf.get_list_of_pets(auth_key)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key():
    status, result = pf.get_list_of_pets({'key': 'fake_key'})
    assert status == 403

def test_add_new_pet_successfully():
    _, auth_key = pf.get_api_key(account_email, account_password)

    status, result = pf.add_new_pet(auth_key, 'test-pet', 'dog', 5, 'dog.png')
    assert status == 200
    assert len(result['id'] > 0)

def test_delete_existing_pet_success():
    _, auth_key = pf.get_api_key(account_email, account_password)

    status, result = pf.get_list_of_pets(auth_key)
    assert len(result['pets']) > 0

    status, result = pf.delete_existing_pet(auth_key, result['pets'][0]['id'])
    assert status == 200

def test_delete_non_existing_pet_should_return_empty_response():
    _, auth_key = pf.get_api_key(account_email, account_password)
    status, result = pf.delete_existing_pet(auth_key, 'non_existing_pet_id')
    assert status == 200
    assert len(result) == 0

def test_update_pet_success():
    _, auth_key = pf.get_api_key(account_email, account_password)
    status, pets_result = pf.get_list_of_pets(auth_key)
    assert len(pets_result['pets']) > 0

    status, result = pf.update_pet_info(auth_key, pets_result['pets'][0]['id'], 'TEST_NAME', 'dog', 10)

    assert status == 200

    assert result['id'] == pets_result['pets'][0]['id']
    assert result['age'] == '10'
    assert result['animal_type'] == 'dog'
    assert result['name'] == 'TEST_NAME'

def test_update_pet_with_non_existing_id_should_return_error():
    _, auth_key = pf.get_api_key(account_email, account_password)
    status, result = pf.update_pet_info(auth_key, 'non_existing_pet_id', 'TEST_NAME', 'dog', 10)

    assert status == 400
