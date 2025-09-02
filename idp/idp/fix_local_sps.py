#!/usr/bin/env python3
import os
import sys
import json

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idp.settings')

import django  # noqa: E402
django.setup()

from djangosaml2idp.models import ServiceProvider  # noqa: E402


def main() -> None:
    valid_mapping = json.dumps({
        "email": "email",
        "first_name": "first_name",
        "last_name": "last_name",
        "username": "username",
        "is_staff": "is_staff",
        "is_superuser": "is_superuser",
    })

    local_entity_ids = [
        "http://localhost:8000/saml2/metadata/",
        "http://localhost:8001/saml2/metadata/",
    ]

    for entity_id in local_entity_ids:
        sp = ServiceProvider.objects.filter(entity_id=entity_id).first()
        if not sp:
            print(f"Missing SP in DB: {entity_id}")
            continue
        sp._attribute_mapping = valid_mapping
        sp.active = True
        sp.save()
        print(f"Fixed mapping and activated: {entity_id}")

    print("Done fixing local SPs.")


if __name__ == "__main__":
    main()


