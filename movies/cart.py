from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect


class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, movie, quantity=1, action=None):
        """
        Add a product to the cart or update its quantity.
        """
        id = movie.id
        newItem = True
        if str(movie.id) not in self.cart.keys():

            self.cart[movie.id] = {
                'userid': self.request.user.id,
                'movie_id': id,
                'title': movie.title,
                'quantity': 1,
                'tagline': movie.tagline,
                'image': movie.image.url
            }
        else:
            newItem = True

            for key, value in self.cart.items():
                if key == str(movie.id):

                    value['quantity'] = value['quantity'] + 1
                    newItem = False
                    self.save()
                    break
            if newItem == True:

                self.cart[movie.id] = {
                    'userid': self.request.user.id,
                    'movie_id': id,
                    'title': movie.title,
                    'quantity': 1,
                    'tagline': movie.tagline,
                    'image': movie.image.url
                }

        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, movie):
        """
        Remove a product from the cart.
        """
        movie_id = str(movie.id)
        if movie_id in self.cart:
            del self.cart[movie_id]
            self.save()

    def decrement(self, movie):
        for key, value in self.cart.items():
            if key == str(movie.id):

                value['quantity'] = value['quantity'] - 1
                if(value['quantity'] < 1):
                    return redirect('cart:cart_detail')
                self.save()
                break
            else:
                print("Something Wrong")

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
