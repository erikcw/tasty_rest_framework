from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import encoders
import datetime
import warnings


class TastyPieJSONEncoder(encoders.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            # TastyPie doesn't modify timestamps, so we won't either.
            # Remove TZ -- this has got to be a bug in TastyPie!
            warning_message = "TastyPieJSONEncoder strips timezone information from datetime objects and converts them to the timezone in settings.TIME_ZONE.  It is recommended that you don't use the TastyPieJSONRenderer unless you require *strict* TastyPie compatibility for datetime JSON serialization."
            warnings.warn(warning_message)
            r = timezone.make_naive(o, timezone.get_current_timezone())
            return r.isoformat()
        return super(TastyPieJSONEncoder, self).default(o)


class TastyPieJSONRenderer(JSONRenderer):

    encoder_class = TastyPieJSONEncoder

