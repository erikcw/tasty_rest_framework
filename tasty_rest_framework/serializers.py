from rest_framework.relations import HyperlinkedIdentityField, HyperlinkedRelatedField
import urllib2

class TastyPieHyperlinkedIdentityField(HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url = super(TastyPieHyperlinkedIdentityField, self).get_url(obj, view_name, request, format)
        # make a relative url by removing the scheme and host.
        parts = urllib2.urlparse.urlsplit(url)
        url = urllib2.urlparse.urlunsplit((None, None, parts.path, parts.query, parts.fragment,))
        return url


class TastyPieHyperlinkedRelatedField(HyperlinkedRelatedField):

    def get_url(self, obj, view_name, request, format):
        url = super(TastyPieHyperlinkedRelatedField, self).get_url(obj, view_name, request, format)

        if not url:
            # return None
            return url

        # make a relative url by removing the scheme and host.
        parts = urllib2.urlparse.urlsplit(url)
        url = urllib2.urlparse.urlunsplit((None, None, parts.path, parts.query, parts.fragment,))
        return url