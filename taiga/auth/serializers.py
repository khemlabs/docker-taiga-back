# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.core import validators
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from taiga.base.api import serializers

import re


class BaseRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=256)
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=4)

    def validate_username(self, attrs, source):
        value = attrs[source]
        validator = validators.RegexValidator(re.compile('^[\w.-]+$'), _("invalid username"), "invalid")

        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError(_("Required. 255 characters or fewer. Letters, numbers "
                                                "and /./-/_ characters'"))
        return attrs

    def validate_email(self, attrs, source):
        value = attrs[source]
        domain_name = value.split("@")[1]

        if settings.REGISTER_ALLOWED_DOMAINS and domain_name not in settings.REGISTER_ALLOWED_DOMAINS:
            raise serializers.ValidationError(_("You email domain is not allowed"))
        return attrs


class PublicRegisterSerializer(BaseRegisterSerializer):
    pass


class PrivateRegisterForNewUserSerializer(BaseRegisterSerializer):
    token = serializers.CharField(max_length=255, required=True)


class PrivateRegisterForExistingUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=4)
    token = serializers.CharField(max_length=255, required=True)
