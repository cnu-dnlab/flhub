import json
import urllib.request
import urllib.parse

from flask import Flask, render_template, url_for, request, redirect, Blueprint

app = Flask(__name__)
