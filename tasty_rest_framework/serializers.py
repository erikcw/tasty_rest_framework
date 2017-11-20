from rest_framework.relations import HyperlinkedIdentityField, HyperlinkedRelatedField
from six.moves import urllib

class TastyPieHyperlinkedIdentityField(HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url = super(TastyPieHyperlinkedIdentityField, self).get_url(obj, view_name, request, format)
        # make a relative url by removing the scheme and host.
        parts = urllib.parse.urlsplit(url)
        url = urllib.parse.urlunsplit(("", None, parts.path, parts.query, parts.fragment,))
        return url


class TastyPieHyperlinkedRelatedField(HyperlinkedRelatedField):

    def get_url(self, obj, view_name, request, format):
        url = super(TastyPieHyperlinkedRelatedField, self).get_url(obj, view_name, request, format)

        if not url:
            # return None
            return url

        # make a relative url by removing the scheme and host.
        parts = urllib.parse.urlsplit(url)
        url = urllib.parse.urlunsplit(("", None, parts.path, parts.query, parts.fragment,))
        return url
