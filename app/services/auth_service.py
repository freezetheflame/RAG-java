import uuid

from flask import Blueprint, request, jsonify

from app.models.user import User


def register_user(data):
    username = data['username']
    password = data['password']
    email = data['email']
    user_type = data['user_type']

    new_user = User()