import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
import random


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def getFact():
    facts = ["The world's oldest trees are 4,600 year old Bristlecone pines in the USA.",
    "An aluminum can may be recycled ad infinitum (forever!).",
    "Every day, American businesses generate enough paper to circle the earth 20 times!",
    "A modern glass bottle takes 4000 years or more to decompose.",
    "Rainforests are being cut down at the rate of 100 acres per minute.",
    "We have explored more of Space than our terrestrial oceans.",
    "If the entire world’s Ice melted, our sea levels will rise by 66 meters.",
    "The five warmest years on record have occurred in the last decade.",
    "Just 10 percent of the world’s plant-rich areas are protected.",
    " 70,000 plant species are utilized for medicine.",
    "68 percent of plants are in danger of going extinct.",
    "Bamboo is the fastest-growing woody plant in the world;",
    "Small pockets of air inside cranberries cause them to bounce and float in water.",
    "The first potatoes were cultivated in Peru about 7,000 years ago",
    "Trees are the longest-living organisms on earth.",
    "Peanuts are not nuts, but legumes related to beans and lentils. ",
    "84% of a raw apple and 96% of a raw cucumber is water.",
    "The largest single flower is the Rafflesia or 'corpse flower'. ",
    "Several centuries ago in Holland, tulips were more valuable than gold.",
    "Broccoli is actually a flower.",
    "In the US, almost 60% of all freshly cut flowers are grown in California.",
    "Bamboos are a flowering plant, but it only flowers every few years.",
    "White flowers smell stronger than colorful ones.",
    "Sunflower seeds contain a chemical which prevents plants from growing near them.",
    "Tulips can keep growing up to an inch per day even after they are cut.",
    "The state flower for Maine is a pinecone.",
    "You can make caffeine-free coffee from dandelion leaves!",
    "There are over 300,000 known species of flowering plants.",
    "The vegetable broccoli is a flower.",
    "The very expensive spice, saffron, comes from a type of crocus flower.",
    "The juice from bluebell flowers was used historically to make glue.",
    "The flower buds of the marsh marigold are pickled as a substitute for capers.",
    "Global forests removed about one-third of fossil fuel emissions annually from 1990 to 2007.",
    ]
    return random.choice(facts)
