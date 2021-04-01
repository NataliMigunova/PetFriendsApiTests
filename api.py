import requests
from requests_toolbelt import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/api"

    def get_api_key(self, email, password):
        """
        Calls API top get valid access key
        :param email: existing user email
        :param password: existing user password
        :return: map with param 'key' which contains auth key
        """

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + '/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key):
        """
        Returns a list of all pets
        :param auth_key: valid auth key
        :return: full list of pets
        """
        headers = {
            'auth_key': auth_key['key']
        }
        res = requests.get(self.base_url + '/pets', headers=headers)
        return self.formatResponse(res)

    def add_new_pet(self, auth_key, name, animal_type, age, photo_name):
        """
        Creates new pet
        :param auth_key: valid auth key
        :param name: pet name
        :param animal_type: pet animal type
        :param age: pet age
        :param photo_name: image name from ./images folder
        :return: pet object contains full info about the pet
        """
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': str(age),
                'pet_photo': (photo_name, open('./images/' + photo_name, 'rb'), 'image/png')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/pets', data=data, headers=headers)
        return self.formatResponse(res)

    def delete_existing_pet(self, auth_key, pet_id):
        """
        Deletes existing pet
        :param auth_key: valid auth key
        :param pet_id: existing pet id
        :return: status code with empty response
        """
        headers = {
            'auth_key': auth_key['key']
        }
        res = requests.delete(self.base_url + '/pets/{}'.format(pet_id), headers=headers)
        return self.formatResponse(res)

    def update_pet_info(self, auth_key, pet_id, name, animal_type, age):
        """
        Updates existing pet
        :param auth_key: valid auth key
        :param pet_id: existing pet id
        :param name: updated name
        :param animal_type: updated animal type
        :param age: updated age
        :return: updated pet object
        """
        headers = {
            'auth_key': auth_key['key']
        }
        params = {
            'pet_id': pet_id,
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(self.base_url + '/pets/{}'.format(pet_id), params=params, headers=headers)
        return self.formatResponse(res)



    def formatResponse(self, res):
        """
        Formats response to JSON/TEXT and extracting status to avoid code duplication
        :param res:
        :return:
        """
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
