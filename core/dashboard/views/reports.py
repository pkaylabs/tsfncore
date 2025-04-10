from django.shortcuts import render, redirect
from django.views import View


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages