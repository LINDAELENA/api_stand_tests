import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(first_name): #Función de prueba positiva
    user_body = get_user_body(first_name) #Cuerpo de la solicitud actualizada
    user_response = sender_stand_request.post_new_user(user_body) #Resultado de la solicitud para crear un nuevo usuario

    assert user_response.status_code == 201 #Comprueba código del estado
    assert user_response.json()["authToken"] != "" #Comprueba que hay authToken y tiene un valor

    users_table_response = sender_stand_request.get_users_table()
    #Resultado de la solicitud de recepción de datos de la tabla "user_model"

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    #String que debe estar en el cuerpo de la respuesta

    assert users_table_response.text.count(str_user) == 1 #Comprueba si el usuario existe y es único

#Función de prueba negativa
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name) #Cuerpo de la solicitud actualizada
    response = sender_stand_request.post_new_user(user_body) #Guarda el resultado de llamar a get_user_body(first_name)

    assert response.status_code == 400 #Comprueba si la respuesta contiene código 400
    assert response.json()["code"] == 400 #Comprueba si el atributo "code" en el cuerpo de respuesta es 400
    assert response.json()["message"] == "El nombre que ingresaste es incorrecto. " \
                                         "Los nombres solo pueden contener caracteres latinos, "\
                                         "los nombres deben tener al menos 2 caracteres y no más de 15 caracteres"

#Función negativa. Mensaje de error "No se han enviado todos los parámetros requeridos"
def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body) #Guarda el resultado de llamar a la función a "response"

    assert response.status_code == 400 #Comprueba si la respuesta contiene código 400
    assert response.json()["code"] == 400 #Comprueba si el atributo "code" contiene 400 en el cuerpo de respuesta
    assert response.json()["message"] == "No se enviaron todos los parámetros requeridos"


#Prueba 1. Nuevo usuario, "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

#Prueba 2. Nuevo usuario, "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

#Prueba 3. "FirstName" contiene un caracter.
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

#Prueba 4. "FirstName" contiene 16 caracteres.
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

#Prueba 5. "FirstName" contiene espacios.
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")

#Prueba 6. "FirstName" contiene caracteres especiales.
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

#Prueba 7. "FirstName" contiene números.
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

#Prueba 8. La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy() #Copia el diccionario con el cuerpo de la solicitud desde el archivo "data"
    user_body.pop("firstName") #Se elimina el parámetro "firstName" de la solicitud
    negative_assert_no_firstname(user_body) #Comprueba la respuesta

#Prueba 9. El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("") #Guarda el cuerpo de la solicitud actualizada
    negative_assert_no_firstname(user_body) #Comprueba la respuesta

#Prueba 10. El tipo del parámetro "firstName" es un número
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12) #Guarda el cuerpo de la solicitud actualizada
    response = sender_stand_request.post_new_user(user_body) #Guarda el resultado de la solicitud para crear un nuevo usuario

    assert response.status_code == 400 #Comprueba si el código de estado de la respuesta es 400