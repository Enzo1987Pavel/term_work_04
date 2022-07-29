import base64
import hashlib

import calendar
import datetime
from os import abort

import jwt

from flask import current_app


def __generate_password_digest(password: str) -> bytes:
	return hashlib.pbkdf2_hmac(
		hash_name="sha256",
		password=password.encode("utf-8"),
		salt=current_app.config["PWD_HASH_SALT"],
		iterations=current_app.config["PWD_HASH_ITERATIONS"],
	)


def generate_password_hash(password: str) -> str:
	return base64.b64encode(__generate_password_digest(password)).decode('utf-8')

# compose_passwords


def compare_passwords_hash(password_hash, other_password) -> bool:
	"""
	Метод возвращает сравнение бинарных последовательностей чисел(из базы данных 'password_hash'
	и сгенерированный 'other_password'), возвращает либо True либо False
	 """
	return password_hash == generate_password_hash(other_password)


def generate_tokens(email, password, password_hash=None, is_refresh=False):
	"""
	Метод, который генерирует access_token и refresh_token, получая email и пароль пользователя
	с проверкой is_refresh (создание новых токенов, а не генерирование refresh_token)
	"""

	# if email is None:
	# 	raise abort()
	#
	# if not is_refresh:
	# 	if not compare_passwords_hash(password, password_hash):
	# 		raise abort()

	data = {
		"email": email,
		"password": password
	}
	# 15 min for access_token
	min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
	data["exp"] = calendar.timegm(min15.timetuple())
	access_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGORITHM"])

	# 130 days for refresh_token
	days130 = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config["TOKEN_EXPIRE_DAYS"])
	data["exp"] = calendar.timegm(days130.timetuple())
	refresh_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGORITHM"])

	return {
		"access_token": access_token,
		"refresh_token": refresh_token
	}


def approve_refresh_token(refresh_token):
	"""
	Получаем информацию о пользователе, извлекает значение 'email' и 'password'.
	 Если токен обновлен 'refresh_token = True', то генерируем новый токен
	"""
	data = jwt.decode(jwt=refresh_token, key=current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGORITHM"]])
	email = data.get("email")
	password = data.get("password")

	return generate_tokens(email, password, is_refresh=True)


def get_data_from_token(refresh_token):
	"""
	Получаем информацию из обновленного токена
	"""
	try:
		data = jwt.decode(jwt=refresh_token, key=current_app.config["SECRET_KEY"], algorithms={current_app.config['ALGORITHM']})
		return data
	except Exception:
		return "No data!"
